class Competencia:
    def __init__(self, id_comp, nome, descricao=None):
        self.id = id_comp
        self.nome = nome
        self.descricao = descricao

    def __str__(self):
        return f"Comp: {self.nome}"