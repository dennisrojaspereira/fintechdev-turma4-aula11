"""Roteiro do tour guiado da Aula 11 — storytelling em 3 atos.

ATO 1 (passos 1-5): a evolucao da IA em quatro eras — descrever, prever,
gerar, agir — cada uma com demo ao vivo, terminando no problema central:
agentes escrevem software; quem valida?

ATO 2 (passos 6-14): a resposta de engenharia — a fabrica TechPix do PRD
aos quality gates, com o bug de concorrencia cacado ao vivo.

ATO 3 (passos 15-17): a mesma disciplina aplicada a IA que gera — RAG,
guardrails e evals.

Passo 18: fechamento amarrando as quatro eras aos seus testes.
"""

STEPS = [
    # ================================================================ ATO 1
    {
        "id": "intro",
        "titulo": "1. Uma história em quatro eras",
        "explicacao": """
## A IA está produzindo mais código. Estamos produzindo mais qualidade?

Uma história em **quatro eras** — todas demonstradas **ao vivo, nesta máquina**.

```mermaid
flowchart LR
  A["📒 Era 1 · Descrever<br/>o que aconteceu?"] --> B["🧍 Era 2 · Prever<br/>o que é isto?"]
  B --> C["🦙 Era 3 · Gerar<br/>produza algo novo"]
  C --> D["🤖 Era 4 · Agir<br/>construa o sistema"]
  D --> P{{"❓ quem valida?"}}
  P --> L["💣 o bug plantado desta aula"]
```

A cada era, a pergunta muda — e o **jeito de testar** muda junto.
""",
        "notas": """
- A IA evoluiu de analisar informações para executar ações.
- Antes precisávamos escrever tudo; agora precisamos validar o que foi gerado.
- A TechPix vai nos ajudar a entender essa evolução.
- Cada tipo de IA resolve problemas diferentes e exige testes diferentes.
- Quanto mais autonomia, maior a responsabilidade sobre a qualidade.
- 🎬 Plano de corte se o tempo apertar: bug de idempotência (p.14–15), sem RAG × com RAG (p.4 e 16), avaliação contraditória (p.18).
""",
        "arquivos": ["README.md"],
        "acoes": [],
    },
    {
        "id": "era-descrever",
        "titulo": "2. Era 1 — IA que descreve",
        "explicacao": """
## Análise NÃO preditiva: o que aconteceu, e por quê

Antes de qualquer "inteligência": **fatos exatos** — extrato, auditoria, dashboards.

- A verdade é **o próprio dado**. Nenhuma previsão, nenhum modelo.
- O teste desta era: **reconciliação** — os números batem?
- Sem fatos confiáveis, as próximas eras constroem **sobre areia**.
""",
        "notas": """
- Antes de prever qualquer coisa, precisamos entender o que aconteceu.
- Auditoria, relatórios, indicadores e conciliação são fundamentais em fintechs.
- Nem todo problema precisa de inteligência artificial.
- Dados incorretos geram decisões incorretas, independentemente do modelo utilizado.
- Reconciliação é uma forma de validar a verdade financeira do sistema.
- 🎬 Demo: "Auditoria + análise descritiva ao vivo" — transferências reais, trilha imutável e agregações derivadas.
""",
        "arquivos": ["docs/analise-preditiva.md"],
        "acoes": [
            {"id": "api_auditoria", "label": "📒 Auditoria + análise descritiva ao vivo", "demorado": False}
        ],
    },
    {
        "id": "preditiva",
        "titulo": "3. Era 2 — IA que prevê (YOLO)",
        "explicacao": """
## Análise preditiva: o que é isto? o que vai acontecer?

Modelos **discriminativos** treinados em dados rotulados — fraude, churn, visão.
Nosso caso KYC: **"a selfie contém uma pessoa?"**, com **YOLOv8 rodando local**.

- A saída não é texto: **classe + caixa + confiança**.
- O teste desta era: **precision/recall + matriz de confusão**.
""",
        "notas": """
- Modelos preditivos aprendem padrões a partir de dados.
- YOLO identifica objetos e apresenta classificações com níveis de confiança.
- Confiança estatística não significa certeza.
- Precision e recall ajudam a entender falsos positivos e falsos negativos.
- A escolha dos limites de confiança depende do risco do negócio.
- 🎬 Demo: bus.jpg (3 pessoas, conf. 0.87, mostrar imagem anotada) → formas.png (nenhuma pessoa; o "frisbee 0.84" é um falso positivo real — use-o!).
""",
        "arquivos": ["vision/detector.py"],
        "acoes": [
            {"id": "yolo_pessoa", "label": "🧍 Detectar em bus.jpg (tem pessoa?)", "demorado": True},
            {"id": "yolo_nao_pessoa", "label": "🔷 Detectar em formas.png (sem pessoa)", "demorado": True},
        ],
    },
    {
        "id": "era-gerar",
        "titulo": "4. Era 3 — IA que gera",
        "explicacao": """
## Generativa: produza algo novo — com um porém

A demo pergunta o limite Pix a um LLM local **sem nenhum dado da empresa**.
Ele vai responder algo **plausível**. E plausível ≠ correto.

- Saída **aberta e não determinística**.
- O modelo não sabe o que não sabe: **alucinação**.
- Domar isso é o **Ato 3** da aula.
""",
        "notas": """
- Modelos generativos produzem conteúdo a partir dos padrões aprendidos.
- Uma resposta convincente não significa uma resposta correta.
- Alucinações aparecem quando o modelo gera informações sem sustentação adequada.
- Lost in the Middle e degradação do contexto afetam a recuperação e o uso das informações.
- SLMs e LLMs apresentam diferentes capacidades, custos e limitações.
- 🎬 Demo: smoke test antes de prometer; depois "perguntar o limite SEM dados" — guardar a resposta errada para o passo 16. (Teoria na tecla T: lost in the middle, dumb zone, SLM × LLM. Plano B: docs/plano-b.md.)
""",
        "arquivos": ["chatbot/app/rag.py"],
        "acoes": [
            {"id": "chat_status", "label": "🩺 Status da stack (smoke test)", "demorado": True},
            {"id": "chat_sem_rag", "label": "🎲 Perguntar o limite SEM dados (alucinação?)", "demorado": True},
        ],
    },
    {
        "id": "era-agir",
        "titulo": "5. Era 4 — IA que age: agentes",
        "explicacao": """
## O gargalo mudou de lugar

Agentes leem specs, escrevem código, rodam testes, abrem PRs. O gargalo migrou
da **escrita** para a **validação**.

> Se a IA escreve o software, **o que** garante que ele está certo?

```mermaid
flowchart LR
  T["🎯 tarefa"] --> R["🧠 raciocínio"]
  R --> A["🔧 ação<br/>(editar, rodar teste, git)"]
  A --> O["👀 observação<br/>(saída do comando)"]
  O -->|"incompleto"| R
  O -->|"pronto"| E["📦 entrega + evidências"]
  E --> H["🧑 gates + revisão humana"]
```
""",
        "notas": """
- Agentes combinam modelos, ferramentas, memória ou estado e execução de ações.
- Conseguem consultar arquivos, modificar código, executar testes e interpretar resultados.
- Existe diferença entre gerar uma resposta e executar uma operação.
- O gargalo começa a migrar da implementação para a validação.
- Autonomia precisa de limites, rastreabilidade e supervisão.
""",
        "arquivos": [".agents/orchestration.md"],
        "acoes": [],
    },
    # ================================================================ ATO 2
    {
        "id": "prd",
        "titulo": "6. Ato 2 · PRD — a fonte de verdade",
        "explicacao": """
## Greenfield: quem define o comportamento correto?

Sem código legado, a verdade é **construída** — e a fonte é o **PRD**.

- Requisitos numerados: RF-01… e **RNF-01: correção sob concorrência**.
- Lacuna de requisito ⇒ **pergunta para humano**, nunca suposição do agente.
- Dinheiro em **centavos (int)** — float em valor monetário é defeito.
""",
        "notas": """
- Um pedido de negócio não representa necessariamente um requisito completo.
- Precisamos explicitar regras, restrições e comportamentos esperados.
- Em Greenfield, a referência de verdade precisa ser construída.
- Requisitos não funcionais também representam regras críticas de negócio.
- Agentes não devem inventar decisões quando existem lacunas no requisito.
""",
        "arquivos": ["docs/prd.md"],
        "acoes": [],
    },
    {
        "id": "adr",
        "titulo": "7. ADRs — decisões com dono",
        "explicacao": """
## Decisões arquiteturais são registradas, não improvisadas

Agentes implementam rápido demais para decisões implícitas.

- Cada decisão vira um **ADR**: contexto, decisão, consequências, alternativas rejeitadas.
- **ADR-0002** já define a solução do bug desta aula: reserva **atômica**, nunca *check-then-act*.
- Dinheiro/segurança ⇒ **aprovação humana** antes do agente implementar.
""",
        "notas": """
- Nem toda decisão técnica deve ficar escondida no código.
- ADRs registram contexto, alternativas, decisões e consequências.
- Agentes precisam entender por que determinada solução foi escolhida.
- Idempotência exige garantias de atomicidade, especialmente sob concorrência.
- Decisões críticas de segurança e dinheiro precisam de governança.
""",
        "arquivos": ["docs/adr/0002-idempotencia-atomica.md", "docs/adr/0003-estados-e-reconciliacao.md"],
        "acoes": [],
    },
    {
        "id": "sdd",
        "titulo": "8. SDD — spec rastreável",
        "explicacao": """
## Specification-Driven Development

A spec traduz o PRD em **contrato verificável**, rastreável de ponta a ponta.

- Cada caso da API: status code + **código de erro estável**.
- **Invariantes (I-1…I-4)**: oráculos que não dependem da implementação.
- Rastreabilidade: **PRD ⇄ spec ⇄ cenário BDD ⇄ teste**.
""",
        "notas": """
- SDD transforma requisitos em especificações rastreáveis.
- Contratos precisam definir entradas, saídas, erros e invariantes.
- Uma implementação correta precisa respeitar o comportamento esperado.
- Testes não devem simplesmente copiar a lógica da implementação.
- Rastreabilidade conecta requisito, decisão arquitetural, especificação e validação.
""",
        "arquivos": ["specs/pix-transfer.md"],
        "acoes": [],
    },
    {
        "id": "bdd",
        "titulo": "9. BDD — Gherkin executável",
        "explicacao": """
## Comportamento que roda, não documento que envelhece

Cenários Gherkin **em português**, executáveis via pytest-bdd.

- Cada `Quando/Então` vira um teste **de verdade**.
- Spec mudou e o código não? O cenário **quebra** — documentação viva não mente.
""",
        "notas": """
- BDD aproxima produto, desenvolvimento e qualidade.
- Gherkin permite descrever comportamentos com exemplos concretos.
- Cenários de aceitação ajudam a eliminar ambiguidades.
- Testes executáveis funcionam como documentação viva.
- Cenários verdes não significam cobertura completa das regras de negócio.
- 🎬 Demo: rodar os 7 cenários BDD contra a API real.
""",
        "arquivos": ["features/pix-transfer.feature", "tests/test_bdd.py"],
        "acoes": [
            {"id": "bdd_tests", "label": "▶ Rodar os 7 cenários BDD", "demorado": False}
        ],
    },
    {
        "id": "agentes",
        "titulo": "10. Agentes com limites",
        "explicacao": """
## Autonomia sem abrir mão da segurança

- **Rules** = restrições · **Skills** = procedimentos · **Agentes** = papéis delimitados.
- O **Testador não lê o código** — só PRD/spec: oráculo independente.
- Worktrees isoladas, contratos read-only, integração via **PR**.

```mermaid
flowchart LR
  AN["Analista"] --> AR["Arquiteto"] --> ES["Especificador"]
  ES --> IM["Implementador<br/>(worktree A)"]
  ES --> TE["Testador<br/>(worktree B, não lê o código)"]
  IM --> PR["PR + quality gates"]
  TE --> PR
  PR --> RE["Revisor"] --> HU["🧑 humano: merge"]
```
""",
        "notas": """
- Rules definem restrições que precisam ser respeitadas.
- Skills representam procedimentos reutilizáveis.
- Agentes possuem responsabilidades, ferramentas e permissões específicas.
- Separar implementação e testes ajuda a construir validações independentes.
- Autonomia deve ser proporcional ao risco das operações.
""",
        "arquivos": [".agents/orchestration.md", ".agents/rules/engenharia.md", ".agents/rules/seguranca.md"],
        "acoes": [],
    },
    {
        "id": "arquitetura",
        "titulo": "11. Pergunta da turma: e a Clean Architecture?",
        "explicacao": """
## "A arquitetura limpa dificulta para a IA — ela se perde e gasta tokens. Qual usar?"

O diagnóstico está certo — mas o culpado é a **cerimônia**, não os princípios.

- Cada salto de indireção = um arquivo a mais no **contexto** do agente.
- Humanos pagam em cliques; agentes pagam em **tokens e erros de navegação**.

```mermaid
flowchart LR
  subgraph CAM["❌ camadas: 1 feature em 6 arquivos"]
    C1["controller"] --> C2["iservice"] --> C3["service"] --> C4["irepo"] --> C5["repo"] --> C6["mapper/dto"]
  end
  subgraph FAT["✅ fatia vertical: tudo junto"]
    F1["transfers/api.py"] --> F2["transfers/service.py"] --> F3["transfers/store.py"]
    F4["transfers/test_transfers.py"]
  end
```

**Receita:** monólito modular + **fatias verticais** + domínio no centro.
**Este repositório é o exemplo:** 6 arquivos planos, construídos por agentes.
""",
        "notas": """
- Arquitetura também influencia o consumo de contexto dos agentes.
- Muitas abstrações podem dificultar a navegação e a compreensão do sistema.
- Clean Architecture não significa criar camadas desnecessárias.
- Fatias verticais ajudam a organizar funcionalidades por comportamento de negócio.
- Precisamos equilibrar separação de responsabilidades, simplicidade e evolução.
""",
        "arquivos": ["docs/arquitetura-para-agentes.md"],
        "acoes": [],
    },
    {
        "id": "api",
        "titulo": "12. A API que os agentes construíram",
        "explicacao": """
## Transferência, idempotência e estados — em requisições reais

A demo executa a API TechPix e mostra **requisição → resposta** de cada caso:

- Transferência nova ⇒ **201**
- Mesma chave, mesmo payload ⇒ **200, sem novo débito**
- Mesma chave, payload diferente ⇒ **409**
""",
        "notas": """
- Uma transferência precisa respeitar contratos e regras financeiras.
- Idempotência evita que a repetição de uma requisição gere nova operação.
- A mesma chave com conteúdo diferente deve produzir um conflito.
- Códigos HTTP e erros estáveis fazem parte do contrato.
- Testes sequenciais não garantem comportamento correto sob concorrência.
- 🎬 Demo: sucesso (201) → mesma chave (200, mesmo id, sem novo débito) → payload diferente (409); apontar o saldo da Alice debitado uma vez.
""",
        "arquivos": ["src/techpix/api.py"],
        "acoes": [
            {"id": "api_fluxo", "label": "▶ Sucesso + idempotência + conflito", "demorado": False}
        ],
    },
    {
        "id": "unknown",
        "titulo": "13. Timeout, UNKNOWN e reconciliação",
        "explicacao": """
## O estado mais importante de um sistema de pagamento

Timeout do provedor ⇒ **não sabemos** se liquidou.

- Estornar pode gerar **débito duplo**; confirmar pode **creditar sem liquidação**.
- Resposta certa: **UNKNOWN** + fundos reservados + **reconciliação** depois.
- Retry com a mesma chave é **seguro**.

```mermaid
stateDiagram-v2
  [*] --> PROCESSING: POST (fundos reservados)
  PROCESSING --> COMPLETED: provedor confirma ✅
  PROCESSING --> FAILED: rejeitada (estorno)
  PROCESSING --> UNKNOWN: ⏱ timeout (reserva mantida)
  UNKNOWN --> COMPLETED: reconciliação confirma
  UNKNOWN --> FAILED: reconciliação nega (estorno)
```
""",
        "notas": """
- Timeout não significa necessariamente que uma operação falhou.
- Sistemas financeiros precisam representar estados de incerteza.
- Confirmar ou estornar sem evidência pode gerar inconsistências.
- Retry seguro depende de idempotência.
- Reconciliação permite resolver operações cujo resultado ainda é desconhecido.
- 🎬 Demo: valor 10099 ⇒ 202 UNKNOWN (reservado) → retry seguro (200) → reconciliação resolve e credita.
""",
        "arquivos": ["docs/adr/0003-estados-e-reconciliacao.md"],
        "acoes": [
            {"id": "api_unknown", "label": "▶ Timeout → UNKNOWN → retry → reconciliação", "demorado": False}
        ],
    },
    {
        "id": "bug",
        "titulo": "14. O bug: check-then-act 💣",
        "explicacao": """
## Quem testa o código que a IA escreve?

A branch `implemented` tem o clássico **check-then-act**: checa a chave e só grava depois.

- Sequencial: funciona. **25 testes verdes**, coverage alto.
- Concorrente: N requisições passam na checagem — e **todas debitam**.
- O oráculo que pega deriva do **PRD (RNF-01)**: 8 threads, mesma chave ⇒ **1 débito**.
""",
        "notas": """
- Testes verdes não garantem ausência de defeitos críticos.
- Check-then-act cria uma janela de corrida entre verificação e execução.
- Requisições simultâneas podem passar pela mesma validação.
- Uma operação de R$ 100 pode resultar em múltiplos débitos indevidos.
- O teste correto deve derivar do requisito de concorrência.
- 🎬 Demo: primeiro o diff (o bug parece inocente); depois o teste na branch com bug — ler em voz alta: "RNF-01 violado: 8 transferências efetivadas".
""",
        "arquivos": [],
        "acoes": [
            {"id": "diff_bug", "label": "👀 Ver o diff do bug (implemented → validated)", "demorado": False},
            {"id": "concurrency_implemented", "label": "💥 Rodar o teste de concorrência NA BRANCH COM BUG", "demorado": False},
        ],
    },
    {
        "id": "fix",
        "titulo": "15. A correção e os quality gates",
        "explicacao": """
## Reserva atômica + gates verdes

A correção (ADR-0002): checagem, reserva e débito na **mesma seção crítica**.

- A janela de corrida deixa de existir **por construção**, não por sorte de timing.
- Em produção: transação + `UNIQUE(idempotency_key)`.
""",
        "notas": """
- Precisamos corrigir a causa do problema, não apenas seus sintomas.
- Atomicidade impede que múltiplas operações efetivem a mesma transferência.
- Locks locais não resolvem sozinhos problemas distribuídos.
- Quality gates combinam testes, análise estática e verificações de segurança.
- Cobertura mede execução de código, não necessariamente correção de negócio.
- 🎬 Demo: mesmo teste na versão corrigida passa; gates completos (26 testes + lint) se houver tempo.
""",
        "arquivos": ["src/techpix/service.py", ".github/workflows/quality.yml"],
        "acoes": [
            {"id": "concurrency_validated", "label": "✅ Rodar o teste de concorrência CORRIGIDO", "demorado": False},
            {"id": "gates_validated", "label": "🛡 Rodar TODOS os gates (26 testes + lint)", "demorado": True},
        ],
    },
    # ================================================================ ATO 3
    {
        "id": "rag",
        "titulo": "16. Ato 3 · RAG — ancorando a era 3",
        "explicacao": """
## A resposta para a alucinação do passo 4

Mesma pergunta — agora o retriever busca a **evidência** no pgvector e o LLM
responde **ancorado, citando as fontes**.

```mermaid
flowchart LR
  subgraph ING["ingestão (offline)"]
    F["FAQ .md"] --> CH["chunks por seção"] --> E1["embeddings"] --> V[("pgvector")]
  end
  Q["pergunta"] --> E2["embedding"] --> V
  V --> K["top-4 trechos"] --> P["prompt com<br/>evidência"] --> LLM["Ollama<br/>qwen2.5:3b"] --> R["resposta +<br/>fontes utilizadas"]
```
""",
        "notas": """
- LLMs não conhecem automaticamente as informações internas da empresa.
- RAG recupera documentos relevantes antes de gerar uma resposta.
- Embeddings permitem representar informações para busca por similaridade.
- Recuperar o documento correto não garante interpretação correta.
- LangChain, Langflow, Ollama e Langfuse possuem responsabilidades diferentes na solução.
- 🎬 Demo: relembrar o chute sem RAG → com RAG responde R$ 5.000 citando [limites]. Langfuse em localhost:3000, Langflow em localhost:7860.
""",
        "arquivos": ["chatbot/app/rag.py"],
        "acoes": [
            {"id": "chat_sem_rag", "label": "🎲 Relembrar: SEM RAG (chute)", "demorado": True},
            {"id": "chat_rag", "label": "✅ Agora COM RAG (fontes citadas)", "demorado": True},
        ],
    },
    {
        "id": "guardrails",
        "titulo": "17. Guardrails determinísticos",
        "explicacao": """
## Regra financeira crítica não se negocia com o modelo

Injection, PII e **ordens de transferência**: bloqueados **antes** do LLM.

- Repare no tempo: **~0 s** — o modelo nem é chamado.
- O bot **informa**; quem executa é o sistema do Ato 2.

```mermaid
flowchart LR
  U["entrada do usuário"] --> GE{"guardrail<br/>de entrada"}
  GE -->|"injection / PII /<br/>ordem de transferência"| B1["🚫 bloqueio ~0s<br/>(LLM nem é chamado)"]
  GE -->|ok| LLM["LLM + RAG"]
  LLM --> GS{"guardrail<br/>de saída"}
  GS -->|"CPF / segredo /<br/>'transferência realizada'"| B2["🚫 bloqueio"]
  GS -->|ok| R["resposta"]
```
""",
        "notas": """
- Nem toda decisão deve ser delegada a um modelo probabilístico.
- Guardrails podem atuar antes e depois da geração.
- Regras determinísticas permitem bloquear operações fora do escopo.
- Prompt injection tenta manipular o comportamento esperado do sistema.
- Guardrails complementam, mas não substituem autorização e segurança da aplicação.
- 🎬 Demo: pedir transferência e tentar injection — bloqueio em ~0 s, "modo": "guardrail" (o LLM nem é chamado).
""",
        "arquivos": ["chatbot/app/guardrails.py"],
        "acoes": [
            {"id": "chat_guardrail", "label": "🚫 Pedir uma transferência ao bot", "demorado": False},
            {"id": "chat_injection", "label": "🚫 Tentar prompt injection", "demorado": False},
        ],
    },
    {
        "id": "evals",
        "titulo": "18. Evals — o Gherkin do chatbot",
        "explicacao": """
## Três réguas diferentes — nenhum número isolado é "qualidade"

1. **Gates determinísticos** — 100% ou reprova. Inegociável.
2. **Heurísticas de texto** — medem *presença*, não correção.
3. **Juiz (groundedness)** — informativo, nunca gate.

**A provocação:** respostas passaram na heurística… e levaram **nota baixa do juiz**.
Quem está certo?
""",
        "notas": """
- Respostas de IA generativa também precisam de testes de regressão.
- Evals representam conjuntos de perguntas, expectativas e critérios de avaliação.
- Heurísticas verificam propriedades específicas, mas podem não detectar erros semânticos.
- LLM as a Judge utiliza outro modelo para avaliar respostas e também pode errar.
- Observabilidade e avaliações contínuas ajudam a identificar degradação de qualidade.
- 🎬 Demo: rodar os 14 evals (~40 s); destacar o q03 (groundedness real) e a divergência heurística × juiz — divergência vira revisão humana, não média.
""",
        "arquivos": ["evals/dataset.json", "evals/results/evidencia-2026-10-21.md"],
        "acoes": [
            {"id": "evals", "label": "🧪 Rodar os 14 evals ao vivo (~40 s)", "demorado": True}
        ],
    },
    # ============================================================ FECHAMENTO
    {
        "id": "fim",
        "titulo": "19. Fechamento — cada era, seu teste",
        "explicacao": """
## IA acelera a implementação. Não transfere a responsabilidade.

A história que percorremos:

| Era | Pergunta | O teste |
|-----|----------|---------|
| **Descrever** | o que aconteceu? | reconciliação — os números batem |
| **Prever** | o que é isto? | precision/recall, matriz de confusão |
| **Gerar** | produza algo novo | evals, groundedness, guardrails |
| **Agir** | construa o sistema | oráculos do requisito + gates + humano |

Quanto mais autonomia a IA ganha, **mais engenharia de validação** ela exige.

> **Qualidade é propriedade da esteira, não do commit.**
""",
        "notas": """
- Análise descritiva exige dados confiáveis e reconciliação.
- Modelos preditivos exigem avaliação estatística de seus resultados.
- IA generativa exige fundamentação, guardrails, evals e observabilidade.
- Agentes exigem requisitos explícitos, validações independentes e governança.
- A IA acelera a implementação, mas a qualidade continua sendo responsabilidade da engenharia.
""",
        "arquivos": ["docs/analise-preditiva.md"],
        "acoes": [],
    },
]

