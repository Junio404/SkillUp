from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Protocol

from .validators import IdValidador, StrValidador, NivelValidador, Validador


# ==============================
# ENUMS
# ==============================

class Nivel(Enum):
    INICIANTE = 0
    INTERMEDIARIO = 1
    AVANCADO = 2


# ==============================
# ENTIDADES DE DOMÍNIO
# ==============================

@dataclass
class Competencia:
    id: int
    nome: str
    descricao: Optional[str] = None

    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    texto_validador: Validador = field(default_factory=StrValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.texto_validador.validar(self.nome)
        if self.descricao is not None and not isinstance(self.descricao, str):
            raise TypeError("Descrição deve ser texto.")


@dataclass
class CompetenciaNivelada(Competencia):
    nivel: Nivel = Nivel.INICIANTE

    nivel_validador: Validador = field(default_factory=NivelValidador, repr=False)

    def __post_init__(self):
        super().__post_init__()
        self.nivel_validador.validar(self.nivel)
        if not isinstance(self.nivel, Nivel):
            try:
                self.nivel = Nivel[self.nivel.upper()]
            except (KeyError, AttributeError):
                raise TypeError("Nível deve ser do tipo Nivel enum.")


# NOTA: CompetenciaCandidato e CursoCompetencia foram movidas para arquivos dedicados
# (competencia_candidato.py e curso_competencia.py) pois são entidades de ligação
# com chaves estrangeiras próprias, não simples subclasses de CompetenciaNivelada.


# ==============================
# MAPPERS
# ==============================

class CompetenciaMapper:

    @staticmethod
    def to_dict(competencia: Competencia) -> dict:
        return {
            "id": competencia.id,
            "nome": competencia.nome,
            "descricao": competencia.descricao
        }

    @staticmethod
    def from_dict(d: dict) -> Competencia:
        return Competencia(
            id=d["id"],
            nome=d["nome"],
            descricao=d.get("descricao")
        )


class CompetenciaNiveladaMapper:

    @staticmethod
    def to_dict(competencia: CompetenciaNivelada) -> dict:
        data = CompetenciaMapper.to_dict(competencia)
        data["nivel"] = competencia.nivel.value
        return data

    @staticmethod
    def from_dict(d: dict) -> CompetenciaNivelada:
        return CompetenciaNivelada(
            id=d["id"],
            nome=d["nome"],
            descricao=d.get("descricao"),
            nivel=Nivel(d["nivel"]) if isinstance(d["nivel"], int) else Nivel[d["nivel"].upper()]
        )