"""Armazenamento em memoria thread-safe.

Em producao seria Postgres: o lock equivale a transacao + UNIQUE(idempotency_key).
"""

from __future__ import annotations

import threading
import time

from .models import Account, Transfer


class Store:
    def __init__(self) -> None:
        self.lock = threading.Lock()
        self.accounts: dict[str, Account] = {}
        self.transfers: dict[str, Transfer] = {}
        self.idempotency: dict[str, str] = {}  # Idempotency-Key -> transfer id
        self.audit: list[dict] = []

    def seed_default_accounts(self) -> None:
        """Contas de desenvolvimento (specs/pix-transfer.md). Dados 100% ficticios."""
        with self.lock:
            self.accounts = {
                "acc-alice": Account("acc-alice", 1_000_000),
                "acc-bruno": Account("acc-bruno", 50_000),
                "acc-carla": Account("acc-carla", 0),
            }

    def log(self, evento: str, **dados: object) -> None:
        """Trilha de auditoria imutavel (RF: I-4). Chamar DENTRO da secao critica."""
        self.audit.append({"ts": time.time(), "evento": evento, **dados})

    def total_centavos(self) -> int:
        """Oraculo do invariante I-1: dinheiro nao e criado nem destruido."""
        with self.lock:
            return sum(
                a.saldo_disponivel_centavos + a.reservado_centavos for a in self.accounts.values()
            )
