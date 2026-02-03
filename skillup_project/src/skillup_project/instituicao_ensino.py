from entidade_publicadora import EntidadePublicadora

class InstituicaoEnsino(EntidadePublicadora):
    def __init__(self, id_instituicao, nome, cnpj, credenciada):
        super().__init__(id_instituicao, nome, cnpj)
        self.credenciada = credenciada 
        
class AreaEnsino:
    def __init__(self, id_area, nome_area):
        self.id_area = id_area
        self.nome_area = nome_area
        

class InstituicaoAreaEnsino:
    def __init__(self, id_instituicao_area, id_instituicao, id_area):
        self.id_instituicao_area = id_instituicao_area
        self.id_instituicao = id_instituicao
        self.id_area = id_area