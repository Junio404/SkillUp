from entidade_publicadora import EntidadePublicadora

class Empresa(EntidadePublicadora):
    def __init__(self, id_empresa, nome, cnpj, porte):
        super().__init__(id_empresa, nome, cnpj)
        self.porte = porte  # Ex: pequeno, medio, grande