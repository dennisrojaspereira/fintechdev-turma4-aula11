"""Cenarios BDD executaveis (features/pix-transfer.feature) via pytest-bdd."""

import pytest
from fastapi.testclient import TestClient
from pytest_bdd import given, parsers, scenarios, then, when

from techpix.api import create_app
from techpix.store import Store

scenarios("../features/pix-transfer.feature")


@pytest.fixture()
def ctx() -> dict:
    return {}


@given("as contas seed padrão", target_fixture="ctx")
def contas_seed() -> dict:
    store = Store()
    store.seed_default_accounts()
    return {"client": TestClient(create_app(store)), "resposta": None, "transfer_id": None}


def _transferir(ctx: dict, valor: int, origem: str, destino: str, chave: str) -> None:
    r = ctx["client"].post(
        "/transfers",
        json={"origem": origem, "destino": destino, "valor_centavos": valor},
        headers={"Idempotency-Key": chave},
    )
    ctx["resposta"] = r
    if r.status_code in (200, 201, 202):
        ctx["transfer_id"] = r.json()["id"]


_RESTO = '{valor:d} centavos de "{origem}" para "{destino}" com a chave "{chave}"'


@when(parsers.parse("transfiro " + _RESTO))
def transfiro(ctx, valor, origem, destino, chave):
    _transferir(ctx, valor, origem, destino, chave)


@when(parsers.parse("transfiro novamente " + _RESTO))
def transfiro_novamente(ctx, valor, origem, destino, chave):
    _transferir(ctx, valor, origem, destino, chave)


@when("executo a reconciliação")
def executo_reconciliacao(ctx):
    ctx["resposta"] = ctx["client"].post("/admin/reconcile")


@then(parsers.parse("a resposta tem status {status:d}"))
def resposta_status(ctx, status):
    assert ctx["resposta"].status_code == status, ctx["resposta"].text


@then(parsers.parse('a transferência fica no estado "{estado}"'))
def transferencia_estado(ctx, estado):
    r = ctx["client"].get(f"/transfers/{ctx['transfer_id']}")
    assert r.status_code == 200
    assert r.json()["estado"] == estado


@then(parsers.parse('o saldo disponível de "{conta}" é {valor:d} centavos'))
def saldo_disponivel(ctx, conta, valor):
    assert ctx["client"].get(f"/accounts/{conta}").json()["saldo_disponivel_centavos"] == valor


@then(parsers.parse('a conta "{conta}" tem {valor:d} centavos reservados'))
def saldo_reservado(ctx, conta, valor):
    assert ctx["client"].get(f"/accounts/{conta}").json()["reservado_centavos"] == valor


@then(parsers.parse('o erro é "{codigo}"'))
def erro_codigo(ctx, codigo):
    assert ctx["resposta"].json()["detail"]["erro"] == codigo
