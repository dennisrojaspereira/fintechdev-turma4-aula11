# Idempotência e duplicidade (conteúdo fictício TechPix)

## O que é idempotência em uma transferência?

Idempotência é a garantia de que repetir a mesma requisição de transferência não
gera cobrança duplicada. Cada requisição na TechPix carrega uma chave de
idempotência (Idempotency-Key); se a mesma chave for reapresentada, o sistema
retorna a transferência original em vez de criar uma nova.

## Fui cobrado duas vezes pelo mesmo Pix. E agora?

Por construção, a TechPix efetiva no máximo uma transferência por chave de
idempotência, mesmo que o app reenvie a requisição por instabilidade de rede.
Se você identificar duas cobranças no extrato, trata-se de duas transferências
distintas; abra um chamado em Ajuda > Contestação no app autenticado.

## É seguro tentar de novo quando dá erro de conexão?

Sim. O app TechPix reutiliza a mesma chave de idempotência no retry, então a
nova tentativa não duplica o débito — ela retorna o estado da transferência
original.
