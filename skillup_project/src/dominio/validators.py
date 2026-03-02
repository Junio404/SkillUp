import re
from typing import List, Protocol


class Validador(Protocol):
    def validar(self, valor) -> None:
        ...


class IdValidador:
    def validar(self, valor: int) -> None:
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("ID deve ser inteiro positivo.")


class StrValidador:
    """Valida strings não vazias."""

    def validar(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Texto inválido.")


class CpfValidador:
    def validar(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor) != 11 or not valor.isdigit():
            raise ValueError("CPF inválido.")


class CnpjValidador:
    def validar(self, valor: str) -> None:
        # Supondo formato apenas dígitos (14). Ajuste se usar máscara.
        if not isinstance(valor, str) or len(valor) != 14 or not valor.isdigit():
            raise ValueError("CNPJ inválido.")


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


class PorteValidador:
    def validar(self, valor: str) -> None:
        if valor not in ["pequeno", "medio", "grande"]:
            raise ValueError("Porte deve ser: pequeno, medio ou grande.")
