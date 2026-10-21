"""Smoke test do Lab 2: verifica cada servico e resume o que falta.

Uso: python scripts/smoke_test.py   (so precisa da stdlib + httpx se disponivel)
"""

from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

CHECAGENS = [
    ("Ollama", "http://localhost:11434/api/tags"),
    ("Langfuse", "http://localhost:3000/api/public/health"),
    ("Langflow", "http://localhost:7860/health"),
    ("Chatbot API", "http://localhost:8080/health"),
]


def checar(nome: str, url: str) -> bool:
    try:
        with urllib.request.urlopen(url, timeout=5) as resp:  # noqa: S310 - URLs locais fixas
            ok = 200 <= resp.status < 300
            corpo = resp.read(200).decode(errors="replace")
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"  [FALHOU] {nome}: {exc}")
        return False
    print(f"  [OK]     {nome}: {corpo.strip()[:80]}")
    return ok


def checar_chat() -> bool:
    """Uma pergunta real com RAG — exige ingestao feita e Ollama com modelos."""
    req = urllib.request.Request(
        "http://localhost:8080/chat",
        data=json.dumps({"pergunta": "O que é o Pix?", "usar_rag": True}).encode(),
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=120) as resp:  # noqa: S310
            body = json.loads(resp.read())
    except (urllib.error.URLError, TimeoutError, OSError) as exc:
        print(f"  [FALHOU] /chat com RAG: {exc}")
        return False
    ok = bool(body.get("resposta")) and bool(body.get("fontes"))
    print(f"  [{'OK' if ok else 'FALHOU'}]     /chat com RAG: fontes={body.get('fontes')}")
    return ok


if __name__ == "__main__":
    print("Smoke test do Lab 2:")
    resultados = [checar(nome, url) for nome, url in CHECAGENS]
    if resultados[0] and resultados[3]:
        resultados.append(checar_chat())
    else:
        print("  [PULADO] /chat com RAG (Ollama ou API indisponiveis)")
    print("\nTudo OK!" if all(resultados) else "\nHa servicos pendentes — veja acima.")
    sys.exit(0 if all(resultados) else 1)
