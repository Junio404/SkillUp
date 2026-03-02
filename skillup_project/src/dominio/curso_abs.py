from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional

from .vaga import Modalidade
from .validators import IdValidador, StrValidador, Validador


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

    # validações por injeção de dependência
    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    texto_validador: Validador = field(default_factory=StrValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.texto_validador.validar(self.nome)
        self.texto_validador.validar(self.area)
        if self.carga_horaria <= 0:
            raise ValueError("Carga horária deve ser positiva.")
        if self.capacidade <= 0:
            raise ValueError("Capacidade deve ser positiva.")

    # --------------------
    # métodos de gestão
    # --------------------
    def publicar(self) -> None:
        self.ativo = True

    def pausar(self) -> None:
        self.ativo = False

    def editar(
        self,
        nome: str | None = None,
        area: str | None = None,
        carga_horaria: int | None = None,
        capacidade: int | None = None,
    ) -> None:
        if nome is not None:
            self.texto_validador.validar(nome)
            self.nome = nome
        if area is not None:
            self.texto_validador.validar(area)
            self.area = area
        if carga_horaria is not None:
            if carga_horaria <= 0:
                raise ValueError("Carga horária deve ser positiva.")
            self.carga_horaria = carga_horaria
        if capacidade is not None:
            if capacidade <= 0:
                raise ValueError("Capacidade deve ser positiva.")
            self.capacidade = capacidade

    def adicionar_competencia(self, competencia) -> None:
        self.competencias_ofertadas.append(competencia)

    # --------------------
    # métodos abstratos
    # --------------------
    @abstractmethod
    def exibir_detalhes(self) -> str:
        ...

    def to_dict(self) -> dict:
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

        if not isinstance(id_curso, int) or id_curso <= 0:
            raise ValueError("ID do curso deve ser um inteiro positivo.")
        if not nome or not area:
            raise ValueError("Nome e área do curso são obrigatórios.")
        if carga_horaria <= 0:
            raise ValueError("Carga horária deve ser positiva.")

        self._id = id_curso
        self.nome = nome
        self.area = area
        self.carga_horaria = carga_horaria
        self.modalidade = modalidade
        self.capacidade = capacidade
        self.prazo_inscricao = prazo_inscricao
        
        # Controle de estado
        self.ativo = True 
        
        # Relacionamento com Competências 
        self.competencias_ofertadas = []

    @property
    def id(self):
        return self._id

    # --------------------
    #  Métodos de Gestão
    # --------------------
    def publicar(self):
        """Torna o curso visível para inscrições."""
        self.ativo = True

    def pausar(self):
        """Suspende novas inscrições no curso."""
        self.ativo = False

    def editar(self, nome: str = None, area: str = None, carga_horaria: int = None, capacidade: int = None):
        """Edita os dados principais do curso."""
        if nome: self.nome = nome
        if area: self.area = area
        if carga_horaria: self.carga_horaria = carga_horaria
        if capacidade: self.capacidade = capacidade

    def adicionar_competencia(self, competencia):
        """Adiciona uma competência que o curso desenvolve."""
        self.competencias_ofertadas.append(competencia)

    # --------------------
    #  Métodos Abstratos
    # --------------------
    @abstractmethod
    def exibir_detalhes(self):
        """Retorna uma string formatada com os detalhes do curso."""
        pass
    
    @abstractmethod
    def to_dict(self):
        """Serializa o objeto para dicionário (base para subclasses)."""
        return {
            "id": self.id,
            "nome": self.nome,
            "area": self.area,
            "carga_horaria": self.carga_horaria,
            "modalidade": self.modalidade.value if hasattr(self.modalidade, 'value') else self.modalidade,
            "capacidade": self.capacidade,
            "prazo_inscricao": self.prazo_inscricao.isoformat() if self.prazo_inscricao else None,
            "ativo": self.ativo,
            # Assumindo que as competencias tenham to_dict ou __str__
            "competencias": [c.to_dict() if hasattr(c, 'to_dict') else str(c) for c in self.competencias_ofertadas]
        }