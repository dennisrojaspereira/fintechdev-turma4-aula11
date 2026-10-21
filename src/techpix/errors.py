"""Erros de negocio com codigo estavel (contrato da API em specs/pix-transfer.md)."""

from __future__ import annotations


class BusinessError(Exception):
    codigo = "erro_negocio"
    http_status = 422

    def __init__(self, mensagem: str = "") -> None:
        self.mensagem = mensagem or self.__doc__ or self.codigo
        super().__init__(self.mensagem)


class ValorInvalido(BusinessError):
    """Valor deve ser um inteiro positivo em centavos."""

    codigo = "valor_invalido"


class MesmaConta(BusinessError):
    """Conta de origem e destino devem ser diferentes."""

    codigo = "mesma_conta"


class LimiteExcedido(BusinessError):
    """Valor acima do limite por transacao (R$ 5.000,00)."""

    codigo = "limite_excedido"


class SaldoInsuficiente(BusinessError):
    """Saldo disponivel insuficiente na conta de origem."""

    codigo = "saldo_insuficiente"


class ContaInexistente(BusinessError):
    """Conta nao encontrada."""

    codigo = "conta_inexistente"
    http_status = 404


class ConflitoIdempotencia(BusinessError):
    """Idempotency-Key ja utilizada com payload diferente."""

    codigo = "conflito_idempotencia"
    http_status = 409
