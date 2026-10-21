"""Servidor do tour guiado da Aula 11.

Uso (da raiz do repo):
    .venv\\Scripts\\python.exe -m uvicorn tour.server:app --port 9000
Abra http://localhost:9000 e navegue pelos passos (setas ← → funcionam).
"""

from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse

from .actions import ACTIONS
from .steps import STEPS

REPO = Path(__file__).resolve().parent.parent
STATIC = Path(__file__).resolve().parent / "static"

# Allowlist de arquivos exibiveis: somente os referenciados pelos passos.
ARQUIVOS_PERMITIDOS = {a for step in STEPS for a in step["arquivos"]}

app = FastAPI(title="Tour — Aula 11 TechPix", docs_url=None, redoc_url=None)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC / "index.html")


@app.get("/notas")
def notas() -> FileResponse:
    """Janela do apresentador: acompanha o passo da janela principal."""
    return FileResponse(STATIC / "notas.html")


@app.get("/api/steps")
def steps() -> list[dict]:
    return STEPS


@app.get("/api/file")
def file(path: str) -> dict:
    if path not in ARQUIVOS_PERMITIDOS:
        raise HTTPException(403, "arquivo fora da allowlist do tour")
    alvo = REPO / path
    if not alvo.is_file():
        raise HTTPException(404, f"{path} não encontrado")
    return {"path": path, "conteudo": alvo.read_text(encoding="utf-8")}


@app.post("/api/run/{action_id}")
def run(action_id: str) -> dict:
    acao = ACTIONS.get(action_id)
    if acao is None:
        raise HTTPException(404, "ação desconhecida")
    return acao()
