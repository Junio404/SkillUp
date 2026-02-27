from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.competencia import Competencia

class ICompetenciaRepositorio(ABC):
    """
    Interface que define o contrato para repositórios de Competencia.
    Classes concretas devem implementar a persistência de competencias.
    """
    @abstractmethod
    def salvar(self, competencia: Competencia) -> None:
        """
        Salva ou atualiza uma competência no armazenamento.
        param competencia: Objeto Competencia a ser persistido.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id_competencia: int) -> Optional[Competencia]:
        """
        Busca uma competência pelo ID.
        param id_competencia: Identificador da competência.
        return: Objeto Competencia encontrado ou None.
        """
        pass

    @abstractmethod
    def buscar_por_nome(self, nome: str) -> Optional[Competencia]:
        """
        Busca uma competência pelo nome exato.
        param nome: Nome da competência.
        return: Objeto Competencia encontrado ou None.
        """
        pass

    @abstractmethod
    def buscar_por_nome_parcial(self, nome: str) -> List[Competencia]:
        """
        Busca competências cujo nome contém a string fornecida.
        param nome: Parte do nome da competência.
        return: Lista de competências encontradas.
        """
        pass

    @abstractmethod
    def listar_todos(self) -> List[Competencia]:
        """
        Retorna todas as competências cadastradas.
        return: Lista de objetos Competencia.
        """
        pass

    @abstractmethod
    def buscar_por_filtros(self, **filtros) -> List[Competencia]:
        """
        Realiza busca de competências com filtros dinâmicos.
        param filtros: Dicionário com filtros (nome, descricao, etc).
        return: Lista de competências que atendem aos filtros.
        """
        pass

    @abstractmethod
    def atualizar(self, competencia: Competencia) -> None:
        """
        Atualiza os dados de uma competência.
        param competencia: Objeto Competencia com dados atualizados.
        """
        pass

    @abstractmethod
    def remover_por_id(self, id_competencia: int) -> bool:
        """
        Remove uma competência pelo ID.
        param id_competencia: Identificador da competência.
        return: True se removeu com sucesso, False caso contrário.
        """
        pass

    @abstractmethod
    def contar_total(self) -> int:
        """
        Retorna o total de competências cadastradas.
        return: Quantidade total de competências.
        """
        pass