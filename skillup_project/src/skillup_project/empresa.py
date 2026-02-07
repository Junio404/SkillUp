from entidade_publicadora import EntidadePublicadora

class Empresa(EntidadePublicadora):
    def __init__(self, id_empresa, nome, cnpj, porte):
        super().__init__(id_empresa, nome, cnpj)
        self.porte = porte  # Ex: pequeno, medio, grande
    
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