from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.vaga import Vaga

class IVagaRepositorio(ABC):
    """
    Interface que define o contrato para repositórios de Vaga.
    Classes concretas devem implementar a persistência de vaga (ex: JSON, Banco).
    """

    @abstractmethod
    def salvar(self, vaga: Vaga) -> None:
        """
        Salva ou atualiza uma vaga no armazenamento.
        param vaga: Objeto Vaga a ser persistido.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id_vaga: int) -> Optional[Vaga]:
        """
        Busca uma vaga pelo seu identificador único.
        param id_vaga: ID da vaga.
        return: Objeto Vaga se encontrado, se não: None.
        """
        pass

    @abstractmethod
    def listar_todas(self) -> List[Vaga]:
        """
        Retorna todas as vagas cadastradas no sistema.
        return: Lista de objetos Vaga.
        """

        pass

    @abstractmethod
    def listar_ativas(self) -> List[Vaga]:
        """
        Retorna apenas as vagas ativas (publicadas), disponíveis para candidatura.
        return: Lista de objetos Vaga com status ativo = True.
        """
        pass

    @abstractmethod
    def excluir(self, id_vaga: int) -> None:
        """
        Exclui uma vaga do sistema.
        param id_vaga: ID da vaga a ser excluída.
        """
        pass
