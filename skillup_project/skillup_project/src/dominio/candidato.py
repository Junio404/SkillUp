class Candidato:
    """Entidade de domínio que representa um candidato."""

    def __init__(
        self,
        id: int,
        nome: str,
        cpf: str,
        email: str,
        areas_interesse: list[str],
        nivel_formacao: str
    ):
        """
        Cria um candidato.

        :param id: Inteiro positivo
        :param nome: Nome do candidato
        :param cpf: CPF com 11 dígitos
        :param email: Email válido
        :param areas_interesse: Lista de áreas
        :param nivel_formacao: Formação acadêmica
        """
        self._validar_id(id)
        self._id = id

        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.areas_interesse = areas_interesse
        self.nivel_formacao = nivel_formacao

    #--------------------
    #     Validações
    #--------------------

    def _validar_id(self, valor):
        """Valida ID."""
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("ID deve ser inteiro positivo")

    def _validar_nome(self, valor):
        """Valida nome."""
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Nome inválido")

    def _validar_cpf(self, valor):
        """Valida CPF."""
        if not isinstance(valor, str) or len(valor) != 11 or not valor.isdigit():
            raise ValueError("CPF inválido")

    def _validar_email(self, valor):
        """Valida email."""
        if not isinstance(valor, str) or "@" not in valor:
            raise ValueError("Email inválido")

    def _validar_areas(self, lista):
        """Valida áreas de interesse."""
        if not isinstance(lista, list):
            raise TypeError("Áreas de interesse devem ser uma lista")

        if not lista:
            raise ValueError("Informe ao menos uma área")

        for area in lista:
            if not isinstance(area, str) or not area.strip():
                raise ValueError("Área inválida")

    #--------------------
    #     Properties
    #--------------------

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
    def cpf(self):
        """Retorna CPF."""
        return self._cpf

    @cpf.setter
    def cpf(self, valor):
        """Define CPF (imutável)."""
        if hasattr(self, "_cpf"):
            raise ValueError("CPF não pode ser alterado")

        self._validar_cpf(valor)
        self._cpf = valor

    @property
    def email(self):
        """Retorna email."""
        return self._email

    @email.setter
    def email(self, valor):
        """Define email."""
        self._validar_email(valor)
        self._email = valor

    @property
    def areas_interesse(self):
        """Retorna cópia das áreas."""
        return list(self._areas_interesse)  #exemplo proteção contra mutação externa

    @areas_interesse.setter
    def areas_interesse(self, lista):
        """Define áreas."""
        self._validar_areas(lista)
        self._areas_interesse = list(lista)

    @property
    def nivel_formacao(self):
        """Retorna formação."""
        return self._nivel_formacao

    @nivel_formacao.setter
    def nivel_formacao(self, valor):
        """Define formação."""
        if not isinstance(valor, str):
            raise TypeError("Nível de formação inválido")

        self._nivel_formacao = valor

    #--------------------
    #     Métodos de Domínio
    #--------------------

    def adicionar_area(self, area: str):
        """Adiciona área."""
        if not isinstance(area, str) or not area.strip():
            raise ValueError("Área inválida")

        if area in self._areas_interesse:
            raise ValueError("Área já cadastrada")

        self._areas_interesse.append(area)

    def remover_area(self, area: str):
        """Remove área."""
        if area not in self._areas_interesse:
            raise ValueError("Área não encontrada")

        if len(self._areas_interesse) == 1:
            raise ValueError("Ao menos uma área é obrigatória")

        self._areas_interesse.remove(area)

    def atualizar_dado(self, campo: str, novo_valor):
        """Atualiza atributo permitido."""
        if campo in ("id", "cpf"):
            raise ValueError(f"'{campo}' não pode ser alterado")

        if not hasattr(self, campo):
            raise AttributeError("Campo inexistente")

        setattr(self, campo, novo_valor)

    #--------------------
    #     Serialização
    #--------------------

    def to_dict(self):
        """Converte para dict."""
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "areas_interesse": self._areas_interesse,
            "nivel_formacao": self.nivel_formacao
        }

    @staticmethod
    def from_dict(d):
        """Cria a partir de dict."""
        return Candidato(
            id=d["id"],
            nome=d["nome"],
            cpf=d["cpf"],
            email=d["email"],
            areas_interesse=d["areas_interesse"],
            nivel_formacao=d["nivel_formacao"]
        )

    def __str__(self):
        """Representação textual."""
        return (
            f"ID: {self.id}\n"
            f"Nome: {self.nome}\n"
            f"CPF: {self.cpf}\n"
            f"Email: {self.email}\n"
            f"Áreas: {', '.join(self._areas_interesse)}\n"
            f"Formação: {self.nivel_formacao}\n"
            "-------------------------"
        )
