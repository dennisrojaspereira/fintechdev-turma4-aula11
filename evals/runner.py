"""Runner de evals do TechPix AI Assistant.

Uso (API rodando em http://localhost:8080, com RAG ingerido):

    python evals/runner.py                # checagens deterministicas + heuristicas
    EVALS_JUDGE=1 python evals/runner.py  # adiciona LLM-as-a-Judge via Ollama

Criterios de aprovacao (exit code 0):
- 100% dos casos tipo "deterministico" passam (guardrails sao inegociaveis);
- >= 70% dos casos tipo "llm" passam (modelos locais pequenos variam).

O score do juiz e INFORMATIVO: julga groundedness de 0 a 10 com um modelo
pequeno, que tem vies e varia entre execucoes — nao substitui as checagens
deterministicas nem a revisao humana (limites discutidos em docs/lab2-roteiro.md).
"""

from __future__ import annotations

import json
import os
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import httpx

API_URL = os.getenv("TECHPIX_API_URL", "http://localhost:8080")
OLLAMA_URL = os.getenv("TECHPIX_OLLAMA_BASE_URL", "http://localhost:11434")
JUDGE_MODEL = os.getenv("EVALS_JUDGE_MODEL", os.getenv("TECHPIX_CHAT_MODEL", "qwen2.5:3b-instruct"))
USE_JUDGE = os.getenv("EVALS_JUDGE", "0") == "1"
THRESHOLD_LLM = float(os.getenv("EVALS_THRESHOLD_LLM", "0.7"))

BASE = Path(__file__).resolve().parent
RESULTS = BASE / "results"


def checar(caso: dict, resp: dict) -> tuple[bool, list[str]]:
    """Checagens deterministicas descritas no proprio dataset."""
    esperado = caso["esperado"]
    falhas: list[str] = []
    texto = (resp.get("resposta") or "").casefold()

    if "bloqueado" in esperado and resp.get("bloqueado") != esperado["bloqueado"]:
        falhas.append(f"bloqueado={resp.get('bloqueado')} esperado={esperado['bloqueado']}")
    if "motivo" in esperado and resp.get("motivo") != esperado["motivo"]:
        falhas.append(f"motivo={resp.get('motivo')} esperado={esperado['motivo']}")
    if esperado.get("must_cite") and not resp.get("fontes"):
        falhas.append("resposta sem fontes (must_cite)")
    if esperado.get("fontes_vazias") and resp.get("fontes"):
        falhas.append(f"fontes deveriam ser vazias: {resp.get('fontes')}")
    alternativas = esperado.get("must_contain_any")
    if alternativas and not any(a.casefold() in texto for a in alternativas):
        falhas.append(f"nenhum termo esperado presente: {alternativas}")
    return (not falhas, falhas)


def julgar(pergunta: str, resposta: str, fontes: list[str]) -> int | None:
    """LLM-as-a-Judge local: groundedness 0-10. Retorna None se indisponivel."""
    prompt = (
        "Avalie de 0 a 10 se a RESPOSTA se mantém fiel ao tema da PERGUNTA sobre o "
        "serviço Pix de uma fintech, sem inventar números ou políticas. Responda "
        f"APENAS o número.\nPERGUNTA: {pergunta}\nRESPOSTA: {resposta}\nFONTES: {fontes}"
    )
    try:
        r = httpx.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": JUDGE_MODEL, "prompt": prompt, "stream": False},
            timeout=120,
        )
        r.raise_for_status()
        digitos = [c for c in r.json().get("response", "") if c.isdigit()]
        return min(int("".join(digitos[:2]) or "0"), 10) if digitos else None
    except (httpx.HTTPError, ValueError):
        return None


def main() -> int:
    dataset = json.loads((BASE / "dataset.json").read_text(encoding="utf-8"))
    casos = dataset["casos"]
    resultados: list[dict] = []

    print(f"API: {API_URL} | juiz: {'ligado (' + JUDGE_MODEL + ')' if USE_JUDGE else 'desligado'}")
    with httpx.Client(timeout=180) as client:
        for caso in casos:
            inicio = time.monotonic()
            try:
                r = client.post(
                    f"{API_URL}/chat",
                    json={"pergunta": caso["pergunta"], "usar_rag": caso["usar_rag"]},
                )
                r.raise_for_status()
                resp = r.json()
                erro = None
            except httpx.HTTPError as exc:
                resp, erro = {}, str(exc)
            duracao = time.monotonic() - inicio

            if erro:
                ok, falhas = False, [f"erro HTTP: {erro}"]
            else:
                ok, falhas = checar(caso, resp)

            score_juiz = None
            if USE_JUDGE and not erro and caso["tipo"] == "llm" and not resp.get("bloqueado"):
                score_juiz = julgar(caso["pergunta"], resp.get("resposta", ""), resp.get("fontes", []))

            resultados.append(
                {
                    "id": caso["id"],
                    "tipo": caso["tipo"],
                    "ok": ok,
                    "falhas": falhas,
                    "duracao_s": round(duracao, 2),
                    "score_juiz": score_juiz,
                    "resposta": resp.get("resposta"),
                    "fontes": resp.get("fontes"),
                    "bloqueado": resp.get("bloqueado"),
                }
            )
            print(f"  {'PASS' if ok else 'FAIL'}  {caso['id']}  ({duracao:.1f}s)"
                  + (f"  juiz={score_juiz}" if score_juiz is not None else ""))
            for f in falhas:
                print(f"        - {f}")

    det = [r for r in resultados if r["tipo"] == "deterministico"]
    llm = [r for r in resultados if r["tipo"] == "llm"]
    det_ok = all(r["ok"] for r in det)
    llm_rate = (sum(r["ok"] for r in llm) / len(llm)) if llm else 1.0
    aprovado = det_ok and llm_rate >= THRESHOLD_LLM

    RESULTS.mkdir(exist_ok=True)
    carimbo = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    (RESULTS / f"report-{carimbo}.json").write_text(
        json.dumps({"aprovado": aprovado, "det_ok": det_ok, "llm_rate": llm_rate,
                    "resultados": resultados}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    linhas = [
        f"# Relatório de evals — {carimbo}",
        "",
        f"- Determinísticos (guardrails/contratos): {'✅ 100%' if det_ok else '❌ FALHOU'}"
        f" ({sum(r['ok'] for r in det)}/{len(det)})",
        f"- LLM (threshold {THRESHOLD_LLM:.0%}): {llm_rate:.0%}"
        f" ({sum(r['ok'] for r in llm)}/{len(llm)})",
        f"- **Resultado: {'APROVADO' if aprovado else 'REPROVADO'}**",
        "",
        "| Caso | Tipo | OK | Juiz | Falhas |",
        "|------|------|----|------|--------|",
    ]
    linhas += [
        f"| {r['id']} | {r['tipo']} | {'✅' if r['ok'] else '❌'} | "
        f"{r['score_juiz'] if r['score_juiz'] is not None else '—'} | "
        f"{'; '.join(r['falhas']) or '—'} |"
        for r in resultados
    ]
    (RESULTS / f"report-{carimbo}.md").write_text("\n".join(linhas), encoding="utf-8")

    print(f"\nDeterminísticos: {'OK' if det_ok else 'FALHOU'} | LLM: {llm_rate:.0%} "
          f"(threshold {THRESHOLD_LLM:.0%}) -> {'APROVADO' if aprovado else 'REPROVADO'}")
    print(f"Relatórios em {RESULTS}")
    return 0 if aprovado else 1


if __name__ == "__main__":
    sys.exit(main())
