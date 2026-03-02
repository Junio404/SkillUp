from dataclasses import dataclass, field
from typing import List

from .entidade_publicadora import EntidadePublicadora
from .validators import (
    IdValidador,
    StrValidador,
    CnpjValidador,
    Validador,
)


@dataclass
class InstituicaoEnsino(EntidadePublicadora):
    id: int
    razao_social: str
    nome_fantasia: str
    _cnpj: str = field(repr=False)
    registro_educacional: str
    tipo: str
    modalidades: List[str] = field(default_factory=list)
    credenciada: bool = True

    # validações
    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    texto_validador: Validador = field(default_factory=StrValidador, repr=False)
    cnpj_validador: Validador = field(default_factory=CnpjValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.texto_validador.validar(self.razao_social)
        self.texto_validador.validar(self.nome_fantasia)
        self.cnpj_validador.validar(self._cnpj)
        self.texto_validador.validar(self.registro_educacional)
        if not isinstance(self.credenciada, bool):
            raise ValueError("Credenciada deve ser booleano")

    @property
    def cnpj(self) -> str:
        return self._cnpj

    # ===== contrato abstrato =====
    def validar_publicacao(self) -> bool:
        if not self.credenciada:
            raise PermissionError("Instituição não credenciada não pode publicar cursos")
        return True

    # ===== serialização =====
    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "razao_social": self.razao_social,
            "nome_fantasia": self.nome_fantasia,
            "cnpj": self.cnpj,
            "registro_educacional": self.registro_educacional,
            "tipo": self.tipo,
            "modalidades": self.modalidades,
            "credenciada": self.credenciada,
        }

    @classmethod
    def from_dict(cls, d: dict):
        return cls(
            id=d["id"],
            razao_social=d.get("razao_social", d.get("nome")),
            nome_fantasia=d.get("nome_fantasia", d.get("nome")),
            _cnpj=d["cnpj"],
            registro_educacional=d["registro_educacional"],
            tipo=d["tipo"],
            modalidades=d.get("modalidades", []),
            credenciada=d.get("credenciada", True),
        )


@dataclass
class AreaEnsino:
    id_area: int
    nome_area: str

    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    texto_validador: Validador = field(default_factory=StrValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id_area)
        self.texto_validador.validar(self.nome_area)


@dataclass
class InstituicaoAreaEnsino:
    id_instituicao_area: int
    id_instituicao: int
    id_area: int

    id_validador: Validador = field(default_factory=IdValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id_instituicao_area)
        self.id_validador.validar(self.id_instituicao)
        self.id_validador.validar(self.id_area)
