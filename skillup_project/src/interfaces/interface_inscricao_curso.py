
from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.inscricao_curso import InscricaoCurso


class IInscricaoCursoRepositorio(ABC):
    """
    Interface que define o contrato para repositórios de InscricaoCurso.
    Classes concretas devem implementar todos os métodos.
    """

    @abstractmethod
    def salvar(self, inscricao: InscricaoCurso) -> None:
        """
        Salva ou atualiza uma inscrição no armazenamento.
        param inscricao: Objeto InscricaoCurso a ser persistido.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id_inscricao: int) -> Optional[InscricaoCurso]:
        """
        Busca uma inscrição pelo ID.
        param id_inscricao: Identificador da inscrição.
        return: Objeto InscricaoCurso encontrado ou None.
        """
        pass

    @abstractmethod
    def listar_todas(self) -> List[InscricaoCurso]:
        """
        Lista todas as inscrições cadastradas.
        return: Lista de objetos InscricaoCurso.
        """
        pass

    @abstractmethod
    def listar_por_aluno(self, id_aluno: int) -> List[InscricaoCurso]:
        """
        Retorna todas as inscrições de um aluno específico.
        param id_aluno: ID do aluno.
        return: Lista de inscrições deste aluno.
        """
        pass

    @abstractmethod
    def listar_por_curso(self, id_curso: int) -> List[InscricaoCurso]:
        """
        Retorna todas as inscrições aplicadas a um curso específico.
        param id_curso: ID do curso.
        return: Lista de inscrições para este curso.
        """
        pass

    @abstractmethod
    def listar_por_status(self, status: str) -> List[InscricaoCurso]:
        """
        Retorna todas as inscrições com um status específico.
        param status: Status desejado.
        return: Lista de inscrições com o status especificado.
        """
        pass

    @abstractmethod
    def contar_por_aluno(self, id_aluno: int) -> int:
        """
        Retorna o total de inscrições de um aluno.
        param id_aluno: ID do aluno.
        return: Quantidade de inscrições.
        """
        pass

    @abstractmethod
    def contar_por_curso(self, id_curso: int) -> int:
        """
        Retorna o total de inscrições para um curso.
        param id_curso: ID do curso.
        return: Quantidade de inscrições.
        """
        pass

    @abstractmethod
    def contar_por_status(self, status: str) -> int:
        """
        Retorna o total de inscrições com um status específico.
        param status: Status a contar.
        return: Quantidade de inscrições.
        """
        pass

    @abstractmethod
    def atualizar_status(self, id_inscricao: int, novo_status: str) -> bool:
        """
        Atualiza apenas o status de uma inscrição.
        param id_inscricao: ID da inscrição.
        param novo_status: Novo status a atribuir.
        return: True se atualizou com sucesso, False caso contrário.
        """
        pass

    @abstractmethod
    def excluir(self, id_inscricao: int) -> None:
        """
        Remove uma inscrição do sistema.
        param id_inscricao: ID da inscrição a ser removida.
        """
        pass
