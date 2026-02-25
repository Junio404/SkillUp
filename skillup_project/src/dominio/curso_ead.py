from skillup_project.src.dominio.curso import Curso

class CursoEAD(Curso):
    def __init__(self, id_curso, nome, carga_horaria, plataforma_url):
        super().__init__(id_curso, nome, carga_horaria)
        self.plataforma_url = plataforma_url

    def exibir_detalhes(self):
        return f"Curso Online: {self.nome} via {self.plataforma_url}"