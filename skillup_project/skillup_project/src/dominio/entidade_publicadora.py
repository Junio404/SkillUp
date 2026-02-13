from abc import ABC, abstractmethod

class EntidadePublicadora(ABC):
    def __init__(self, id_entidade: int, nome: str, cnpj: str):
        self._id = id_entidade
        self.nome = nome
        self.cnpj = cnpj

    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor:
            raise ValueError("Nome é obrigatório")
        self._nome = valor

    @property
    def cnpj(self):
        return self._cnpj

    @cnpj.setter
    def cnpj(self, valor):
        if not valor or len(valor) != 14:
            raise ValueError("CNPJ inválido")
        self._cnpj = valor

    @abstractmethod
    def validar_publicacao(self):
        pass
