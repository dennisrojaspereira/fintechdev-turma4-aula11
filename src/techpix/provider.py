"""Provedor de liquidacao Pix SIMULADO e deterministico.

NAO ha integracao real com SPI/BACEN. As regras abaixo existem apenas para
tornar os testes reproduziveis (specs/pix-transfer.md):

- liquidar: valor terminado em 99 centavos -> TIMEOUT (resultado desconhecido);
  qualquer outro valor -> CONFIRMADA.
- consultar (reconciliacao): (valor // 100) par -> CONFIRMADA; impar -> NEGADA.
"""

from __future__ import annotations

from enum import StrEnum


class ResultadoLiquidacao(StrEnum):
    CONFIRMADA = "CONFIRMADA"
    NEGADA = "NEGADA"
    TIMEOUT = "TIMEOUT"


def liquidar(valor_centavos: int) -> ResultadoLiquidacao:
    """Tenta liquidar a transferencia no 'provedor'."""
    if valor_centavos % 100 == 99:
        return ResultadoLiquidacao.TIMEOUT
    return ResultadoLiquidacao.CONFIRMADA


def consultar(valor_centavos: int) -> ResultadoLiquidacao:
    """Consulta o resultado real de uma liquidacao que estourou timeout."""
    if (valor_centavos // 100) % 2 == 0:
        return ResultadoLiquidacao.CONFIRMADA
    return ResultadoLiquidacao.NEGADA
