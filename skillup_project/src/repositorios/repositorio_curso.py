from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.curso_abs import Curso

'''Interface para repositório de Curso. Define os métodos que qualquer implementação deve seguir.'''
class ICursoRepositorio(ABC):
    """
    Interface que define o contrato para repositórios de Curso.
    Classes concretas devem implementar a persistência de cursos (EAD e Presencial).
    """

    @abstractmethod
    def salvar(self, curso: Curso) -> None:
        """
        Salva ou atualiza um curso no armazenamento.
        param curso: Objeto Curso a ser persistido.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id_curso: int) -> Optional[Curso]:
        """
        Busca um curso pelo seu identificador único.
        param id_curso: ID do curso.
        return: Objeto Curso se encontrado, se não: None.
        """
        pass

    @abstractmethod
    def listar_todos(self) -> List[Curso]:
        """
        Retorna todos os cursos cadastrados no sistema.
        return: Lista de objetos Curso.
        """
        pass

    @abstractmethod
    def listar_por_nome(self, nome: str) -> List[Curso]:
        """
        Retorna cursos que correspondem ao nome especificado.
        param nome: Nome ou parte do nome do curso.
        return: Lista de cursos encontrados.
        """
        pass

    @abstractmethod
    def listar_por_tipo(self, tipo: str) -> List[Curso]:
        """
        Retorna cursos de um tipo específico (EAD ou Presencial).
        param tipo: Tipo do curso ('ead' ou 'presencial').
        return: Lista de cursos do tipo especificado.
        """
        pass

    @abstractmethod
    def listar_por_carga_horaria_minima(self, carga_horaria: int) -> List[Curso]:
        """
        Retorna cursos com carga horária mínima especificada.
        param carga_horaria: Carga horária mínima em horas.
        return: Lista de cursos com carga horária >= especificada.
        """
        pass

    @abstractmethod
    def buscar_por_filtros(self, **filtros) -> List[Curso]:
        """
        Realiza busca de cursos com filtros dinâmicos.
        param filtros: Dicionário com filtros (nome, tipo, carga_horaria_min, etc).
        return: Lista de cursos que atendem aos filtros.
        """
        pass

    @abstractmethod
    def atualizar(self, curso: Curso) -> None:
        """
        Atualiza os dados de um curso.
        param curso: Objeto Curso com dados atualizados.
        """
        pass

    @abstractmethod
    def remover_por_id(self, id_curso: int) -> bool:
        """
        Remove um curso do sistema.
        param id_curso: ID do curso a ser removido.
        return: True se removeu com sucesso, False caso contrário.
        """
        pass

    @abstractmethod
    def contar_total(self) -> int:
        """
        Retorna o total de cursos cadastrados.
        return: Quantidade total de cursos.
        """
        pass