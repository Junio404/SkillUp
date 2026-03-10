from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Protocol

from .validators import IdValidador, StatusCandidaturaValidador, DataValidador, StrValidador, Validador


# ==============================
# ENUMS
# ==============================

class StatusCandidatura(Enum):
    ENVIADO = "Enviado"
    EM_ANALISE = "Em analise"
    ACEITO = "Aceito"
    RECUSADO = "Recusado"
    CANCELADO = "Cancelado"


class TipoVagaCandidatura(Enum):
    """Identifica o subtipo de vaga para desambiguar a referência."""
    CLT = "CLT"
    ESTAGIO = "ESTAGIO"


# ==============================
# ENTIDADE DE DOMÍNIO
# ==============================

@dataclass
class Candidatura:
    id: int
    id_vaga: int
    tipo_vaga: TipoVagaCandidatura  # Desambigua entre repositórios CLT e Estágio
    id_candidato: int
    status: StatusCandidatura = StatusCandidatura.ENVIADO
    data_candidatura: str | None = None

    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    status_validador: Validador = field(default_factory=StatusCandidaturaValidador, repr=False)
    data_validador: Validador = field(default_factory=DataValidador, repr=False)
    texto_validador: Validador = field(default_factory=StrValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.id_validador.validar(self.id_vaga)
        self.id_validador.validar(self.id_candidato)
        
        # Valida tipo_vaga
        if isinstance(self.tipo_vaga, str):
            try:
                self.tipo_vaga = TipoVagaCandidatura(self.tipo_vaga)
            except ValueError:
                raise ValueError(f"Tipo de vaga inválido: {self.tipo_vaga}. Use CLT ou ESTAGIO.")
        if not isinstance(self.tipo_vaga, TipoVagaCandidatura):
            raise TypeError("tipo_vaga deve ser TipoVagaCandidatura")
        
        if not self.data_candidatura:
            self.data_candidatura = datetime.now().date().isoformat()
        self.data_validador.validar(self.data_candidatura)
        
        if isinstance(self.status, str):
            try:
                self.status = StatusCandidatura(self.status)
            except ValueError:
                self.status = StatusCandidatura.ENVIADO
        
        self.status_validador.validar(self.status.value)

    # ==============================
    # REGRAS DE NEGÓCIO
    # ==============================

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


# ==============================
# MAPPER
# ==============================

class CandidaturaMapper:

    @staticmethod
    def to_dict(candidatura: Candidatura) -> dict:
        return {
            "id_candidatura": candidatura.id,
            "id_vaga": candidatura.id_vaga,
            "tipo_vaga": candidatura.tipo_vaga.value,
            "id_candidato": candidatura.id_candidato,
            "status": candidatura.status.value,
            "data_candidatura": candidatura.data_candidatura,
        }

    @staticmethod
    def from_dict(d: dict) -> Candidatura:
        return Candidatura(
            id=d["id_candidatura"],
            id_vaga=d["id_vaga"],
            tipo_vaga=TipoVagaCandidatura(d["tipo_vaga"]),
            id_candidato=d["id_candidato"],
            status=StatusCandidatura(d.get("status", StatusCandidatura.ENVIADO.value)),
            data_candidatura=d.get("data_candidatura"),
        )
