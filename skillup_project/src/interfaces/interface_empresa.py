from abc import ABC, abstractmethod
from src.dominio.empresa import Empresa

'''Interface para repositório de Empresa. Define os métodos que qualquer implementação deve seguir.'''
class IEmpresa(ABC):

    @abstractmethod
    def salvar(self, empresa: Empresa):
        """Armazena a empresa"""
        pass

    @abstractmethod
    def listar(self) -> list[Empresa]:
        """Retorna todas as empresas"""
        pass

    @abstractmethod
    def buscar_por_id(self, id_empresa: int) -> Empresa | None:
        """Faz a busca de uma empresa por ID"""
        pass

    @abstractmethod
    def buscar_por_filtros(self, **filtros) -> list[Empresa]:
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