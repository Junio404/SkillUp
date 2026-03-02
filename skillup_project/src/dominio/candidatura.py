from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Optional

from .validators import IdValidador, Validador


class StatusCandidatura(Enum):
    ENVIADO = "Enviado"
    EM_ANALISE = "Em analise"
    ACEITO = "Aceito"
    RECUSADO = "Recusado"
    CANCELADO = "Cancelado"


@dataclass
class Candidatura:
    id: int
    id_vaga: int
    id_candidato: int
    status: StatusCandidatura = StatusCandidatura.ENVIADO
    data_candidatura: str | None = None

    id_validador: Validador = field(default_factory=IdValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.id_validador.validar(self.id_vaga)
        self.id_validador.validar(self.id_candidato)
        if not self.data_candidatura:
            self.data_candidatura = datetime.now().date().isoformat()
        if isinstance(self.status, str):
            try:
                self.status = StatusCandidatura(self.status)
            except ValueError:
                self.status = StatusCandidatura.ENVIADO

    # --------------------
    # Métodos de domínio
    # --------------------
    def aprovar(self) -> None:
        self.status = StatusCandidatura.ACEITO

    def reprovar(self) -> None:
        self.status = StatusCandidatura.RECUSADO

    def cancelar(self) -> None:
        if self.status in (StatusCandidatura.ACEITO, StatusCandidatura.RECUSADO):
            raise ValueError("Não é possível cancelar uma candidatura já finalizada.")
        self.status = StatusCandidatura.CANCELADO

    def analisar(self) -> None:
        self.status = StatusCandidatura.EM_ANALISE

    # --------------------
    # Serialização (mapper)
    # --------------------
    def to_dict(self) -> dict:
        return {
            "id_candidatura": self.id,
            "id_vaga": self.id_vaga,
            "id_candidato": self.id_candidato,
            "status": self.status.value,
            "data_candidatura": self.data_candidatura,
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            id=d["id_candidatura"],
            id_vaga=d["id_vaga"],
            id_candidato=d["id_candidato"],
            status=StatusCandidatura(d.get("status", StatusCandidatura.ENVIADO.value)),
            data_candidatura=d.get("data_candidatura"),
        )

    def __str__(self) -> str:
        return (
            f"Candidatura #{self.id}\n"
            f"Vaga ID: {self.id_vaga}\n"
            f"Candidato ID: {self.id_candidato}\n"
            f"Data: {self.data_candidatura}\n"
            f"Status: {self.status.value}\n"
            "-------------------------"
        )
