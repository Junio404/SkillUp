from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import List, Tuple

from .validators import (
    IdValidador,
    StrValidador,
    Validador,
)


class Modalidade(Enum):
    PRESENCIAL = "Presencial"
    REMOTO = "Remoto"
    HIBRIDO = "Híbrido"


class TipoVaga(Enum):
    EMPREGO = "Emprego"
    ESTAGIO = "Estágio"
    TRAINEE = "Trainee"


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

    # dependências de validação
    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    texto_validador: Validador = field(default_factory=StrValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.texto_validador.validar(self.titulo)
        self.texto_validador.validar(self.descricao)
        self.texto_validador.validar(self.area)

    # --------------------
    # Métodos de domínio
    # --------------------
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

    # --------------------
    # Serialização (mapper)
    # --------------------
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

    @classmethod
    def from_dict(cls, d: dict):
        # subclass should call this via super() or override
        return cls(
            id=d["id"],
            titulo=d["titulo"],
            descricao=d["descricao"],
            area=d["area"],
            modalidade=Modalidade(d["modalidade"]),
            tipo=TipoVaga(d["tipo"]),
            prazo_inscricao=d.get("prazo_inscricao"),
        )


@dataclass
class VagaCLT(Vaga):
    salario_base: float

    def __post_init__(self):
        super().__post_init__()
        if self.salario_base <= 0:
            raise ValueError("Salário base deve ser positivo")

    def calcular_custo_contratacao(self) -> float:
        return self.salario_base * 1.8

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["salario_base"] = self.salario_base
        return data

    @classmethod
    def from_dict(cls, d: dict):
        vaga = super().from_dict(d)
        vaga.salario_base = d["salario_base"]
        return vaga


@dataclass
class VagaEstagio(Vaga):
    bolsa_auxilio: float
    instituicao_conveniada: str

    def __post_init__(self):
        super().__post_init__()
        if self.bolsa_auxilio <= 0:
            raise ValueError("Bolsa auxílio deve ser positiva")
        self.texto_validador.validar(self.instituicao_conveniada)

    def calcular_custo_contratacao(self) -> float:
        return self.bolsa_auxilio * 1.1

    def to_dict(self) -> dict:
        data = super().to_dict()
        data["bolsa_auxilio"] = self.bolsa_auxilio
        data["instituicao_conveniada"] = self.instituicao_conveniada
        return data

    @classmethod
    def from_dict(cls, d: dict):
        vaga = super().from_dict(d)
        vaga.bolsa_auxilio = d["bolsa_auxilio"]
        vaga.instituicao_conveniada = d["instituicao_conveniada"]
        return vaga
