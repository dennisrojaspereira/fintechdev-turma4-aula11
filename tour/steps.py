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

Esta aula é uma história em **quatro eras da IA** — e vamos visitar todas ao vivo,
nesta máquina:

1. **Descrever** — dados que contam o que aconteceu (extrato, auditoria).
2. **Prever** — modelos que classificam e antecipam (fraude, KYC com visão).
3. **Gerar** — modelos que produzem texto, código, respostas.
4. **Agir** — agentes que usam tudo isso para **escrever o software**.

A cada era a pergunta muda — e o **jeito de testar** muda junto. O clímax: na era 4,
a IA escreve o código... e plantamos um bug para descobrir **quem pega**.
""",
        "notas": """
- Abrir perguntando: **"quem já recebeu um PR gigante gerado por IA?"** — deixar 2 ou 3 responderem.
- Vender a jornada: *"vamos subir a escada da IA ao vivo: descrever → prever → gerar → agir. Tem bug plantado, detecção de pessoa com YOLO e LLM rodando na GTX 1660 desta máquina."*
- Tese que repete a aula inteira: **cada era tem sua pergunta E seu teste**. Errar o teste da era = incidente.
- Conectar com as perguntas da turma (Matheus: throughput/testes; Renato: autonomia×segurança; Cauã: Greenfield; Cláudio: pipeline BMAD+BDD+SDD) — todas moram na era 4.
- ⏱ ~5 min. Não detalhar tecnologia aqui; os cards são só um trailer.
- **Plano de corte se o tempo apertar:** as 3 demos inegociáveis são (1) o bug de idempotência (p.13–14), (2) sem RAG × com RAG (p.4 e 15) e (3) a avaliação contraditória dos evals (p.17). O resto comprime.
""",
        "arquivos": ["README.md"],
        "acoes": [],
    },
    {
        "id": "era-descrever",
        "titulo": "2. Era 1 — IA que descreve",
        "explicacao": """
## Análise NÃO preditiva: o que aconteceu, e por quê

Antes de qualquer "inteligência": **dados exatos**. Extrato, trilha de auditoria,
dashboards, agregações. Nenhuma previsão — a verdade é o próprio dado, e o teste é
**reconciliação** (os números batem?).

É a fundação de tudo: sem fatos confiáveis, as próximas eras constroem sobre areia.
A demo roda transferências reais na API TechPix e mostra a **trilha de auditoria
imutável** + a análise descritiva (volume, contagens) derivada dela.
""",
        "notas": """
- Frase de abertura: *"a era mais subestimada — e a que sustenta todas as outras."*
- Rodar a demo e apontar: cada evento é um **fato imutável** com timestamp; a análise é **agregação exata**, não palpite.
- Pergunta retórica: *"isso é IA?"* — é analytics. E 80% do valor de dados em fintech ainda mora aqui (conciliação, fechamento contábil, BACEN).
- Teste desta era: **reconciliação e pipeline de dados testada** — número errado aqui é bug de query, não de modelo.
- Gancho para a era 2: *"descrever o passado não barra a fraude de amanhã. Para isso, precisamos prever."*
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

Modelos **discriminativos** treinados em dados rotulados: score de fraude, churn — e
visão computacional. Nosso caso KYC fictício: **"a selfie enviada contém uma
pessoa?"**, respondido pelo **YOLOv8** rodando local.

A saída não é texto: é **classe + caixa + confiança**. Determinístico o bastante para
teste de regressão clássico — e o teste da era é **precision/recall + matriz de
confusão**, sobre um conjunto rotulado que o modelo nunca viu.
""",
        "notas": """
- YOLO = preditivo **discriminativo**: não escreve nada, classifica. COCO (80 classes), yolov8n com ~6 MB.
- Rodar `bus.jpg`: 3 pessoas com confiança até 0.87 — mostrar a **imagem anotada** com as caixas. Depois `formas.png`: nenhuma pessoa.
- **Bônus real da preparação:** no formas.png o modelo viu o círculo verde como "frisbee" com 0.84 — **falso positivo ao vivo**. Para a pergunta "tem pessoa?" o veredito segue certo, mas é por isso que limiar e matriz de confusão existem.
- **O limiar de confiança é decisão de negócio** (recall × falso positivo) — igual ao limite de R$ 5.000 que veremos no PRD. Produto + risco decidem, não o dev.
- Riscos desta era: **drift** (câmera/iluminação novas) e adversarial — não alucinação.
- Gancho para a era 3: *"prever rótulos é poderoso, mas não conversa com o cliente nem escreve código. Entra a IA generativa."*
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

