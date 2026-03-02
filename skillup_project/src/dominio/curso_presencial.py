from dataclasses import dataclass, field
from datetime import date
from .curso_abs import Curso
from .vaga import Modalidade
from .validators import StrValidador, Validador


@dataclass
class CursoPresencial(Curso):
    localidade: str
    _texto_val: Validador = field(default_factory=StrValidador, repr=False)

    def __post_init__(self):
        if not self.localidade:
            raise ValueError("A localidade é obrigatória para cursos presenciais.")
        self._texto_val.validar(self.localidade)
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