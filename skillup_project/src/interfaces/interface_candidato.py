from abc import ABC, abstractmethod
from src.dominio.candidato import Candidato

'''Interface para repositório de candidatos. Define os métodos que qualquer implementação deve seguir.'''
class ICandidatoRepositorio(ABC):

    @abstractmethod
    def salvar(self, candidato: Candidato):
        pass

    @abstractmethod
    def listar(self) -> list[Candidato]:
        pass

    @abstractmethod
    def buscar_por_id(self, id_candidato: int) -> Candidato | None:
        pass

    @abstractmethod
    def buscar_por_filtros(self, **filtros) -> list[Candidato]:
        pass

    @abstractmethod
    def atualizar(self, candidato: Candidato):
        pass

    @abstractmethod
    def deletar(self, id_candidato: int):
        pass
