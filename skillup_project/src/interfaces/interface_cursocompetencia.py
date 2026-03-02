from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.curso_competencia import CursoCompetencia

'''Interface para repositório de CursoCompetencia. Define os métodos que qualquer implementação deve seguir.'''
class ICursoCompetenciaRepositorio(ABC):
    """
    Interface que define o contrato para repositórios de CursoCompetencia.
    Classes concretas devem implementar a persistência de competências oferecidas por cursos.
    """

    @abstractmethod
    def salvar(self, curso_competencia: CursoCompetencia) -> None:
        """
        Salva ou atualiza uma competência de curso no armazenamento.
        param curso_competencia: Objeto CursoCompetencia a ser persistido.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id_curso_competencia: int) -> Optional[CursoCompetencia]:
        """
        Busca uma competência de curso pelo ID.
        param id_curso_competencia: Identificador da competência do curso.
        return: Objeto CursoCompetencia encontrado ou None.
        """
        pass

    @abstractmethod
    def listar_todas(self) -> List[CursoCompetencia]:
        """
        Retorna todas as competências de cursos cadastradas.
        return: Lista de objetos CursoCompetencia.
        """
        pass

    @abstractmethod
    def listar_por_curso(self, id_curso: int) -> List[CursoCompetencia]:
        """
        Retorna todas as competências oferecidas por um curso específico.
        param id_curso: ID do curso.
        return: Lista de competências do curso.
        """
        pass

    @abstractmethod
    def listar_por_competencia(self, id_competencia: int) -> List[CursoCompetencia]:
        """
        Retorna todos os cursos que oferecem uma competência específica.
        param id_competencia: ID da competência.
        return: Lista de cursos que oferecem esta competência.
        """
        pass

    @abstractmethod
    def listar_por_nivel(self, nivel: str) -> List[CursoCompetencia]:
        """
        Retorna todas as competências de cursos com um nível específico.
        param nivel: Nível desejado (iniciante, intermediario, avancado).
        return: Lista de competências do nível especificado.
        """
        pass

    @abstractmethod
    def buscar_por_curso_e_competencia(self, id_curso: int, id_competencia: int) -> Optional[CursoCompetencia]:
        """
        Busca uma competência específica oferecida por um curso.
        param id_curso: ID do curso.
        param id_competencia: ID da competência.
        return: Objeto CursoCompetencia encontrado ou None.
        """
        pass

    @abstractmethod
    def atualizar(self, curso_competencia: CursoCompetencia) -> None:
        """
        Atualiza uma competência de um curso.
        param curso_competencia: Objeto CursoCompetencia com dados atualizados.
        """
        pass

    @abstractmethod
    def remover_por_id(self, id_curso_competencia: int) -> bool:
        """
        Remove uma competência de um curso pelo ID.
        param id_curso_competencia: Identificador da competência do curso.
        return: True se removeu com sucesso, False caso contrário.
        """
        pass

    @abstractmethod
    def remover_por_curso(self, id_curso: int) -> bool:
        """
        Remove todas as competências de um curso (ao deletar curso).
        param id_curso: ID do curso.
        return: True se removeu com sucesso, False caso contrário.
        """
        pass

    @abstractmethod
    def contar_competencias_curso(self, id_curso: int) -> int:
        """
        Retorna a quantidade de competências oferecidas por um curso.
        param id_curso: ID do curso.
        return: Quantidade de competências.
        """
        pass