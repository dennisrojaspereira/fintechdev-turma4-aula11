# Arquitetura para desenvolvimento assistido por IA

> Pergunta da turma: *"Clean Architecture acaba dificultando para a IA — ela se perde,
> não encontra arquivos e gasta mais tokens. Existe arquitetura recomendada para novos
> projetos pensando em IA? Recomendam alguma skill?"*

## O diagnóstico está certo — mas o culpado não é a Clean Architecture

O que atrapalha o agente não são os **princípios** (dependências apontando para dentro,
domínio isolado de I/O, testabilidade). É a **cerimônia**: indireção especulativa.
Cada salto — interface → implementação → factory → DI container → camada → mapper —
é um arquivo a mais que o agente precisa **carregar no contexto** para entender um
comportamento. Humanos pagam esse custo em cliques; agentes pagam em **tokens e erros
de navegação**.

```text
custo p/ o agente ≈ (nº de arquivos para entender 1 comportamento) × (tamanho médio)
```

Clean Architecture "de livro" em projeto pequeno: 1 regra de negócio espalhada em
7 arquivos de 5 camadas. O agente erra o arquivo, lê os 7, ou "inventa" o oitavo.

## O que funciona: 6 propriedades de uma arquitetura AI-friendly

### 1. Fatias verticais (vertical slice) em vez de camadas horizontais

Organize por **feature/domínio**, não por tipo técnico. Tudo que muda junto, mora junto.

```text
❌ camadas (espalha a feature)        ✅ fatias (colocation)
src/                                  src/
├── controllers/transfer_controller   ├── transfers/
├── services/transfer_service         │   ├── api.py
├── repositories/transfer_repo        │   ├── service.py
├── dtos/transfer_dto                 │   ├── store.py
├── mappers/transfer_mapper           │   └── test_transfers.py
└── interfaces/itransfer_service      └── accounts/
```

### 2. Screaming architecture (nomes gritam o domínio)

`transfers/`, `accounts/`, `reconciliation/` — não `utils/`, `helpers/`, `managers/`,
`impl/`. O agente navega por **nome**; nome genérico é um buraco negro de tokens.

### 3. Indireção só com segunda implementação (YAGNI para abstrações)

Interface com uma única implementação, factory de objeto único, event bus interno de
um módulo só: cada um é um salto a mais sem benefício presente. **Extraia a abstração
quando a segunda implementação chegar** — refatorar depois é barato (a IA mesma faz).

### 4. Convenção previsível > esperteza

- Teste ao lado do código (`test_X.py` perto de `X.py`) ou espelhado 1:1 em `tests/`.
- Sem barrel files/re-exports que escondem onde o símbolo mora.
- Arquivos coesos de tamanho médio (nem um `main.py` de 3.000 linhas, nem 40 arquivos
  de 12 linhas).
- Tipagem forte: o erro do type checker é feedback que o agente consome sozinho.

### 5. Documentação-mapa na raiz (o "GPS" do agente)

- **`CLAUDE.md` / `AGENTS.md`**: visão da arquitetura, comandos (build/test/run),
  convenções e o que NÃO fazer. É a primeira coisa que o agente lê — cada linha ali
  economiza uma exploração inteira do repo.
- **ADRs** (`docs/adr/`): o *porquê* das decisões, para o agente não "melhorar" o que
  foi decidido de propósito.
- **Specs/contratos** (`specs/`, `features/`): a fonte de verdade que vira prompt.
- READMEs curtos por módulo quando o repo cresce.

### 6. Feedback loop rápido e determinístico

Suíte de testes que roda em segundos, lint e type check locais: o agente itera
sozinho contra eles. Teste lento ou flaky quebra o loop de autocorreção — o agente
"chuta" em vez de verificar.

## Então qual arquitetura usar num projeto novo?

**Monólito modular com fatias verticais + núcleo de domínio puro.** Em uma frase:
o *espírito* da Clean Architecture (domínio no centro, I/O na borda, testável) com a
*forma* mais plana possível (poucas camadas, colocation, nomes de domínio). Este
repositório é o exemplo vivo: [src/techpix/](../src/techpix/) tem 6 arquivos planos —
`api` (borda HTTP) → `service` (regras) → `store`/`provider` (estado e mundo externo)
— e foi construído e testado por agentes sem se perder.

Microserviços, event sourcing, CQRS: continuam válidos **quando o problema pede**
(escala de times, auditoria regulatória) — mas como evolução, não ponto de partida.
Complexidade especulativa custa dobrado na era dos agentes: você paga para criar
e paga em tokens para cada tarefa futura navegar nela.

## E skills? Recomendações práticas (Claude Code)

| Recurso | O que resolve | Exemplo neste repo |
|---------|---------------|--------------------|
| `/init` → `CLAUDE.md` | o mapa do projeto no contexto de toda sessão | — (gere no seu projeto) |
| Rules (`.agents/rules/` ou regras no CLAUDE.md) | restrições que o agente não pode violar | [.agents/rules/](../.agents/rules/) |
| Skills de projeto (`.claude/skills/` ou `.agents/skills/`) | procedimentos repetíveis: rodar gates, criar ADR, subir o app | [.agents/skills/run-quality-gates.md](../.agents/skills/run-quality-gates.md) |
| Subagentes com papéis | implementador ≠ testador ≠ revisor (oráculo independente) | [.agents/orchestration.md](../.agents/orchestration.md) |
| `git worktree` | paralelismo sem conflito de arquivos | demo do passo do bug |

Regra de bolso para fechar: **se um estagiário no primeiro dia acharia o arquivo certo
em 30 segundos só pelos nomes de pasta, o agente também acha.** Arquitetura
AI-friendly é, no fundo, arquitetura humano-friendly com documentação executável.
