from dataclasses import dataclass, field
from typing import Dict

from .validators import IdValidador, StrValidador, Validador
from .competencia import Nivel


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

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.id_validador.validar(self.id_candidato)
        self.id_validador.validar(self.id_competencia)
        self.texto_validador.validar(self.nivel_atual)
        self.nivel_atual = self.nivel_atual.lower()
        if self.nivel_atual not in self._valid_levels:
            raise ValueError("Nível inválido. Use: iniciante, intermediario ou avancado")

    # --------------------
    # Métodos de domínio
    # --------------------
    def atualizar_nivel(self, novo_nivel: str) -> None:
        self.texto_validador.validar(novo_nivel)
        novo_nivel = novo_nivel.lower()
        if novo_nivel not in self._valid_levels:
            raise ValueError("Nível inválido. Use: iniciante, intermediario ou avancado")
        self.nivel_atual = novo_nivel

    def nivel_como_inteiro(self) -> int:
        return self._valid_levels[self.nivel_atual]

    # --------------------
    # Serialização (mapper)
    # --------------------
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "candidato_id": self.id_candidato,
            "competencia_id": self.id_competencia,
            "nivel": self.nivel_como_inteiro(),
        }

    @classmethod
    def from_dict(cls, d: dict):
        mapa_inverso = {0: "iniciante", 1: "intermediario", 2: "avancado"}
        return cls(
            id=d["id"],
            id_candidato=d["candidato_id"],
            id_competencia=d["competencia_id"],
            nivel_atual=mapa_inverso[d["nivel"]],
        )

    def __str__(self) -> str:
        return (
            f"ID: {self.id}\n"
            f"Candidato ID: {self.id_candidato}\n"
            f"Competência ID: {self.id_competencia}\n"
            f"Nível Atual: {self.nivel_atual}\n"
            "-------------------------"
        )
