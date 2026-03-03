from dataclasses import dataclass, field
from typing import Protocol

from .validators import (
    IdValidador,
    StrValidador,
    CnpjValidador,
    PorteValidador,
    Validador,
)


# ==============================
# VALIDATORS
# ==============================

# (Utilizando os validators já definidos em validators.py)


# ==============================
# ENTIDADE DE DOMÍNIO
# ==============================

@dataclass
class Empresa:
    id: int
    nome: str
    _cnpj: str = field(repr=False)
    porte: str

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

    # ==============================
    # REGRAS DE NEGÓCIO
    # ==============================

    def validar_publicacao(self, oportunidade) -> bool:
        return True

    def obter_limites_publicacao(self) -> int:
        limites = {"pequeno": 5, "medio": 15, "grande": 50}
        return limites.get(self.porte, 0)


# ==============================
# MAPPER
# ==============================

class EmpresaMapper:

    @staticmethod
    def to_dict(empresa: Empresa) -> dict:
        return {
            "id": empresa.id,
            "nome": empresa.nome,
            "cnpj": empresa.cnpj,
            "porte": empresa.porte,
        }

    @staticmethod
    def from_dict(dados: dict) -> Empresa:
        return Empresa(
            id=dados["id"],
            nome=dados["nome"],
            _cnpj=dados["cnpj"],
            porte=dados["porte"],
        )
