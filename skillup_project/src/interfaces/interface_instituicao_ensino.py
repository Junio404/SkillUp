from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.instituicao_ensino import InstituicaoEnsino

'''Interface para repositório de Instituição de Ensino. Define os métodos que qualquer implementação deve seguir.'''
class IInstituicaoEnsino(ABC):

    @abstractmethod
    def salvar(self, instituicao: InstituicaoEnsino):
        """Armazena a instituição de ensino"""
        pass

    @abstractmethod
    def listar(self) -> List[InstituicaoEnsino]:
        """Retorna todas as instituições de ensino"""
        pass

    @abstractmethod
    def buscar_por_id(self, id_instituicao: int) -> Optional[InstituicaoEnsino]:
        """Faz a busca de uma instituição de ensino por ID"""
        pass

    @abstractmethod
    def buscar_por_cnpj(self, cnpj: str) -> Optional[InstituicaoEnsino]:
        """Busca uma instituição pelo CNPJ"""
        pass

    @abstractmethod
    def buscar_por_nome(self, nome: str) -> List[InstituicaoEnsino]:
        """Busca instituições pelo nome ou parte dele"""
        pass

    @abstractmethod
    def buscar_por_tipo(self, tipo: str) -> List[InstituicaoEnsino]:
        """Retorna instituições de um tipo específico"""
        pass

    @abstractmethod
    def buscar_credenciadas(self) -> List[InstituicaoEnsino]:
        """Retorna apenas as instituições credenciadas"""
        pass

    @abstractmethod
    def buscar_por_modalidade(self, modalidade: str) -> List[InstituicaoEnsino]:
        """Retorna instituições que oferecem uma modalidade específica"""
        pass

    @abstractmethod
    def buscar_por_filtros(self, **filtros) -> List[InstituicaoEnsino]:
        """Realiza a busca de instituições com filtro dinâmico"""
        pass

    @abstractmethod
    def atualizar(self, instituicao: InstituicaoEnsino):
        """Atualiza dados de uma instituição de ensino"""
        pass

    @abstractmethod
    def deletar(self, id_instituicao: int):
        """Remove uma instituição de ensino com o ID"""
        pass

    @abstractmethod
    def contar_total(self) -> int:
        """Retorna o total de instituições cadastradas"""
        pass

    @abstractmethod
    def contar_credenciadas(self) -> int:
        """Retorna o total de instituições credenciadas"""
        pass
