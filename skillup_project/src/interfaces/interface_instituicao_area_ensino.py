from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.instituicao_ensino import InstituicaoAreaEnsino


'''Interface para repositório de InstituicaoAreaEnsino. Define os métodos que qualquer implementação deve seguir.'''
class IInstituicaoAreaEnsinoRepositorio(ABC):
    """
    Interface que define o contrato para repositórios de InstituicaoAreaEnsino.
    Classes concretas devem implementar a persistência das relações instituição-área.
    """

    @abstractmethod
    def salvar(self, inst_area: InstituicaoAreaEnsino) -> None:
        """
        Salva ou atualiza uma relação instituição-área no armazenamento.
        param inst_area: Objeto InstituicaoAreaEnsino a ser persistido.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id_instituicao_area: int) -> Optional[InstituicaoAreaEnsino]:
        """
        Busca uma relação instituição-área pelo ID.
        param id_instituicao_area: Identificador da relação.
        return: Objeto InstituicaoAreaEnsino encontrado ou None.
        """
        pass

    @abstractmethod
    def listar_todas(self) -> List[InstituicaoAreaEnsino]:
        """
        Retorna todas as relações instituição-área cadastradas.
        return: Lista de objetos InstituicaoAreaEnsino.
        """
        pass

    @abstractmethod
    def listar_por_instituicao(self, id_instituicao: int) -> List[InstituicaoAreaEnsino]:
        """
        Retorna todas as áreas de uma instituição específica.
        param id_instituicao: ID da instituição.
        return: Lista de relações da instituição.
        """
        pass

    @abstractmethod
    def listar_por_area(self, id_area: int) -> List[InstituicaoAreaEnsino]:
        """
        Retorna todas as instituições que oferecem uma área específica.
        param id_area: ID da área.
        return: Lista de relações com esta área.
        """
        pass

    @abstractmethod
    def buscar_por_instituicao_e_area(self, id_instituicao: int, id_area: int) -> Optional[InstituicaoAreaEnsino]:
        """
        Busca uma relação específica entre instituição e área.
        param id_instituicao: ID da instituição.
        param id_area: ID da área.
        return: Objeto InstituicaoAreaEnsino encontrado ou None.
        """
        pass

    @abstractmethod
    def atualizar(self, inst_area: InstituicaoAreaEnsino) -> None:
        """
        Atualiza uma relação instituição-área.
        param inst_area: Objeto InstituicaoAreaEnsino com dados atualizados.
        """
        pass

    @abstractmethod
    def remover_por_id(self, id_instituicao_area: int) -> bool:
        """
        Remove uma relação instituição-área pelo ID.
        param id_instituicao_area: Identificador da relação.
        return: True se removeu com sucesso, False caso contrário.
        """
        pass

    @abstractmethod
    def remover_por_instituicao(self, id_instituicao: int) -> bool:
        """
        Remove todas as relações de uma instituição (ao deletar instituição).
        param id_instituicao: ID da instituição.
        return: True se removeu com sucesso, False caso contrário.
        """
        pass

    @abstractmethod
    def contar_areas_por_instituicao(self, id_instituicao: int) -> int:
        """
        Retorna a quantidade de áreas de uma instituição.
        param id_instituicao: ID da instituição.
        return: Quantidade de áreas.
        """
        pass

    @abstractmethod
    def contar_instituicoes_por_area(self, id_area: int) -> int:
        """
        Retorna a quantidade de instituições que oferecem uma área.
        param id_area: ID da área.
        return: Quantidade de instituições.
        """
        pass
