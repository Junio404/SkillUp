from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from .validators import IdValidador, StrValidador, CnpjValidador, Validador


@dataclass
class EntidadePublicadora(ABC):
    id: int
    nome: str
    _cnpj: str = field(repr=False)

    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    nome_validador: Validador = field(default_factory=StrValidador, repr=False)
    cnpj_validador: Validador = field(default_factory=CnpjValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.nome_validador.validar(self.nome)
        self.cnpj_validador.validar(self._cnpj)

    @property
    def cnpj(self) -> str:
        return self._cnpj

    @abstractmethod
    def validar_publicacao(self):
        ...

