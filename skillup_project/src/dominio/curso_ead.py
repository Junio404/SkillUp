from datetime import date
from .curso_abs import Curso
from .vaga import Modalidade

class CursoEAD(Curso):
    """
    Representa um curso na modalidade de Ensino a Distância (EAD).
    """
    def __init__(self, id_curso: int, nome: str, area: str, carga_horaria: int, 
                 capacidade: int, prazo_inscricao: date, plataforma_url: str):
        """
        Inicializa um novo curso EAD.
        
        :param id_curso: Identificador único do curso.
        :param nome: Nome do curso.
        :param area: Área do conhecimento.
        :param carga_horaria: Carga horária total em horas.
        :param capacidade: Número máximo de vagas.
        :param prazo_inscricao: Data limite para inscrição.
        :param plataforma_url: URL da plataforma onde o curso é disponibilizado.
        """
        if not plataforma_url:
            raise ValueError("A URL da plataforma é obrigatória para cursos EAD.")

        # Inicializa a classe base (Curso) com todos os argumentos
        super().__init__(
            id_curso=id_curso,
            nome=nome,
            area=area,
            carga_horaria=carga_horaria,
            modalidade=Modalidade.REMOTO, # Fixado como REMOTO para EAD
            capacidade=capacidade,
            prazo_inscricao=prazo_inscricao
        )
        
        self.plataforma_url = plataforma_url

    def exibir_detalhes(self):
        """Retorna os detalhes do curso formatados."""
        status = "Ativo" if self.ativo else "Inativo"
        prazo = self.prazo_inscricao.strftime('%d/%m/%Y') if self.prazo_inscricao else "Indefinido"
        
        return (f"Curso EAD: {self.nome} ({self.area})\n"
                f"Carga: {self.carga_horaria}h | Modalidade: {self.modalidade.value}\n"
                f"Plataforma: {self.plataforma_url}\n"
                f"Status: {status} | Inscrições até: {prazo}")

    def to_dict(self):
        """Serializa o curso para dicionário."""
        data = super().to_dict()
        data.update({
            "plataforma_url": self.plataforma_url,
            "tipo": "EAD"
        })
        return data