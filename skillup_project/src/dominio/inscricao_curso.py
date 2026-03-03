from dataclasses import dataclass, field
from enum import Enum
from datetime import date
from typing import Protocol

from .validators import IdValidador, DataInscricaoValidador, StatusInscricaoValidador, Validador


# ==============================
# ENUMS
# ==============================

class StatusInscricao(Enum):
    DEFERIDO = 0
    INDEFERIDO = 1


# ==============================
# ENTIDADE DE DOMÍNIO
# ==============================

@dataclass
class InscricaoCurso:
    id: int
    id_curso: int
    id_aluno: int
    data_inscricao: date
    status: StatusInscricao = StatusInscricao.DEFERIDO

    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    data_validador: Validador = field(default_factory=DataInscricaoValidador, repr=False)
    status_validador: Validador = field(default_factory=StatusInscricaoValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.id_validador.validar(self.id_curso)
        self.id_validador.validar(self.id_aluno)
        self.data_validador.validar(self.data_inscricao)
        self.status_validador.validar(self.status)

    # ==============================
    # REGRAS DE NEGÓCIO
    # ==============================

    def deferir(self) -> None:
        self.status = StatusInscricao.DEFERIDO

    def indeferir(self) -> None:
        self.status = StatusInscricao.INDEFERIDO


# ==============================
# MAPPER
# ==============================

class InscricaoCursoMapper:

    @staticmethod
    def to_dict(inscricao: InscricaoCurso) -> dict:
        return {
            "id": inscricao.id,
            "curso_id": inscricao.id_curso,
            "aluno_id": inscricao.id_aluno,
            "data_inscricao": inscricao.data_inscricao.isoformat(),
            "status": inscricao.status.value,
        }

    @staticmethod
    def from_dict(d: dict) -> InscricaoCurso:
        return InscricaoCurso(
            id=d["id"],
            id_curso=d["curso_id"],
            id_aluno=d["aluno_id"],
            data_inscricao=date.fromisoformat(d["data_inscricao"]),
            status=StatusInscricao(d["status"]),
        )
