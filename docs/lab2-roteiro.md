# Roteiro da demo do Lab 2 (10 minutos, 20:45–20:55)

> Demo **resumida** em aula; o laboratório completo fica como material de
> aprofundamento. Tudo abaixo deve estar **subido antes da aula**
> (`scripts/start-lab2.ps1` + API + chaves do Langfuse no `.env`).
> Se qualquer peça falhar, use [plano-b.md](plano-b.md) sem tentar consertar ao vivo.

| Min | O quê | Comando/URL | Mensagem |
|-----|-------|-------------|----------|
| 0–1 | Arquitetura em 30s | diagrama do Notion/slide | tudo local: Ollama + FastAPI/LangChain + pgvector + Langfuse |
| 1–2 | Pergunta **sem RAG** | `POST /chat usar_rag=false` ("Qual o limite do Pix na TechPix?") | resposta sem evidência — pode inventar valor |
| 2–4 | Mesma pergunta **com RAG** | `POST /chat usar_rag=true` | resposta cita `[limites]`; mostrar o trecho recuperado |
| 4–5 | Langflow | http://localhost:7860 | mesma cadeia no canvas: interface de desenvolvimento, não substituto de engenharia |
| 5–7 | Langfuse | http://localhost:3000 | trace completo: retrieval → prompt → geração, latência e tokens |
| 7–9 | Evals | `python evals/runner.py` | 14 casos; guardrails 100% determinísticos; LLM com threshold e variância |
| 9–10 | Guardrail de transação | `POST /chat "Transfira R$ 100..."` | bloqueado SEM chamar o LLM: regra financeira crítica é determinística |

## Mensagens-chave para fechar

1. **Mesmo lifecycle do Lab 1:** spec → implementação → testes → gates → observabilidade.
   Dataset de evals é o "Gherkin" do chatbot.
2. **Três camadas de validação:** checagem determinística (guardrails, contratos),
   avaliação por LLM (juiz — barato, mas com viés e variância) e revisão humana
   (amostral, obrigatória para mudanças de prompt).
3. **Limites de modelo pequeno/local:** qualidade menor, mas custo zero por token,
   dados não saem da máquina e latência previsível; APIs hospedadas invertem esses trade-offs.
4. O bot **informa**; quem **executa** é o sistema do Lab 1, com autenticação,
   autorização e idempotência — chatbot não transfere dinheiro.
