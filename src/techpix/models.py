"""Entidades de dominio. Dinheiro SEMPRE em centavos (int) — ver .agents/rules/dinheiro.md."""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field
from enum import StrEnum


class TransferState(StrEnum):
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    UNKNOWN = "UNKNOWN"


@dataclass
class Account:
    id: str
    saldo_disponivel_centavos: int
    reservado_centavos: int = 0


@dataclass
class Transfer:
    idempotency_key: str
    origem: str
    destino: str
    valor_centavos: int
    estado: TransferState = TransferState.PROCESSING
    id: str = field(default_factory=lambda: f"trf-{uuid.uuid4().hex[:12]}")
    criada_em: float = field(default_factory=time.time)
    motivo_falha: str | None = None

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "idempotency_key": self.idempotency_key,
            "origem": self.origem,
            "destino": self.destino,
            "valor_centavos": self.valor_centavos,
            "estado": self.estado.value,
            "criada_em": self.criada_em,
            "motivo_falha": self.motivo_falha,
        }
