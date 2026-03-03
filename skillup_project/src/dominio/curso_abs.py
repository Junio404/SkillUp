from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional

from .vaga import Modalidade
from .validators import IdValidador, StrValidador, CargaHorariaValidador, CapacidadeValidador, ModalidadeCursoValidador, PrazoValidador, AtivoValidador, Validador


# ==============================
# ENTIDADE DE DOMÍNIO ABSTRATA
# ==============================

@dataclass
class Curso(ABC):
    id: int
    nome: str
    area: str
    carga_horaria: int
    modalidade: Modalidade
    capacidade: int
    prazo_inscricao: Optional[date] = None
    ativo: bool = True
    competencias_ofertadas: List = field(default_factory=list, repr=False)

    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    texto_validador: Validador = field(default_factory=StrValidador, repr=False)
    carga_validador: Validador = field(default_factory=CargaHorariaValidador, repr=False)
    capacidade_validador: Validador = field(default_factory=CapacidadeValidador, repr=False)
    modalidade_validador: Validador = field(default_factory=ModalidadeCursoValidador, repr=False)
    prazo_validador: Validador = field(default_factory=PrazoValidador, repr=False)
    ativo_validador: Validador = field(default_factory=AtivoValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.texto_validador.validar(self.nome)
        self.texto_validador.validar(self.area)
        self.carga_validador.validar(self.carga_horaria)
        self.capacidade_validador.validar(self.capacidade)
        self.modalidade_validador.validar(self.modalidade)
        self.prazo_validador.validar(self.prazo_inscricao)
        self.ativo_validador.validar(self.ativo)

    # ==============================
    # REGRAS DE NEGÓCIO
    # ==============================

    def publicar(self) -> None:
        """Torna o curso visível para inscrições."""
        self.ativo = True

    def pausar(self) -> None:
        """Suspende novas inscrições no curso."""
        self.ativo = False

    def editar(
        self,
        nome: str | None = None,
        area: str | None = None,
        carga_horaria: int | None = None,
        capacidade: int | None = None,
    ) -> None:
        """Edita os dados principais do curso com validação."""
        if nome is not None:
            self.texto_validador.validar(nome)
            self.nome = nome
        if area is not None:
            self.texto_validador.validar(area)
            self.area = area
        if carga_horaria is not None:
            self.carga_validador.validar(carga_horaria)
            self.carga_horaria = carga_horaria
        if capacidade is not None:
            self.capacidade_validador.validar(capacidade)
            self.capacidade = capacidade

    def adicionar_competencia(self, competencia) -> None:
        """Adiciona uma competência que o curso desenvolve."""
        self.competencias_ofertadas.append(competencia)

    # ==============================
    # MÉTODOS ABSTRATOS
    # ==============================

    @abstractmethod
    def exibir_detalhes(self) -> str:
        """Retorna uma string formatada com os detalhes do curso."""
        ...

    def to_dict(self) -> dict:
        """Serializa o objeto para dicionário (base para subclasses)."""
        return {
            "id": self.id,
            "nome": self.nome,
            "area": self.area,
            "carga_horaria": self.carga_horaria,
            "modalidade": self.modalidade.value,
            "capacidade": self.capacidade,
            "prazo_inscricao": self.prazo_inscricao.isoformat() if self.prazo_inscricao else None,
            "ativo": self.ativo,
            "competencias": [
                c.to_dict() if hasattr(c, "to_dict") else str(c)
                for c in self.competencias_ofertadas
            ],
        }