"""Regras de negocio da transferencia Pix (simulada).

ATENCAO (checkpoint `implemented`): a idempotencia abaixo usa o padrao
check-then-act — consulta a chave e so grava depois de validar e "ir ao banco".
Sob concorrencia, duas requisicoes com a mesma chave passam pela checagem antes
de qualquer gravacao e AMBAS debitam. O teste
tests/test_idempotency_concurrency.py (oraculo derivado do PRD, RNF-01)
demonstra o defeito. Correcao no checkpoint `validated` (ADR-0002).
"""

from __future__ import annotations

import time

from . import provider
from .errors import (
    ConflitoIdempotencia,
    ContaInexistente,
    LimiteExcedido,
    MesmaConta,
    SaldoInsuficiente,
    ValorInvalido,
)
from .models import Transfer, TransferState
from .store import Store

LIMITE_POR_TRANSACAO_CENTAVOS = 500_000  # R$ 5.000,00 (RF-03)

# Simula a latencia de um round-trip ao banco/provedor entre a checagem da
# chave e a gravacao — e exatamente essa janela que torna o bug reproduzivel.
_LATENCIA_SIMULADA_S = 0.02


class TransferService:
    def __init__(self, store: Store) -> None:
        self.store = store

    # ------------------------------------------------------------------ util
    def _validar_payload(self, origem: str, destino: str, valor_centavos: int) -> None:
        if valor_centavos <= 0:
            raise ValorInvalido()
        if origem == destino:
            raise MesmaConta()
        if valor_centavos > LIMITE_POR_TRANSACAO_CENTAVOS:
            raise LimiteExcedido()

    def _mesma_requisicao(self, t: Transfer, origem: str, destino: str, valor: int) -> bool:
        return t.origem == origem and t.destino == destino and t.valor_centavos == valor

    # ------------------------------------------------------------- transferir
    def create_transfer(
        self, idempotency_key: str, origem: str, destino: str, valor_centavos: int
    ) -> tuple[Transfer, bool]:
        """Cria (ou retorna) a transferencia. Retorna (transfer, reutilizada)."""
        self._validar_payload(origem, destino, valor_centavos)

        # BUG (check-then-act): checagem da chave FORA da secao critica.
        existente_id = self.store.idempotency.get(idempotency_key)
        if existente_id is not None:
            t = self.store.transfers[existente_id]
            if not self._mesma_requisicao(t, origem, destino, valor_centavos):
                raise ConflitoIdempotencia()
            return t, True

        if origem not in self.store.accounts or destino not in self.store.accounts:
            raise ContaInexistente()
        conta_origem = self.store.accounts[origem]
        if conta_origem.saldo_disponivel_centavos < valor_centavos:
            raise SaldoInsuficiente()

        # "Ida ao banco": entre a checagem acima e a gravacao abaixo existe uma
        # janela de corrida — outra requisicao com a mesma chave passa pela
        # checagem enquanto esta dorme aqui.
        time.sleep(_LATENCIA_SIMULADA_S)

        t = Transfer(
            idempotency_key=idempotency_key,
            origem=origem,
            destino=destino,
            valor_centavos=valor_centavos,
        )
        with self.store.lock:
            conta_origem.saldo_disponivel_centavos -= valor_centavos
            conta_origem.reservado_centavos += valor_centavos
            self.store.transfers[t.id] = t
            self.store.idempotency[idempotency_key] = t.id  # act — tarde demais
            self.store.log(
                "transferencia_criada",
                transfer_id=t.id,
                idempotency_key=idempotency_key,
                origem=origem,
                destino=destino,
                valor_centavos=valor_centavos,
            )

        self._liquidar(t)
        return t, False

    # ------------------------------------------------------------- liquidacao
    def _liquidar(self, t: Transfer) -> None:
        resultado = provider.liquidar(t.valor_centavos)
        if resultado is provider.ResultadoLiquidacao.TIMEOUT:
            with self.store.lock:
                t.estado = TransferState.UNKNOWN
                self.store.log("liquidacao_timeout", transfer_id=t.id)
            return
        self._finalizar(t, resultado)

    def _finalizar(self, t: Transfer, resultado: provider.ResultadoLiquidacao) -> None:
        with self.store.lock:
            origem = self.store.accounts[t.origem]
            if resultado is provider.ResultadoLiquidacao.CONFIRMADA:
                origem.reservado_centavos -= t.valor_centavos
                self.store.accounts[t.destino].saldo_disponivel_centavos += t.valor_centavos
                t.estado = TransferState.COMPLETED
                self.store.log(
                    "transferencia_efetivada",
                    transfer_id=t.id,
                    idempotency_key=t.idempotency_key,
                    valor_centavos=t.valor_centavos,
                )
            else:
                origem.reservado_centavos -= t.valor_centavos
                origem.saldo_disponivel_centavos += t.valor_centavos
                t.estado = TransferState.FAILED
                t.motivo_falha = "negada_pelo_provedor"
                self.store.log("transferencia_negada", transfer_id=t.id)

    # ----------------------------------------------------------- reconciliacao
    def reconcile(self) -> list[Transfer]:
        """Resolve transferencias UNKNOWN consultando o provedor (RF-05, ADR-0003)."""
        with self.store.lock:
            pendentes = [
                t for t in self.store.transfers.values() if t.estado is TransferState.UNKNOWN
            ]
        resolvidas: list[Transfer] = []
        for t in pendentes:
            resultado = provider.consultar(t.valor_centavos)
            self._finalizar(t, resultado)
            with self.store.lock:
                self.store.log(
                    "reconciliacao", transfer_id=t.id, resultado=resultado.value
                )
            resolvidas.append(t)
        return resolvidas
