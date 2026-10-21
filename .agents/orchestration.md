# Orquestração de agentes — TechPix

Pipeline BMAD + SDD + BDD com papéis delimitados. Cada agente trabalha em
**worktree isolada** e integra via PR.

## Papéis

| Agente | Entrada | Saída | Ferramentas | Limites |
|--------|---------|-------|-------------|---------|
| **Analista** | PRD | discovery: lacunas, riscos, perguntas | leitura, escrita em `docs/` | não decide arquitetura |
| **Arquiteto** | PRD + discovery | ADRs, `docs/architecture.md`, contratos | leitura, escrita em `docs/`, `specs/` | não implementa |
| **Especificador** | ADRs | `specs/*.md` + `features/*.feature` | escrita em `specs/`, `features/` | não altera `src/` |
| **Implementador** | specs + Gherkin | `src/` + testes unitários | worktree própria, pytest | não altera specs nem features |
| **Testador** | PRD + specs (NÃO o código) | testes de integração/concorrência/invariantes | worktree própria | oráculos independentes da implementação |
| **Revisor** | diff do PR + evidências | aprovação/pedido de mudança | leitura, comentários | não commita correções no PR revisado |

## Regras de paralelismo

- 1 worktree por tarefa: `git worktree add ../wt-<tarefa> -b feat/<tarefa>`.
- Contratos compartilhados (`specs/`, `features/`) são **read-only** para Implementador
  e Testador; mudança de contrato volta para o Especificador.
- Arquivos de alto conflito (ex.: `store.py`) têm no máximo 1 agente por vez.
- Integração sempre por PR: rebase, gates verdes, revisão humana, merge.

## Decisões humanas obrigatórias

1. Aprovação de ADRs que afetam dinheiro/segurança.
2. Merge para `main`.
3. Resolução de qualquer pergunta aberta de discovery.
4. Autorização das operações listadas em `.agents/rules/seguranca.md`.
