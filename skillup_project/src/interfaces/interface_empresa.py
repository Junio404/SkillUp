from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.empresa import Empresa

'''Interface para repositório de Empresa. Define os métodos que qualquer implementação deve seguir.'''
class IEmpresa(ABC):

    @abstractmethod
    def salvar(self, empresa: Empresa):
        """Armazena a empresa"""
        pass

    @abstractmethod
    def listar(self) -> List[Empresa]:
        """Retorna todas as empresas"""
        pass

    @abstractmethod
    def buscar_por_id(self, id_empresa: int) -> Optional[Empresa]:
        """Faz a busca de uma empresa por ID"""
        pass

    @abstractmethod
    def buscar_por_cnpj(self, cnpj: str) -> Optional[Empresa]:
        """Busca uma empresa pelo CNPJ"""
        pass

    @abstractmethod
    def buscar_por_nome(self, nome: str) -> List[Empresa]:
        """Busca empresas pelo nome ou parte dele"""
        pass

    @abstractmethod
    def buscar_por_porte(self, porte: str) -> List[Empresa]:
        """Retorna empresas de um porte específico (pequeno, medio, grande)"""
        pass

    @abstractmethod
    def buscar_por_filtros(self, **filtros) -> List[Empresa]:
        """Realiza a busca de empresas com filtro dinâmico"""
        pass

    @abstractmethod
    def atualizar(self, empresa: Empresa):
        """Atualiza dados de uma empresa"""
        pass

    @abstractmethod
    def deletar(self, id_empresa: int):
        """Remove uma empresa com o ID"""
        pass

    @abstractmethod
    def contar_total(self) -> int:
        """Retorna o total de empresas cadastradas"""
        pass

    @abstractmethod
    def contar_por_porte(self, porte: str) -> int:
        """Retorna o total de empresas de um porte específico"""
        pass