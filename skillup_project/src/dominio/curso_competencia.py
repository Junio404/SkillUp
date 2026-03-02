from dataclasses import dataclass, field

from .validators import IdValidador, StrValidador, Validador
from .competencia import Nivel


@dataclass
class CursoCompetencia:
    id: int
    id_curso: int
    id_competencia: int
    nivel_conferido: str

    _valid_levels: dict = field(init=False, repr=False, default_factory=lambda: {nivel.name: nivel.value for nivel in Nivel})
    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    texto_validador: Validador = field(default_factory=StrValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.id_validador.validar(self.id_curso)
        self.id_validador.validar(self.id_competencia)
        self.texto_validador.validar(self.nivel_conferido)
        self.nivel_conferido = self.nivel_conferido.lower()
        if self.nivel_conferido.upper() not in self._valid_levels:
            raise ValueError("Nível inválido. Use: iniciante, intermediario ou avancado")

    # --------------------
    # Domínio
    # --------------------
    def atualizar_nivel(self, novo_nivel: str) -> None:
        self.texto_validador.validar(novo_nivel)
        novo_nivel = novo_nivel.lower()
        if novo_nivel.upper() not in self._valid_levels:
            raise ValueError("Nível inválido. Use: iniciante, intermediario ou avancado")
        self.nivel_conferido = novo_nivel

    def nivel_como_inteiro(self) -> int:
        return self._valid_levels[self.nivel_conferido.upper()]

    # --------------------
    # Serialização
    # --------------------
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "curso_id": self.id_curso,
            "competencia_id": self.id_competencia,
            "nivel": self.nivel_como_inteiro(),
        }

    @classmethod
    def from_dict(cls, d: dict):
        mapa_inverso = {0: "iniciante", 1: "intermediario", 2: "avancado"}
        return cls(
            id=d["id"],
            id_curso=d["curso_id"],
            id_competencia=d["competencia_id"],
            nivel_conferido=mapa_inverso[d["nivel"]],
        )

    def __str__(self) -> str:
        return (
            f"ID: {self.id}\n"
            f"Curso ID: {self.id_curso}\n"
            f"Competência ID: {self.id_competencia}\n"
            f"Nível Conferido: {self.nivel_conferido}\n"
            "-------------------------"
        )
