from entidade_publicadora import EntidadePublicadora

class InstituicaoEnsino(EntidadePublicadora):
    def __init__(self, id_instituicao, nome, cnpj, credenciada):
        super().__init__(id_instituicao, nome, cnpj)
        self.credenciada = credenciada 