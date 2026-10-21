# Rule — Representação de dinheiro

- Todo valor monetário é `int` em **centavos de BRL** (`valor_centavos`).
- Proibido `float`/`Decimal` implícito em cálculo de saldo, limite ou transferência.
- Conversão para exibição (R$ x,yy) acontece apenas na borda (UI/log), nunca no domínio.
- Limite por transação: `500_000` centavos (R$ 5.000,00) — constante única em `service.py`.
