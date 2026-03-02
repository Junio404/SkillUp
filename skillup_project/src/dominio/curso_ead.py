from dataclasses import dataclass, field
from datetime import date
from .curso_abs import Curso
from .vaga import Modalidade
from .validators import StrValidador, Validador


@dataclass
class CursoEAD(Curso):
    plataforma_url: str
    _texto_val: Validador = field(default_factory=StrValidador, repr=False)

    def __post_init__(self):
        if not self.plataforma_url:
            raise ValueError("A URL da plataforma é obrigatória para cursos EAD.")
        self._texto_val.validar(self.plataforma_url)
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