from entidade_publicadora import EntidadePublicadora

class Empresa(EntidadePublicadora):
    def __init__(self, id_empresa, nome, cnpj, porte):
        super().__init__(id_empresa, nome, cnpj)
        self.porte = porte  # Ex: pequeno, medio, grande
    

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
    def cnpj(self):
        """Retorna CNPJ."""
        return self._cnpj

    @cnpj.setter
    def cnpj(self, valor):
        """Define CNPJ (imutável)."""
        if hasattr(self, "_cnpj"):
            raise ValueError("CNPJ não pode ser alterado")

        self._validar_cnpj(valor)
        self._cnpj = valor

    @property
    def porte(self):
        """Retorna porte da empresa."""
        return self._porte

    @porte.setter
    def porte(self, valor):
        """Define porte."""
        if valor not in ["pequeno", "medio", "grande"]:
            raise ValueError("Porte deve ser: pequeno, medio ou grande")
        self._porte = valor

    #--------------------
    #     Métodos de Domínio
    #--------------------

    def validar_publicacao(self, oportunidade):
        """
        Empresa pode publicar Vagas de Emprego e Cursos Empresariais.
        Regras trabalhistas e de vínculo serão validadas na oportunidade.
        """
        return True

    def obter_limites_publicacao(self):
        """
        Limites podem variar conforme o porte da empresa.
        """
        if self.porte == "pequeno":
            return 5
        elif self.porte == "medio":
            return 15
        elif self.porte == "grande":
            return 50
        return 0

    def _str_(self):
        return f"Empresa: {self.nome} ({self.porte})"