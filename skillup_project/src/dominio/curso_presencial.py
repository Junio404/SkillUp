from datetime import date
from .curso_abs import Curso
from .vaga import Modalidade

class CursoPresencial(Curso):
    """
    Representa um curso na modalidade Presencial.
    """
    def __init__(self, id_curso: int, nome: str, area: str, carga_horaria: int, 
                capacidade: int, prazo_inscricao: date, localidade: str):
        """
        Inicializa um novo curso presencial.
        
        id_curso: Identificador único.
        nome: Nome do curso.
        area: Área do conhecimento.
        carga_horaria: Carga horária em horas.
        capacidade: Número máximo de vagas.
        prazo_inscricao: Data limite para inscrição.
        localidade: Endereço, cidade ou sala onde o curso ocorre.
        """
        if not localidade:
            raise ValueError("A localidade é obrigatória para cursos presenciais.")

        # Inicializa a classe base (Curso) com todos os argumentos
        super().__init__(
            id_curso=id_curso,
            nome=nome,
            area=area,
            carga_horaria=carga_horaria,
            modalidade=Modalidade.PRESENCIAL,
            capacidade=capacidade,
            prazo_inscricao=prazo_inscricao
        )

        self.localidade = localidade

    def exibir_detalhes(self):
        """Retorna os detalhes formatados."""
        status = "Ativo" if self.ativo else "Inativo"
        prazo = self.prazo_inscricao.strftime('%d/%m/%Y') if self.prazo_inscricao else "Indefinido"
        
        return (f"Curso Presencial: {self.nome} ({self.area})\n"
                f"Carga: {self.carga_horaria}h | Local: {self.localidade}\n"
                f"Status: {status} | Inscrições até: {prazo}")

    def to_dict(self):
        """Serializa o curso para dicionário."""
        data = super().to_dict()
        data.update({
            "localidade": self.localidade,
            "tipo": "PRESENCIAL"
        })
        return data