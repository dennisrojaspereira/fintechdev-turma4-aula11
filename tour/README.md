# Tour guiado da Aula 11

Servidor local de apresentação: 14 passos com explicação didática, os arquivos
reais do repositório e botões **"Ao vivo"** que executam as demos de verdade
(testes, API, bug de concorrência, RAG, guardrails, evals).

## Subir

```powershell
# da raiz do repo (usa o venv do Lab 1, já instalado)
.venv\Scripts\python.exe -m uvicorn tour.server:app --port 9000
```

Abra **http://localhost:9000**. Navegue com as setas **← →** do teclado ou pelo
menu lateral.

## Notas do apresentador (segunda janela)

Clique em **🗒 Notas** (ou tecle **N**) para abrir **http://localhost:9000/notas**
em outra janela — arraste para o segundo monitor ou deixe fora da projeção.
Ela **acompanha sozinha** o passo da janela principal (BroadcastChannel/localStorage,
mesmo navegador) e mostra: o que falar, perguntas para a turma, dicas de tempo,
relógio e tempo decorrido da apresentação, além do título do próximo passo.

A tela principal fica limpa para o público; o "o que falar" vive só nas notas.

## Pré-requisitos por passo

| Passos | Precisa de |
|--------|-----------|
| 1–10 (Lab 1) | nada além do venv da raiz (worktree `.wt-implemented` é criada sozinha) |
| 11–13 (Lab 2) | `docker compose up -d`, Ollama com os modelos e a API do chatbot na porta 8080 (`scripts/start-lab2.ps1` + uvicorn) |

Se o chatbot estiver fora do ar, os botões do Lab 2 explicam como subir, sem
quebrar a apresentação.

## Segurança

O navegador só envia **ids de ação** de uma allowlist fixa (`tour/actions.py`);
nenhum comando arbitrário é executado, e a leitura de arquivos é restrita aos
caminhos referenciados pelos passos.
