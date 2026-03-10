from dataclasses import dataclass, field
from enum import Enum

from .validators import IdValidador, StrValidador, CursoNivelValidador, Validador
from .competencia import Nivel


# ==============================
# ENUMS
# ==============================

class TipoCursoCompetencia(Enum):
    """Identifica o subtipo de curso para desambiguar a referência."""
    EAD = "EAD"
    PRESENCIAL = "PRESENCIAL"


# ==============================
# ENTIDADE DE DOMÍNIO
# ==============================

@dataclass
class CursoCompetencia:
    id: int
    id_curso: int
    tipo_curso: TipoCursoCompetencia  # Desambigua entre repositórios EAD e Presencial
    id_competencia: int
    nivel_conferido: str

    _valid_levels: dict = field(init=False, repr=False, default_factory=lambda: {nivel.name: nivel.value for nivel in Nivel})
    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    texto_validador: Validador = field(default_factory=StrValidador, repr=False)
    nivel_validador: Validador = field(default_factory=CursoNivelValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.id_validador.validar(self.id_curso)
        self.id_validador.validar(self.id_competencia)
        
        # Valida tipo_curso
        if isinstance(self.tipo_curso, str):
            try:
                self.tipo_curso = TipoCursoCompetencia(self.tipo_curso)
            except ValueError:
                raise ValueError(f"Tipo de curso inválido: {self.tipo_curso}. Use EAD ou PRESENCIAL.")
        if not isinstance(self.tipo_curso, TipoCursoCompetencia):
            raise TypeError("tipo_curso deve ser TipoCursoCompetencia")
        
        self.texto_validador.validar(self.nivel_conferido)
        self.nivel_validador.validar(self.nivel_conferido)
        self.nivel_conferido = self.nivel_conferido.lower()

    # ==============================
    # REGRAS DE NEGÓCIO
    # ==============================

    def atualizar_nivel(self, novo_nivel: str) -> None:
        self.texto_validador.validar(novo_nivel)
        self.nivel_validador.validar(novo_nivel)
        self.nivel_conferido = novo_nivel.lower()

    def nivel_como_inteiro(self) -> int:
        return self._valid_levels[self.nivel_conferido.upper()]


# ==============================
# MAPPER
# ==============================

class CursoCompetenciaMapper:

    @staticmethod
    def to_dict(curso_competencia: CursoCompetencia) -> dict:
        return {
            "id": curso_competencia.id,
            "curso_id": curso_competencia.id_curso,
            "tipo_curso": curso_competencia.tipo_curso.value,
            "competencia_id": curso_competencia.id_competencia,
            "nivel": curso_competencia.nivel_como_inteiro(),
        }

    @staticmethod
    def from_dict(d: dict) -> CursoCompetencia:
        mapa_inverso = {0: "iniciante", 1: "intermediario", 2: "avancado"}
        return CursoCompetencia(
            id=d["id"],
            id_curso=d["curso_id"],
            tipo_curso=TipoCursoCompetencia(d["tipo_curso"]),
            id_competencia=d["competencia_id"],
            nivel_conferido=mapa_inverso[d["nivel"]],
        )
