import json
import os

CAMINHO_ARQUIVO = os.path.join("data", "candidato.json")


class Candidato:
    def __init__(self, id: int, nome: str, cpf: str, email: str, area_interesse: str, nivel_formacao: str):
        self._id = id
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.area_interesse = area_interesse
        self.nivel_formacao = nivel_formacao

    # ===== PROPERTIES =====
    @property
    def id(self):
        return self._id

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor:
            raise ValueError("Nome não pode ser vazio")
        self._nome = valor

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, valor):
        if not valor or len(valor) != 11:
            raise ValueError("CPF inválido")
        self._cpf = valor

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, valor):
        if "@" not in valor:
            raise ValueError("Email inválido")
        self._email = valor

    @property
    def area_interesse(self):
        return self._area_interesse

    @area_interesse.setter
    def area_interesse(self, valor):
        self._area_interesse = valor

    @property
    def nivel_formacao(self):
        return self._nivel_formacao

    @nivel_formacao.setter
    def nivel_formacao(self, valor):
        self._nivel_formacao = valor

    # ===== JSON =====
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cpf": self.cpf,
            "email": self.email,
            "area_interesse": self.area_interesse,
            "nivel_formacao": self.nivel_formacao
        }

    @staticmethod
    def from_dict(d):
        return Candidato(
            id=d["id"],
            nome=d["nome"],
            cpf=d["cpf"],
            email=d["email"],
            area_interesse=d["area_interesse"],
            nivel_formacao=d["nivel_formacao"]
        )
