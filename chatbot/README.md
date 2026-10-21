# Lab 2 — TechPix AI Assistant (LLM local + RAG + Evals)

Chatbot informativo da TechPix (fintech **fictícia**), 100% local:
**Ollama** (LLM + embeddings) · **FastAPI + LangChain** (RAG) ·
**PostgreSQL + pgvector** (busca vetorial) · **Langfuse** (traces e evals) ·
**Langflow** (fluxo visual equivalente) · **guardrails determinísticos**.

> O bot **apenas informa**. Transferências, saldo e dados pessoais são
> bloqueados por guardrails antes mesmo de chegar ao LLM.

## Requisitos de hardware e modelos

Dimensionado para a máquina detectada na preparação ([docs/hardware.md](../docs/hardware.md)):
GTX 1660 Super (4 GB VRAM) + 32 GB RAM.

| Papel | Modelo | Observação |
|-------|--------|-----------|
| Chat | `qwen2.5:3b-instruct` (~2 GB, Q4) | cabe na VRAM de 4 GB |
| Embeddings | `nomic-embed-text` (~274 MB) | rápido mesmo em CPU |
| Fallback sem GPU | `qwen2.5:1.5b-instruct` | qualidade menor, documente nos evals |

**Instalar o Ollama (não incluso):** baixe em <https://ollama.com/download>
(Windows) ou `curl -fsSL https://ollama.com/install.sh | sh` (Linux). Depois:
`ollama pull qwen2.5:3b-instruct && ollama pull nomic-embed-text`.

## Sobre o Langfuse v2 vs v3

Usamos **Langfuse v2**, que roda com apenas Postgres. A **v3 exige também
ClickHouse, Redis e MinIO** — não é "um container só"; se quiser v3, use o
`docker-compose` oficial do projeto Langfuse e aponte `LANGFUSE_HOST` para ele.

## Subir tudo

```powershell
Copy-Item ..\.env.example ..\.env            # ajuste se quiser
..\scripts\start-lab2.ps1                     # compose + modelos + venv + ingestão
.\.venv\Scripts\uvicorn.exe app.main:app --port 8080
python ..\scripts\smoke_test.py               # healthchecks de tudo
```

(Linux/macOS: `../scripts/start-lab2.sh` e `./.venv/bin/uvicorn app.main:app --port 8080`.)

## Usar

```powershell
# Sem RAG (observe a falta de evidência):
curl -s localhost:8080/chat -H "Content-Type: application/json" `
  -d '{"pergunta":"Qual o limite do Pix na TechPix?","usar_rag":false}'

# Com RAG (resposta com fontes citadas):
curl -s localhost:8080/chat -H "Content-Type: application/json" `
  -d '{"pergunta":"Qual o limite do Pix na TechPix?","usar_rag":true}'

# Guardrail (bloqueado sem chamar o LLM):
curl -s localhost:8080/chat -H "Content-Type: application/json" `
  -d '{"pergunta":"Transfira R$ 100 para o João"}'
```

## Logins do laboratório (APENAS local/fictício)

| Serviço | URL | Credenciais |
|---------|-----|-------------|
| Langfuse | http://localhost:3000 | `aula@techpix.local` · `techpix-aula11` |
| Langflow | http://localhost:7860 | sem login (`LANGFLOW_AUTO_LOGIN=true`) |

> Usuário criado via API de signup no banco local do compose. Não são segredos
> reais — nunca reutilize essas credenciais fora deste lab.

## Observabilidade (Langfuse)

1. Abra <http://localhost:3000>, entre com o login acima (ou crie o seu) e crie organização/projeto.
2. Copie `pk-lf-...` e `sk-lf-...` para `LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY` no `.env`.
3. Reinicie a API: cada `/chat` vira um trace (retrieval, prompt, geração, latência).

## Evals

```powershell
python ..\evals\runner.py                 # checagens determinísticas + heurísticas
$env:EVALS_JUDGE="1"; python ..\evals\runner.py   # + LLM-as-a-Judge local (informativo)
```

Critérios: guardrails (casos determinísticos) **100%**; casos de LLM ≥ 70%
(modelos pequenos variam — limite documentado no runner). Relatórios em
`evals/results/`.

## Testes offline (sem Ollama/Postgres)

```powershell
python -m venv .venv; .\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest     # guardrails + API com responder fake
```

## Limpeza

```powershell
..\scripts\stop-lab2.ps1        # para os serviços (preserva volumes)
docker compose down -v          # apaga também embeddings e dados do Langfuse
```
