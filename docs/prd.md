# PRD — TechPix Transferências Pix (simulado)

**Status:** aprovado para o laboratório · **Dono:** Produto TechPix · **Data:** 2026-10-21

## 1. Contexto e problema

A TechPix (fintech fictícia) precisa de um serviço de transferência Pix interno que seja
**correto sob concorrência**, auditável e resiliente a falhas do provedor de liquidação.
Este PRD é a **fonte de verdade** do laboratório (cenário Greenfield): não existe código
legado para servir de referência de comportamento.

## 2. Objetivos

1. Permitir transferências entre contas TechPix com débito/crédito atômicos.
2. Garantir **idempotência**: a mesma `Idempotency-Key` nunca efetiva duas transferências,
   mesmo sob requisições concorrentes.
3. Registrar **trilha de auditoria** imutável de todas as operações.
4. Tratar indisponibilidade do provedor: estado `UNKNOWN` + **reconciliação** posterior.

## 3. Fora de escopo

- Integração real com SPI/Banco Central, DICT ou chaves Pix reais.
- Autenticação/autorização de usuários finais (assumida upstream).
- Multi-moeda. Valores em BRL, representados em **centavos (int)** — nunca float.

## 4. Requisitos funcionais

| ID | Requisito |
|----|-----------|
| RF-01 | Criar transferência com `origem`, `destino`, `valor_centavos` e header `Idempotency-Key` obrigatório. |
| RF-02 | Reapresentação da mesma `Idempotency-Key` retorna a transferência original (HTTP 200), sem novo débito. |
| RF-03 | Rejeitar: valor ≤ 0, origem = destino, conta inexistente, saldo insuficiente, valor acima do limite por transação (R$ 5.000,00). |
| RF-04 | Estados: `PROCESSING → COMPLETED \| FAILED \| UNKNOWN`. `UNKNOWN` quando o provedor não confirma (timeout). |
| RF-05 | Endpoint de reconciliação resolve transferências `UNKNOWN` consultando o provedor (simulado). |
| RF-06 | Consultar transferência por id, consultar saldo de conta, listar trilha de auditoria. |

## 5. Requisitos não funcionais

| ID | Requisito |
|----|-----------|
| RNF-01 | **Correção sob concorrência**: N requisições simultâneas com a mesma chave ⇒ exatamente 1 débito. |
| RNF-02 | Nenhum segredo/credencial no repositório; dados 100% fictícios. |
| RNF-03 | Suíte de testes completa em < 2 min em máquina de desenvolvimento. |
| RNF-04 | Toda mudança passa por quality gates (lint, security scan, testes, BDD) + revisão humana. |

## 6. Métricas de sucesso do laboratório

- Teste de concorrência prova RNF-01 (falha no checkpoint `implemented`, passa no `validated`).
- 100% dos cenários Gherkin executáveis e verdes no checkpoint `validated`.

## 7. Riscos e perguntas abertas (discovery)

- **R1:** idempotência implementada como *check-then-act* sem atomicidade é o defeito clássico — exigir teste de concorrência como oráculo independente do código.
- **R2:** `UNKNOWN` não é falha: fundos ficam reservados até reconciliação (decisão em [ADR-0003](adr/0003-estados-e-reconciliacao.md)).
- **Q1 (respondida):** limite por transação fixo em R$ 5.000,00 nesta versão; limites dinâmicos ficam para v2.
