from skillup_project.src.dominio.competencia import Nivel

class RequisitoVaga:
    """Entidade de domínio que representa uma competência exigida por uma vaga."""


    def __init__(
        self,
        id: int,
        id_vaga: int,
        id_competencia: int,
        nivel_minimo: Nivel,
        obrigatorio: bool = True
    ):
        """
        Cria um requisito de vaga.

        :param id: Inteiro positivo (PK)
        :param id_vaga: FK da vaga
        :param id_competencia: FK da competência
        :param nivel_minimo: iniciante | intermediario | avancado
        :param obrigatorio: Se é requisito eliminatório
        """

        self._validar_id(id)
        self._id = id

        self._validar_id(id_vaga)
        self._id_vaga = id_vaga

        self._validar_id(id_competencia)
        self._id_competencia = id_competencia

        self.nivel_minimo = nivel_minimo
        self.obrigatorio = obrigatorio

    # --------------------
    #     Validaçoes
    # --------------------

    def _validar_id(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("ID deve ser inteiro positivo")

    def _validar_nivel(self, valor):
        if not isinstance(valor, str):
            raise TypeError("Nível deve ser string")

        if valor not in [nivel.name for nivel in Nivel]:
            raise ValueError(
                "Nível inválido. Use: iniciante, intermediario ou avancado"
            )

    def _validar_obrigatorio(self, valor):
        if not isinstance(valor, bool):
            raise TypeError("Obrigatório deve ser booleano")

    # --------------------
    #     Properties
    # --------------------

    @property
    def id(self):
        return self._id

    @property
    def id_vaga(self):
        return self._id_vaga

    @property
    def id_competencia(self):
        return self._id_competencia

    @property
    def nivel_minimo(self):
        return self._nivel_minimo

    @nivel_minimo.setter
    def nivel_minimo(self, valor):
        self._validar_nivel(valor)
        self._nivel_minimo = valor

    @property
    def obrigatorio(self):
        return self._obrigatorio

    @obrigatorio.setter
    def obrigatorio(self, valor):
        self._validar_obrigatorio(valor)
        self._obrigatorio = valor

    # --------------------
    #     Métodos de Domínio
    # --------------------

    def atualizar_nivel(self, novo_nivel: str):
        """Atualiza o nível mínimo exigido."""
        self.nivel_minimo = novo_nivel

    def tornar_opcional(self):
        """Marca requisito como não obrigatório."""
        self._obrigatorio = False

    def tornar_obrigatorio(self):
        """Marca requisito como obrigatório."""
        self._obrigatorio = True

    def nivel_como_inteiro(self):
        """Retorna nível como inteiro (0,1,2) para persistência."""
        return Nivel[self.nivel_minimo].value
    # --------------------
    #     Serialização
    # --------------------

    def to_dict(self):
        return {
            "id": self.id,
            "vaga_id": self.id_vaga,
            "competencia_id": self.id_competencia,
            "nivel": self.nivel_como_inteiro(),
            "obrigatorio": self.obrigatorio
        }

    @staticmethod
    def from_dict(d):
        mapa_inverso = {
            0: "iniciante",
            1: "intermediario",
            2: "avancado"
        }

        return RequisitoVaga(
            id=d["id"],
            id_vaga=d["vaga_id"],
            id_competencia=d["competencia_id"],
            nivel_minimo=mapa_inverso[d["nivel"]],
            obrigatorio=d.get("obrigatorio", True)
        )

    def __str__(self):
        return (
            f"ID: {self.id}\n"
            f"Vaga ID: {self.id_vaga}\n"
            f"Competência ID: {self.id_competencia}\n"
            f"Nível Mínimo: {self.nivel_minimo}\n"
            f"Obrigatório: {self.obrigatorio}\n"
            "-------------------------"
        )