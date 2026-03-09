from dataclasses import dataclass, field
from datetime import date
from .curso_abs import Curso
from .validators import StrValidador, LocalidadeValidador, Validador


# ==============================
# ENTIDADE DE DOMÍNIO
# ==============================

@dataclass
class CursoPresencial(Curso):
    localidade: str = ""

    texto_validador: Validador = field(default_factory=StrValidador, repr=False)
    localidade_validador: Validador = field(default_factory=LocalidadeValidador, repr=False)

    def __post_init__(self):
        from .vaga import Modalidade
        self.modalidade = Modalidade.PRESENCIAL
        self.localidade_validador.validar(self.localidade)
        super().__post_init__()

    def exibir_detalhes(self) -> str:
        status = "Ativo" if self.ativo else "Inativo"
        prazo = self.prazo_inscricao.strftime("%d/%m/%Y") if self.prazo_inscricao else "Indefinido"
        return (
            f"Curso Presencial: {self.nome} ({self.area})\n"
            f"Carga: {self.carga_horaria}h | Local: {self.localidade}\n"
            f"Status: {status} | Inscrições até: {prazo}"
        )

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"localidade": self.localidade, "tipo": "PRESENCIAL"})
        return data


# ==============================
# MAPPER
# ==============================

class CursoPresencialMapper:

    @staticmethod
    def to_dict(curso: CursoPresencial) -> dict:
        return curso.to_dict()

    @staticmethod
    def from_dict(d: dict) -> CursoPresencial:
        from .vaga import Modalidade
        return CursoPresencial(
            id=d["id"],
            nome=d["nome"],
            area=d["area"],
            carga_horaria=d["carga_horaria"],
            modalidade=Modalidade.PRESENCIAL,
            capacidade=d["capacidade"],
            prazo_inscricao=date.fromisoformat(d["prazo_inscricao"]) if d.get("prazo_inscricao") else None,
            ativo=d.get("ativo", True),
            localidade=d.get("localidade", ""),
        )