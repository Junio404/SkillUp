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
        Salva ou atualiza uma candidatura no armazenamento.
        param candidatura: Objeto Candidatura a ser persistido.
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
    def excluir(self, id_candidatura: int) -> None:
        """
        Remove uma candidatura do sistema.
        param id_candidatura: ID da candidatura a ser removida.
        """
        pass
