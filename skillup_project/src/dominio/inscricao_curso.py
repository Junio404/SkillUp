from dataclasses import dataclass, field
from enum import Enum
from datetime import date
from typing import Protocol

from .validators import IdValidador, DataInscricaoValidador, StatusInscricaoValidador, Validador


# ==============================
# ENUMS
# ==============================

class StatusInscricao(Enum):
    DEFERIDO = "Deferido"
    INDEFERIDO = "Indeferido"
    CONCLUIDO = "Concluído"


class TipoCursoInscricao(Enum):
    """Identifica o subtipo de curso para desambiguar a referência."""
    EAD = "EAD"
    PRESENCIAL = "PRESENCIAL"


# ==============================
# ENTIDADE DE DOMÍNIO
# ==============================

@dataclass
class InscricaoCurso:
    id: int
    id_curso: int
    tipo_curso: TipoCursoInscricao  # Desambigua entre repositórios EAD e Presencial
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
        
        # Valida tipo_curso
        if isinstance(self.tipo_curso, str):
            try:
                self.tipo_curso = TipoCursoInscricao(self.tipo_curso)
            except ValueError:
                raise ValueError(f"Tipo de curso inválido: {self.tipo_curso}. Use EAD ou PRESENCIAL.")
        if not isinstance(self.tipo_curso, TipoCursoInscricao):
            raise TypeError("tipo_curso deve ser TipoCursoInscricao")
        
        self.data_validador.validar(self.data_inscricao)
        self.status_validador.validar(self.status)

    # ==============================
    # REGRAS DE NEGÓCIO
    # ==============================

    def deferir(self) -> None:
        self.status = StatusInscricao.DEFERIDO

    def indeferir(self) -> None:
        self.status = StatusInscricao.INDEFERIDO

    def concluir(self) -> None:
        """Marca a inscrição como concluída."""
        if self.status != StatusInscricao.DEFERIDO:
            raise ValueError("Somente inscrições deferidas podem ser concluídas.")
        self.status = StatusInscricao.CONCLUIDO


# ==============================
# MAPPER
# ==============================

class InscricaoCursoMapper:

    @staticmethod
    def to_dict(inscricao: InscricaoCurso) -> dict:
        return {
            "id": inscricao.id,
            "curso_id": inscricao.id_curso,
            "tipo_curso": inscricao.tipo_curso.value,
            "aluno_id": inscricao.id_aluno,
            "data_inscricao": inscricao.data_inscricao.isoformat(),
            "status": inscricao.status.value,
        }

    @staticmethod
    def from_dict(d: dict) -> InscricaoCurso:
        return InscricaoCurso(
            id=d["id"],
            id_curso=d["curso_id"],
            tipo_curso=TipoCursoInscricao(d["tipo_curso"]),
            id_aluno=d["aluno_id"],
            data_inscricao=date.fromisoformat(d["data_inscricao"]),
            status=StatusInscricao(d["status"]),
        )
