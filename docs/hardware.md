# Hardware detectado e dimensionamento do Lab 2

Detecção feita em 2026-10-21 na máquina de preparação da aula.

| Recurso | Valor |
|---------|-------|
| OS | Windows 11 Pro 64 bits |
| CPU | AMD Ryzen 5 3500X (6 núcleos / 6 threads) |
| RAM | 32 GB (≈17 GB livres na medição) |
| GPU | NVIDIA GTX 1660 Super, **4 GB VRAM** |
| Docker | 29.x instalado |
| Python | 3.14 instalado |
| Ollama | **não instalado** — instalar de <https://ollama.com/download> |

## Modelo recomendado

- **Chat: `qwen2.5:3b-instruct`** — quantizado Q4 ocupa ~2 GB, cabe inteiro nos
  4 GB de VRAM com folga para contexto; latência esperada de poucos segundos
  por resposta curta.
- **Embeddings: `nomic-embed-text`** — ~274 MB, roda bem até em CPU.
- Modelos 7B+ **não** cabem na VRAM: parte das camadas vai para CPU/RAM e a
  latência fica incompatível com demo ao vivo.

## Fallbacks

1. GPU ocupada/indisponível ⇒ `qwen2.5:1.5b-instruct` (CPU tolerável).
2. Ollama não instalado na hora ⇒ usar o [plano B pré-gravado](plano-b.md).
3. Máquina da sala sem Docker ⇒ apenas a parte Ollama + API (sem Langfuse/Langflow)
   também funciona: o RAG exige Postgres, então use `usar_rag=false` + plano B.
