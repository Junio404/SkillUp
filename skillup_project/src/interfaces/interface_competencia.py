from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.competencia import Competencia

class ICompetenciaRepositorio(ABC):
    @abstractmethod
    def salvar(self, competencia: Competencia) -> None:
        pass

    @abstractmethod
    def buscar_por_id(self, id_competencia: int) -> Optional[Competencia]:
        pass

    @abstractmethod
    def buscar_por_nome(self, nome: str) -> Optional[Competencia]:
        pass

    @abstractmethod
    def listar_todos(self) -> List[Competencia]:
        pass

    @abstractmethod
    def remover_por_id(self, id_competencia: int) -> bool:
        pass