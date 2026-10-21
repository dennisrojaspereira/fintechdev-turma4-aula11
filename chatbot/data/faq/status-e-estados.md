# Status de uma transferência (conteúdo fictício TechPix)

## Quais são os estados de uma transferência TechPix?

Uma transferência Pix na TechPix passa pelos estados: PROCESSING (em
processamento), COMPLETED (concluída), FAILED (falhou, com estorno de qualquer
valor reservado) e UNKNOWN (resultado desconhecido).

## O que significa o estado UNKNOWN?

UNKNOWN significa que o provedor de liquidação não confirmou o resultado dentro
do tempo esperado (timeout). O valor fica reservado — não é debitado em
definitivo nem devolvido — até a reconciliação, um processo automático que
consulta o provedor e resolve a transferência para COMPLETED ou FAILED.
Normalmente a reconciliação ocorre em poucos minutos.

## Minha transferência está PROCESSING há muito tempo. O que fazer?

A maioria das transferências conclui em segundos. Se permanecer PROCESSING por
mais de 5 minutos, ela será tratada pela reconciliação automática. Você pode
acompanhar o status no app TechPix, na aba Extrato.
