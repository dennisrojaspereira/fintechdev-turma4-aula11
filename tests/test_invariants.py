"""Invariantes do dominio (specs/pix-transfer.md, secao Invariantes).

Oraculos independentes: derivam do PRD, nao da implementacao.
"""

from tests.conftest import post_transfer

TOTAL_INICIAL = 1_000_000 + 50_000 + 0


def test_i1_conservacao_de_dinheiro(client, store):
    """I-1: nenhuma sequencia de operacoes cria ou destroi centavos."""
    post_transfer(client, "k-inv-00000", "acc-alice", "acc-bruno", 15_000)   # COMPLETED
    post_transfer(client, "k-inv-00001", "acc-alice", "acc-bruno", 10_099)   # UNKNOWN
    post_transfer(client, "k-inv-00002", "acc-bruno", "acc-carla", 1_000)    # COMPLETED
    post_transfer(client, "k-inv-00003", "acc-alice", "acc-bruno", 10_199)   # UNKNOWN
    assert store.total_centavos() == TOTAL_INICIAL

    client.post("/admin/reconcile")  # resolve os UNKNOWN (1 confirma, 1 nega)
    assert store.total_centavos() == TOTAL_INICIAL


def test_i3_unknown_reserva_exata_e_nao_credita(client):
    """I-3: UNKNOWN mantem exatamente o valor reservado e nunca credita o destino."""
    post_transfer(client, "k-inv-unkwn", "acc-alice", "acc-bruno", 10_099)
    alice = client.get("/accounts/acc-alice").json()
    bruno = client.get("/accounts/acc-bruno").json()
    assert alice["reservado_centavos"] == 10_099
    assert bruno["saldo_disponivel_centavos"] == 50_000


def test_i4_auditoria_imutavel_em_ordem(client):
    """I-4: eventos de auditoria tem timestamp e ordem monotonica."""
    post_transfer(client, "k-inv-audit", "acc-alice", "acc-bruno", 15_000)
    eventos = client.get("/audit").json()
    assert eventos, "auditoria nao pode ser vazia apos operacao"
    timestamps = [e["ts"] for e in eventos]
    assert timestamps == sorted(timestamps)
