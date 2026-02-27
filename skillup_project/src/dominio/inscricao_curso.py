from enum import Enum
from datetime import date


class StatusInscricao(Enum):
    DEFERIDO = 0
    INDEFERIDO = 1


class InscricaoCurso:
    """Entidade de domínio que representa a inscrição de um aluno em um curso."""

    def __init__(
        self,
        id: int,
        id_curso: int,
        id_aluno: int,
        data_inscricao: date,
        status: StatusInscricao = StatusInscricao.DEFERIDO
    ):
        """
        Cria uma inscrição em curso.

        :param id: Inteiro positivo (PK)
        :param id_curso: FK do curso
        :param id_aluno: FK do aluno
        :param data_inscricao: Data da inscrição
        :param status: StatusInscricao (Enum)
        """

        self._validar_id(id)
        self._id = id

        self._validar_id(id_curso)
        self._id_curso = id_curso

        self._validar_id(id_aluno)
        self._id_aluno = id_aluno

        self.data_inscricao = data_inscricao
        self.status = status

    # --------------------
    #     Validações
    # --------------------

    def _validar_id(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("ID deve ser inteiro positivo")

    def _validar_data(self, valor):
        if not isinstance(valor, date):
            raise TypeError("Data de inscrição inválida")

    def _validar_status(self, valor):
        if not isinstance(valor, StatusInscricao):
            raise TypeError("Status deve ser do tipo StatusInscricao")

    # --------------------
    #     Properties
    # --------------------

    @property
    def id(self):
        return self._id

    @property
    def id_curso(self):
        return self._id_curso

    @property
    def id_aluno(self):
        return self._id_aluno

    @property
    def data_inscricao(self):
        return self._data_inscricao

    @data_inscricao.setter
    def data_inscricao(self, valor):
        self._validar_data(valor)
        self._data_inscricao = valor

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, valor):
        self._validar_status(valor)
        self._status = valor

    # --------------------
    #     Métodos de Domínio
    # --------------------

    def deferir(self):
        """Define inscrição como deferida."""
        self._status = StatusInscricao.DEFERIDO

    def indeferir(self):
        """Define inscrição como indeferida."""
        self._status = StatusInscricao.INDEFERIDO

    # --------------------
    #     Serialização
    # --------------------

    def to_dict(self):
        return {
            "id": self.id,
            "curso_id": self.id_curso,
            "aluno_id": self.id_aluno,
            "data_inscricao": self.data_inscricao.isoformat(),
            "status": self.status.value
        }

    @staticmethod
    def from_dict(d):
        return InscricaoCurso(
            id=d["id"],
            id_curso=d["curso_id"],
            id_aluno=d["aluno_id"],
            data_inscricao=date.fromisoformat(d["data_inscricao"]),
            status=StatusInscricao(d["status"])
        )

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Curso ID: {self.id_curso}\n"
            f"Aluno ID: {self.id_aluno}\n"
            f"Data Inscrição: {self.data_inscricao}\n"
            f"Status: {self.status.name}\n"
            "-------------------------"
        )