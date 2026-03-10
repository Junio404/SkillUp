from dataclasses import dataclass, field
from datetime import date
from .curso_abs import Curso
from .validators import StrValidador, UrlValidador, Validador


# ==============================
# ENTIDADE DE DOMÍNIO
# ==============================

@dataclass
class CursoEAD(Curso):
    plataforma_url: str = ""

    texto_validador: Validador = field(default_factory=StrValidador, repr=False)
    url_validador: Validador = field(default_factory=UrlValidador, repr=False)

    def __post_init__(self):
        from .vaga import Modalidade
        self.modalidade = Modalidade.REMOTO
        self.url_validador.validar(self.plataforma_url)
        super().__post_init__()

    def exibir_detalhes(self) -> str:
        status = "Ativo" if self.ativo else "Inativo"
        prazo = self.prazo_inscricao.strftime("%d/%m/%Y") if self.prazo_inscricao else "Indefinido"
        return (
            f"Curso EAD: {self.nome} ({self.area})\n"
            f"Carga: {self.carga_horaria}h | Modalidade: {self.modalidade.value}\n"
            f"Plataforma: {self.plataforma_url}\n"
            f"Status: {status} | Inscrições até: {prazo}"
        )

    def to_dict(self) -> dict:
        data = super().to_dict()
        data.update({"plataforma_url": self.plataforma_url, "tipo": "EAD"})
        return data


# ==============================
# MAPPER
# ==============================

class CursoEADMapper:

    @staticmethod
    def to_dict(curso: CursoEAD) -> dict:
        return curso.to_dict()

    @staticmethod
    def from_dict(d: dict) -> CursoEAD:
        from .vaga import Modalidade
        return CursoEAD(
            id=d["id"],
            id_instituicao=d["id_instituicao"],
            nome=d["nome"],
            area=d["area"],
            carga_horaria=d["carga_horaria"],
            modalidade=Modalidade.REMOTO,
            capacidade=d["capacidade"],
            prazo_inscricao=date.fromisoformat(d["prazo_inscricao"]) if d.get("prazo_inscricao") else None,
            ativo=d.get("ativo", True),
            plataforma_url=d.get("plataforma_url", ""),
        )