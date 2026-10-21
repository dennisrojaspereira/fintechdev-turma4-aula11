# language: pt
# Executável via pytest-bdd (tests/test_bdd.py). Rastreabilidade: specs/pix-transfer.md
Funcionalidade: Transferência Pix TechPix
  Como cliente TechPix
  Quero transferir dinheiro entre contas
  Para pagar e receber com segurança, sem duplicidade

  Contexto:
    Dado as contas seed padrão

  @sucesso
  Cenário: Transferência com sucesso
    Quando transfiro 15000 centavos de "acc-alice" para "acc-bruno" com a chave "k-sucesso-1"
    Então a resposta tem status 201
    E a transferência fica no estado "COMPLETED"
    E o saldo disponível de "acc-alice" é 985000 centavos
    E o saldo disponível de "acc-bruno" é 65000 centavos

  @duplicidade
  Cenário: Reapresentação da mesma chave de idempotência não debita duas vezes
    Quando transfiro 15000 centavos de "acc-alice" para "acc-bruno" com a chave "k-dup-1"
    E transfiro novamente 15000 centavos de "acc-alice" para "acc-bruno" com a chave "k-dup-1"
    Então a resposta tem status 200
    E a transferência fica no estado "COMPLETED"
    E o saldo disponível de "acc-alice" é 985000 centavos

  @conflito
  Cenário: Mesma chave com payload diferente é rejeitada
    Quando transfiro 15000 centavos de "acc-alice" para "acc-bruno" com a chave "k-conf-1"
    E transfiro novamente 20000 centavos de "acc-alice" para "acc-bruno" com a chave "k-conf-1"
    Então a resposta tem status 409

  @saldo
  Cenário: Saldo insuficiente
    Quando transfiro 60000 centavos de "acc-bruno" para "acc-alice" com a chave "k-saldo-1"
    Então a resposta tem status 422
    E o erro é "saldo_insuficiente"

  @limite
  Cenário: Valor acima do limite por transação
    Quando transfiro 500001 centavos de "acc-alice" para "acc-bruno" com a chave "k-limite-1"
    Então a resposta tem status 422
    E o erro é "limite_excedido"

  @timeout
  Cenário: Timeout do provedor deixa a transferência UNKNOWN e o retry é seguro
    Quando transfiro 10099 centavos de "acc-alice" para "acc-bruno" com a chave "k-timeout-1"
    Então a resposta tem status 202
    E a transferência fica no estado "UNKNOWN"
    E a conta "acc-alice" tem 10099 centavos reservados
    E o saldo disponível de "acc-bruno" é 50000 centavos
    Quando transfiro novamente 10099 centavos de "acc-alice" para "acc-bruno" com a chave "k-timeout-1"
    Então a resposta tem status 200
    E a transferência fica no estado "UNKNOWN"

  @reconciliacao
  Cenário: Reconciliação resolve transferência UNKNOWN confirmada pelo provedor
    Quando transfiro 10099 centavos de "acc-alice" para "acc-bruno" com a chave "k-recon-1"
    E executo a reconciliação
    Então a transferência fica no estado "COMPLETED"
    E a conta "acc-alice" tem 0 centavos reservados
    E o saldo disponível de "acc-bruno" é 60099 centavos
