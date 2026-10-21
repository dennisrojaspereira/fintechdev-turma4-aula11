# Sobe o Lab 2 (Windows). Pre-requisitos: Docker Desktop e Ollama instalados.
$ErrorActionPreference = "Stop"
$repo = Split-Path $PSScriptRoot -Parent
Set-Location $repo

Write-Host "[1/4] Subindo Postgres+pgvector, Langfuse e Langflow..."
docker compose up -d

Write-Host "[2/4] Garantindo modelos locais no Ollama..."
ollama pull qwen2.5:3b-instruct
ollama pull nomic-embed-text

Write-Host "[3/4] Instalando dependencias do chatbot (venv proprio)..."
Set-Location "$repo\chatbot"
if (-not (Test-Path .venv)) { python -m venv .venv }
.\.venv\Scripts\python.exe -m pip install --quiet -r requirements.txt

Write-Host "[4/4] Ingerindo FAQ no pgvector..."
.\.venv\Scripts\python.exe -m app.ingest

Write-Host ""
Write-Host "Pronto. Proximos passos:"
Write-Host "  API:      cd chatbot; .\.venv\Scripts\uvicorn.exe app.main:app --port 8080"
Write-Host "  Smoke:    python scripts\smoke_test.py"
Write-Host "  Langfuse: http://localhost:3000  (crie usuario/projeto e cole as chaves no .env)"
Write-Host "  Langflow: http://localhost:7860"
