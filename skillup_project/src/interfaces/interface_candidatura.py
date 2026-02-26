from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.candidatura import Candidatura

class ICandidaturaRepositorio(ABC):
    
    @abstractmethod
    def salvar(self, candidatura: Candidatura) -> None:
        pass

    @abstractmethod
    def buscar_por_id(self, id_candidatura: int) -> Optional[Candidatura]:
        pass

    @abstractmethod
    def listar_todas(self) -> List[Candidatura]:
        pass

    @abstractmethod
    def listar_por_candidato(self, id_candidato: int) -> List[Candidatura]:
        pass

    @abstractmethod
    def listar_por_vaga(self, id_vaga: int) -> List[Candidatura]:
        pass

    @abstractmethod
    def excluir(self, id_candidatura: int) -> None:
        pass
