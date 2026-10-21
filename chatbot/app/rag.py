"""Cadeia RAG em LangChain: retriever pgvector + LLM local via Ollama.

Com chaves do Langfuse no ambiente, cada chamada gera um trace completo
(retrieval, prompt, geracao, latencia). Sem chaves, roda normalmente sem traces.
"""

from __future__ import annotations

import os

from langchain_core.prompts import ChatPromptTemplate
from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_postgres import PGVector

from .config import Settings

PROMPT_RAG = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é o assistente informativo da TechPix, uma fintech FICTÍCIA de "
            "laboratório. Responda em português, em até 5 frases, APENAS com base "
            "no CONTEXTO abaixo. Cite as fontes usadas no formato [nome-da-fonte]. "
            "Se o contexto não contém a resposta, diga explicitamente que não há "
            "essa informação na base de conhecimento e não invente. Você nunca "
            "executa transferências nem acessa dados de contas.\n\nCONTEXTO:\n{contexto}",
        ),
        ("human", "{pergunta}"),
    ]
)

PROMPT_SEM_RAG = ChatPromptTemplate.from_messages(
    [
        (
            "system",
            "Você é o assistente informativo da TechPix, uma fintech FICTÍCIA de "
            "laboratório. Responda em português, em até 5 frases. Você nunca executa "
            "transferências nem acessa dados de contas.",
        ),
        ("human", "{pergunta}"),
    ]
)


def _langfuse_callbacks() -> list:
    """Callback do Langfuse apenas quando as chaves existem no ambiente."""
    if os.getenv("LANGFUSE_PUBLIC_KEY") and os.getenv("LANGFUSE_SECRET_KEY"):
        from langfuse.callback import CallbackHandler

        return [CallbackHandler()]
    return []


class Responder:
    """Responde perguntas com ou sem RAG. Construcao preguicosa das conexoes."""

    def __init__(self, settings: Settings) -> None:
        self.settings = settings
        self._llm: ChatOllama | None = None
        self._vectorstore: PGVector | None = None

    @property
    def llm(self) -> ChatOllama:
        if self._llm is None:
            self._llm = ChatOllama(
                model=self.settings.chat_model,
                base_url=self.settings.ollama_base_url,
                temperature=self.settings.temperature,
            )
        return self._llm

    @property
    def vectorstore(self) -> PGVector:
        if self._vectorstore is None:
            self._vectorstore = PGVector(
                embeddings=OllamaEmbeddings(
                    model=self.settings.embedding_model,
                    base_url=self.settings.ollama_base_url,
                ),
                collection_name=self.settings.collection,
                connection=self.settings.database_url,
            )
        return self._vectorstore

    def __call__(self, pergunta: str, usar_rag: bool = True) -> dict:
        config = {"callbacks": _langfuse_callbacks(), "run_name": "techpix-chat"}

        if not usar_rag:
            msg = (PROMPT_SEM_RAG | self.llm).invoke({"pergunta": pergunta}, config=config)
            return {"resposta": msg.content, "fontes": [], "modo": "sem_rag"}

        docs = self.vectorstore.as_retriever(
            search_kwargs={"k": self.settings.retriever_k}
        ).invoke(pergunta, config=config)
        contexto = "\n\n".join(
            f"[{d.metadata.get('fonte', 'desconhecida')}]\n{d.page_content}" for d in docs
        )
        msg = (PROMPT_RAG | self.llm).invoke(
            {"contexto": contexto or "(nenhum trecho recuperado)", "pergunta": pergunta},
            config=config,
        )
        fontes = sorted({d.metadata.get("fonte", "desconhecida") for d in docs})
        return {"resposta": msg.content, "fontes": fontes, "modo": "rag"}
