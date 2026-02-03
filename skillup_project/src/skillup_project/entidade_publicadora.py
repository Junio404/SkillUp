from abc import ABC, abstractmethod

class EntidadePublicadora(ABC):
    def __init__(self, id_entidade, nome, cnpj):
        self.id = id_entidade
        self.nome = nome
        self.cnpj = cnpj