# Tecnologias destacadas em cada passo (cards animados na tela do publico).
TECNOLOGIAS = {
    "intro": [
        {"icone": "📒", "nome": "Auditoria", "desc": "era 1: descrever"},
        {"icone": "🧍", "nome": "YOLOv8", "desc": "era 2: prever"},
        {"icone": "🦙", "nome": "Ollama + RAG", "desc": "era 3: gerar"},
        {"icone": "🤖", "nome": "Agentes", "desc": "era 4: agir"},
        {"icone": "⚡", "nome": "FastAPI", "desc": "a TechPix que eles construíram"},
        {"icone": "🧪", "nome": "pytest + BDD", "desc": "os testes que seguram tudo"},
        {"icone": "📊", "nome": "Langfuse", "desc": "observabilidade e evals"},
        {"icone": "🐳", "nome": "Docker", "desc": "stack 100% local"},
    ],
    "era-descrever": [
        {"icone": "📒", "nome": "Trilha de auditoria", "desc": "fatos imutáveis com timestamp"},
        {"icone": "➕", "nome": "Agregação exata", "desc": "soma e contagem, não palpite"},
        {"icone": "🤝", "nome": "Reconciliação", "desc": "o teste desta era"},
    ],
    "preditiva": [
        {"icone": "🧍", "nome": "YOLOv8", "desc": "classe + caixa + confiança numa passada"},
        {"icone": "🔥", "nome": "PyTorch", "desc": "inferência local em CPU"},
        {"icone": "📊", "nome": "Matriz de confusão", "desc": "o teste desta era"},
        {"icone": "🎚", "nome": "Limiar de confiança", "desc": "decisão de negócio, não técnica"},
    ],
    "era-gerar": [
        {"icone": "🦙", "nome": "Ollama", "desc": "qwen2.5:3b na GTX 1660"},
        {"icone": "🐜", "nome": "SLM", "desc": "pequeno, local, privado — frágil em instruções"},
        {"icone": "🐘", "nome": "LLM", "desc": "fronteira: raciocínio e agentes (teoria: tecla T)"},
        {"icone": "🎲", "nome": "Não determinismo", "desc": "plausível ≠ correto"},
        {"icone": "👻", "nome": "Alucinação", "desc": "a fratura da era 3"},
    ],
    "era-agir": [
        {"icone": "🤖", "nome": "Agentes", "desc": "leem spec, escrevem código, abrem PR"},
        {"icone": "🌿", "nome": "git worktrees", "desc": "paralelismo com isolamento"},
        {"icone": "⚖️", "nome": "O novo gargalo", "desc": "validação, não escrita"},
    ],
    "prd": [
        {"icone": "📄", "nome": "Docs-as-code", "desc": "PRD versionado junto do código"},
        {"icone": "🔢", "nome": "Centavos (int)", "desc": "dinheiro nunca em float"},
        {"icone": "🎯", "nome": "RNF-01", "desc": "correção sob concorrência"},
    ],
    "adr": [
        {"icone": "📐", "nome": "ADR", "desc": "decisão com contexto e consequências"},
        {"icone": "🧑‍⚖️", "nome": "Aprovação humana", "desc": "dinheiro/segurança não é automático"},
    ],
    "sdd": [
        {"icone": "📋", "nome": "SDD", "desc": "spec rastreável PRD ⇄ teste"},
        {"icone": "🧭", "nome": "Invariantes", "desc": "oráculos independentes do código"},
        {"icone": "🎲", "nome": "Provedor determinístico", "desc": "teste sem flakiness"},
    ],
    "bdd": [
        {"icone": "🥒", "nome": "Gherkin", "desc": "comportamento em português"},
        {"icone": "🧪", "nome": "pytest-bdd", "desc": "cada Então vira assert"},
    ],
    "agentes": [
        {"icone": "🤖", "nome": "Agentes com papéis", "desc": "analista → revisor, limites claros"},
        {"icone": "🌿", "nome": "git worktrees", "desc": "isolamento por tarefa"},
        {"icone": "📦", "nome": "devcontainer", "desc": "sandbox com menor privilégio"},
        {"icone": "🔒", "nome": "Rules", "desc": "restrições que agente não afrouxa"},
    ],
    "arquitetura": [
        {"icone": "🍰", "nome": "Fatias verticais", "desc": "tudo da feature mora junto"},
        {"icone": "📣", "nome": "Screaming arch", "desc": "pastas gritam o domínio"},
        {"icone": "🗺", "nome": "CLAUDE.md", "desc": "o GPS do agente no repo"},
        {"icone": "✂️", "nome": "YAGNI", "desc": "indireção só com 2ª implementação"},
    ],
    "api": [
        {"icone": "⚡", "nome": "FastAPI", "desc": "endpoints tipados + OpenAPI"},
        {"icone": "🛡", "nome": "Pydantic", "desc": "validação na borda"},
        {"icone": "🔑", "nome": "Idempotency-Key", "desc": "contrato contra duplicidade"},
    ],
    "unknown": [
        {"icone": "🔁", "nome": "Máquina de estados", "desc": "PROCESSING → … → UNKNOWN"},
        {"icone": "🤝", "nome": "Reconciliação", "desc": "resolve o desconhecido depois"},
        {"icone": "🏦", "nome": "Reserva de fundos", "desc": "timeout não cria nem destrói dinheiro"},
    ],
    "bug": [
        {"icone": "🧵", "nome": "threading.Barrier", "desc": "corrida determinística no teste"},
        {"icone": "🌿", "nome": "git worktree", "desc": "branch com bug rodando ao lado"},
        {"icone": "💣", "nome": "check-then-act", "desc": "o anti-padrão clássico"},
    ],
    "fix": [
        {"icone": "🔐", "nome": "Seção crítica", "desc": "checar + reservar numa operação"},
        {"icone": "🧹", "nome": "ruff", "desc": "lint / static analysis"},
        {"icone": "🕵", "nome": "bandit + gitleaks", "desc": "security e secrets no CI"},
        {"icone": "⚙️", "nome": "GitHub Actions", "desc": "gates bloqueantes no PR"},
    ],
    "rag": [
        {"icone": "🦜", "nome": "LangChain", "desc": "retriever + prompt + LLM"},
        {"icone": "🐘", "nome": "pgvector", "desc": "embeddings no Postgres"},
        {"icone": "📎", "nome": "Citação de fontes", "desc": "resposta com evidência"},
        {"icone": "📊", "nome": "Langfuse", "desc": "trace de cada resposta"},
        {"icone": "🎨", "nome": "Langflow", "desc": "mesma cadeia, canvas visual"},
    ],
    "guardrails": [
        {"icone": "🚫", "nome": "Guardrails", "desc": "regex determinístico, pré-LLM"},
        {"icone": "🧱", "nome": "Entrada E saída", "desc": "injection, PII, 'transferi!'"},
        {"icone": "⚖️", "nome": "Informar ≠ executar", "desc": "quem transfere é o Ato 2"},
    ],
    "evals": [
        {"icone": "🏆", "nome": "Golden dataset", "desc": "14 casos versionados"},
        {"icone": "✅", "nome": "Checagem determinística", "desc": "guardrails: 100% ou reprova"},
        {"icone": "⚖️", "nome": "LLM-as-a-Judge", "desc": "informativo, nunca gate"},
    ],
    "fim": [
        {"icone": "📒", "nome": "Descrever", "desc": "teste: reconciliação"},
        {"icone": "🧍", "nome": "Prever", "desc": "teste: matriz de confusão"},
        {"icone": "🦙", "nome": "Gerar", "desc": "teste: evals + guardrails"},
        {"icone": "🤖", "nome": "Agir", "desc": "teste: oráculos + gates + humano"},
    ],
}

