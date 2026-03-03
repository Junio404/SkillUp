from dataclasses import dataclass, field
from typing import Tuple

from .validators import IdValidador, StrValidador, NivelMinimoValidador, BooleanValidador, Validador
from .competencia import Nivel


# ==============================
# ENTIDADE DE DOMÍNIO
# ==============================

@dataclass
class RequisitoVaga:
    id: int
    id_vaga: int
    id_competencia: int
    nivel_minimo: str
    obrigatorio: bool = True

    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    texto_validador: Validador = field(default_factory=StrValidador, repr=False)
    nivel_validador: Validador = field(default_factory=NivelMinimoValidador, repr=False)
    bool_validador: Validador = field(default_factory=BooleanValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.id_validador.validar(self.id_vaga)
        self.id_validador.validar(self.id_competencia)
        self.texto_validador.validar(self.nivel_minimo)
        self.nivel_validador.validar(self.nivel_minimo)
        self.bool_validador.validar(self.obrigatorio)

    # ==============================
    # REGRAS DE NEGÓCIO
    # ==============================

    def atualizar_nivel(self, novo_nivel: str) -> None:
        self.texto_validador.validar(novo_nivel)
        self.nivel_validador.validar(novo_nivel)
        self.nivel_minimo = novo_nivel

    def tornar_opcional(self) -> None:
        self.obrigatorio = False

    def tornar_obrigatorio(self) -> None:
        self.obrigatorio = True

    def nivel_como_inteiro(self) -> int:
        return Nivel[self.nivel_minimo.upper()].value


# ==============================
# MAPPER
# ==============================

class RequisitoVagaMapper:

    @staticmethod
    def to_dict(requisito: RequisitoVaga) -> dict:
        return {
            "id": requisito.id,
            "vaga_id": requisito.id_vaga,
            "competencia_id": requisito.id_competencia,
            "nivel": requisito.nivel_como_inteiro(),
            "obrigatorio": requisito.obrigatorio,
        }

    @staticmethod
    def from_dict(d: dict) -> RequisitoVaga:
        mapa_inverso = {0: "INICIANTE", 1: "INTERMEDIARIO", 2: "AVANCADO"}
        return RequisitoVaga(
            id=d["id"],
            id_vaga=d["vaga_id"],
            id_competencia=d["competencia_id"],
            nivel_minimo=mapa_inverso[d["nivel"]],
            obrigatorio=d.get("obrigatorio", True),
        )
