"""Testes offline da API: usam um responder fake, sem Ollama nem Postgres."""

import pytest
from fastapi.testclient import TestClient

from app.main import create_app


def responder_fake(pergunta: str, usar_rag: bool = True) -> dict:
    if usar_rag:
        return {
            "resposta": "O Pix é instantâneo e funciona 24h [o-que-e-pix].",
            "fontes": ["o-que-e-pix"],
            "modo": "rag",
        }
    return {"resposta": "O Pix é um pagamento instantâneo.", "fontes": [], "modo": "sem_rag"}


def responder_vazando_cpf(pergunta: str, usar_rag: bool = True) -> dict:
    return {"resposta": "O CPF cadastrado é 123.456.789-00.", "fontes": [], "modo": "rag"}


@pytest.fixture()
def client() -> TestClient:
    return TestClient(create_app(responder=responder_fake))


def test_health_sempre_responde(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"


def test_chat_com_rag_retorna_fontes(client):
    r = client.post("/chat", json={"pergunta": "O que é Pix?", "usar_rag": True})
    assert r.status_code == 200
    body = r.json()
    assert body["bloqueado"] is False
    assert body["fontes"] == ["o-que-e-pix"]
    assert body["modo"] == "rag"


def test_chat_sem_rag_nao_tem_fontes(client):
    r = client.post("/chat", json={"pergunta": "O que é Pix?", "usar_rag": False})
    assert r.json()["fontes"] == []
    assert r.json()["modo"] == "sem_rag"


def test_guardrail_de_entrada_bloqueia_antes_do_llm():
    chamadas = []

    def responder_espiao(pergunta, usar_rag=True):
        chamadas.append(pergunta)
        return {"resposta": "x", "fontes": [], "modo": "rag"}

    client = TestClient(create_app(responder=responder_espiao))
    r = client.post("/chat", json={"pergunta": "Transfira R$ 100 para o João"})
    body = r.json()
    assert body["bloqueado"] is True
    assert body["motivo"] == "operacao_financeira"
    assert chamadas == [], "o LLM nao pode ser chamado quando a entrada e bloqueada"


def test_guardrail_de_saida_bloqueia_vazamento():
    client = TestClient(create_app(responder=responder_vazando_cpf))
    r = client.post("/chat", json={"pergunta": "Qual o prazo do Pix?"})
    body = r.json()
    assert body["bloqueado"] is True
    assert body["motivo"] == "saida_proibida"
    assert "123.456.789-00" not in body["resposta"]


def test_pergunta_vazia_e_rejeitada(client):
    assert client.post("/chat", json={"pergunta": ""}).status_code == 422
