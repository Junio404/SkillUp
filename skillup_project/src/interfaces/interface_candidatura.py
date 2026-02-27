from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.candidatura import Candidatura

class ICandidaturaRepositorio(ABC):
    """
    Interface que define o contrato para repositórios de Candidatura.
    Classes concretas devem implementar todos os métodos.
    
    """

    @abstractmethod
    def salvar(self, candidatura: Candidatura) -> None:
        """
        Salva ou atualiza uma candidatura no armazenamento.
        param candidatura: Objeto Candidatura a ser persistido.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id_candidatura: int) -> Optional[Candidatura]:
        """
        Busca uma candidatura pelo ID.
        param id_candidatura: Identificador da candidatura.
        return: Objeto Candidatura encontrado ou None.
        """
        pass

    @abstractmethod
    def listar_todas(self) -> List[Candidatura]:
        """
        Lista todas as candidaturas cadastradas.
        return: Lista de objetos Candidatura.
        """
        pass

    @abstractmethod
    def listar_por_candidato(self, id_candidato: int) -> List[Candidatura]:
        """
        Retorna todas as candidaturas de um candidato específico.
        param id_candidato: ID do candidato.
        return: Lista de candidaturas deste candidato.
        """
        pass

    @abstractmethod
    def listar_por_vaga(self, id_vaga: int) -> List[Candidatura]:
        """
        Retorna todas as candidaturas aplicadas a uma vaga específica.        
        param id_vaga: ID da vaga.
        return: Lista de candidaturas para esta vaga.
        """
        pass

    @abstractmethod
    def listar_por_status(self, status: str) -> List[Candidatura]:
        """
        Retorna todas as candidaturas com um status específico.
        param status: Status desejado (enviado, em_analise, aceito, recusado, cancelado).
        return: Lista de candidaturas com o status especificado.
        """
        pass

    @abstractmethod
    def contar_por_candidato(self, id_candidato: int) -> int:
        """
        Retorna o total de candidaturas de um candidato.
        param id_candidato: ID do candidato.
        return: Quantidade de candidaturas.
        """
        pass

    @abstractmethod
    def contar_por_vaga(self, id_vaga: int) -> int:
        """
        Retorna o total de candidaturas para uma vaga.
        param id_vaga: ID da vaga.
        return: Quantidade de candidaturas.
        """
        pass

    @abstractmethod
    def contar_por_status(self, status: str) -> int:
        """
        Retorna o total de candidaturas com um status específico.
        param status: Status a contar.
        return: Quantidade de candidaturas.
        """
        pass

    @abstractmethod
    def atualizar_status(self, id_candidatura: int, novo_status: str) -> bool:
        """
        Atualiza apenas o status de uma candidatura.
        param id_candidatura: ID da candidatura.
        param novo_status: Novo status a atribuir.
        return: True se atualizou com sucesso, False caso contrário.
        """
        pass

    @abstractmethod
    def excluir(self, id_candidatura: int) -> None:
        """
        Remove uma candidatura do sistema.
        param id_candidatura: ID da candidatura a ser removida.
        """
        pass
