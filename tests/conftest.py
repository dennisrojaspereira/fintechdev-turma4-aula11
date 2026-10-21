import pytest
from fastapi.testclient import TestClient

from techpix.api import create_app
from techpix.service import TransferService
from techpix.store import Store


@pytest.fixture()
def store() -> Store:
    s = Store()
    s.seed_default_accounts()
    return s


@pytest.fixture()
def service(store: Store) -> TransferService:
    return TransferService(store)


@pytest.fixture()
def client(store: Store) -> TestClient:
    return TestClient(create_app(store))


def post_transfer(client: TestClient, chave: str, origem: str, destino: str, valor: int):
    return client.post(
        "/transfers",
        json={"origem": origem, "destino": destino, "valor_centavos": valor},
        headers={"Idempotency-Key": chave},
    )
