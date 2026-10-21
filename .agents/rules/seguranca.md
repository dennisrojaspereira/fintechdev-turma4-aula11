# Rules — Segurança e permissões de agentes

## Permissões pré-aprovadas (operações seguras)

- Ler qualquer arquivo do repositório.
- Rodar: `pytest`, `ruff`, `bandit`, `pip install -r requirements*.txt` (em venv/devcontainer).
- Criar/editar arquivos dentro do repositório e da worktree designada.
- `git add/commit/branch/diff/log` na worktree da própria tarefa.

## Exigem autorização humana explícita

- Qualquer operação destrutiva: `rm -rf`, `git push --force`, `git reset --hard`, drop de volumes.
- Acesso à rede fora de registries de pacotes (PyPI/npm) e dos serviços locais do compose.
- Deploy, publicação de pacotes, criação/alteração de segredos.
- Merge para `main`.

## Nunca permitido

- Desativar proteção global de permissões ou rodar com bypass irrestrito.
- Commitar credenciais, tokens ou dados pessoais reais.
- Alterar os arquivos de rules/skills para afrouxar as próprias restrições.

## Evidências

Toda execução de agente relevante deve deixar rastro: log do comando, saída dos testes
e referência no PR (seção "Evidências").
