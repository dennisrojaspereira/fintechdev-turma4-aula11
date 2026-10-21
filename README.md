# TechPix — Engenharia de Software com Agentes de IA

Repositório demonstrativo da **Aula 11 — FintechDev Turma 4**: uma "fábrica de software"
do PRD à produção, com agentes de IA, quality gates e validação humana.

> ⚠️ **TechPix é uma fintech fictícia.** A API de transferência Pix é **simulada**
> (sem integração real com SPI/Banco Central), sem credenciais e sem dados reais.

## Laboratórios

| Lab | Conteúdo | Pasta |
|-----|----------|-------|
| **Lab 1** | Pipeline BMAD + SDD + BDD: PRD → ADR → specs → Gherkin → implementação → quality gates | raiz, `src/`, `tests/` |
| **Lab 2** | TechPix AI Assistant: LLM local (Ollama) + RAG (LangChain + pgvector) + Langfuse + evals + guardrails | `chatbot/`, `evals/`, `docker-compose.yml` |

## Checkpoints (branches)

| Branch | Estado |
|--------|--------|
| `starter` | Requisitos, PRD, ADRs, specs, Gherkin e estrutura — sem implementação |
| `implemented` | API implementada **com bug controlado de idempotência sob concorrência** |
| `validated` | Bug corrigido, todos os gates verdes |
| `main` | `validated` + Lab 2 (chatbot, RAG, evals) |

## Setup (Lab 1)

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1          # Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
```

## Executar

```powershell
uvicorn techpix.api:app --reload --app-dir src   # http://127.0.0.1:8000/docs
```

## Testes e quality gates

```powershell
pytest -v                     # unitários + integração + BDD + concorrência
ruff check src tests          # lint / static analysis
bandit -r src -q              # security scan
```

### Demo do bug de idempotência (roteiro de aula)

```powershell
git checkout implemented
pytest tests/test_idempotency_concurrency.py -v   # ❌ FALHA: duas transferências efetivadas
git checkout validated
pytest tests/test_idempotency_concurrency.py -v   # ✅ PASSA: apenas uma efetivada
```

## Limpeza

```powershell
deactivate; Remove-Item -Recurse -Force .venv
docker compose down -v        # Lab 2
```

## Estrutura

```
techpix-ai-engineering/
├── docs/            # PRD, arquitetura, ADRs
├── specs/           # SDD — especificação rastreável
├── features/        # BDD — cenários Gherkin executáveis (pytest-bdd)
├── .agents/         # rules, skills e orquestração dos agentes
├── src/techpix/     # API Pix simulada
├── tests/           # unitários, integração, BDD, concorrência
├── chatbot/         # Lab 2 — AI Assistant (RAG local)
├── evals/           # Lab 2 — datasets e runner de avaliações
└── .github/workflows/quality.yml
```

Lab 2: veja [chatbot/README.md](chatbot/README.md).
