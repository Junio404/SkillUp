class CompetenciaCandidato:
    """Entidade de domínio que representa o nível de uma competência de um candidato."""

    NIVEIS_VALIDOS = {
        "iniciante": 0,
        "intermediario": 1,
        "avancado": 2
    }

    def __init__(
        self,
        id: int,
        id_candidato: int,
        id_competencia: int,
        nivel_atual: str
    ):
        """
        Cria relação entre Candidato e Competência.

        :param id: Inteiro positivo (PK)
        :param id_candidato: FK do candidato;
        :param id_competencoa: FK da competência
        param nivel_atual: iniciante | intermediario | avancado
        """

        self._validar_id(id)
        self._id = id

        self._validar_id(id_candidato)
        self._id_candidato = id_candidato

        self._validar_id(id_competencia)
        self._id_competencia = id_competencia

        self.nivel_atual = nivel_atual

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
    def id_candidato(self):
        return self._id_candidato

    @property
    def id_competencia(self):
        return self._id_competencia

    @property
    def nivel_atual(self):
        return self._nivel_atual

    @nivel_atual.setter
    def nivel_atual(self, valor):
        self._validar_nivel(valor)
        self._nivel_atual = valor.lower()

    # --------------------
    #     Métodos de Domínio
    # --------------------

    def atualizar_nivel(self, novo_nivel: str):
        """Atualiza o nível atual da competência."""
        self.nivel_atual = novo_nivel

    def nivel_como_inteiro(self):
        """Retorna nível como inteiro (0,1,2) para persistência."""
        return self.NIVEIS_VALIDOS[self._nivel_atual]

    # --------------------
    #     Serialização
    # --------------------

    def to_dict(self):
        return {
            "id": self.id,
            "candidato_id": self.id_candidato,
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

        return CompetenciaCandidato(
            id=d["id"],
            id_candidato=d["candidato_id"],
            id_competencia=d["competencia_id"],
            nivel_atual=mapa_inverso[d["nivel"]]
        )

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Candidato ID: {self.id_candidato}\n"
            f"Competência ID: {self.id_competencia}\n"
            f"Nível Atual: {self.nivel_atual}\n"
            "-------------------------"
        )