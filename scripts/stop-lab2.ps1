# Para o Lab 2 preservando os dados (volumes).
# Para apagar TUDO (incl. embeddings e dados do Langfuse): docker compose down -v
$repo = Split-Path $PSScriptRoot -Parent
Set-Location $repo
docker compose down
Write-Host "Servicos parados. Volumes preservados (use 'docker compose down -v' para apagar)."
