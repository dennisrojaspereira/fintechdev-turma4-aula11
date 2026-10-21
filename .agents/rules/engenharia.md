# Rules — Engenharia TechPix

Restrições obrigatórias para qualquer agente (ou humano) que escreva código neste repo.

1. **Fonte de verdade:** `docs/prd.md` + `specs/pix-transfer.md`. Não inventar regras de
   negócio; lacuna na spec ⇒ abrir pergunta para humano, nunca assumir.
2. **Dinheiro é `int` em centavos.** Float em valor monetário é defeito, não estilo.
3. **Idempotência é atômica** (ADR-0002). Check-then-act em chave de idempotência é
   defeito conhecido e bloqueia merge.
4. **Todo requisito tem oráculo independente:** o teste deriva do PRD/spec, nunca da
   implementação. Teste que só confirma o que o código faz não conta como cobertura.
5. **Nenhum segredo no repo.** Credenciais só por variável de ambiente (`.env` ignorado,
   `.env.example` versionado). Secrets scanning no CI é gate bloqueante.
6. **Nenhuma integração real** com SPI/Pix/BACEN. Provedor é simulado e determinístico.
7. **Nunca desabilitar controles**: não remover gates do CI, não usar `--no-verify`,
   não pedir bypass de sandbox/permissões.
8. **Toda mudança via PR** com testes verdes + revisão humana. Agente não aprova o
   próprio PR.
