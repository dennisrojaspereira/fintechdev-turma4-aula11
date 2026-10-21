"""Roteiro do tour guiado da Aula 11.

Cada passo tem: explicacao (tela do publico), notas (janela do apresentador,
/notas), arquivos exibiveis e acoes executaveis ao vivo.
"""

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
""",
        "notas": """
- Abrir perguntando: **"quem já recebeu um PR gigante gerado por IA?"** — deixar 2 ou 3 responderem.
- Tese da aula: especificação, testes e gates ficam **mais** importantes com IA, não menos.
- Avisar: tudo roda **nesta máquina, ao vivo** — inclusive um bug plantado de propósito que vamos caçar.
- Conectar com as perguntas da turma (Matheus: throughput/testes; Renato: autonomia×segurança; Cauã: Greenfield; Cláudio: pipeline BMAD+BDD+SDD).
- ⏱ ~5 min aqui, não mais.
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
""",
        "notas": """
- Responde a pergunta do **Cauã**: no Greenfield a verdade é **construída** — PRD + ADRs + contratos + cenários de aceite + baselines.
- Contraponto Brownfield: a verdade vem de código + contratos + incidentes — e **legado também mente** (produção ≠ especificação correta).
- Destacar no arquivo: dinheiro em **centavos (int)** — float em dinheiro é defeito, não estilo.
- **RNF-01 é a estrela da noite**: N requisições concorrentes com a mesma chave ⇒ exatamente 1 débito. Guardem isso.
- Mostrar a seção de riscos: o R1 literalmente prevê o bug que vamos plantar.
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
""",
        "notas": """
- ADR que afeta dinheiro/segurança exige **aprovação humana** antes do agente implementar.
- O ADR é o que faz um agente (ou dev) novo entender o "porquê" em 2 minutos — contexto barato para o próximo prompt.
- Abrir o ADR-0002 e ler só a frase da decisão: checagem + reserva **na mesma operação crítica**.
- ADR-0003 (UNKNOWN): plantar a semente — "timeout não é sucesso nem falha" — volta no passo 8.
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
""",
        "notas": """
- A tabela de casos é literalmente o roteiro dos testes de integração — mostrar 2 linhas (idempotência e limite).
- **Invariantes = oráculos independentes**: o teste deriva do requisito, não do código. Se a implementação e o teste nascem do mesmo lugar (o código), os dois podem estar errados juntos — pergunta do Cláudio.
- Provedor simulado **determinístico** (valor terminado em 99 ⇒ timeout): reproduzível, sem flakiness. Em produção seria um test double do SPI.
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
""",
        "notas": """
