import re
from dataclasses import dataclass, field
from typing import List, Protocol, Tuple


# ==============================
# ABSTRAÇÕES (DIP)
# ==============================


class Validador(Protocol):
    def validar(self, valor) -> None:
        ...


# ==============================
# IMPLEMENTAÇÕES CONCRETAS
# ==============================

class IdValidador:
    def validar(self, valor: int) -> None:
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("ID deve ser inteiro positivo.")


class NomeValidador:
    def validar(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Nome inválido.")


class CpfValidador:
    def validar(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor) != 11 or not valor.isdigit():
            raise ValueError("CPF inválido.")


class EmailValidador:
    EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    def validar(self, valor: str) -> None:
        if not re.match(self.EMAIL_REGEX, valor):
            raise ValueError("Email inválido.")


class AreasValidador:
    def validar(self, valor: List[str]) -> None:
        if not isinstance(valor, list) or not valor:
            raise ValueError("Informe ao menos uma área.")

        for area in valor:
            if not isinstance(area, str) or not area.strip():
                raise ValueError("Área inválida.")


class NivelFormacaoValidador:
    def validar(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("Nível de formação inválido.")


# ==============================
# ENTIDADE DE DOMÍNIO
# ==============================


@dataclass
class Candidato:
    id: int
    nome: str
    _cpf: str = field(repr=False)
    email: str
    _areas_interesse: List[str] = field(default_factory=list, repr=False)
    nivel_formacao: str = ""
    curriculo: str | None = None

    # Dependências injetadas
    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    nome_validador: Validador = field(default_factory=NomeValidador, repr=False)
    cpf_validador: Validador = field(default_factory=CpfValidador, repr=False)
    email_validador: Validador = field(default_factory=EmailValidador, repr=False)
    areas_validador: Validador = field(default_factory=AreasValidador, repr=False)
    nivel_validador: Validador = field(default_factory=NivelFormacaoValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.nome_validador.validar(self.nome)
        self.cpf_validador.validar(self._cpf)
        self.email_validador.validar(self.email)
        self.areas_validador.validar(self._areas_interesse)
        self.nivel_validador.validar(self.nivel_formacao)

        # Proteção contra mutação externa
        self._areas_interesse = [a.strip() for a in self._areas_interesse]


    # ==============================
    # PROPRIEDADES
    # ==============================

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def areas_interesse(self) -> Tuple[str, ...]:
        return tuple(self._areas_interesse)


    # ==============================
    # REGRAS DE NEGÓCIO
    # ==============================

    def adicionar_area(self, area: str) -> None:
        area = area.strip()
        if not area:
            raise ValueError("Área inválida.")
        if area in self._areas_interesse:
            raise ValueError("Área já cadastrada.")
        self._areas_interesse.append(area)

    def remover_area(self, area: str) -> None:
        if area not in self._areas_interesse:
            raise ValueError("Área não encontrada.")
        if len(self._areas_interesse) <= 1:
            raise ValueError("Ao menos uma área é obrigatória.")
        self._areas_interesse.remove(area)


# ==============================
# MAPPER (Responsabilidade isolada)
# ==============================


class CandidatoMapper:

    @staticmethod
    def to_dict(candidato: Candidato) -> dict:
        return {
            "id": candidato.id,
            "nome": candidato.nome,
            "cpf": candidato.cpf,
            "email": candidato.email,
            "areas_interesse": list(candidato.areas_interesse),
            "nivel_formacao": candidato.nivel_formacao,
            "curriculo": candidato.curriculo
        }

    @staticmethod
    def from_dict(dados: dict) -> Candidato:
        return Candidato(
            id=dados["id"],
            nome=dados["nome"],
            _cpf=dados["cpf"],
            email=dados["email"],
            _areas_interesse=dados["areas_interesse"],
            nivel_formacao=dados["nivel_formacao"],
            curriculo=dados.get("curriculo")
        )
