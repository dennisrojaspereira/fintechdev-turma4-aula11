"""Cadeia RAG em LangChain: retriever pgvector + LLM local via Ollama.

Com chaves do Langfuse no ambiente, cada chamada gera um trace completo
(retrieval, prompt, geracao, latencia). Sem chaves, roda normalmente sem traces.
"""

from __future__ import annotations

import os
import re
import unicodedata

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
            "no CONTEXTO abaixo. Se o contexto não contém a resposta, diga "
            "explicitamente que não há essa informação na base de conhecimento e "
            "não invente. Você nunca executa transferências nem acessa dados de "
            "contas.\n"
            "OBRIGATÓRIO: termine a resposta com uma última linha que lista, entre "
            "colchetes, só as fontes do contexto que você realmente usou. Por "
            "exemplo, se os trechos usados vieram de [limites] e [prazos-horarios], "
            "a última linha é:\nFontes: [limites] [prazos-horarios]\n\n"
            "CONTEXTO:\n{contexto}",
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


def _palavras(texto: str) -> set[str]:
    """Palavras de conteudo normalizadas (sem acento, >= 4 chars)."""
    t = unicodedata.normalize("NFKD", texto.lower())
    t = "".join(c for c in t if not unicodedata.combining(c))
    return set(re.findall(r"[a-z0-9]{4,}", t))


def _fontes_utilizadas(resposta: str, docs: list) -> list[str]:
    """Atribuicao ESTRUTURAL de fontes: modelo pequeno nao segue contrato de
    citacao por prompt de forma confiavel, entao a API mede quais trechos
    recuperados sustentam a resposta — marcador explicito [fonte] OU
    sobreposicao lexical alta entre a resposta e o conteudo do trecho."""
    resp = _palavras(resposta)
    por_fonte: dict[str, set[str]] = {}
    for d in docs:
        fonte = d.metadata.get("fonte", "desconhecida")
        por_fonte.setdefault(fonte, set()).update(_palavras(d.page_content))
    utilizadas = []
    for fonte, palavras_fonte in por_fonte.items():
        explicita = f"[{fonte}]" in resposta
        cobertura = len(resp & palavras_fonte) / max(len(resp), 1)
        if explicita or cobertura >= 0.45:
            utilizadas.append(fonte)
    return sorted(utilizadas)


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
        # Recuperar um documento NAO significa fundamentar a resposta nele:
        # "fontes" sao as efetivamente utilizadas (citacao explicita ou
        # atribuicao lexical); as recuperadas vao separadas, e os trechos
        # alimentam o juiz dos evals.
        recuperadas = sorted({d.metadata.get("fonte", "desconhecida") for d in docs})
        citadas = _fontes_utilizadas(msg.content, docs)
        trechos = [
            {"fonte": d.metadata.get("fonte", "desconhecida"), "texto": d.page_content}
            for d in docs
        ]
        return {
            "resposta": msg.content,
            "fontes": citadas,
            "fontes_recuperadas": recuperadas,
            "trechos": trechos,
            "modo": "rag",
        }
