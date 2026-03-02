from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .validators import IdValidador, StrValidador, Validador


class Nivel(Enum):
    INICIANTE = 0
    INTERMEDIARIO = 1
    AVANCADO = 2


@dataclass
class Competencia:
    id: int
    nome: str
    descricao: Optional[str] = None

    # validações
    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    texto_validador: Validador = field(default_factory=StrValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.texto_validador.validar(self.nome)
        if self.descricao is not None and not isinstance(self.descricao, str):
            raise TypeError("Descrição deve ser texto.")

    def to_dict(self) -> dict:
        return {"id": self.id, "nome": self.nome, "descricao": self.descricao}

    @classmethod
    def from_dict(cls, d: dict):
        return cls(id=d["id"], nome=d["nome"], descricao=d.get("descricao"))

    def __str__(self) -> str:
        return f"{self.nome} ({self.descricao or 'Sem descrição'})"


@dataclass
class CompetenciaNivelada(Competencia):
    nivel: Nivel

    def __post_init__(self):
        super().__post_init__()
        if not isinstance(self.nivel, Nivel):
            raise TypeError("Nível deve ser do tipo Nivel enum.")

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["nivel"] = self.nivel.value
        return data


class CompetenciaCandidato(CompetenciaNivelada):
    """Competência possuída por um candidato."""
    pass


class CursoCompetencia(CompetenciaNivelada):
    """Competência exigida por um curso ou vaga."""
    pass