from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.instituicao_ensino import AreaEnsino


'''Interface para repositório de AreaEnsino. Define os métodos que qualquer implementação deve seguir.'''
class IAreaEnsinoRepositorio(ABC):
    """
    Interface que define o contrato para repositórios de AreaEnsino.
    Classes concretas devem implementar a persistência de áreas de ensino.
    """

    @abstractmethod
    def salvar(self, area: AreaEnsino) -> None:
        """
        Salva ou atualiza uma área de ensino no armazenamento.
        param area: Objeto AreaEnsino a ser persistido.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id_area: int) -> Optional[AreaEnsino]:
        """
        Busca uma área de ensino pelo ID.
        param id_area: Identificador da área.
        return: Objeto AreaEnsino encontrado ou None.
        """
        pass

    @abstractmethod
    def buscar_por_nome(self, nome: str) -> Optional[AreaEnsino]:
        """
        Busca uma área de ensino pelo nome exato.
        param nome: Nome da área.
        return: Objeto AreaEnsino encontrado ou None.
        """
        pass

    @abstractmethod
    def buscar_por_nome_parcial(self, nome: str) -> List[AreaEnsino]:
        """
        Busca áreas de ensino cujo nome contém a string fornecida.
        param nome: Parte do nome da área.
        return: Lista de áreas encontradas.
        """
        pass

    @abstractmethod
    def listar_todas(self) -> List[AreaEnsino]:
        """
        Retorna todas as áreas de ensino cadastradas.
        return: Lista de objetos AreaEnsino.
        """
        pass

    @abstractmethod
    def atualizar(self, area: AreaEnsino) -> None:
        """
        Atualiza os dados de uma área de ensino.
        param area: Objeto AreaEnsino com dados atualizados.
        """
        pass

    @abstractmethod
    def remover_por_id(self, id_area: int) -> bool:
        """
        Remove uma área de ensino pelo ID.
        param id_area: Identificador da área.
        return: True se removeu com sucesso, False caso contrário.
        """
        pass

    @abstractmethod
    def contar_total(self) -> int:
        """
        Retorna o total de áreas de ensino cadastradas.
        return: Quantidade total de áreas.
        """
        pass
