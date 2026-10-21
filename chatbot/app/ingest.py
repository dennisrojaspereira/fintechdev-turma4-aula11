"""Ingestao do FAQ ficticio: chunking por secao + embeddings locais -> pgvector.

Execute a partir de chatbot/:  python -m app.ingest
Pre-requisitos: docker compose up -d postgres  e  ollama pull nomic-embed-text
"""

from __future__ import annotations

import re
from pathlib import Path

from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_postgres import PGVector

from .config import settings

FAQ_DIR = Path(__file__).resolve().parent.parent / "data" / "faq"


def carregar_chunks() -> list[Document]:
    """Um chunk por secao `## ...` de cada arquivo, com a fonte nos metadados."""
    docs: list[Document] = []
    for arquivo in sorted(FAQ_DIR.glob("*.md")):
        texto = arquivo.read_text(encoding="utf-8")
        secoes = re.split(r"(?m)^## ", texto)
        for secao in secoes:
            corpo = secao.strip()
            if not corpo or corpo.startswith("# "):
                continue
            docs.append(
                Document(
                    page_content=f"## {corpo}" if not corpo.startswith("#") else corpo,
                    metadata={"fonte": arquivo.stem},
                )
            )
    return docs


def main() -> None:
    chunks = carregar_chunks()
    print(f"{len(chunks)} chunks de {FAQ_DIR}")

    vectorstore = PGVector(
        embeddings=OllamaEmbeddings(
            model=settings.embedding_model, base_url=settings.ollama_base_url
        ),
        collection_name=settings.collection,
        connection=settings.database_url,
        pre_delete_collection=True,  # re-ingestao idempotente
    )
    vectorstore.add_documents(chunks)
    print(f"Ingestao concluida na colecao '{settings.collection}'.")


if __name__ == "__main__":
    main()
