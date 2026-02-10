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


# ========= FUNÇÕES DE PERSISTÊNCIA =========

def _carregar_dados():
    if not os.path.exists(CAMINHO_ARQUIVO):
        return []

    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
        return json.load(f)


def _salvar_dados(lista):
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
        json.dump(lista, f, indent=4, ensure_ascii=False)


def _proximo_id():
    dados = _carregar_dados()
    if not dados:
        return 1
    return max(item["id"] for item in dados) + 1


def cadastrar_candidato(nome, cpf, email, area_interesse, nivel_formacao):
    dados = _carregar_dados()

    # Regra de negócio: CPF único
    if any(c["cpf"] == cpf for c in dados):
        raise ValueError("Já existe candidato com este CPF")

    novo_id = _proximo_id()
    candidato = Candidato(novo_id, nome, cpf, email, area_interesse, nivel_formacao)

    dados.append(candidato.to_dict())
    _salvar_dados(dados)

    return candidato


def listar_candidatos():
    dados = _carregar_dados()
    return [Candidato.from_dict(d) for d in dados]
