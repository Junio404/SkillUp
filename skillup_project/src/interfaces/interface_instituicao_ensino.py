from abc import ABC, abstractmethod
from src.dominio.instituicao_ensino import InstituicaoEnsino

'''Interface para repositório de Instituição de Ensino. Define os métodos que qualquer implementação deve seguir.'''
class IInstituicaoEnsino(ABC):

    @abstractmethod
    def salvar(self, instituicao: InstituicaoEnsino):
        """Armazena a instituição de ensino"""
        pass

    @abstractmethod
    def listar(self) -> list[InstituicaoEnsino]:
        """Retorna todas as instituições de ensino"""
        pass

    @abstractmethod
    def buscar_por_id(self, id_instituicao: int) -> InstituicaoEnsino | None:
        """Faz a busca de uma instituição de ensino por ID"""
        pass

    @abstractmethod
    def buscar_por_filtros(self, **filtros) -> list[InstituicaoEnsino]:
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
