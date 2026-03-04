from dataclasses import dataclass, field
from typing import List

from .entidade_publicadora import EntidadePublicadora
from .validators import (
    IdValidador,
    StrValidador,
    CnpjValidador,
    CredenciadoValidador,
    ModalidadesValidador,
    Validador,
)


# ==============================
# ENTIDADES DE DOMÍNIO
# ==============================

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

    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    texto_validador: Validador = field(default_factory=StrValidador, repr=False)
    cnpj_validador: Validador = field(default_factory=CnpjValidador, repr=False)
    credenciado_validador: Validador = field(default_factory=CredenciadoValidador, repr=False)
    modalidades_validador: Validador = field(default_factory=ModalidadesValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.texto_validador.validar(self.razao_social)
        self.texto_validador.validar(self.nome_fantasia)
        self.cnpj_validador.validar(self._cnpj)
        self.texto_validador.validar(self.registro_educacional)
        self.texto_validador.validar(self.tipo)
        self.credenciado_validador.validar(self.credenciada)
        self.modalidades_validador.validar(self.modalidades)

    @property
    def cnpj(self) -> str:
        return self._cnpj

    # ==============================
    # REGRAS DE NEGÓCIO
    # ==============================

    def validar_publicacao(self) -> bool:
        """Valida se a instituição pode publicar cursos."""
        if not self.credenciada:
            raise PermissionError("Instituição não credenciada não pode publicar cursos")
        return True


# ==============================
# MAPPERS
# ==============================

class InstituicaoEnsinoMapper:

    @staticmethod
    def to_dict(instituicao: InstituicaoEnsino) -> dict:
        return {
            "id": instituicao.id,
            "razao_social": instituicao.razao_social,
            "nome_fantasia": instituicao.nome_fantasia,
            "cnpj": instituicao.cnpj,
            "registro_educacional": instituicao.registro_educacional,
            "tipo": instituicao.tipo,
            "modalidades": instituicao.modalidades,
            "credenciada": instituicao.credenciada,
        }

    @staticmethod
    def from_dict(d: dict) -> InstituicaoEnsino:
        return InstituicaoEnsino(
            id=d["id"],
            razao_social=d.get("razao_social", d.get("nome")),
            nome_fantasia=d.get("nome_fantasia", d.get("nome")),
            _cnpj=d["cnpj"],
            registro_educacional=d["registro_educacional"],
            tipo=d["tipo"],
            modalidades=d.get("modalidades", []),
            credenciada=d.get("credenciada", True),
        )


# ==============================
# ENTIDADES COMPLEMENTARES
# ==============================

@dataclass
class AreaEnsino:
    id_area: int
    nome_area: str

    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    texto_validador: Validador = field(default_factory=StrValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id_area)
        self.texto_validador.validar(self.nome_area)


class AreaEnsinoMapper:

    @staticmethod
    def to_dict(area: AreaEnsino) -> dict:
        return {
            "id_area": area.id_area,
            "nome_area": area.nome_area,
        }

    @staticmethod
    def from_dict(d: dict) -> AreaEnsino:
        return AreaEnsino(
            id_area=d["id_area"],
            nome_area=d["nome_area"],
        )


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


class InstituicaoAreaEnsinoMapper:

    @staticmethod
    def to_dict(inst_area: InstituicaoAreaEnsino) -> dict:
        return {
            "id_instituicao_area": inst_area.id_instituicao_area,
            "id_instituicao": inst_area.id_instituicao,
            "id_area": inst_area.id_area,
        }

    @staticmethod
    def from_dict(d: dict) -> InstituicaoAreaEnsino:
        return InstituicaoAreaEnsino(
            id_instituicao_area=d["id_instituicao_area"],
            id_instituicao=d["id_instituicao"],
            id_area=d["id_area"],
        )
