# ADR-0003 — Máquina de estados com UNKNOWN e reconciliação

**Status:** aceito · **Data:** 2026-10-21

## Contexto

O provedor de liquidação pode não responder (timeout). Nesse momento o débito já
foi reservado, mas não sabemos se a liquidação ocorreu. Tratar timeout como falha
e estornar imediatamente pode gerar **débito duplo** se o provedor tiver efetivado;
tratar como sucesso pode **creditar sem liquidação**.

## Decisão

- Timeout ⇒ estado **`UNKNOWN`**: a reserva de fundos é **mantida**, nada é estornado
  nem creditado.
- Um processo de **reconciliação** (`POST /admin/reconcile`) consulta o provedor
  pelo id da transferência e resolve: confirmada ⇒ `COMPLETED` (credita destino);
  negada ⇒ `FAILED` (estorna reserva).
- Reapresentar a mesma `Idempotency-Key` enquanto `UNKNOWN` **não** cria nova
  transferência: retorna a existente (retry seguro para o cliente).

## Consequências

- (+) Nenhum caminho de timeout cria ou destrói dinheiro.
- (+) `UNKNOWN` vira um estado observável, com métrica e trilha de auditoria.
- (−) Saldo "disponível" difere de saldo "contábil" enquanto houver reservas — exposto
  na API como `saldo_disponivel_centavos` e `reservado_centavos`.
