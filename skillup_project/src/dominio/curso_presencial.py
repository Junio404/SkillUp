from skillup_project.src.dominio.curso import Curso 

class CursoPresencial(Curso):
    def __init__(self, id_curso, nome, carga_horaria, endereco):
        super().__init__(id_curso, nome, carga_horaria)
        self.endereco = endereco

    def exibir_detalhes(self):
        return f"Curso Presencial:: {self.nome} em {self.endereco}"