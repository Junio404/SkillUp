from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.vaga import Vaga

class IVagaRepositorio(ABC):

    @abstractmethod
    def salvar(self, vaga: Vaga) -> None:
        pass

    @abstractmethod
    def buscar_por_id(self, id_vaga: int) -> Optional[Vaga]:
        pass

    @abstractmethod
    def listar_todas(self) -> List[Vaga]:
        pass

    @abstractmethod
    def listar_ativas(self) -> List[Vaga]:
        pass

    @abstractmethod
    def excluir(self, id_vaga: int) -> None:
        pass
