# Fluxo Langflow — TechPix RAG (visual)

## Onde ver na aula

1. Abra **http://localhost:7860** (sem login — auto-login ativo).
2. Na página inicial, entre na pasta/projeto **"Starter Project"** (menu lateral).
3. Abra o fluxo **"TechPix RAG (visual)"** — canvas com ChatInput → Knowledge
   (retrieval) → Prompt → Agent/LLM → ChatOutput.
4. Use o **Playground** (botão no topo) para conversar dentro do próprio Langflow.

> ⚠️ O Langflow **não** recebe as perguntas do chat da porta 8080 — ele é um
> ambiente paralelo de desenvolvimento visual. O caminho de "produção" é
> chat → FastAPI → LangChain → pgvector/Ollama (traces no Langfuse). Essa
> separação é proposital e vale uma fala na aula: *canvas é interface de
> desenvolvimento, não um proxy.*

## Sobre este fluxo

- `techpix_rag_flow.json` é o **export real** (importação verificada no Langflow
  1.12.7): clonado do template oficial **Vector Store RAG** e renomeado, por isso
  renderiza e executa. Importe por **Import Flow** se precisar recriar.
- Os componentes padrão do template usam provedores hospedados (ex.: OpenAI).
  Para rodar **100% local**, troque no canvas: modelo → **Ollama**
  (`qwen2.5:3b-instruct`, base URL `http://host.docker.internal:11434`),
  embeddings → **Ollama Embeddings** (`nomic-embed-text`) e o vector store →
  **PGVector** (`postgresql+psycopg://techpix:techpix-local-dev@postgres:5432/techpix`,
  coleção `techpix_faq`). São ~3 minutos de demo — e mostram que canvas e
  código são **duas interfaces para a mesma cadeia**.

## O que mostrar na aula

- A mesma pergunta nos dois lugares: chat da porta 8080 (código) × Playground (canvas).
- Onde cada parâmetro (k do retriever, temperature, modelo) mora em cada interface.
- O que o canvas **não** dá de graça: guardrails, testes, CI — continuam sendo engenharia.
