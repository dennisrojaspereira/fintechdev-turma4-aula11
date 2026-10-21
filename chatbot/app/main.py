"""API do TechPix AI Assistant (Lab 2).

Execute a partir de chatbot/:  uvicorn app.main:app --port 8080
"""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import httpx
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

STATIC = Path(__file__).resolve().parent / "static"

from .config import settings
from .guardrails import avaliar_entrada, avaliar_saida


class ChatIn(BaseModel):
    pergunta: str = Field(min_length=1, max_length=2000)
    usar_rag: bool = True


def create_app(responder: Callable[..., dict] | None = None) -> FastAPI:
    app = FastAPI(
        title="TechPix AI Assistant",
        description="Chatbot informativo FICTÍCIO (laboratório). Não executa operações financeiras.",
        version="0.1.0",
    )
    app.state.responder = responder

    def get_responder() -> Callable[..., dict]:
        if app.state.responder is None:
            from .rag import Responder  # import tardio: exige deps de LLM

            app.state.responder = Responder(settings)
        return app.state.responder

    @app.get("/")
    def ui() -> FileResponse:
        """Tela de chat que mostra por onde a informacao passa (pipeline didatico)."""
        return FileResponse(STATIC / "chat.html")

    @app.get("/health")
    def health() -> dict:
        ollama_ok = False
        try:
            r = httpx.get(f"{settings.ollama_base_url}/api/tags", timeout=2)
            ollama_ok = r.status_code == 200
        except httpx.HTTPError:
            pass
        return {
            "status": "ok",
            "ollama": "ok" if ollama_ok else "indisponivel",
            "chat_model": settings.chat_model,
            "embedding_model": settings.embedding_model,
        }

    @app.post("/chat")
    def chat(body: ChatIn) -> dict:
        entrada = avaliar_entrada(body.pergunta)
        if not entrada.permitido:
            return {
                "resposta": entrada.resposta,
                "fontes": [],
                "modo": "guardrail",
                "bloqueado": True,
                "motivo": entrada.motivo,
            }

        out = get_responder()(body.pergunta, usar_rag=body.usar_rag)

        saida = avaliar_saida(out["resposta"])
        if not saida.permitido:
            return {
                "resposta": saida.resposta,
                "fontes": [],
                "modo": "guardrail",
                "bloqueado": True,
                "motivo": saida.motivo,
            }

        return {**out, "bloqueado": False, "motivo": None}

    return app


app = create_app()
