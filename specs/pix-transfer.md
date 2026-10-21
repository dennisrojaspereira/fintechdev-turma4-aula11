# SPEC — Transferência Pix TechPix (SDD)

Rastreabilidade: cada regra referencia o PRD ([docs/prd.md](../docs/prd.md)) e os
cenários BDD ([features/pix-transfer.feature](../features/pix-transfer.feature)).

## API

### POST /transfers

Headers: `Idempotency-Key: <string 8..64 chars>` (obrigatório — RF-01)

```json
{ "origem": "acc-alice", "destino": "acc-bruno", "valor_centavos": 15000 }
```

| Caso | Resposta | Regra | PRD | BDD |
|------|----------|-------|-----|-----|
| Sucesso | `201` + transferência `COMPLETED` | débito origem + crédito destino atômicos | RF-01 | `@sucesso` |
| Chave repetida, mesmo payload | `200` + transferência original; **sem novo débito** | reserva atômica da chave (ADR-0002) | RF-02 | `@duplicidade` |
| Chave repetida, payload diferente | `409` | conflito de idempotência | RF-02 | `@conflito` |
| Sem header `Idempotency-Key` | `422` | header obrigatório | RF-01 | — |
| Saldo insuficiente | `422` + `saldo_insuficiente` | saldo disponível < valor | RF-03 | `@saldo` |
| valor_centavos ≤ 0 | `422` + `valor_invalido` | | RF-03 | — |
| origem = destino | `422` + `mesma_conta` | | RF-03 | — |
| Conta inexistente | `404` + `conta_inexistente` | | RF-03 | — |
| Valor > R$ 5.000,00 (500000 centavos) | `422` + `limite_excedido` | limite por transação | RF-03 | `@limite` |
| Timeout do provedor | `202` + transferência `UNKNOWN`; reserva mantida | ADR-0003 | RF-04 | `@timeout` |

### GET /transfers/{id} → `200` transferência | `404`

### GET /accounts/{id} → `200` `{saldo_disponivel_centavos, reservado_centavos}` | `404`

### POST /admin/reconcile → `200` `{resolvidas: [...]}` — resolve `UNKNOWN` (RF-05)

### GET /audit → `200` lista de eventos imutáveis (RF-06)

### GET /health → `200` `{"status": "ok"}`

## Invariantes (oráculos independentes da implementação)

1. **I-1 (conservação):** soma dos saldos + reservas é constante, exceto por criação de contas.
2. **I-2 (idempotência):** para qualquer chave K, no máximo 1 transferência com débito efetivado — **mesmo com N requisições concorrentes** (RNF-01).
3. **I-3 (UNKNOWN):** transferência `UNKNOWN` mantém exatamente `valor_centavos` reservado; nunca credita destino antes da reconciliação.
4. **I-4 (auditoria):** todo evento de negócio gera registro de auditoria com timestamp e não é jamais alterado.

## Simulação determinística do provedor

Para testes reproduzíveis (sem flakiness):

- `valor_centavos % 100 == 99` ⇒ provedor **estoura timeout** ⇒ `UNKNOWN`.
- Na reconciliação, o provedor confirma se `valor_centavos % 2 == 1`, nega caso contrário.
- Qualquer outro valor ⇒ confirmação imediata ⇒ `COMPLETED`.

## Contas seed (fixture de desenvolvimento)

| Conta | Saldo inicial |
|-------|---------------|
| `acc-alice` | R$ 10.000,00 (1_000_000 centavos) |
| `acc-bruno` | R$ 500,00 (50_000) |
| `acc-carla` | R$ 0,00 |
