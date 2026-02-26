class CursoCompetencia:
    """Entidade de domínio que representa a competência conferida por um curso."""

    NIVEIS_VALIDOS = {
        "iniciante": 0,
        "intermediario": 1,
        "avancado": 2
    }

    def __init__(
        self,
        id: int,
        id_curso: int,
        id_competencia: int,
        nivel_conferido: str
    ):
        """
        Cria uma relação entre Curso e Competência.

        :param id: Inteiro positivo (PK)
        :param id_curso: ID do curso (FK)
        :param id_competencia: ID da competência (FK)
        :param nivel_conferido: iniciante | intermediario | avancado
        """

        self._validar_id(id)
        self._id = id

        self._validar_id(id_curso)
        self._id_curso = id_curso

        self._validar_id(id_competencia)
        self._id_competencia = id_competencia

        self.nivel_conferido = nivel_conferido

    # --------------------
    #     Validações
    # --------------------

    def _validar_id(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("ID deve ser inteiro positivo")

    def _validar_nivel(self, valor):
        if not isinstance(valor, str):
            raise TypeError("Nível deve ser string")

        if valor.lower() not in self.NIVEIS_VALIDOS:
            raise ValueError(
                "Nível inválido. Use: iniciante, intermediario ou avancado"
            )

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
    def id_competencia(self):
        return self._id_competencia

    @property
    def nivel_conferido(self):
        return self._nivel_conferido

    @nivel_conferido.setter
    def nivel_conferido(self, valor):
        self._validar_nivel(valor)
        self._nivel_conferido = valor.lower()

    # --------------------
    #     Métodos de Domínio
    # --------------------

    def atualizar_nivel(self, novo_nivel: str):
        """Atualiza o nível conferido."""
        self.nivel_conferido = novo_nivel

    def nivel_como_inteiro(self):
        """Retorna nível como inteiro (0,1,2) para persistência."""
        return self.NIVEIS_VALIDOS[self._nivel_conferido]

    # --------------------
    #     Serialização
    # --------------------

    def to_dict(self):
        return {
            "id": self.id,
            "curso_id": self.id_curso,
            "competencia_id": self.id_competencia,
            "nivel": self.nivel_como_inteiro()
        }

    @staticmethod
    def from_dict(d):
        mapa_inverso = {
            0: "iniciante",
            1: "intermediario",
            2: "avancado"
        }

        return CursoCompetencia(
            id=d["id"],
            id_curso=d["curso_id"],
            id_competencia=d["competencia_id"],
            nivel_conferido=mapa_inverso[d["nivel"]]
        )

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Curso ID: {self.id_curso}\n"
            f"Competência ID: {self.id_competencia}\n"
            f"Nível Conferido: {self.nivel_conferido}\n"
            "-------------------------"
        )