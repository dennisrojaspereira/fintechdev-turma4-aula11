"""Oraculo de RNF-01 / I-2: N requisicoes concorrentes com a MESMA Idempotency-Key
efetivam EXATAMENTE UMA transferencia.

Este teste deriva do PRD (nao da implementacao) e e o gate que diferencia os
checkpoints `implemented` (falha: check-then-act) e `validated` (passa: reserva
atomica, ADR-0002).
"""

import threading

from techpix.errors import BusinessError
from techpix.models import TransferState
from techpix.service import TransferService
from techpix.store import Store

N_CONCORRENTES = 8
VALOR = 10_000
SALDO_ALICE = 1_000_000
SALDO_BRUNO = 50_000


def test_concorrencia_mesma_chave_efetiva_apenas_uma_transferencia():
    store = Store()
    store.seed_default_accounts()
    service = TransferService(store)

    barreira = threading.Barrier(N_CONCORRENTES)
    erros: list[Exception] = []

    def requisicao() -> None:
        barreira.wait()  # todas as threads disparam juntas
        try:
            service.create_transfer("k-concorrente", "acc-alice", "acc-bruno", VALOR)
        except BusinessError:
            pass  # 409/422 sao respostas validas sob corrida
        except Exception as exc:  # noqa: BLE001 - qualquer outra falha reprova
            erros.append(exc)

    threads = [threading.Thread(target=requisicao) for _ in range(N_CONCORRENTES)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()

    assert not erros, f"erros inesperados: {erros}"

    efetivadas = [
        t
        for t in store.transfers.values()
        if t.idempotency_key == "k-concorrente" and t.estado is TransferState.COMPLETED
    ]
    alice = store.accounts["acc-alice"]
    bruno = store.accounts["acc-bruno"]

    assert len(efetivadas) == 1, (
        f"RNF-01 violado: {len(efetivadas)} transferencias efetivadas para a mesma chave"
    )
    assert alice.saldo_disponivel_centavos == SALDO_ALICE - VALOR, (
        f"debito duplicado: saldo de alice = {alice.saldo_disponivel_centavos}"
    )
    assert bruno.saldo_disponivel_centavos == SALDO_BRUNO + VALOR
    assert alice.reservado_centavos == 0
