# ADR-0001 — Python + FastAPI + store em memória

**Status:** aceito · **Data:** 2026-10-21

## Contexto

O laboratório precisa de uma API executável em minutos, em qualquer máquina,
sem cloud nem infraestrutura paga, mas com fidelidade suficiente para
demonstrar idempotência, concorrência, estados e auditoria.

## Decisão

- **Python 3.12+ / FastAPI** para a API (tipagem, validação Pydantic, OpenAPI automático).
- **Armazenamento em memória** protegido por `threading.Lock`, atrás de uma interface
  (`store.py`) que em produção seria Postgres com `UNIQUE(idempotency_key)` e transações.
- **Provedor de liquidação simulado e determinístico** (`provider.py`) para que os testes
  sejam reproduzíveis.

## Consequências

- (+) Setup < 2 min; testes rápidos; zero credenciais.
- (−) O lock em memória não cobre múltiplos processos — em produção a atomicidade
  viria do banco (constraint única + transação). O teste de concorrência cobre o
  comportamento dentro do processo, que é onde o bug didático vive.

## Alternativas rejeitadas

- **Postgres desde o início:** mais fiel, porém setup mais pesado para a aula; o Lab 2 já usa Postgres.
- **Node/NestJS:** válido, mas Python mantém consistência com o Lab 2 (LangChain).