# Teoria de cada passo (painel expansivel "📚 Teoria" na tela do publico; tecla T).
TEORIA = {
    "intro": """
### Onde cada coisa mora

**IA ⊃ Machine Learning ⊃ Deep Learning.** IA é o guarda-chuva (qualquer técnica que
simule comportamento inteligente, até regras `if/else`); **ML** é o subconjunto que
*aprende dos dados* em vez de ser programado regra a regra; **Deep Learning** usa redes
neurais profundas; e os **LLMs/difusão** são deep learning **generativo**.

A linha do tempo que esta aula percorre:

| Década | Dominante | Exemplo |
|--------|-----------|---------|
| 1990s–2000s | Regras + BI | relatórios, SQL, data warehouse |
| 2000s–2010s | ML clássico | regressão, árvores, SVM — score de crédito |
| 2012–2020 | Deep learning | visão (CNNs/YOLO), voz |
| 2020→ | Transformers/LLMs | GPT, Claude, Qwen — texto e código |
| 2023→ | **Agentes** | LLM + ferramentas + loop de ação |

**Discriminativo × generativo**, formalmente: o discriminativo aprende **P(rótulo | entrada)**
("dado o pixel, qual a classe?"); o generativo aprende a **distribuição do próprio dado**
e amostra dela ("qual o próximo token provável?"). É por isso que um classifica com
confiança calibrável e o outro *inventa com fluência*.
""",
    "era-descrever": """
### Analytics descritiva e diagnóstica

O modelo de maturidade analítica (popularizado pelo Gartner) tem 4 degraus:
**descritiva** (o que aconteceu?) → **diagnóstica** (por quê?) → **preditiva** (o que
vai acontecer?) → **prescritiva** (o que fazer a respeito?). As duas primeiras são
"não preditivas": **não há modelo aprendendo** — há agregação, filtro e junção de fatos.

Conceitos-chave:

- **OLTP × OLAP:** o banco transacional (OLTP) otimiza escritas pequenas e consistentes
  (a API Pix); o analítico (OLAP) otimiza varreduras e agregações (o dashboard). Misturar
  os dois derruba o sistema de pagamento no fechamento do mês.
- **Event log / auditoria imutável:** em vez de guardar só o estado final, guarda-se a
  sequência de **eventos** (append-only). O estado é derivável; o inverso não. É a base
  de event sourcing, da trilha exigida pelo BACEN e da reconciliação.
- **Reconciliação:** comparar duas fontes independentes do mesmo fato (meu ledger × o
  do provedor) e explicar toda diferença. É o "teste" desta era: exato, binário, sem
  probabilidade.
""",
    "preditiva": """
### Aprendizado supervisionado em 5 linhas

O modelo recebe pares **(entrada, rótulo)** — fotos + "tem pessoa/não tem" — e ajusta
parâmetros para minimizar o erro. Depois é avaliado em dados **que nunca viu**
(split treino/teste); decorar o treino e falhar no teste é **overfitting**.

### As métricas que importam

Com a **matriz de confusão** (VP, FP, FN, VN):

- **Precision = VP / (VP + FP)** — das que eu disse "pessoa", quantas eram?
- **Recall = VP / (VP + FN)** — das pessoas reais, quantas eu achei?
- **F1** = média harmônica das duas. Acurácia engana com classes desbalanceadas
  (99% dos frames sem fraude ⇒ "nunca é fraude" tem 99% de acurácia e recall 0).

O **limiar de confiança** desliza o equilíbrio: limiar baixo ⇒ recall alto, mais falsos
positivos; limiar alto ⇒ o contrário. A curva disso é a ROC/PR.

### YOLO por dentro (1 parágrafo)

YOLO = *You Only Look Once*: uma CNN divide a imagem em grade e, em **uma única
passada**, prevê para cada célula caixas (regressão de coordenadas), classes e
confiança; o **NMS** (non-maximum suppression) remove caixas sobrepostas usando **IoU**
(interseção sobre união). Uma passada ⇒ rápido ⇒ tempo real. O "n" de yolov8**n** é
nano: menos parâmetros, menos precisão, mais velocidade.

```mermaid
flowchart LR
  I["🖼 imagem"] --> C["CNN<br/>(uma passada)"]
  C --> G["grade: caixas +<br/>classes + confiança"]
  G --> N["NMS<br/>(remove sobrepostas por IoU)"]
  N --> L{"person ≥ limiar?"}
  L -->|sim| S["✅ PESSOA DETECTADA"]
  L -->|não| X["🚫 sem pessoa"]
```
""",
    "era-gerar": """
### O que um LLM realmente faz

Um transformer treinado em trilhões de tokens aprende **P(próximo token | contexto)**.
Gerar texto = amostrar dessa distribuição, token a token. A **temperatura** regula a
amostragem: 0 ≈ sempre o mais provável (mais estável), alta = mais diversidade.

```mermaid
flowchart LR
  P["contexto<br/>(prompt + já gerado)"] --> M["transformer"]
  M --> D["P(próximo token)"]
  D --> A["amostragem<br/>(temperatura)"]
  A --> T["token"]
  T -->|"anexa ao contexto"| P
  T --> F["texto final"]
```

Consequências diretas:

1. **Alucinação não é bug, é a física do modelo:** ele otimiza *plausibilidade
   linguística*, não *verdade factual*. Sem evidência no contexto, o token mais provável
   para "o limite é R$ ___" é um número plausível qualquer.
2. **Janela de contexto:** o modelo só "sabe", na hora, o que está no prompt (+ pesos
   congelados do treino). Conhecimento da empresa precisa **entrar pelo contexto** —
   é exatamente o que o RAG faz no Ato 3.
3. **Não determinismo:** mesma pergunta pode gerar respostas diferentes (amostragem,
   batching). Por isso teste de igualdade exata não funciona — precisamos de evals.
4. **Escala local:** um 3B quantizado (Q4) ocupa ~2 GB e roda numa GTX 1660; um
   modelo de fronteira não. O trade-off é capacidade de seguir instruções — que vocês
   vão ver falhar ao vivo no contrato de citação.

### A janela de contexto tem geografia: *lost in the middle* e a *dumb zone*

A janela de contexto não é uma memória uniforme — **onde** a informação está e
**quanto** da janela você usa mudam a qualidade da resposta:

**Lost in the middle** (Liu et al., 2023): em contextos longos, os modelos recuperam
muito melhor o que está no **começo** e no **fim** do prompt; informação enterrada no
**meio** tem recall drasticamente menor. A curva é um **U**:

```text
recall
 alto │ ███                                         ███
      │ ████                                       ████
      │ █████                                     █████
baixo │ ████████████████████████████████████████████████
      └────────────────────────────────────────────────→
       início          MEIO (vale do U)            fim
                "enterrou no meio = quase não existe"
```

**Dumb zone** (ou *context rot*): a degradação por **ocupação**. Um modelo "de 128k
tokens" não rende igual com a janela cheia — a qualidade de raciocínio e de seguir
instruções cai bem **antes** do limite duro, tipicamente a partir de ~40–60% de uso.
O limite anunciado é até onde ele *aceita* tokens; a zona útil é até onde ele
*pensa bem* com eles.

| Sintoma na prática | Causa |
|--------------------|-------|
| "Ele esqueceu a instrução que dei lá em cima" | instrução no meio do contexto (vale do U) |
| Agente fica repetitivo/perdido em sessão longa | dumb zone: janela cheia de histórico |
| RAG com 20 chunks responde pior que com 4 | evidência diluída + meio do contexto |
| Resumir documento gigante perde o miolo | literalmente lost in the middle |

**O que fazer a respeito (e onde o lab já faz):**

1. **Posição importa:** instruções críticas no início E repetidas no fim; no nosso RAG,
   a evidência entra no system prompt e a **pergunta vem por último** (perto da geração).
2. **Contexto enxuto > contexto cheio:** top-4 chunks, não top-20 — curadoria vence
   volume. Mais contexto ≠ mais qualidade; a partir de um ponto, é o contrário.
3. **Compactação/sumarização** em sessões longas de agente: resumir o histórico e
   recomeçar com o resumo, em vez de arrastar a janela cheia pela dumb zone.
4. **Arquitetura do repo** (passo 11): fatias verticais e CLAUDE.md curto existem para
   o agente **não precisar** encher a janela — menos arquivos carregados = longe da
   dumb zone = mais inteligente na tarefa.

### SLM × LLM: a mesma física, escalas diferentes

**SLM** (*Small Language Model*, ~0.5B–8B parâmetros) e **LLM** (dezenas a centenas de
bilhões) são a **mesma arquitetura** (transformer prevendo o próximo token) — o que
muda com a escala não é "o que ele é", é **o que emerge**: seguir instruções longas,
raciocínio em múltiplos passos, conhecimento de cauda longa e calibração.

| | **SLM** (ex.: Qwen 3B, Phi, Gemma 2B–9B) | **LLM** (ex.: Claude, GPT, Qwen 72B+) |
|---|---|---|
| Parâmetros | ~0.5B–8B (Q4 ⇒ cabe em 2–6 GB) | 30B–1T+ (datacenter/API) |
| Onde roda | sua GPU/CPU, celular, edge, **offline** | nuvem (ou cluster próprio caro) |
| Custo por token | ~zero (energia) | pago por uso |
| Privacidade | dado **não sai da máquina** | depende do contrato/provedor |
| Latência | previsível, sem rede | rede + fila, mas throughput alto |
| Segue instruções complexas | frágil (vimos: ignorou o contrato de citação, copiou placeholder) | forte |
| Raciocínio multi-passo / agentes | limitado | é onde agentes funcionam |
| Conhecimento factual próprio | raso ⇒ **precisa de RAG** | amplo (mas também alucina) |
| Como juiz/avaliador | ruidoso e descalibrado (nota 0 em recusa correta) | utilizável com rubrica |

**Regra de decisão** — pense em *tarefa estreita × tarefa aberta*:

```mermaid
flowchart LR
  Q{"a tarefa é estreita e<br/>bem especificada?"}
  Q -->|"sim (classificar, extrair,<br/>FAQ com RAG, roteamento)"| P{"dado sensível /<br/>volume alto / offline?"}
  P -->|sim| SLM["✅ SLM local<br/>+ RAG + guardrails + evals"]
  P -->|não| TANTO["SLM ou LLM —<br/>decida por custo"]
  Q -->|"não (raciocínio longo,<br/>código, agente, juiz)"| LLM["✅ LLM de fronteira<br/>(API)"]
  SLM -.-> H["híbrido comum:<br/>SLM no fluxo, LLM nos casos difíceis<br/>(cascata/roteador)"]
  LLM -.-> H
```

O padrão de mercado é **híbrido em cascata**: o SLM resolve os 80% baratos e um
roteador escala os 20% difíceis para o LLM — custo de SLM, qualidade de LLM onde
importa. E a disciplina da aula não muda com o tamanho: **quanto menor o modelo, MAIS
o sistema em volta (RAG, guardrails, evals) carrega a qualidade** — o Lab 2 é a prova.
""",
    "era-agir": """
### De chatbot a agente

**Agente = LLM + ferramentas + loop.** O padrão clássico é o **ReAct**: o modelo
alterna *raciocínio* ("preciso rodar os testes") e *ação* (chama a ferramenta
`run_tests`), observa o resultado e decide o próximo passo — até concluir a tarefa.

Níveis de autonomia (simplificado):

| Nível | Quem decide | Exemplo |
|-------|-------------|---------|
| Assistente | humano a cada passo | autocomplete, chat |
| Copiloto | humano aprova lotes | PR gerado para review |
| **Agente** | máquina decide, humano nos gates | implementa a feature inteira |

O risco cresce com a autonomia porque **erros compõem**: um agente que erra o passo 2
constrói os passos 3–20 sobre o erro. Dois antídotos de teoria de controle:
**limites de ação** (sandbox, permissões, menor privilégio — o que ele *pode* fazer) e
**funções de verificação externas** (testes, gates — como sabemos que *fez certo*).
Confiar no agente para se auto-avaliar viola a independência do oráculo — mesmo
princípio do Testador que não lê o código.
""",
    "prd": """
### Requisitos como contrato

- **Requisito funcional (RF):** o que o sistema *faz* (transferir, rejeitar, consultar).
- **Não funcional (RNF):** *propriedades* do fazer — desempenho, segurança,
  **correção sob concorrência**. RNFs são os mais caros de retrofitar e os que agentes
  mais ignoram, porque raramente aparecem no "exemplo de código" médio do treino.
- **Discovery:** o processo de achar o que o PRD não diz. A regra de ouro com agentes:
  **lacuna vira pergunta, não suposição** — uma suposição plausível do modelo é
  indistinguível de requisito para quem lê o código depois.

**Greenfield × Brownfield:** sem legado, a verdade precisa ser *construída* (PRD, ADRs,
contratos, baselines); com legado, a verdade é *arqueologia* (código, incidentes,
comportamento observado) — e legado mente: produção contém bugs normalizados que
ninguém mais questiona. Em ambos, a disciplina é a mesma: **explicitar a fonte de
verdade antes de gerar código**.

Por que **dinheiro em centavos (int)**: ponto flutuante representa 0.1 como dízima
binária — `0.1 + 0.2 ≠ 0.3`. Em dinheiro isso vira centavo sumindo em escala. Inteiros
na menor unidade (centavos) tornam toda soma exata.
""",
    "adr": """
### Architecture Decision Records

Formato proposto por Michael Nygard (2011): um arquivo curto e **imutável** por decisão
arquitetural relevante, com **Contexto** (o problema e as forças em jogo), **Decisão**
(uma frase no presente: "usaremos X"), **Consequências** (o preço, não só o benefício)
e **Alternativas rejeitadas** (com o porquê — é o que evita reabrir o debate).

Por que isso importa *mais* com agentes:

1. **Contexto é o insumo do agente.** Um ADR de 20 linhas no prompt evita que o
   implementador "melhore" a arquitetura para um padrão que o time rejeitou.
2. **Decisão ≠ código.** O código mostra *o que* foi feito; o ADR preserva *por quê* —
   e o porquê é o que impede a próxima pessoa (ou modelo) de desfazer sem saber.
3. **Supersessão, não edição:** decisão mudou ⇒ novo ADR marcando o antigo como
   "substituído". O histórico de decisões é tão auditável quanto o de código.
""",
    "sdd": """
### Specification-Driven Development e a teoria do oráculo

**SDD:** a especificação é um artefato de primeira classe, rastreável (requisito ⇄
spec ⇄ teste), escrita *antes* da implementação — e, na era dos agentes, ela é
literalmente o **prompt estruturado** do implementador.

**O problema do oráculo** (teoria de teste): um teste tem duas partes — o *estímulo*
(entrada) e o **oráculo** (como decidir se a saída está certa). A armadilha com código
gerado: se o oráculo deriva da implementação ("rodei, deu 42, então espero 42"), teste
e código erram **juntos**. Oráculo saudável deriva do **requisito**.

**Invariantes** são os oráculos mais fortes: propriedades que valem para *qualquer*
execução ("dinheiro não é criado nem destruído"), não para um exemplo. É a base do
property-based testing: em vez de 3 exemplos, uma propriedade × milhares de entradas.

**Determinismo do ambiente de teste:** o provedor simulado responde por regra fixa
(valor termina em 99 ⇒ timeout) para eliminar *flakiness* — teste intermitente é pior
que não ter teste, porque ensina o time a ignorar vermelho.

```mermaid
flowchart LR
  PRD["PRD<br/>(RF / RNF)"] --> SPEC["Spec<br/>(casos + invariantes)"]
  SPEC --> BDD["Gherkin<br/>executável"]
  SPEC --> ORA["testes / oráculos<br/>independentes"]
  BDD --> CI["gates no CI"]
  ORA --> CI
  CI --> H["🧑 revisão humana"]
```
""",
    "bdd": """
### Behavior-Driven Development

Criado por Dan North (2006) como evolução do TDD: descrever comportamento **na língua
do negócio** para que produto, QA, dev — e agora agentes — leiam **o mesmo contrato**.

A gramática **Given/When/Then** (Dado/Quando/Então) mapeia para o padrão de teste
*Arrange/Act/Assert*: estado inicial → ação → resultado observável. Cada cenário é
um exemplo concreto; o conjunto de cenários é a **documentação viva** — "viva" porque
executa: se a spec muda e o código não, o cenário **quebra**, e vice-versa. Documento
que não executa envelhece em silêncio.

**Example mapping:** a técnica de descoberta por trás — para cada regra, buscar
exemplos que a confirmam **e o contraexemplo** que a quebra (o cenário de timeout/
UNKNOWN nasceu assim). Com agentes, os cenários funcionam como *casos de aceite
executáveis* do prompt: o implementador termina quando todos passam — critério
objetivo, não opinião.
""",
    "agentes": """
### Os princípios de segurança por trás das rules

- **Menor privilégio** (Saltzer & Schroeder, 1975): cada agente recebe o mínimo de
  acesso para a sua tarefa — o Testador não escreve em `src/`, ninguém escreve em
  `specs/` além do Especificador. Não é desconfiança do modelo: é limitar o **raio de
  explosão** de qualquer erro, humano ou não.
- **Separação de deveres:** quem implementa ≠ quem testa ≠ quem aprova. Vem de
  auditoria financeira; aqui garante a **independência do oráculo** (o Testador que lê
  a implementação é como auditor que lê a resposta antes de conferir a conta).
- **Sandbox/devcontainer:** o processo roda num ambiente onde o pior caso é destruir o
  container, não a máquina. `cap-drop`, `no-new-privileges`, rede restrita.

### git worktree em 3 linhas

Um repositório git pode ter **várias árvores de trabalho** apontando para o mesmo
`.git`: `git worktree add ../wt-tarefa -b feat/tarefa` cria um diretório com outra
branch em checkout **simultâneo**. Agentes paralelos ganham isolamento de arquivos sem
clonar o repo — e a integração continua sendo por merge/PR, onde os gates moram.
""",
    "arquitetura": """
### O custo de contexto: a métrica invisível da arquitetura

Um agente entende o código **carregando arquivos no contexto**. O custo de uma tarefa
é proporcional a quantos arquivos (e saltos de indireção) são necessários para
entender **um** comportamento. Arquitetura em camadas espalha cada feature por N
camadas; fatia vertical concentra. Para humanos a diferença é ergonomia; para agentes
é **tokens, latência e taxa de erro de navegação**.

**O que a Clean Architecture realmente prescreve** (e continua valendo): a **regra da
dependência** — código de domínio não conhece banco, HTTP nem framework; dependências
apontam para dentro. Isso cabe em 3 arquivos planos (`api` → `service` → `store`),
como neste repo. **O que ela não prescreve** (e viram cerimônia): uma interface por
classe, DTOs e mappers entre todas as camadas, factories para objetos únicos.

**Vertical Slice Architecture** (Jimmy Bogard): organizar por caso de uso/feature;
cada fatia decide internamente sua sofisticação — fatia simples fica simples, a
complexa ganha camadas *dentro dela*. **Screaming Architecture** (Uncle Bob, ironia:
o mesmo autor): a estrutura de pastas deve gritar o que o sistema *faz*, não qual
framework usa — princípio que ficou MAIS importante com agentes, porque navegação por
nome é como eles exploram.

Com IA, dois custos mudaram de preço: **escrever código ficou barato** (refatorar para
extrair abstração quando precisar custa pouco) e **carregar contexto ficou caro**
(cada indireção cobra em toda tarefa futura). A conclusão inverte o hábito: comece
plano, extraia sob demanda — o oposto de "deixar os pontos de extensão prontos".

E o custo de contexto não é só financeiro: pela **dumb zone** (passo 4, teoria),
janela mais cheia = modelo **pior** — arquivos espalhados não gastam apenas tokens,
empurram o agente para a zona onde ele raciocina mal. Arquitetura plana mantém o
agente na parte inteligente da janela.
""",
    "api": """
### Idempotência, formalmente

Uma operação `f` é **idempotente** quando `f(f(x)) = f(x)` — aplicar duas vezes tem o
mesmo efeito de aplicar uma. Em HTTP: `GET`, `PUT` e `DELETE` são idempotentes por
contrato; **`POST` não é** — e criar transferência é POST. A solução da indústria
(Stripe popularizou): o cliente manda uma **Idempotency-Key**, e o servidor garante
*no máximo um efeito por chave*, devolvendo a resposta original nas repetições.

Por que o cliente precisa disso: numa falha de rede, ele **não sabe** se o request
chegou (resposta perdida ≠ request perdido). Sem idempotência, o retry seguro é
impossível: repetir pode duplicar; não repetir pode perder a operação.

```mermaid
sequenceDiagram
  participant C as Cliente
  participant A as API TechPix
  C->>A: POST /transfers (Idempotency-Key: K)
  Note over C,A: 💥 resposta se perde na rede
  C->>A: retry — mesmo POST, mesma chave K
  A-->>C: 200 transferência ORIGINAL (nenhum débito novo)
```

Detalhes de contrato que a spec fixa:

- mesma chave + **mesmo payload** ⇒ 200 com a transferência original;
- mesma chave + **payload diferente** ⇒ 409 (o cliente tem um bug — não mascarar);
- códigos de erro **estáveis** (`saldo_insuficiente`) são API: clientes e testes
  dependem deles programaticamente, mensagens humanas podem mudar.
""",
    "unknown": """
### Timeout não é resposta: o problema dos dois generais

Em sistemas distribuídos, quando a chamada ao provedor estoura o tempo, há **três**
possibilidades indistinguíveis: o request não chegou, chegou e falhou, ou chegou e
**funcionou** (a resposta é que se perdeu). É o clássico *Two Generals*: não existe
protocolo que garanta certeza com canal não confiável.

Consequência: **"exactly-once delivery" é mito.** O que existe é *at-least-once*
(reenvia até confirmar) **+ idempotência** no receptor = *effectively-once* no efeito.
É o par retry seguro + Idempotency-Key do passo anterior.

O padrão aqui é o de **saga/reconciliação**: diante da incerteza, (1) não finalize —
estado `UNKNOWN` explícito; (2) **reserve** o recurso (o débito não se perde nem se
duplica); (3) um processo assíncrono consulta a fonte da verdade e converge o estado.
Dualidade com contabilidade: fundos reservados = partidas em trânsito; a reconciliação
é literalmente a prática contábil de bater razão × extrato, agora automatizada.
""",
    "bug": """
### Race condition e TOCTOU

Uma **condição de corrida** existe quando o resultado depende da ordem de execução de
threads/processos concorrentes. O padrão específico aqui é **TOCTOU** —
*Time-Of-Check to Time-Of-Use*: entre **checar** uma condição ("a chave existe?") e
**usar** o resultado ("então gravo"), o mundo muda. As duas requisições leem "não
existe" **antes** de qualquer uma gravar — e ambas debitam.

Por que testes comuns não pegam:

1. Teste sequencial nunca abre a janela: uma requisição termina antes da outra começar.
2. Mesmo testes "paralelos" ingênuos raramente colidem na janela de microssegundos —
   passam 99 vezes e falham na centésima (flaky ao contrário: verde mentiroso).

O oráculo correto **força** a colisão: `threading.Barrier` solta as 8 threads no mesmo
instante, e a latência simulada (sleep entre check e act) **alarga a janela** até a
corrida ser determinística. Técnica geral: não torça para a corrida acontecer —
**construa-a**.

```mermaid
sequenceDiagram
  participant R1 as Requisição 1
  participant S as Store
  participant R2 as Requisição 2
  R1->>S: chave K existe? → não
  R2->>S: chave K existe? → não
  Note over R1,R2: ⚠️ janela TOCTOU — as duas passaram na checagem
  R1->>S: debita + grava K
  R2->>S: debita + grava K
  Note over S: 💸 débito duplo (RNF-01 violado)
```

Nota de realismo: TOCTOU em chave de idempotência é bug recorrente em gateways de
pagamento reais; o "check" e o "insert" em queries separadas sem transação é a
assinatura clássica.
""",
    "fix": """
### Exclusão mútua e atomicidade

A correção aplica **exclusão mútua**: checagem + reserva da chave + débito viram uma
**seção crítica** — ou executa tudo, ou nada, e nunca intercalado. Em memória, um
`Lock`; em banco, **transação + constraint**:

```sql
INSERT INTO idempotency (key, transfer_id) VALUES ($1, $2)
ON CONFLICT (key) DO NOTHING;   -- quem inseriu é o dono; o resto lê o existente
```

O `UNIQUE` é o lock distribuído que você não precisa escrever: o banco serializa por
você. É o **I** de ACID (isolamento) fazendo o trabalho — e por isso o lab avisa que o
lock de processo único não basta com réplicas.

### Gates em camadas (modelo do queijo suíço)

Cada defesa tem furos; a esteira empilha fatias para nenhum furo atravessar tudo:
**lint** (bugs sintáticos) → **security scan** (padrões perigosos) → **secrets scan**
(credencial commitada) → **testes de exemplo** (regressões) → **oráculo de
concorrência** (RNF-01) → **revisão humana** (intenção e contexto). Cobertura mede
quanto código o teste *executa*, não o que ele *verifica* — por isso 100% de cobertura
com oráculo fraco é falsa segurança.

```mermaid
flowchart LR
  C["commit do agente"] --> L["ruff<br/>lint"] --> B["bandit<br/>security"] --> G["gitleaks<br/>secrets"]
  G --> T["pytest + BDD<br/>26 testes"] --> K["oráculo de<br/>concorrência"] --> H["🧑 revisão<br/>humana"] --> M["merge"]
```
""",
    "rag": """
### Embeddings e busca vetorial

Um **embedding** é um vetor denso (768 dims no nomic-embed-text) em que **proximidade
geométrica ≈ proximidade semântica**: "limite do Pix" e "teto por transação" caem
perto, apesar de não dividirem palavras. A similaridade usa o **cosseno** do ângulo
entre vetores (1 = mesma direção). O pgvector guarda esses vetores no Postgres e
indexa com HNSW/IVFFlat para busca aproximada rápida.

### O pipeline RAG

**Ingestão** (offline): documentos → *chunking* (pedaços por seção — pequenos o
bastante para serem específicos, grandes o bastante para terem contexto) → embedding
→ banco vetorial. **Consulta** (online): pergunta → embedding → top-k chunks →
prompt = instruções + **evidência** + pergunta → LLM.

Por que reduz alucinação: transforma "complete de memória" em **compreensão de texto
com evidência no contexto** — tarefa em que até modelos pequenos são bons. Mas atenção
à lição do lab: **recuperar ≠ fundamentar**. O chunk certo no prompt não garante que a
resposta o usou (q03 contradisse a evidência!) — por isso atribuição de fontes e
groundedness se mede, não se assume.
""",
    "guardrails": """
### Por que prompt injection existe (e não tem patch)

No transformer, **instrução e dado viajam no mesmo canal**: tudo é token no mesmo
contexto. "Ignore suas instruções" não é um exploit do software — é **conteúdo
linguisticamente plausível** que o modelo pode seguir. É o SQL injection dos anos 2000,
com um agravante: não existe o equivalente perfeito do *prepared statement* para
linguagem natural.

Logo, a defesa é **em profundidade**, com camadas de naturezas diferentes:

1. **Determinística pré-LLM** (este passo): regex/regras sobre a entrada — custo ~0,
   recall imperfeito, mas o que ela bloqueia, bloqueia *sempre*.
2. **Separação de capacidades:** o chatbot **não tem ferramenta de transferir**.
   Guardrail que só "pede" para o modelo não fazer é política; não dar a ferramenta
   é **arquitetura**.
3. **Determinística pós-LLM:** a saída também é inspecionada (CPF, "transferência
   realizada") — pega o que passou pelas camadas 1 e 2.
4. **Autorização fora do modelo:** operação financeira exige autenticação forte no
   sistema do Ato 2 — o LLM nunca está na cadeia de autorização.

Regra de bolso: **o que for inaceitável errar 1 vez em 1.000, não pode depender só
do modelo.**
""",
    "evals": """
### A teoria de medir um sistema não determinístico

Com saída aberta, não existe `assert resposta == esperado`. A disciplina vira
**propriedades medidas por réguas diferentes** — e cada régua tem física própria:

| Régua | Mede | Natureza | Papel |
|-------|------|----------|-------|
| Checagem determinística | contratos (bloqueou? citou? campo existe?) | exata, binária | **gate** |
| Heurística textual | presença de termos esperados | proxy barato | gate com threshold |
| LLM-as-a-Judge | groundedness/relevância | probabilística | **sinal**, nunca gate |
| Revisão humana | intenção, tom, risco | cara, amostral | árbitro das divergências |

Vieses conhecidos do juiz-LLM (literatura de 2023–24): **posição** (prefere a primeira
opção), **verbosidade** (nota alta para resposta longa), **auto-preferência** (gosta do
próprio estilo) e descalibração em modelos pequenos — vocês viram: nota 0 para recusas
*corretas*, porque "não groundeado" ≠ "errado". Mitigações: rubrica explícita, saída
estruturada (JSON validado), evidência no prompt, e **nunca** promover o juiz a gate.

**Golden dataset** = o conjunto de casos versionado junto do código. Rodar a cada
mudança de prompt/modelo transforma "parece melhor" em **diff mensurável** — é o teste
de regressão da era generativa.

```mermaid
flowchart LR
  D["golden dataset<br/>14 casos"] --> API["/chat"]
  API --> C1{"checagens<br/>determinísticas"}
  C1 -->|"guardrail falhou"| REP["❌ gate reprova"]
  C1 -->|ok| H2["heurísticas<br/>de texto"]
  API --> J["juiz LLM<br/>(trechos + JSON)"]
  H2 --> REL["relatório:<br/>3 réguas separadas"]
  J --> REL
  REL --> HU["🧑 divergências →<br/>revisão humana"]
```
""",
    "fim": """
### A síntese teórica da aula

1. **Hierarquia de validação:** quanto mais aberta a saída, mais indireta a medição —
   do `assert` exato (era 1) à matriz de confusão (era 2), aos evals multi-régua
   (era 3), aos oráculos independentes + gates + humano (era 4). O erro de categoria
   clássico é aplicar a régua de uma era à outra.
2. **Independência do oráculo:** em toda era, quem verifica não pode derivar de quem
   produz — auditor ≠ contador, teste ≠ implementação, juiz ≠ gerador. Quando os dois
   nascem da mesma fonte, erram juntos e em silêncio.
3. **Automation bias:** humanos tendem a aceitar a saída da máquina conforme ela fica
   mais fluente — e a fluência dos LLMs é exatamente a variável que mais cresceu.
   A resposta institucional não é "confie menos", é **estrutura**: gates que não
   dependem de atenção individual.
4. **Custo do defeito** (Boehm): o preço de um erro cresce ordens de magnitude de
   requisito → código → produção. A IA baixou o custo de *gerar* código; o de
   *corrigir em produção* continua o mesmo — logo o valor relativo de especificar e
   testar **subiu**.
""",
}

for _s in STEPS:
    _s["tecnologias"] = TECNOLOGIAS.get(_s["id"], [])
    _s["teoria"] = TEORIA.get(_s["id"], "")
