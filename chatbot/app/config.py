"""Configuracao via variaveis de ambiente (.env.example na raiz do repo).

Nenhum valor sensivel e hardcoded; chaves do Langfuse sao opcionais.
"""

from __future__ import annotations

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="TECHPIX_", env_file=".env", extra="ignore")

    ollama_base_url: str = "http://localhost:11434"
    chat_model: str = "qwen2.5:3b-instruct"
    embedding_model: str = "nomic-embed-text"
    database_url: str = "postgresql+psycopg://techpix:techpix-local-dev@localhost:5433/techpix"
    collection: str = "techpix_faq"
    retriever_k: int = 4
    temperature: float = 0.1


settings = Settings()
