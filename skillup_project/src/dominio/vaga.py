from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple

from .validators import (
    IdValidador,
    StrValidador,
    ModalidadeValidador,
    TipoVagaValidador,
    RequisitosValidador,
    SalarioValidador,
    PrazoValidador,
    AtivoValidador,
    Validador,
)


# ==============================
# ENUMS
# ==============================

class Modalidade(Enum):
    PRESENCIAL = "Presencial"
    REMOTO = "Remoto"
    HIBRIDO = "Híbrido"


class TipoVaga(Enum):
    EMPREGO = "Emprego"
    ESTAGIO = "Estágio"
    TRAINEE = "Trainee"


# ==============================
# ENTIDADES DE DOMÍNIO
# ==============================

@dataclass
class Vaga(ABC):
    id: int
    titulo: str
    descricao: str
    area: str
    modalidade: Modalidade
    tipo: TipoVaga
    prazo_inscricao: str | None = None

    requisitos: List[str] = field(default_factory=list, repr=False)
    ativa: bool = True

    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    texto_validador: Validador = field(default_factory=StrValidador, repr=False)
    modalidade_validador: Validador = field(default_factory=ModalidadeValidador, repr=False)
    tipo_validador: Validador = field(default_factory=TipoVagaValidador, repr=False)
    requisitos_validador: Validador = field(default_factory=RequisitosValidador, repr=False)
    prazo_validador: Validador = field(default_factory=PrazoValidador, repr=False)
    ativo_validador: Validador = field(default_factory=AtivoValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.texto_validador.validar(self.titulo)
        self.texto_validador.validar(self.descricao)
        self.texto_validador.validar(self.area)
        self.modalidade_validador.validar(self.modalidade)
        self.tipo_validador.validar(self.tipo)
        self.requisitos_validador.validar(self.requisitos)
        self.prazo_validador.validar(self.prazo_inscricao)
        self.ativo_validador.validar(self.ativa)

    # ==============================
    # REGRAS DE NEGÓCIO
    # ==============================

    @abstractmethod
    def calcular_custo_contratacao(self):
        ...

    def adicionar_requisito(self, requisito: str) -> None:
        requisito = requisito.strip()
        if not requisito:
            raise ValueError("Requisito não pode ser vazio.")
        self.requisitos.append(requisito)

    def pausar(self) -> None:
        self.ativa = False

    def publicar(self) -> None:
        self.ativa = True

    def editar(self, titulo: str = None, descricao: str = None) -> None:
        if titulo:
            self.texto_validador.validar(titulo)
            self.titulo = titulo
        if descricao:
            self.texto_validador.validar(descricao)
            self.descricao = descricao

    # ==============================
    # MAPPER BASE
    # ==============================

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "area": self.area,
            "modalidade": self.modalidade.value,
            "tipo": self.tipo.value,
            "requisitos": list(self.requisitos),
            "ativa": self.ativa,
            "prazo_inscricao": self.prazo_inscricao,
        }


@dataclass
class VagaCLT(Vaga):
    salario_base: float = 0.0
    localidade: str = ""

    salario_validador: Validador = field(default_factory=SalarioValidador, repr=False)

    def __post_init__(self):
        super().__post_init__()
        if self.salario_base > 0:
            self.salario_validador.validar(self.salario_base)
        if not isinstance(self.localidade, str):
            raise TypeError("Localidade deve ser uma string.")
        self.localidade = self.localidade.strip()

    def calcular_custo_contratacao(self) -> float:
        return self.salario_base * 1.8

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["salario_base"] = self.salario_base
        data["localidade"] = self.localidade
        data["tipo_vaga"] = "CLT"
        return data


@dataclass
class VagaEstagio(Vaga):
    bolsa_auxilio: float = 0.0
    instituicao_conveniada: str = ""
    localidade: str = ""

    bolsa_validador: Validador = field(default_factory=SalarioValidador, repr=False)

    def __post_init__(self):
        super().__post_init__()
        if self.bolsa_auxilio > 0:
            self.bolsa_validador.validar(self.bolsa_auxilio)
        self.texto_validador.validar(self.instituicao_conveniada)
        if not isinstance(self.localidade, str):
            raise TypeError("Localidade deve ser uma string.")
        self.localidade = self.localidade.strip()

    def calcular_custo_contratacao(self) -> float:
        return self.bolsa_auxilio * 1.1

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["bolsa_auxilio"] = self.bolsa_auxilio
        data["instituicao_conveniada"] = self.instituicao_conveniada
        data["localidade"] = self.localidade
        data["tipo_vaga"] = "ESTAGIO"
        return data


# ==============================
# MAPPERS
# ==============================

class VagaCLTMapper:

    @staticmethod
    def to_dict(vaga: VagaCLT) -> dict:
        return vaga.to_dict()

    @staticmethod
    def from_dict(d: dict) -> VagaCLT:
        return VagaCLT(
            id=d["id"],
            titulo=d["titulo"],
            descricao=d["descricao"],
            area=d["area"],
            modalidade=Modalidade(d["modalidade"]),
            tipo=TipoVaga(d["tipo"]),
            prazo_inscricao=d.get("prazo_inscricao"),
            requisitos=d.get("requisitos", []),
            ativa=d.get("ativa", True),
            salario_base=d.get("salario_base", 0.0),
            localidade=d.get("localidade", "")
        )


class VagaEstagioMapper:

    @staticmethod
    def to_dict(vaga: VagaEstagio) -> dict:
        return vaga.to_dict()

    @staticmethod
    def from_dict(d: dict) -> VagaEstagio:
        return VagaEstagio(
            id=d["id"],
            titulo=d["titulo"],
            descricao=d["descricao"],
            area=d["area"],
            modalidade=Modalidade(d["modalidade"]),
            tipo=TipoVaga(d["tipo"]),
            prazo_inscricao=d.get("prazo_inscricao"),
            requisitos=d.get("requisitos", []),
            ativa=d.get("ativa", True),
            bolsa_auxilio=d.get("bolsa_auxilio", 0.0),
            instituicao_conveniada=d.get("instituicao_conveniada", ""),
            localidade=d.get("localidade", "")
        )
