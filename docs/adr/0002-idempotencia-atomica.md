# ADR-0002 — Idempotência por reserva atômica da chave

**Status:** aceito · **Data:** 2026-10-21

## Contexto

RF-02/RNF-01 exigem que N requisições concorrentes com a mesma `Idempotency-Key`
efetivem **exatamente uma** transferência. A implementação ingênua
(*check-then-act*: `GET` da chave e depois `INSERT` em passos separados) tem uma
janela de corrida em que duas requisições passam pela checagem antes de qualquer
gravação — o defeito clássico de sistemas de pagamento.

## Decisão

A chave é **reservada atomicamente** em uma única operação crítica
(`store.reserve_idempotency_key`), dentro do lock:

- Se a reserva é nova ⇒ a requisição é a "dona" e executa a transferência.
- Se a chave já existe com o **mesmo payload** ⇒ retorna a transferência original (200).
- Se a chave já existe com **payload diferente** ⇒ `409 Conflict`.

Em produção, o equivalente é `INSERT ... ON CONFLICT DO NOTHING` sobre
`UNIQUE(idempotency_key)` dentro da transação do débito.

## Consequências

- (+) Elimina a janela de corrida por construção, não por sorte de timing.
- (+) O oráculo do requisito é um **teste de concorrência** derivado do PRD
  (`tests/test_idempotency_concurrency.py`), independente da implementação.
- (−) Exige disciplina: toda escrita correlata (débito + reserva) na mesma seção crítica.
