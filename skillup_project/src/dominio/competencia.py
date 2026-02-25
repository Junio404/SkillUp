class Competencia:
    """Entidade de domínio que representa uma competência."""

    def __init__(
        self,
        id: int,
        nome: str,
        descricao: str
    ):
        """
        Cria uma competência.

        :param id: Inteiro positivo
        :param nome: Nome único da competência
        :param descricao: Descrição da competência
        """
        self._validar_id(id)
        self._id = id

        self.nome = nome
        self.descricao = descricao

    # --------------------
    #     Validações
    # --------------------

    def _validar_id(self, valor):
        """Valida ID."""
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("ID deve ser inteiro positivo")

    def _validar_nome(self, valor):
        """Valida nome."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Nome inválido")

        if len(valor) > 150:
            raise ValueError("Nome deve ter no máximo 150 caracteres")

    def _validar_descricao(self, valor):
        """Valida descrição."""
        if not isinstance(valor, str):
            raise TypeError("Descrição inválida")

    # --------------------
    #     Properties
    # --------------------

    @property
    def id(self):
        """Retorna ID."""
        return self._id

    @property
    def nome(self):
        """Retorna nome."""
        return self._nome

    @nome.setter
    def nome(self, valor):
        """Define nome."""
        self._validar_nome(valor)
        self._nome = valor

    @property
    def descricao(self):
        """Retorna descrição."""
        return self._descricao

    @descricao.setter
    def descricao(self, valor):
        """Define descrição."""
        self._validar_descricao(valor)
        self._descricao = valor

    # --------------------
    #     Métodos de Domínio
    # --------------------

    def atualizar_dado(self, campo: str, novo_valor):
        """Atualiza atributo permitido."""
        if campo == "id":
            raise ValueError("'id' não pode ser alterado")

        if not hasattr(self, campo):
            raise AttributeError("Campo inexistente")

        setattr(self, campo, novo_valor)

    # --------------------
    #     Serialização
    # --------------------

    def to_dict(self):
        """Converte para dict."""
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao
        }

    @staticmethod
    def from_dict(d):
        """Cria a partir de dict."""
        return Competencia(
            id=d["id"],
            nome=d["nome"],
            descricao=d["descricao"]
        )

    def __str__(self):
        """Representação textual."""
        return (
            f"ID: {self.id}\n"
            f"Nome: {self.nome}\n"
            f"Descrição: {self.descricao}\n"
            "-------------------------"
        )