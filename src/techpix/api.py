"""API HTTP da TechPix (FastAPI). Contrato em specs/pix-transfer.md."""

from __future__ import annotations

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from .errors import BusinessError
from .models import TransferState
from .service import TransferService
from .store import Store


class TransferIn(BaseModel):
    origem: str = Field(min_length=1)
    destino: str = Field(min_length=1)
    valor_centavos: int


def create_app(store: Store | None = None) -> FastAPI:
    store = store or Store()
    if not store.accounts:
        store.seed_default_accounts()
    service = TransferService(store)

    app = FastAPI(
        title="TechPix — API Pix SIMULADA",
        description="Laboratorio didatico. Nenhuma integracao real com SPI/BACEN.",
        version="0.1.0",
    )
    app.state.store = store
    app.state.service = service

    @app.exception_handler(BusinessError)
    async def business_error_handler(_, exc: BusinessError) -> JSONResponse:
        return JSONResponse(
            status_code=exc.http_status,
            content={"detail": {"erro": exc.codigo, "mensagem": exc.mensagem}},
        )

    @app.get("/health")
    def health() -> dict:
        return {"status": "ok"}

    @app.post("/transfers", status_code=201)
    def create_transfer(
        body: TransferIn,
        idempotency_key: str = Header(min_length=8, max_length=64, alias="Idempotency-Key"),
    ) -> JSONResponse:
        transfer, reutilizada = service.create_transfer(
            idempotency_key, body.origem, body.destino, body.valor_centavos
        )
        if reutilizada:
            status = 200
        elif transfer.estado is TransferState.UNKNOWN:
            status = 202
        else:
            status = 201
        return JSONResponse(status_code=status, content=transfer.to_dict())

    @app.get("/transfers/{transfer_id}")
    def get_transfer(transfer_id: str) -> dict:
        t = store.transfers.get(transfer_id)
        if t is None:
            raise HTTPException(404, detail={"erro": "transferencia_inexistente"})
        return t.to_dict()

    @app.get("/accounts/{account_id}")
    def get_account(account_id: str) -> dict:
        conta = store.accounts.get(account_id)
        if conta is None:
            raise HTTPException(404, detail={"erro": "conta_inexistente"})
        return {
            "id": conta.id,
            "saldo_disponivel_centavos": conta.saldo_disponivel_centavos,
            "reservado_centavos": conta.reservado_centavos,
        }

    @app.post("/admin/reconcile")
    def reconcile() -> dict:
        resolvidas = service.reconcile()
        return {"resolvidas": [t.to_dict() for t in resolvidas]}

    @app.get("/audit")
    def audit() -> list[dict]:
        return store.audit

    return app


app = create_app()
