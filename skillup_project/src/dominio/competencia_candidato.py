from dataclasses import dataclass, field
from typing import Dict

from .validators import IdValidador, StrValidador, NivelAtualizavelValidador, Validador


# ==============================
# ENTIDADE DE DOMÍNIO
# ==============================

@dataclass
class CompetenciaCandidato:
    id: int
    id_candidato: int
    id_competencia: int
    nivel_atual: str

    _valid_levels: Dict[str, int] = field(init=False, repr=False, default_factory=lambda: {
        "iniciante": 0,
        "intermediario": 1,
        "avancado": 2,
    })

    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    texto_validador: Validador = field(default_factory=StrValidador, repr=False)
    nivel_validador: Validador = field(default_factory=NivelAtualizavelValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.id_validador.validar(self.id_candidato)
        self.id_validador.validar(self.id_competencia)
        self.texto_validador.validar(self.nivel_atual)
        self.nivel_validador.validar(self.nivel_atual)
        self.nivel_atual = self.nivel_atual.lower()

    # ==============================
    # REGRAS DE NEGÓCIO
    # ==============================

    def atualizar_nivel(self, novo_nivel: str) -> None:
        self.texto_validador.validar(novo_nivel)
        self.nivel_validador.validar(novo_nivel)
        self.nivel_atual = novo_nivel.lower()

    def nivel_como_inteiro(self) -> int:
        return self._valid_levels[self.nivel_atual]


# ==============================
# MAPPER
# ==============================

class CompetenciaCandidatoMapper:

    @staticmethod
    def to_dict(competencia: CompetenciaCandidato) -> dict:
        return {
            "id": competencia.id,
            "candidato_id": competencia.id_candidato,
            "competencia_id": competencia.id_competencia,
            "nivel": competencia.nivel_como_inteiro(),
        }

    @staticmethod
    def from_dict(d: dict) -> CompetenciaCandidato:
        mapa_inverso = {0: "iniciante", 1: "intermediario", 2: "avancado"}
        return CompetenciaCandidato(
            id=d["id"],
            id_candidato=d["candidato_id"],
            id_competencia=d["competencia_id"],
            nivel_atual=mapa_inverso[d["nivel"]],
        )
