import re
from typing import List, Protocol
from enum import Enum
from datetime import date

class Validador(Protocol):
    def validar(self, valor) -> None:
        ...


# ==============================
# VALIDATORS GENÉRICOS
# ==============================

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


class BooleanValidador:
    """Valida valores booleanos."""
    
    def validar(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise TypeError("Valor deve ser booleano.")


# ==============================
# VALIDATORS ESPECÍFICOS DE DOMÍNIO
# ==============================

# --- Candidatura ---
class StatusCandidaturaValidador:
    def validar(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("Status deve ser string.")
        from .candidatura import StatusCandidatura
        status_values = [s.value for s in StatusCandidatura]
        if valor not in status_values:
            raise ValueError(f"Status inválido. Use: {', '.join(status_values)}")


class DataValidador:
    def validar(self, valor: str) -> None:
        if valor is not None:
            if not isinstance(valor, str):
                raise TypeError("Data deve ser string no formato ISO.")


# --- Competência ---
class NivelValidador:
    def validar(self, valor) -> None:
        from .competencia import Nivel
        if isinstance(valor, str):
            niveis_validos = [n.name for n in Nivel]
            if valor.upper() not in niveis_validos:
                raise ValueError(f"Nível inválido. Use: {', '.join(niveis_validos)}")
        elif isinstance(valor, Enum):
            pass
        else:
            raise TypeError("Nível deve ser string ou Nivel enum.")


# --- Competência Candidato ---
class NivelAtualizavelValidador:
    """Valida níveis de competência do candidato."""
    
    _valid_levels: dict = {
        "iniciante": 0,
        "intermediario": 1,
        "avancado": 2,
    }

    def validar(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("Nível deve ser string.")
        valor_lower = valor.lower()
        if valor_lower not in self._valid_levels:
            raise ValueError(f"Nível inválido. Use: {', '.join(self._valid_levels.keys())}")


# --- Curso Competência ---
class CursoNivelValidador:
    """Valida níveis de competência do curso."""
    
    def __init__(self):
        from .competencia import Nivel
        self._valid_levels = {nivel.name: nivel.value for nivel in Nivel}

    def validar(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("Nível deve ser string.")
        valor_upper = valor.upper()
        if valor_upper not in self._valid_levels:
            raise ValueError(f"Nível inválido. Use: {', '.join(self._valid_levels.keys())}")


# --- Inscrição Curso ---
class DataInscricaoValidador:
    def validar(self, valor) -> None:
        from datetime import date
        if not isinstance(valor, date):
            raise TypeError("Data de inscrição deve ser do tipo date.")


class StatusInscricaoValidador:
    def validar(self, valor) -> None:
        from .inscricao_curso import StatusInscricao
        if not isinstance(valor, StatusInscricao):
            raise TypeError("Status deve ser do tipo StatusInscricao.")


# --- Requisitos Vaga ---
class NivelMinimoValidador:
    """Valida níveis mínimos de competência para a vaga."""
    
    def __init__(self):
        from .competencia import Nivel
        self._valid_levels = {nivel.name: nivel.value for nivel in Nivel}

    def validar(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("Nível mínimo deve ser string.")
        valor_upper = valor.upper()
        if valor_upper not in self._valid_levels:
            raise ValueError(f"Nível inválido. Use: {', '.join(self._valid_levels.keys())}")


# --- Vaga ---
class ModalidadeValidador:
    """Valida modalidade de vaga."""
    def validar(self, valor) -> None:
        from .vaga import Modalidade
        if not isinstance(valor, Modalidade):
            raise TypeError("Modalidade deve ser do tipo Modalidade enum.")


class TipoVagaValidador:
    def validar(self, valor) -> None:
        from .vaga import TipoVaga
        if not isinstance(valor, TipoVaga):
            raise TypeError("Tipo de vaga deve ser do tipo TipoVaga enum.")


class RequisitosValidador:
    def validar(self, valor: List[str]) -> None:
        if not isinstance(valor, list):
            raise TypeError("Requisitos devem ser uma lista.")
        for req in valor:
            if not isinstance(req, str) or not req.strip():
                raise ValueError("Cada requisito deve ser uma string não vazia.")


class SalarioValidador:
    def validar(self, valor: float) -> None:
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValueError("Salário deve ser um número positivo.")


# --- Curso ---
class CargaHorariaValidador:
    """Valida carga horária de cursos."""
    
    def validar(self, valor: int) -> None:
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("Carga horária deve ser um inteiro positivo.")


class CapacidadeValidador:
    """Valida capacidade de alunos nos cursos."""
    
    def validar(self, valor: int) -> None:
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("Capacidade deve ser um inteiro positivo.")


class ModalidadeCursoValidador:
    """Valida modalidade de course."""
    
    def validar(self, valor) -> None:
        from .vaga import Modalidade
        if not isinstance(valor, Modalidade):
            raise TypeError("Modalidade deve ser do tipo Modalidade enum.")


# --- Curso EAD ---
class UrlValidador:
    """Valida URLs de plataforma EAD."""
    
    def validar(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("URL da plataforma é obrigatória para cursos EAD.")


# --- Curso Presencial ---
class LocalidadeValidador:
    """Valida localidade de cursos presenciais."""
    
    def validar(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("A localidade é obrigatória para cursos presenciais.")


# --- Instituição de Ensino ---
class CredenciadoValidador:
    """Valida status de credenciamento."""
    
    def validar(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise TypeError("Credenciada deve ser booleano.")


class ModalidadesValidador:
    """Valida lista de modalidades."""
    
    def validar(self, valor: List[str]) -> None:
        if not isinstance(valor, list):
            raise TypeError("Modalidades deve ser uma lista.")
        for modalidade in valor:
            if not isinstance(modalidade, str) or not modalidade.strip():
                raise ValueError("Cada modalidade deve ser uma string não vazia.")


# --- Prazo ---
class PrazoValidador:
    """Valida prazos em formato ISO ou None."""
    
    def validar(self, valor: str | None) -> None:
        if valor is not None and not isinstance(valor, str):
            raise TypeError("Prazo deve ser string no formato ISO ou None.")
        if valor < date.today():
            raise ValueError("Prazo de inscrição não pode ser no passado.")


# --- Ativo ---
class AtivoValidador:
    """Valida status ativo (booleano)."""
    
    def validar(self, valor: bool) -> None:
        if not isinstance(valor, bool):
            raise TypeError("Ativo deve ser booleano.")
