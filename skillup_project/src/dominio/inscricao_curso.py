from dataclasses import dataclass, field
from enum import Enum
from datetime import date
from typing import Optional

from .validators import IdValidador, Validador


class StatusInscricao(Enum):
    DEFERIDO = 0
    INDEFERIDO = 1


@dataclass
class InscricaoCurso:
    id: int
    id_curso: int
    id_aluno: int
    data_inscricao: date
    status: StatusInscricao = StatusInscricao.DEFERIDO

    id_validador: Validador = field(default_factory=IdValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.id_validador.validar(self.id_curso)
        self.id_validador.validar(self.id_aluno)
        if not isinstance(self.data_inscricao, date):
            raise TypeError("Data de inscrição inválida")
        if not isinstance(self.status, StatusInscricao):
            raise TypeError("Status deve ser do tipo StatusInscricao")

    # domínio
    def deferir(self) -> None:
        self.status = StatusInscricao.DEFERIDO

    def indeferir(self) -> None:
        self.status = StatusInscricao.INDEFERIDO

    # serialização
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "curso_id": self.id_curso,
            "aluno_id": self.id_aluno,
            "data_inscricao": self.data_inscricao.isoformat(),
            "status": self.status.value,
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            id=d["id"],
            id_curso=d["curso_id"],
            id_aluno=d["aluno_id"],
            data_inscricao=date.fromisoformat(d["data_inscricao"]),
            status=StatusInscricao(d["status"]),
        )

    def __str__(self) -> str:
        return (
            f"ID: {self.id}\n"
            f"Curso ID: {self.id_curso}\n"
            f"Aluno ID: {self.id_aluno}\n"
            f"Data Inscrição: {self.data_inscricao}\n"
            f"Status: {self.status.name}\n"
            "-------------------------"
        )
