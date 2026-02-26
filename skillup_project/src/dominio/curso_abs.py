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

