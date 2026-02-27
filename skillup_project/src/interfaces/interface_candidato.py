from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.candidato import Candidato

'''Interface para repositório de candidatos. Define os métodos que qualquer implementação deve seguir.'''
class ICandidatoRepositorio(ABC):

    @abstractmethod
    def salvar(self, candidato: Candidato):
        """Armazena o candidato"""
        pass

    @abstractmethod
    def listar(self) -> List[Candidato]:
        """Retorna todos os candidatos"""
        pass

    @abstractmethod
    def buscar_por_id(self, id_candidato: int) -> Optional[Candidato]:
        """Busca um candidato por ID"""
        pass

    @abstractmethod
    def buscar_por_cpf(self, cpf: str) -> Optional[Candidato]:
        """Busca um candidato pelo CPF"""
        pass

    @abstractmethod
    def buscar_por_email(self, email: str) -> Optional[Candidato]:
        """Busca um candidato pelo email"""
        pass

    @abstractmethod
    def buscar_por_filtros(self, **filtros) -> List[Candidato]:
        """Realiza a busca de candidatos com filtro dinâmico"""
        pass

    @abstractmethod
    def buscar_por_area_interesse(self, area: str) -> List[Candidato]:
        """Retorna candidatos com uma área de interesse específica"""
        pass

    @abstractmethod
    def buscar_por_nivel_formacao(self, nivel: str) -> List[Candidato]:
        """Retorna candidatos com um nível de formação específico"""
        pass

    @abstractmethod
    def atualizar(self, candidato: Candidato):
        """Atualiza dados de um candidato"""
        pass

    @abstractmethod
    def deletar(self, id_candidato: int):
        """Remove um candidato com o ID"""
        pass

    @abstractmethod
    def contar_total(self) -> int:
        """Retorna o total de candidatos cadastrados"""
        pass
