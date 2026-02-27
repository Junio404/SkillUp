from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.competencia_candidato import CompetenciaCandidato

'''Interface para repositório de CompetenciaCandidato. Define os métodos que qualquer implementação deve seguir.'''
class ICompetenciaCandidatoRepositorio(ABC):
    """
    Interface que define o contrato para repositórios de CompetenciaCandidato.
    Classes concretas devem implementar a persistência de competências de candidatos.
    """

    @abstractmethod
    def salvar(self, competencia_candidato: CompetenciaCandidato) -> None:
        """
        Salva ou atualiza uma competência do candidato no armazenamento.
        param competencia_candidato: Objeto CompetenciaCandidato a ser persistido.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id_competencia_candidato: int) -> Optional[CompetenciaCandidato]:
        """
        Busca uma competência do candidato pelo ID.
        param id_competencia_candidato: Identificador da competência do candidato.
        return: Objeto CompetenciaCandidato encontrado ou None.
        """
        pass

    @abstractmethod
    def listar_todas(self) -> List[CompetenciaCandidato]:
        """
        Retorna todas as competências de candidatos cadastradas.
        return: Lista de objetos CompetenciaCandidato.
        """
        pass

    @abstractmethod
    def listar_por_candidato(self, id_candidato: int) -> List[CompetenciaCandidato]:
        """
        Retorna todas as competências de um candidato específico.
        param id_candidato: ID do candidato.
        return: Lista de competências do candidato.
        """
        pass

    @abstractmethod
    def listar_por_competencia(self, id_competencia: int) -> List[CompetenciaCandidato]:
        """
        Retorna todos os candidatos que possuem uma competência específica.
        param id_competencia: ID da competência.
        return: Lista de competências dos candidatos para esta competência.
        """
        pass

    @abstractmethod
    def listar_por_nivel(self, nivel: str) -> List[CompetenciaCandidato]:
        """
        Retorna todas as competências de candidatos com um nível específico.
        param nivel: Nível desejado (iniciante, intermediario, avancado).
        return: Lista de competências do nível especificado.
        """
        pass

    @abstractmethod
    def buscar_por_candidato_e_competencia(self, id_candidato: int, id_competencia: int) -> Optional[CompetenciaCandidato]:
        """
        Busca a competência de um candidato específico.
        param id_candidato: ID do candidato.
        param id_competencia: ID da competência.
        return: Objeto CompetenciaCandidato encontrado ou None.
        """
        pass

    @abstractmethod
    def atualizar(self, competencia_candidato: CompetenciaCandidato) -> None:
        """
        Atualiza uma competência do candidato.
        param competencia_candidato: Objeto CompetenciaCandidato com dados atualizados.
        """
        pass

    @abstractmethod
    def remover_por_id(self, id_competencia_candidato: int) -> bool:
        """
        Remove uma competência do candidato pelo ID.
        param id_competencia_candidato: Identificador da competência do candidato.
        return: True se removeu com sucesso, False caso contrário.
        """
        pass

    @abstractmethod
    def remover_por_candidato(self, id_candidato: int) -> bool:
        """
        Remove todas as competências de um candidato (ao deletar candidato).
        param id_candidato: ID do candidato.
        return: True se removeu com sucesso, False caso contrário.
        """
        pass
