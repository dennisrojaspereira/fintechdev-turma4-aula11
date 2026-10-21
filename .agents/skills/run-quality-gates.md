# Skill — run-quality-gates

Procedimento reutilizável para validar qualquer mudança antes de abrir PR.

## Passos

```powershell
ruff check src tests            # 1. lint / static analysis (zero findings)
bandit -r src -q                # 2. security scan (zero HIGH/MEDIUM)
pytest -v                       # 3. unitários + integração + BDD + concorrência
pytest tests/test_idempotency_concurrency.py -v   # 4. oráculo de RNF-01 isolado
```

## Critérios de saída

- Todos os comandos com exit code 0.
- Nenhum teste pulado sem justificativa escrita.
- Saída dos comandos anexada ao PR em "Evidências".

## Em caso de falha

1. Não "ajustar o teste para passar": verificar primeiro se o teste reflete o PRD/spec.
2. Se o teste está certo ⇒ corrigir o código. Se a spec está ambígua ⇒ pergunta ao humano.
