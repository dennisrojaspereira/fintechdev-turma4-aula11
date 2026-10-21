"""Testes de integracao da API. Oraculos derivados de specs/pix-transfer.md."""

from tests.conftest import post_transfer


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_transferencia_sucesso(client):
    r = post_transfer(client, "k-api-sucesso", "acc-alice", "acc-bruno", 15_000)
    assert r.status_code == 201
    body = r.json()
    assert body["estado"] == "COMPLETED"
    assert client.get("/accounts/acc-alice").json()["saldo_disponivel_centavos"] == 985_000
    assert client.get("/accounts/acc-bruno").json()["saldo_disponivel_centavos"] == 65_000


def test_idempotencia_sequencial_nao_debita_duas_vezes(client):
    r1 = post_transfer(client, "k-api-dup", "acc-alice", "acc-bruno", 15_000)
    r2 = post_transfer(client, "k-api-dup", "acc-alice", "acc-bruno", 15_000)
    assert r1.status_code == 201
    assert r2.status_code == 200
    assert r2.json()["id"] == r1.json()["id"]
    assert client.get("/accounts/acc-alice").json()["saldo_disponivel_centavos"] == 985_000


def test_mesma_chave_payload_diferente_409(client):
    post_transfer(client, "k-api-conf", "acc-alice", "acc-bruno", 15_000)
    r = post_transfer(client, "k-api-conf", "acc-alice", "acc-bruno", 20_000)
    assert r.status_code == 409
    assert r.json()["detail"]["erro"] == "conflito_idempotencia"


def test_header_idempotency_obrigatorio(client):
    r = client.post(
        "/transfers",
        json={"origem": "acc-alice", "destino": "acc-bruno", "valor_centavos": 100},
    )
    assert r.status_code == 422


def test_saldo_insuficiente(client):
    r = post_transfer(client, "k-api-saldo", "acc-bruno", "acc-alice", 60_000)
    assert r.status_code == 422
    assert r.json()["detail"]["erro"] == "saldo_insuficiente"


def test_limite_excedido(client):
    r = post_transfer(client, "k-api-limite", "acc-alice", "acc-bruno", 500_001)
    assert r.status_code == 422
    assert r.json()["detail"]["erro"] == "limite_excedido"


def test_valor_invalido(client):
    r = post_transfer(client, "k-api-valor", "acc-alice", "acc-bruno", 0)
    assert r.status_code == 422
    assert r.json()["detail"]["erro"] == "valor_invalido"


def test_mesma_conta(client):
    r = post_transfer(client, "k-api-mesma", "acc-alice", "acc-alice", 100)
    assert r.status_code == 422
    assert r.json()["detail"]["erro"] == "mesma_conta"


def test_conta_inexistente(client):
    r = post_transfer(client, "k-api-404", "acc-nao-existe", "acc-bruno", 100)
    assert r.status_code == 404
    assert r.json()["detail"]["erro"] == "conta_inexistente"


def test_timeout_unknown_e_retry_seguro(client):
    r1 = post_transfer(client, "k-api-timeout", "acc-alice", "acc-bruno", 10_099)
    assert r1.status_code == 202
    assert r1.json()["estado"] == "UNKNOWN"
    alice = client.get("/accounts/acc-alice").json()
    assert alice["reservado_centavos"] == 10_099
    assert client.get("/accounts/acc-bruno").json()["saldo_disponivel_centavos"] == 50_000

    r2 = post_transfer(client, "k-api-timeout", "acc-alice", "acc-bruno", 10_099)
    assert r2.status_code == 200
    assert r2.json()["id"] == r1.json()["id"]
    assert client.get("/accounts/acc-alice").json()["reservado_centavos"] == 10_099


def test_reconciliacao_confirmada(client):
    # 10_099: (10099 // 100) = 100 (par) -> provedor confirma na reconciliacao
    post_transfer(client, "k-api-recon-ok", "acc-alice", "acc-bruno", 10_099)
    r = client.post("/admin/reconcile")
    assert r.status_code == 200
    resolvidas = r.json()["resolvidas"]
    assert len(resolvidas) == 1
    assert resolvidas[0]["estado"] == "COMPLETED"
    assert client.get("/accounts/acc-alice").json()["reservado_centavos"] == 0
    assert client.get("/accounts/acc-bruno").json()["saldo_disponivel_centavos"] == 60_099


def test_reconciliacao_negada_estorna(client):
    # 10_199: (10199 // 100) = 101 (impar) -> provedor nega -> estorno
    post_transfer(client, "k-api-recon-neg", "acc-alice", "acc-bruno", 10_199)
    r = client.post("/admin/reconcile")
    resolvida = r.json()["resolvidas"][0]
    assert resolvida["estado"] == "FAILED"
    alice = client.get("/accounts/acc-alice").json()
    assert alice["saldo_disponivel_centavos"] == 1_000_000
    assert alice["reservado_centavos"] == 0


def test_auditoria_registra_eventos(client):
    post_transfer(client, "k-api-audit", "acc-alice", "acc-bruno", 15_000)
    eventos = [e["evento"] for e in client.get("/audit").json()]
    assert "transferencia_criada" in eventos
    assert "transferencia_efetivada" in eventos


def test_get_transferencia_inexistente(client):
    assert client.get("/transfers/trf-nao-existe").status_code == 404
