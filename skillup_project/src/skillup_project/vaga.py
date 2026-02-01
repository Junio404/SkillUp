from abc import ABC, abstractmethod

class Vaga(ABC):
    def __init__(self, id_vaga, titulo, descricao, area, modalidade):
        self.id = id_vaga
        self.titulo = titulo
        self.descricao = descricao
        self.area = area
        self.modalidade = modalidade  # Ex: Presencial, Remoto, Híbrido
        self.requisitos = []          

    @abstractmethod
    def calcular_custo_contratacao(self):
        """Método para cálculo de impostos/custos"""
        pass

    def adicionar_requisito(self, requisito):
        self.requisitos.append(requisito)

class VagaCLT(Vaga):
    def __init__(self, id_vaga, titulo, descricao, area, modalidade, salario_base):
        super().__init__(id_vaga, titulo, descricao, area, modalidade)
        self.salario_base = salario_base

    def calcular_custo_contratacao(self):
        
        return self.salario_base * 1.8 #simulaçao de acordo com a vida real

class VagaEstagio(Vaga):
    def __init__(self, id_vaga, titulo, descricao, area, modalidade, bolsa_auxilio, instituicao_conveniada):
        super().__init__(id_vaga, titulo, descricao, area, modalidade)
        self.bolsa_auxilio = bolsa_auxilio
        self.instituicao_conveniada = instituicao_conveniada

    def calcular_custo_contratacao(self):
        return self.bolsa_auxilio * 1.1 #simulaçao de acordo com a vida real