- Abrir o `.feature` primeiro: linguagem de negócio, legível por produto/QA/dev/**agente** — todos leem o mesmo contrato.
- Depois clicar **Executar** e mostrar os 7 cenários verdes contra a API real.
- História real da preparação: o cenário de duplicidade **falhou** porque a chave de teste tinha 7 caracteres e o contrato exige 8–64 — o gate pegou erro **do próprio teste**. Vale contar.
- Gancho para o Cláudio: BDD é a camada "comportamento" da pipeline BMAD+SDD+BDD dele.
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
""",
        "notas": """
- Responde o **Renato** (autonomia sem abrir mão de segurança): pré-aprovar operações seguras (testes, lint, leitura), exigir humano para destrutivas/segredos/deploy/merge — **nunca** bypass irrestrito.
- Responde o **Matheus** (worktrees/paralelismo): 1 worktree por tarefa, contratos compartilhados read-only, 1 agente por arquivo quente, integração via PR. Paralelismo não elimina dependência — pode aumentar retrabalho.
- Detalhe que rende discussão: o Testador **não lê a implementação**. Por quê? Oráculo independente.
- Mostrar a tabela de papéis no orchestration.md.
- Pergunta para a turma: *"quais permissões vocês dariam ao agente no terminal de vocês?"*
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
""",
        "notas": """
- Clicar e narrar devagar as 3 requisições: 201 → 200 (mesmo `id`! sem novo débito) → 409.
- Apontar o saldo final da Alice: começou com 1.000.000, debitou **uma** vez (985.000).
- Código de erro **estável** (`conflito_idempotencia`) = contrato, não mensagem solta — é o que permite o cliente (e os testes) reagirem programaticamente.
- Se perguntarem do armazenamento: memória com lock, atrás de interface — em produção é Postgres com `UNIQUE(idempotency_key)` (ADR-0001).
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
""",
        "notas": """
- Perguntar antes de clicar: *"timeout do provedor: vocês estornam ou confirmam?"* — deixar errarem; a resposta é **nenhum dos dois**.
- Narrar a demo: 202 UNKNOWN → valor reservado (nada no Bruno) → retry seguro (200, mesma transferência) → reconciliação resolve → reserva zerada, Bruno creditado.
- Invariante I-1 em ação: nenhum caminho de timeout cria ou destrói dinheiro.
- Frase de efeito: **UNKNOWN não é erro — é honestidade do sistema + processo para resolver.**
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
""",
        "notas": """
- **Momento principal da aula.** Ordem: (1) diff, (2) teste falhando.
- No diff, apontar: o bug cabe em ~10 linhas e **parece inocente** — checagem fora do lock + "ida ao banco" no meio. Review humano cansado deixa passar.
- Antes de rodar, lembrar: 25 testes passam nessa branch. Coverage alto. Tudo verde — menos o oráculo de concorrência.
- Rodar e ler em voz alta: **"RNF-01 violado: 8 transferências efetivadas para a mesma chave"** — débito de R$ 800 em vez de R$ 100.
- Pergunta do **Matheus** (como testar throughput de código de agente): não é "mais testes", é **o teste certo derivado do requisito** + barreira de sincronização para tornar a corrida determinística.
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
""",
        "notas": """
- Rodar o mesmo teste na versão corrigida: **passa** — e não por sorte de timing, por construção.
- Rodar os gates completos (se o tempo permitir): 26/26 + ruff + bandit. No CI entram também gitleaks (secrets) — e o merge ainda exige **revisão humana**.
- Responder: *"100% de cobertura garante segurança financeira?"* **Não** — cobertura mede o que o teste executa, não o que ele verifica. O que segura é oráculo independente + invariantes + gates + humano.
- Transição para o Lab 2: *"e quando a saída não é determinística? Chatbot."*
- ⏱ Se estiver atrasado, pule o botão de gates completos e mostre só o teste de concorrência.
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
""",
        "notas": """
- Checar o status (smoke) ANTES de prometer qualquer coisa. Se algo caiu: plano B (docs/plano-b.md) sem tentar consertar ao vivo.
- Pergunta demo: limite por transação. **Sem RAG** ele chuta um valor plausível; **com RAG** responde R$ 5.000 citando `[limites]`.
- Stack para citar rápido: Ollama (inferência local, grátis, dado não sai da máquina), LangChain (cadeia em código), pgvector (busca vetorial no Postgres), Langfuse (traces em http://localhost:3000), Langflow (mesma cadeia em canvas, http://localhost:7860).
- Langflow ≠ substituto de engenharia: é outra **interface** para a mesma cadeia — canvas não dá guardrail, teste nem CI de graça.
- Latência de modelo 3B local: segundos. Trade-off vs API hospedada: custo por token zero × qualidade menor.
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
""",
        "notas": """
- Rodar os dois bloqueios e apontar o campo `"modo": "guardrail"` e o tempo ~0 s: **o modelo nem foi chamado**.
- Mensagem central: regra financeira crítica é **determinística** — não se pede "por favor" para o LLM obedecer.
- Três camadas de validação: determinística (gate) → avaliação por LLM (informativa) → revisão humana (amostral).
- Existe guardrail de **saída** também: CPF ou "transferência realizada" na resposta ⇒ bloqueio (mostrar no guardrails.py se pedirem).
- Ligar com o Lab 1: o bot **informa**; quem executa é a API com autenticação + idempotência. Separação informar×executar.
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
""",
        "notas": """
- Rodar e usar os ~40 s para explicar os tipos de caso enquanto a tela rola.
- **Contar o resultado real da preparação:** o q03 reprovou de verdade — o retrieval trouxe o chunk certo do limite noturno e o Qwen 3B respondeu que o limite "permanece constante". **Falha de groundedness real**, pega pelo eval; teste manual de 2 perguntas nunca pegaria.
- Juiz 3B deu nota 4–6 a respostas boas e 0 a recusas corretas ⇒ **juiz pequeno é informativo, nunca gate**. Checagem determinística decide; juiz sinaliza; humano arbitra.
- Paralelo explícito para fechar: dataset de evals : chatbot :: Gherkin : API. Mesmo lifecycle (pergunta do Cláudio sobre aplicar a pipeline a chatbot).
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
""",
        "notas": """
- Fechar respondendo nominalmente as 4 perguntas da turma (Matheus, Renato, Cauã, Cláudio) em 1 frase cada — tudo foi demonstrado ao vivo.
- Perguntas de discussão (escolher 2):
  - *Onde a automação deve parar para uma decisão humana no contexto de vocês?*
  - *Qual é a "chave de idempotência" do processo de vocês — o invariante que ninguém testou ainda?*
  - *Se IA escreve implementação E testes, como evitar que ambos estejam errados juntos?* (resposta: oráculo derivado do requisito + papéis separados)
- Encerrar com: **qualidade é propriedade da esteira, não do commit.**
- Repo fica disponível: branches starter → implemented → validated para reproduzirem em casa.
""",
        "arquivos": [".agents/orchestration.md"],
        "acoes": [],
    },
]
