"""Roteiro do tour guiado da Aula 11 — cada passo tem explicacao, arquivos e acoes ao vivo."""

STEPS = [
    {
        "id": "intro",
        "titulo": "1. O gargalo mudou",
        "explicacao": """
## A IA está produzindo mais código. Estamos produzindo mais qualidade?

A IA tirou o gargalo da **escrita** do código e o empurrou para a **validação**:
revisar, testar, garantir segurança e arquitetura. Este lab mostra uma "fábrica de
software" completa — do PRD à produção — onde agentes implementam, mas **a
responsabilidade continua do time**.

**O que falar:**
- Pergunte: *"quem já recebeu um PR gigante gerado por IA?"*
- A tese da aula: especificação, testes e gates ficam **mais** importantes com IA, não menos.
- Tudo que vocês vão ver roda nesta máquina, agora, ao vivo — inclusive um bug plantado de propósito.
""",
        "arquivos": ["README.md"],
        "acoes": [],
    },
    {
        "id": "prd",
        "titulo": "2. PRD — a fonte de verdade",
        "explicacao": """
## Greenfield: quem define o comportamento correto?

Não existe código legado aqui (Greenfield). A fonte de verdade é o **PRD**: requisitos
funcionais numerados (RF-01…), não funcionais (RNF-01: correção sob concorrência) e
**perguntas abertas de discovery** — lacuna de requisito vira pergunta para humano,
nunca suposição do agente.

**O que falar:**
- Dinheiro em **centavos (int)** — float em valor monetário é defeito, não estilo.
- RNF-01 é a estrela da aula: *N requisições concorrentes com a mesma chave ⇒ exatamente 1 débito*.
- No Brownfield a "verdade" vem do código + incidentes + contratos — e legado também mente.
""",
        "arquivos": ["docs/prd.md"],
        "acoes": [],
    },
    {
        "id": "adr",
        "titulo": "3. ADRs — decisões com dono",
        "explicacao": """
## Decisões arquiteturais são registradas, não improvisadas

Agentes implementam rápido demais para decisões implícitas. Cada decisão relevante vira
um **ADR**: contexto, decisão, consequências (prós **e** contras) e alternativas
rejeitadas. O ADR-0002 define a solução do bug que vamos plantar: idempotência por
**reserva atômica**, nunca *check-then-act*.

**O que falar:**
- ADRs que afetam dinheiro/segurança exigem **aprovação humana** antes do agente implementar.
- O ADR é o que permite a um agente novo (ou humano novo) entender o "porquê" em 2 minutos.
""",
        "arquivos": ["docs/adr/0002-idempotencia-atomica.md", "docs/adr/0003-estados-e-reconciliacao.md"],
        "acoes": [],
    },
    {
        "id": "sdd",
        "titulo": "4. SDD — spec rastreável",
        "explicacao": """
## Specification-Driven Development

A spec traduz o PRD em **contrato verificável**: cada caso da API tem status code,
código de erro estável e rastreabilidade (PRD ⇄ spec ⇄ cenário BDD). No fim, os
**invariantes** (I-1 a I-4) são os oráculos que não dependem da implementação —
ex.: I-1, *dinheiro não é criado nem destruído*.

**O que falar:**
- A tabela de casos é literalmente o roteiro dos testes de integração.
- O provedor simulado é **determinístico** (valor terminado em 99 ⇒ timeout): teste reproduzível, sem flakiness.
""",
        "arquivos": ["specs/pix-transfer.md"],
        "acoes": [],
    },
    {
        "id": "bdd",
        "titulo": "5. BDD — Gherkin executável",
        "explicacao": """
## Comportamento que roda, não documento que envelhece

Os cenários Gherkin (em português!) são **executáveis** via pytest-bdd: cada linha
`Quando/Então` vira um step de teste de verdade. Se a spec mudar e o código não, o
cenário quebra — a documentação não consegue mentir.

**O que falar:**
- BDD é o contrato legível por produto/QA/dev/agente — todos leem a mesma coisa.
- Clique em **Executar** e mostre os 7 cenários rodando contra a API real.
""",
        "arquivos": ["features/pix-transfer.feature", "tests/test_bdd.py"],
        "acoes": [
            {"id": "bdd_tests", "label": "▶ Rodar os 7 cenários BDD", "demorado": False}
        ],
    },
    {
        "id": "agentes",
        "titulo": "6. Rules, skills e orquestração",
        "explicacao": """
## Autonomia com limites explícitos

- **Rules** = restrições (nunca float em dinheiro, nunca segredo no repo, nunca desligar gates).
- **Skills** = procedimentos reutilizáveis (como rodar gates, como criar ADR).
- **Agentes** = papéis com entrada/saída/ferramentas delimitadas — o **Testador não lê o código**,
  só o PRD/spec, para os oráculos serem independentes.
- **Orquestração** = worktrees isoladas, contratos read-only, integração via PR.

**O que falar:**
- Segurança: operações pré-aprovadas vs. as que exigem humano (deploy, merge, destrutivas).
- *"Se três agentes trabalham em paralelo, quem garante consistência?"* → contratos compartilhados + 1 agente por arquivo quente.
""",
        "arquivos": [".agents/orchestration.md", ".agents/rules/engenharia.md", ".agents/rules/seguranca.md"],
        "acoes": [],
    },
    {
        "id": "api",
        "titulo": "7. A API ao vivo",
        "explicacao": """
## Transferência, idempotência e estados — em requisições reais

As ações abaixo executam a API TechPix em memória e mostram **requisição → resposta**
de cada caso: sucesso (201), reapresentação da mesma chave (200, sem novo débito) e
conflito de payload (409).

**O que falar:**
- Observe o saldo da Alice: debita **uma** vez, mesmo repetindo a chamada.
- O código de erro é **estável** (`conflito_idempotencia`) — contrato, não mensagem solta.
""",
        "arquivos": ["src/techpix/api.py"],
        "acoes": [
            {"id": "api_fluxo", "label": "▶ Sucesso + idempotência + conflito", "demorado": False}
        ],
    },
    {
        "id": "unknown",
        "titulo": "8. Timeout, UNKNOWN e reconciliação",
        "explicacao": """
## O estado mais importante de um sistema de pagamento

Quando o provedor não responde, **não sabemos** se liquidou. Estornar pode gerar débito
duplo; confirmar pode creditar sem liquidação. Resposta certa: estado **UNKNOWN**,
fundos **reservados**, e **reconciliação** depois (ADR-0003). O retry do cliente com a
mesma chave é seguro: retorna a transferência existente.

**O que falar:**
- Nenhum caminho de timeout cria ou destrói dinheiro (invariante I-1).
- UNKNOWN não é erro: é honestidade do sistema + processo para resolver.
""",
        "arquivos": ["docs/adr/0003-estados-e-reconciliacao.md"],
        "acoes": [
            {"id": "api_unknown", "label": "▶ Timeout → UNKNOWN → retry → reconciliação", "demorado": False}
        ],
    },
    {
        "id": "bug",
        "titulo": "9. O bug: check-then-act 💣",
        "explicacao": """
## Quem testa o código que a IA escreve?

A branch `implemented` tem o defeito clássico de pagamento: a idempotência checa a
chave e **só grava depois** (check-then-act). Sequencialmente funciona — todos os
testes "normais" passam. Sob concorrência, N requisições passam pela checagem antes
de qualquer gravação e **todas debitam**.

O oráculo que pega isso deriva do **PRD** (RNF-01), não da implementação: 8 threads,
mesma chave, barreira de sincronização ⇒ exatamente 1 débito.

**O que falar:**
- Primeiro mostre o **diff** (o bug cabe em 10 linhas e parece inocente).
- Depois rode o teste na branch com bug: **8 transferências efetivadas**. Coverage e
  testes verdes não garantem correção — o teste certo é o que deriva do requisito.
""",
        "arquivos": [],
        "acoes": [
            {"id": "diff_bug", "label": "👀 Ver o diff do bug (implemented → validated)", "demorado": False},
            {"id": "concurrency_implemented", "label": "💥 Rodar o teste de concorrência NA BRANCH COM BUG", "demorado": False},
        ],
    },
    {
        "id": "fix",
        "titulo": "10. A correção e os quality gates",
        "explicacao": """
## Reserva atômica + gates verdes

A correção (ADR-0002) move checagem da chave, validação de saldo, reserva de fundos e
registro da chave para a **mesma seção crítica** — elimina a janela de corrida por
construção. Em produção: transação + `UNIQUE(idempotency_key)`.

**O que falar:**
- Rode o mesmo teste na versão corrigida: passa.
- Depois a suíte completa: 26/26 + ruff + bandit. No CI, entram também secrets
  scanning (gitleaks) — e o merge ainda exige **revisão humana**.
- *"100% de cobertura garante segurança financeira?"* Não — o que garante é oráculo
  independente + invariantes + gates + humano no loop.
""",
        "arquivos": ["src/techpix/service.py", ".github/workflows/quality.yml"],
        "acoes": [
            {"id": "concurrency_validated", "label": "✅ Rodar o teste de concorrência CORRIGIDO", "demorado": False},
            {"id": "gates_validated", "label": "🛡 Rodar TODOS os gates (26 testes + lint)", "demorado": True},
        ],
    },
    {
        "id": "rag",
        "titulo": "11. Lab 2: RAG com LLM local",
        "explicacao": """
## E se fosse um chatbot? Mesmo lifecycle.

O TechPix AI Assistant roda 100% local: **Ollama** (qwen2.5:3b na GTX 1660) +
**LangChain** + **pgvector** com o FAQ fictício. Compare as duas respostas para a
mesma pergunta:

- **Sem RAG:** o modelo responde "de memória" — plausível e sem evidência.
- **Com RAG:** responde ancorado nos chunks recuperados e **cita as fontes**.

**O que falar:**
- A pergunta do limite é ótima: sem RAG ele chuta; com RAG cita `[limites]`.
- Pré-requisito: API do chatbot rodando na porta 8080 (botão de status abaixo).
""",
        "arquivos": ["chatbot/app/rag.py"],
        "acoes": [
            {"id": "chat_status", "label": "🩺 Status da stack (smoke test)", "demorado": True},
            {"id": "chat_sem_rag", "label": "▶ Perguntar SEM RAG", "demorado": True},
            {"id": "chat_rag", "label": "▶ Perguntar COM RAG", "demorado": True},
        ],
    },
    {
        "id": "guardrails",
        "titulo": "12. Guardrails determinísticos",
        "explicacao": """
## Regra financeira crítica não se negocia com o modelo

Prompt injection, pedido de dados pessoais e **ordens de transferência** são bloqueados
por regras determinísticas **antes** do LLM — repare no tempo: ~0 s, o modelo nem é
chamado. O bot informa; quem executa é o sistema do Lab 1, com autenticação e
idempotência.

**O que falar:**
- Três camadas: checagem determinística (gate), avaliação por LLM (informativa), revisão humana.
- O guardrail de saída também existe: CPF ou "transferência realizada" na resposta ⇒ bloqueio.
""",
        "arquivos": ["chatbot/app/guardrails.py"],
        "acoes": [
            {"id": "chat_guardrail", "label": "🚫 Pedir uma transferência ao bot", "demorado": False},
            {"id": "chat_injection", "label": "🚫 Tentar prompt injection", "demorado": False},
        ],
    },
    {
        "id": "evals",
        "titulo": "13. Evals — o Gherkin do chatbot",
        "explicacao": """
## Dataset dourado + checagens + juiz (com limites)

14 casos: perguntas conhecidas, fora da base, injeção, PII, transferência, citação.
Critério: guardrails **100%** (inegociável), casos de LLM ≥ 70% (modelo pequeno varia).

**O que falar (resultado real da preparação):**
- O caso **q03** reprovou de verdade: o retrieval trouxe o chunk certo do limite
  noturno e o Qwen 3B respondeu que o limite "permanece constante" — **falha de
  groundedness real**, capturada pelo eval.
- O juiz 3B deu nota 4–6 a respostas boas e 0 a recusas corretas: juiz pequeno é
  **informativo**, nunca gate.
""",
        "arquivos": ["evals/dataset.json", "evals/results/evidencia-2026-10-21.md"],
        "acoes": [
            {"id": "evals", "label": "🧪 Rodar os 14 evals ao vivo (~40 s)", "demorado": True}
        ],
    },
    {
        "id": "fim",
        "titulo": "14. Fechamento",
        "explicacao": """
## IA acelera a implementação. Não transfere a responsabilidade.

O que esta esteira demonstrou:

1. **Fonte de verdade explícita** (PRD/spec/BDD) — o agente não inventa regra.
2. **Oráculos independentes** — o teste que pegou o bug deriva do requisito, não do código.
3. **Gates em camadas** — lint, security, testes, concorrência, secrets, humano.
4. **Mesmo lifecycle para IA generativa** — dataset de evals, guardrails determinísticos,
   observabilidade (Langfuse), juiz com limites declarados.
5. **Decisões humanas obrigatórias** — ADRs de dinheiro/segurança, merges, discovery.

**Perguntas para a turma:**
- Onde a automação deve parar para uma decisão humana no *seu* contexto?
- O que é a "chave de idempotência" do processo de vocês — o invariante que ninguém testou ainda?
""",
        "arquivos": [".agents/orchestration.md"],
        "acoes": [],
    },
]
