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
    def listar_inativas(self) -> List[Vaga]:
        """
        Retorna apenas as vagas inativas (pausadas).
        return: Lista de objetos Vaga com status ativo = False.
        """
        pass

    @abstractmethod
    def listar_por_area(self, area: str) -> List[Vaga]:
        """
        Retorna vagas de uma área específica.
        param area: Área de atuação desejada.
        return: Lista de vagas da área.
        """
        pass

    @abstractmethod
    def listar_por_modalidade(self, modalidade: str) -> List[Vaga]:
        """
        Retorna vagas de uma modalidade específica (presencial, remoto, hibrido).
        param modalidade: Modalidade desejada.
        return: Lista de vagas da modalidade.
        """
        pass

    @abstractmethod
    def listar_por_tipo(self, tipo: str) -> List[Vaga]:
        """
        Retorna vagas de um tipo específico (emprego, estagio, trainee).
        param tipo: Tipo de vaga desejado.
        return: Lista de vagas do tipo.
        """
        pass

    @abstractmethod
    def listar_por_titulo(self, titulo: str) -> List[Vaga]:
        """
        Retorna vagas cujo título contém a string fornecida.
        param titulo: Parte do título da vaga.
        return: Lista de vagas encontradas.
        """
        pass

    @abstractmethod
    def buscar_por_filtros(self, **filtros) -> List[Vaga]:
        """
        Realiza busca de vagas com múltiplos filtros.
        param filtros: Dicionário com filtros (area, modalidade, tipo, ativa, etc).
        return: Lista de vagas que atendem aos filtros.
        """
        pass

    @abstractmethod
    def atualizar(self, vaga: Vaga) -> None:
        """
        Atualiza os dados de uma vaga.
        param vaga: Objeto Vaga com dados atualizados.
        """
        pass

    @abstractmethod
    def excluir(self, id_vaga: int) -> None:
        """
        Exclui uma vaga do sistema.
        param id_vaga: ID da vaga a ser excluída.
        """
        pass

    @abstractmethod
    def contar_total(self) -> int:
        """
        Retorna o total de vagas cadastradas.
        return: Quantidade total de vagas.
        """
        pass

    @abstractmethod
    def contar_ativas(self) -> int:
        """
        Retorna o total de vagas ativas.
        return: Quantidade de vagas ativas.
        """
        pass

    @abstractmethod
    def contar_por_area(self, area: str) -> int:
        """
        Retorna o total de vagas de uma área específica.
        param area: Área desejada.
        return: Quantidade de vagas.
        """
        pass
