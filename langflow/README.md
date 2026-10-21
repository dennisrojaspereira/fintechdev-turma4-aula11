# Fluxo Langflow equivalente à cadeia Python

O arquivo `techpix_rag_flow.json` descreve o fluxo RAG equivalente ao de
`chatbot/app/rag.py`, para importar no Langflow (http://localhost:7860 →
**Import Flow**).

> ⚠️ O formato de export do Langflow muda entre versões. Este JSON foi escrito
> para a família 1.x; se a importação falhar ou algum nó vier "desligado",
> reconstrua o fluxo em ~3 minutos com o passo a passo abaixo (é inclusive um
> bom momento da demo: mostra que **canvas visual e código são duas interfaces
> para a mesma cadeia**, não substitutos diretos).

## Reconstrução manual (3 min)

1. **Chat Input** — entrada do usuário.
2. **Ollama Embeddings** — model `nomic-embed-text`, base URL
   `http://host.docker.internal:11434` (Langflow roda em container; o Ollama está no host).
3. **PGVector** (Vector Store, modo busca) — connection string
   `postgresql+psycopg://techpix:techpix-local-dev@postgres:5432/techpix`,
   collection `techpix_faq`, ligado ao Embeddings; entrada de busca vem do Chat Input.
4. **Parser / Combine Text** — junta os documentos recuperados em um texto `{contexto}`.
5. **Prompt** — cole o template do system prompt de `chatbot/app/rag.py`
   (responder só com base no contexto, citar fontes, não executar operações),
   com variáveis `{contexto}` e `{pergunta}`.
6. **Ollama** (LLM) — model `qwen2.5:3b-instruct`, base URL
   `http://host.docker.internal:11434`, temperature `0.1`.
7. **Chat Output** — resposta final.

Ligações: Chat Input → PGVector(busca) e Prompt(`pergunta`); PGVector → Parser →
Prompt(`contexto`); Prompt → Ollama → Chat Output.

## O que mostrar na aula

- A mesma pergunta nos dois lugares (código via `/chat`, canvas via Playground).
- Onde cada parâmetro (k do retriever, temperature, modelo) aparece em cada interface.
- O que o canvas **não** dá de graça: guardrails, testes, CI — continuam sendo engenharia.
