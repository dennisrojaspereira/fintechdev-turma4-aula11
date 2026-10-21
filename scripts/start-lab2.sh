#!/usr/bin/env bash
# Sobe o Lab 2 (Linux/macOS). Pre-requisitos: Docker e Ollama instalados.
set -euo pipefail
repo="$(cd "$(dirname "$0")/.." && pwd)"
cd "$repo"

echo "[1/4] Subindo Postgres+pgvector, Langfuse e Langflow..."
docker compose up -d

echo "[2/4] Garantindo modelos locais no Ollama..."
ollama pull qwen2.5:3b-instruct
ollama pull nomic-embed-text

echo "[3/4] Instalando dependencias do chatbot (venv proprio)..."
cd "$repo/chatbot"
[ -d .venv ] || python3 -m venv .venv
./.venv/bin/python -m pip install --quiet -r requirements.txt

echo "[4/4] Ingerindo FAQ no pgvector..."
./.venv/bin/python -m app.ingest

cat <<EOF

Pronto. Proximos passos:
  API:      cd chatbot && ./.venv/bin/uvicorn app.main:app --port 8080
  Smoke:    python3 scripts/smoke_test.py
  Langfuse: http://localhost:3000  (crie usuario/projeto e cole as chaves no .env)
  Langflow: http://localhost:7860
EOF
