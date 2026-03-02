from dataclasses import dataclass, field
from typing import Protocol

from .validators import (
    IdValidador,
    StrValidador,
    CnpjValidador,
    PorteValidador,
    Validador,
)


@dataclass
class Empresa:
    id: int
    nome: str
    _cnpj: str = field(repr=False)
    porte: str

    # validação
    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    nome_validador: Validador = field(default_factory=StrValidador, repr=False)
    cnpj_validador: Validador = field(default_factory=CnpjValidador, repr=False)
    porte_validador: Validador = field(default_factory=PorteValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.nome_validador.validar(self.nome)
        self.cnpj_validador.validar(self._cnpj)
        self.porte_validador.validar(self.porte)

    @property
    def cnpj(self) -> str:
        return self._cnpj

    # --------------------
    # Métodos de domínio
    # --------------------
    def validar_publicacao(self, oportunidade) -> bool:
        return True

    def obter_limites_publicacao(self) -> int:
        limites = {"pequeno": 5, "medio": 15, "grande": 50}
        return limites.get(self.porte, 0)

    # --------------------
    # Serialização (mapper)
    # --------------------
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj,
            "porte": self.porte,
        }

    @classmethod
    def from_dict(cls, dados: dict):
        return cls(
            id=dados["id"],
            nome=dados["nome"],
            _cnpj=dados["cnpj"],
            porte=dados["porte"],
        )

    def __str__(self) -> str:
        return (
            f"ID: {self.id}\n"
            f"Nome: {self.nome}\n"
            f"CNPJ: {self.cnpj}\n"
            f"Porte: {self.porte}\n"
            "-------------------------"
        )
