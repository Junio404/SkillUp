from abc import ABC, abstractmethod

class Curso(ABC):
    def __init__(self, id_curso, nome, carga_horaria):
        self.id = id_curso
        self.nome = nome
        self.carga_horaria = carga_horaria
        self.competencias_ofertadas = [] 

    @abstractmethod
    def exibir_detalhes(self):
        pass

class CursoPresencial(Curso):
    def __init__(self, id_curso, nome, carga_horaria, endereco):
        super().__init__(id_curso, nome, carga_horaria)
        self.endereco = endereco

    def exibir_detalhes(self):
        return f"Curso Presencial:: {self.nome} em {self.endereco}"

class CursoEAD(Curso):
    def __init__(self, id_curso, nome, carga_horaria, plataforma_url):
        super().__init__(id_curso, nome, carga_horaria)
        self.plataforma_url = plataforma_url

    def exibir_detalhes(self):
        return f"Curso Online: {self.nome} via {self.plataforma_url}"