LLMs produzem texto, código, respostas. A saída é **aberta e não determinística** —
e aí mora o problema: a demo abaixo pergunta o limite Pix da TechPix a um LLM local
**sem acesso a nenhum dado da empresa**. Ele vai responder algo **plausível**.
Plausível ≠ correto.

Essa é a fratura da era 3: o modelo não sabe o que não sabe. Como ancorar, bloquear
e medir isso é o **Ato 3** da aula — primeiro precisamos da era 4, onde a coisa
fica séria.
""",
        "notas": """
- Rodar a pergunta SEM RAG e saborear a resposta: um valor plausível, confiante e **sem evidência nenhuma**. (Se a stack do Lab 2 estiver fora: plano B em docs/plano-b.md, não consertar ao vivo.)
- Nomear o fenômeno: **alucinação** — não é bug do modelo, é a natureza dele: gerar o provável, não o verdadeiro.
- *Cliffhanger explícito:* **"guardem essa resposta errada. No Ato 3 voltamos com RAG, guardrails e evals para domar exatamente isso."**
- Trade-offs de rodar local (Ollama, qwen2.5:3b na GTX 1660): custo por token zero, dado não sai da máquina × qualidade menor que API hospedada.
- Gancho para a era 4: *"e se, em vez de responder FAQ, essa IA escrever o sistema de pagamento?"*
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

Agentes combinam as três eras anteriores e **agem**: leem specs, escrevem código,
rodam testes, abrem PRs. A velocidade de implementação explodiu — e o gargalo
migrou da **escrita** para a **validação**: revisar, testar, garantir segurança
e arquitetura.

**Todo o resto desta aula é a resposta a uma pergunta:**

> Se a IA escreve o software, *o que* garante que ele está certo?

A TechPix — nossa fintech fictícia — foi construída exatamente assim: agentes
implementaram, a esteira validou. Incluindo um bug que **só o teste certo pega**.
""",
        "notas": """
- Este é o pivô da aula: fim do "tour pelas eras", começo da engenharia. Respirar.
- Responde o espírito das 4 perguntas da turma: a era 4 não é um produto, é um **modo de produção** — e exige esteira própria.
- Anunciar o Ato 2: *"vamos percorrer a fábrica: PRD → ADR → spec → BDD → agentes com limites → API → e um bug plantado que 25 testes verdes NÃO pegam."*
- Dica de ritmo: daqui até o passo 14 é o coração dos 40 min de lab. ⏱
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

Não existe código legado aqui (Greenfield). A fonte de verdade é o **PRD**: requisitos
funcionais numerados (RF-01…), não funcionais (RNF-01: correção sob concorrência) e
**perguntas abertas de discovery** — lacuna de requisito vira pergunta para humano,
nunca suposição do agente.
""",
        "notas": """
