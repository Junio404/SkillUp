from src.dominio.entidade_publicadora import EntidadePublicadora

class InstituicaoEnsino(EntidadePublicadora):
    """
    Representa uma Instituição de Ensino na plataforma.
    Herda de EntidadePublicadora, sua função no sistema é publicar e gerenciar cursos.
    """

    def __init__(self, id_instituicao: int, razao_social: str, nome_fantasia: str, cnpj: str,
                registro_educacional: str, tipo: str, modalidades: str = "", credenciada: bool = True):
        """
        Inicializa uma nova instância de Instituição de Ensino no domínio do sistema.

        """
        super().__init__(id_instituicao, nome_fantasia, cnpj)
        
        self.razao_social = razao_social
        self.registro_educacional = registro_educacional
        self.tipo = tipo
        self.modalidades = modalidades
        self.credenciada = credenciada
        # Lista de áreas pode ser adicionada aqui se necessário, ou gerenciada externamente via InstituicaoAreaEnsino

    # ===== PROPERTIES =====
    
    @property
    def razao_social(self):
        return self._razao_social
    
    @razao_social.setter
    def razao_social(self, valor):
        if not valor:
            raise ValueError("Razão Social é obrigatória")
        self._razao_social = valor

    @property
    def nome_fantasia(self):
        return self.nome
    
    @nome_fantasia.setter
    def nome_fantasia(self, valor):
        self.nome = valor

    @property
    def modalidades(self):
        return self._modalidades

    @modalidades.setter
    def modalidades(self, valor):
        self._modalidades = valor


    @property
    def registro_educacional(self):
        return self._registro_educacional

    @registro_educacional.setter
    def registro_educacional(self, valor):
        if not valor:
            raise ValueError("Registro educacional é obrigatório")
        self._registro_educacional = valor

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):
        self._tipo = valor

    @property
    def credenciada(self):
        return self._credenciada

    @credenciada.setter
    def credenciada(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("Credenciada deve ser booleano")
        self._credenciada = valor

    # ===== CONTRATO ABSTRATO =====
    def validar_publicacao(self):
        """
        Implementação do método abstrato de EntidadePublicadora.
        """
        if not self.credenciada:
            raise PermissionError("Instituição não credenciada não pode publicar cursos")
        return True

    # ===== JSON =====
    def to_dict(self):
        """Converte a entidade para um dicionário."""
        return {
            "id": self.id,
            "razao_social": self.razao_social,
            "nome_fantasia": self.nome_fantasia,
            "cnpj": self.cnpj,
            "registro_educacional": self.registro_educacional,
            "tipo": self.tipo,
            "modalidades": self.modalidades,
            "credenciada": self.credenciada
        }

    @staticmethod
    def from_dict(d):
        """Cria uma instância de InstituicaoEnsino a partir de um dicionário."""
        return InstituicaoEnsino(
            id_instituicao=d["id"],
            razao_social=d.get("razao_social", d.get("nome")), # Fallback para compatibilidade
            nome_fantasia=d.get("nome_fantasia", d.get("nome")),
            cnpj=d["cnpj"],
            registro_educacional=d["registro_educacional"],
            tipo=d["tipo"],
            modalidades=d.get("modalidades", ""),
            credenciada=d.get("credenciada", True)
        )

class AreaEnsino:
    """
    Representa uma Área de conhecimento ou ensino
    Utilizada para categorizar cursos e instituições.
    """
    def __init__(self, id_area, nome_area):
        self.id_area = id_area
        self.nome_area = nome_area
        

class InstituicaoAreaEnsino:
    """
    Entidade associativa que mapeia a relação N:N entre Instituição e Área de Ensino.
    Indica quais áreas de conhecimento uma instituição abrange.
    """
    def __init__(self, id_instituicao_area, id_instituicao, id_area):
        self.id_instituicao_area = id_instituicao_area
        self.id_instituicao = id_instituicao
        self.id_area = id_area