from dataclasses import dataclass, field
from typing import Tuple

from .validators import IdValidador, StrValidador, Validador
from .competencia import Nivel


@dataclass
class RequisitoVaga:
    id: int
    id_vaga: int
    id_competencia: int
    nivel_minimo: str
    obrigatorio: bool = True

    # dependências
    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    texto_validador: Validador = field(default_factory=StrValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.id_validador.validar(self.id_vaga)
        self.id_validador.validar(self.id_competencia)
        self.texto_validador.validar(self.nivel_minimo)
        if not isinstance(self.obrigatorio, bool):
            raise TypeError("Obrigatório deve ser booleano")

    # --------------------
    # Métodos de domínio
    # --------------------
    def atualizar_nivel(self, novo_nivel: str) -> None:
        self.texto_validador.validar(novo_nivel)
        if novo_nivel not in [nivel.name for nivel in Nivel]:
            raise ValueError("Nível inválido.")
        self.nivel_minimo = novo_nivel

    def tornar_opcional(self) -> None:
        self.obrigatorio = False

    def tornar_obrigatorio(self) -> None:
        self.obrigatorio = True

    def nivel_como_inteiro(self) -> int:
        return Nivel[self.nivel_minimo].value

    # --------------------
    # Serialização (mapper)
    # --------------------
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "vaga_id": self.id_vaga,
            "competencia_id": self.id_competencia,
            "nivel": self.nivel_como_inteiro(),
            "obrigatorio": self.obrigatorio,
        }

    @classmethod
    def from_dict(cls, d: dict):
        mapa_inverso = {0: "iniciante", 1: "intermediario", 2: "avancado"}
        return cls(
            id=d["id"],
            id_vaga=d["vaga_id"],
            id_competencia=d["competencia_id"],
            nivel_minimo=mapa_inverso[d["nivel"]],
            obrigatorio=d.get("obrigatorio", True),
        )
