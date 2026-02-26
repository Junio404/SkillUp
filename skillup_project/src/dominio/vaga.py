from abc import ABC, abstractmethod
from enum import Enum

class Modalidade(Enum):
    PRESENCIAL = "Presencial"
    REMOTO = "Remoto"
    HIBRIDO = "Híbrido"

class TipoVaga(Enum):
    EMPREGO = "Emprego"
    ESTAGIO = "Estágio"
    TRAINEE = "Trainee"

class Vaga(ABC):

    def __init__(self, id_vaga: int, titulo: str, descricao: str, area: str,
                modalidade: Modalidade, tipo: TipoVaga, prazo_inscricao: str = None):
        if not isinstance(id_vaga, int) or id_vaga <= 0:
            raise ValueError("ID da vaga deve ser inteiro positivo.")

        if not titulo or not descricao or not area:
            raise ValueError("Título, descrição e área são obrigatórios.")

        self.id_vaga = id_vaga
        self.titulo = titulo
        self.descricao = descricao
        self.area = area
        # Validação de Enum simplificada
        self.modalidade = modalidade
        self.tipo = tipo
        self.prazo_inscricao = prazo_inscricao
        self.requisitos = []
        self.ativa = True  # Controle de estado (publicada/pausada)

    # --------------------
    #     Métodos de Domínio
    # --------------------
    @abstractmethod
    def calcular_custo_contratacao(self):
        
        pass

    def adicionar_requisito(self, requisito: str):
    
        if not requisito:
            raise ValueError("Requisito não pode ser vazio.")
        self.requisitos.append(requisito)

    def pausar(self):
        
        self.ativa = False

    def publicar(self):
        self.ativa = True

    def editar(self, titulo: str = None, descricao: str = None):
        if titulo: self.titulo = titulo
        if descricao: self.descricao = descricao

    # --------------------
    #     Serialização
    # --------------------
    def to_dict(self):
        return {
            "id": self.id_vaga,
            "titulo": self.titulo,
            "descricao": self.descricao,
            "area": self.area,
            "modalidade": self.modalidade.value if hasattr(self.modalidade, 'value') else self.modalidade,
            "tipo": self.tipo.value if hasattr(self.tipo, 'value') else self.tipo,
            "requisitos": self.requisitos,
            "ativa": self.ativa,
            "prazo_inscricao": self.prazo_inscricao
        }

class VagaCLT(Vaga):

    def __init__(self, id_vaga, titulo, descricao, area, modalidade, salario_base: float):
        super().__init__(id_vaga, titulo, descricao, area, modalidade, TipoVaga.EMPREGO)
        if salario_base <= 0:
            raise ValueError("Salário base deve ser positivo")
        self.salario_base = salario_base

    def calcular_custo_contratacao(self):
        return self.salario_base * 1.8

    def to_dict(self):
        data = super().to_dict()
        data["salario_base"] = self.salario_base
        return data

class VagaEstagio(Vaga):

    def __init__(self, id_vaga, titulo, descricao, area, modalidade, bolsa_auxilio: float, instituicao_conveniada: str):
        super().__init__(id_vaga, titulo, descricao, area, modalidade, TipoVaga.ESTAGIO)
        if bolsa_auxilio <= 0:
            raise ValueError("Bolsa auxílio deve ser positiva")
        self.bolsa_auxilio = bolsa_auxilio
        self.instituicao_conveniada = instituicao_conveniada

    def calcular_custo_contratacao(self):
        return self.bolsa_auxilio * 1.1

    def to_dict(self):
        data = super().to_dict()
        data["bolsa_auxilio"] = self.bolsa_auxilio
        data["instituicao_conveniada"] = self.instituicao_conveniada
        return data