- Responde a pergunta do **Cauã**: no Greenfield a verdade é **construída** — PRD + ADRs + contratos + cenários de aceite + baselines.
- Contraponto Brownfield: a verdade vem de código + contratos + incidentes — e **legado também mente** (produção ≠ especificação correta).
- Destacar no arquivo: dinheiro em **centavos (int)** — float em dinheiro é defeito, não estilo.
- **RNF-01 é a estrela da noite**: N requisições concorrentes com a mesma chave ⇒ exatamente 1 débito. Guardem.
- Mostrar a seção de riscos: o R1 literalmente prevê o bug que vamos plantar.
""",
        "arquivos": ["docs/prd.md"],
        "acoes": [],
    },
    {
        "id": "adr",
        "titulo": "7. ADRs — decisões com dono",
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
- ADR-0003 (UNKNOWN): plantar a semente — "timeout não é sucesso nem falha" — volta no passo 12.
""",
        "arquivos": ["docs/adr/0002-idempotencia-atomica.md", "docs/adr/0003-estados-e-reconciliacao.md"],
        "acoes": [],
    },
    {
        "id": "sdd",
        "titulo": "8. SDD — spec rastreável",
        "explicacao": """
## Specification-Driven Development

A spec traduz o PRD em **contrato verificável**: cada caso da API tem status code,
código de erro estável e rastreabilidade (PRD ⇄ spec ⇄ cenário BDD). No fim, os
**invariantes** (I-1 a I-4) são os oráculos que não dependem da implementação —
ex.: I-1, *dinheiro não é criado nem destruído*.
""",
        "notas": """
- A tabela de casos é literalmente o roteiro dos testes de integração — mostrar 2 linhas (idempotência e limite).
- **Invariantes = oráculos independentes**: o teste deriva do requisito, não do código. Se implementação e teste nascem do mesmo lugar, os dois erram juntos — pergunta do Cláudio.
- Provedor simulado **determinístico** (valor terminado em 99 ⇒ timeout): reproduzível, sem flakiness. Em produção seria um test double do SPI.
""",
        "arquivos": ["specs/pix-transfer.md"],
        "acoes": [],
    },
    {
        "id": "bdd",
        "titulo": "9. BDD — Gherkin executável",
        "explicacao": """
## Comportamento que roda, não documento que envelhece

Os cenários Gherkin (em português!) são **executáveis** via pytest-bdd: cada linha
`Quando/Então` vira um step de teste de verdade. Se a spec mudar e o código não, o
cenário quebra — a documentação não consegue mentir.
""",
        "notas": """
- Abrir o `.feature` primeiro: linguagem de negócio, legível por produto/QA/dev/**agente** — todos leem o mesmo contrato.
- Clicar **Executar** e mostrar os 7 cenários verdes contra a API real.
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
        "titulo": "10. Agentes com limites",
        "explicacao": """
## Autonomia sem abrir mão da segurança

- **Rules** = restrições (nunca float em dinheiro, nunca segredo no repo, nunca desligar gates).
- **Skills** = procedimentos reutilizáveis (como rodar gates, como criar ADR).
- **Agentes** = papéis com entrada/saída/ferramentas delimitadas — o **Testador não lê o código**,
  só o PRD/spec, para os oráculos serem independentes.
- **Orquestração** = worktrees isoladas, contratos read-only, integração via PR.
""",
        "notas": """
- Responde o **Renato** (autonomia × segurança): pré-aprovar operações seguras (testes, lint, leitura), exigir humano para destrutivas/segredos/deploy/merge — **nunca** bypass irrestrito.
- Responde o **Matheus** (worktrees/paralelismo): 1 worktree por tarefa, contratos read-only, 1 agente por arquivo quente, integração via PR. Paralelismo não elimina dependência — pode aumentar retrabalho.
- Detalhe que rende discussão: o Testador **não lê a implementação**. Por quê? Oráculo independente.
- Mostrar a tabela de papéis no orchestration.md.
- Pergunta para a turma: *"quais permissões vocês dariam ao agente no terminal de vocês?"*
""",
        "arquivos": [".agents/orchestration.md", ".agents/rules/engenharia.md", ".agents/rules/seguranca.md"],
        "acoes": [],
    },
    {
        "id": "api",
        "titulo": "11. A API que os agentes construíram",
        "explicacao": """
## Transferência, idempotência e estados — em requisições reais

As ações abaixo executam a API TechPix em memória e mostram **requisição → resposta**
de cada caso: sucesso (201), reapresentação da mesma chave (200, sem novo débito) e
conflito de payload (409).
""",
        "notas": """
- Clicar e narrar devagar as 3 requisições: 201 → 200 (mesmo `id`! sem novo débito) → 409.
- Apontar o saldo final da Alice: começou com 1.000.000, debitou **uma** vez (985.000).
- Código de erro **estável** (`conflito_idempotencia`) = contrato, não mensagem solta — é o que permite cliente e testes reagirem programaticamente.
- Se perguntarem do armazenamento: memória com lock, atrás de interface. **Dizer explicitamente:** o lock só protege **um processo** — com réplicas em produção, a idempotência exige garantia persistente e compartilhada: transação + `UNIQUE(idempotency_key)` / `INSERT ... ON CONFLICT` (ADR-0001, architecture.md).
""",
        "arquivos": ["src/techpix/api.py"],
        "acoes": [
            {"id": "api_fluxo", "label": "▶ Sucesso + idempotência + conflito", "demorado": False}
        ],
    },
    {
        "id": "unknown",
        "titulo": "12. Timeout, UNKNOWN e reconciliação",
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
- Callback da era 1: a reconciliação é **análise descritiva** operando como rede de segurança.
- Frase de efeito: **UNKNOWN não é erro — é honestidade do sistema + processo para resolver.**
""",
        "arquivos": ["docs/adr/0003-estados-e-reconciliacao.md"],
        "acoes": [
            {"id": "api_unknown", "label": "▶ Timeout → UNKNOWN → retry → reconciliação", "demorado": False}
        ],
    },
    {
        "id": "bug",
        "titulo": "13. O bug: check-then-act 💣",
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
- **Clímax da aula.** Ordem: (1) diff, (2) teste falhando.
- No diff, apontar: o bug cabe em ~10 linhas e **parece inocente** — checagem fora do lock + "ida ao banco" no meio. Review humano cansado deixa passar.
- Antes de rodar, lembrar: 25 testes passam nessa branch. Coverage alto. Tudo verde — menos o oráculo de concorrência.
- Rodar e ler em voz alta: **"RNF-01 violado: 8 transferências efetivadas para a mesma chave"** — débito de R$ 800 em vez de R$ 100.
- Pergunta do **Matheus** (como testar throughput de código de agente): não é "mais testes", é **o teste certo derivado do requisito** + barreira para tornar a corrida determinística.
""",
        "arquivos": [],
        "acoes": [
            {"id": "diff_bug", "label": "👀 Ver o diff do bug (implemented → validated)", "demorado": False},
            {"id": "concurrency_implemented", "label": "💥 Rodar o teste de concorrência NA BRANCH COM BUG", "demorado": False},
        ],
    },
    {
        "id": "fix",
        "titulo": "14. A correção e os quality gates",
        "explicacao": """
## Reserva atômica + gates verdes

A correção (ADR-0002) move checagem da chave, validação de saldo, reserva de fundos e
registro da chave para a **mesma seção crítica** — elimina a janela de corrida por
construção. Em produção: transação + `UNIQUE(idempotency_key)`.
""",
        "notas": """
- Rodar o mesmo teste na versão corrigida: **passa** — não por sorte de timing, por construção.
- Rodar os gates completos (se o tempo permitir): 26/26 + ruff + bandit. No CI entram gitleaks (secrets) — e o merge ainda exige **revisão humana**.
- Responder: *"100% de cobertura garante segurança financeira?"* **Não** — cobertura mede o que o teste executa, não o que ele verifica.
- **Transição para o Ato 3:** *"lembram da resposta alucinada da era 3? Hora de pagar essa dívida: a mesma disciplina, aplicada à IA que gera."*
- ⏱ Atrasado? Pule o botão de gates completos.
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
        "titulo": "15. Ato 3 · RAG — ancorando a era 3",
        "explicacao": """
## A resposta para a alucinação do passo 4

No passo 4, o modelo **chutou** o limite Pix. Agora a mesma pergunta com **RAG**:
o retriever busca os trechos relevantes do FAQ no **pgvector** e o LLM responde
**ancorado no contexto, citando as fontes**.

Spec → implementação → teste: para o chatbot, a "spec" é a base de conhecimento, e
a resposta certa aponta a evidência.
""",
        "notas": """
- Callback explícito: *"lembram do chute do passo 4? Mesma pergunta, agora com RAG."* Rodar e comparar: R$ 5.000 citando `[limites]`.
- Mostrar que a resposta traz `fontes` — contrato de citação que os evals vão checar.
- Stack em uma frase cada: Ollama (inferência local), LangChain (cadeia em código), pgvector (busca vetorial), Langfuse (traces em http://localhost:3000), Langflow (mesma cadeia em canvas, http://localhost:7860).
- Langflow ≠ substituto de engenharia: outra **interface** para a mesma cadeia — canvas não dá guardrail, teste nem CI de graça.
""",
        "arquivos": ["chatbot/app/rag.py"],
        "acoes": [
            {"id": "chat_sem_rag", "label": "🎲 Relembrar: SEM RAG (chute)", "demorado": True},
            {"id": "chat_rag", "label": "✅ Agora COM RAG (fontes citadas)", "demorado": True},
        ],
    },
    {
        "id": "guardrails",
        "titulo": "16. Guardrails determinísticos",
        "explicacao": """
## Regra financeira crítica não se negocia com o modelo

Prompt injection, pedido de dados pessoais e **ordens de transferência** são bloqueados
por regras determinísticas **antes** do LLM — repare no tempo: ~0 s, o modelo nem é
chamado. O bot informa; quem executa é o sistema do Ato 2, com autenticação e
idempotência.
""",
        "notas": """
- Rodar os dois bloqueios e apontar `"modo": "guardrail"` e o tempo ~0 s: **o modelo nem foi chamado**.
- Mensagem central: regra financeira crítica é **determinística** — não se pede "por favor" para o LLM obedecer.
- Três camadas: determinística (gate) → avaliação por LLM (informativa) → revisão humana (amostral).
- Existe guardrail de **saída** também: CPF ou "transferência realizada" na resposta ⇒ bloqueio (mostrar no guardrails.py se pedirem).
- Amarra com o Ato 2: o bot **informa**; quem transfere é a API com idempotência. Separação informar × executar.
""",
        "arquivos": ["chatbot/app/guardrails.py"],
        "acoes": [
            {"id": "chat_guardrail", "label": "🚫 Pedir uma transferência ao bot", "demorado": False},
            {"id": "chat_injection", "label": "🚫 Tentar prompt injection", "demorado": False},
        ],
    },
    {
        "id": "evals",
        "titulo": "17. Evals — o Gherkin do chatbot",
        "explicacao": """
## Três réguas diferentes — nenhum número isolado é "qualidade"

14 casos: perguntas conhecidas, fora da base, injeção, PII, transferência, citação.
O runner reporta **três medições separadas**, de propósito:

1. **Gates determinísticos** (guardrails/contratos): 100% ou reprova — inegociável.
2. **Heurísticas de texto** (termos e citações esperados): medem *presença*, não correção.
3. **Groundedness pelo juiz** (LLM local lendo os **trechos recuperados**): informativo.

**A provocação registrada em 21/10:** 8/9 respostas passaram nas heurísticas… e
algumas levaram **nota baixa do juiz**. Como? Porque **avaliadores diferentes medem
propriedades diferentes** — divergência não vira média, vira revisão humana.
""",
        "notas": """
- Rodar e usar os ~40 s para explicar as três réguas enquanto a tela rola.
- **A provocação central:** *"8 de 9 passaram na heurística — e o juiz deu nota baixa em algumas. Quem está certo?"* Resposta: os dois — medem coisas diferentes. Heurística = o termo apareceu; juiz = a resposta é sustentada pelos trechos. **Nunca apresentar um % único como qualidade global.**
- **Caso q03 (real):** retrieval trouxe o chunk certo do limite noturno e o Qwen 3B respondeu que o limite "permanece constante" — **falha de groundedness** que a heurística pegou. Teste manual de 2 perguntas nunca pegaria.
- O juiz agora recebe os **trechos recuperados** (não só nomes de fontes) e responde **JSON validado 0–10** — mesmo assim: juiz 3B é informativo, **nunca gate**. Determinístico decide; juiz sinaliza; humano arbitra.
- Detalhe fino: o campo `fontes` da API só lista fontes **citadas no texto** — recuperar um documento ≠ fundamentar a resposta nele.
- Amarra com o **Matheus**: validar código gerado em escala e validar respostas geradas é o MESMO problema — escolher o oráculo certo para cada propriedade.
- Fechar o paralelo das eras em voz alta — é a ponte para o fechamento.
""",
        "arquivos": ["evals/dataset.json", "evals/results/evidencia-2026-10-21.md"],
        "acoes": [
            {"id": "evals", "label": "🧪 Rodar os 14 evals ao vivo (~40 s)", "demorado": True}
        ],
    },
    # ============================================================ FECHAMENTO
    {
        "id": "fim",
        "titulo": "18. Fechamento — cada era, seu teste",
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
Fonte de verdade explícita, oráculos independentes, gates em camadas e decisões
humanas obrigatórias — **qualidade é propriedade da esteira, não do commit**.
""",
        "notas": """
- Fechar respondendo nominalmente as 4 perguntas da turma (Matheus, Renato, Cauã, Cláudio) em 1 frase cada — tudo foi demonstrado ao vivo.
- Reprisar a tabela apontando as demos: auditoria (p.2), YOLO/frisbee (p.3), chute vs RAG (p.4 e 15), bug RNF-01 (p.13).
- Perguntas de discussão (escolher 2):
  - *Onde a automação deve parar para uma decisão humana no contexto de vocês?*
  - *Qual é a "chave de idempotência" do processo de vocês — o invariante que ninguém testou ainda?*
  - *Se IA escreve implementação E testes, como evitar que ambos estejam errados juntos?* (oráculo do requisito + papéis separados)
- Última frase: **qualidade é propriedade da esteira, não do commit.**
- Repo no GitHub: branches starter → implemented → validated para reproduzirem em casa.
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

for _s in STEPS:
    _s["tecnologias"] = TECNOLOGIAS.get(_s["id"], [])
