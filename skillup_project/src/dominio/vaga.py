from abc import ABC, abstractmethod
from enum import Enum

class Modalidade(Enum):
    """Enumeração para as modalidades de trabalho de uma vaga."""
    PRESENCIAL = "Presencial"
    REMOTO = "Remoto"
    HIBRIDO = "Híbrido"

class TipoVaga(Enum):
    """Enumeração para os tipos de contrato de uma vaga."""
    EMPREGO = "Emprego"
    ESTAGIO = "Estágio"
    TRAINEE = "Trainee"

class Vaga(ABC):
    """
    Classe abstrata que representa uma Vaga no sistema.
    Define a estrutura base e comportamentos comuns para todos os tipos de vagas.
    """

    def __init__(self, id_vaga: int, titulo: str, descricao: str, area: str,
                modalidade: Modalidade, tipo: TipoVaga, prazo_inscricao: str = None):
        """
        Inicializa uma nova Vaga.
        param id_vaga: Identificador único da vaga (inteiro positivo).
        param titulo: Título da vaga.
        param descricao: Descrição detalhada das atividades.
        param area: Área de atuação.
        param modalidade: Modalidade de trabalho
        param tipo: Tipo de contrato
        param prazo_inscricao: Data limite para inscrição
        """
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
        """
        Método abstrato para cálculo de custos de contratação.
        Deve ser implementado pelas subclasses (VagaCLT, VagaEstagio).
        """
        pass

    def adicionar_requisito(self, requisito: str):
        """
        Adiciona um requisito à lista de requisitos da vaga.
        param requisito: Descrição do requisito.
        """

        if not requisito:
            raise ValueError("Requisito não pode ser vazio.")
        self.requisitos.append(requisito)

    def pausar(self):
        """Pausa a vaga, impedindo novas candidaturas."""
        self.ativa = False

    def publicar(self):
        """Publica a vaga, permitindo novas candidaturas."""
        self.ativa = True

    def editar(self, titulo: str = None, descricao: str = None):
        """Edita os dados da vaga."""
        if titulo: self.titulo = titulo
        if descricao: self.descricao = descricao

    # --------------------
    #     Serialização
    # --------------------
    def to_dict(self):
        """Converte a vaga para um dicionário json."""
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
    """Representa uma vaga de emprego formal."""
    def __init__(self, id_vaga, titulo, descricao, area, modalidade, salario_base: float):
        super().__init__(id_vaga, titulo, descricao, area, modalidade, TipoVaga.EMPREGO)
        if salario_base <= 0:
            raise ValueError("Salário base deve ser positivo")
        self.salario_base = salario_base

    def calcular_custo_contratacao(self):
        """Calcula custo de contratação com base no salário base."""
        return self.salario_base * 1.8

    def to_dict(self):
        data = super().to_dict()
        data["salario_base"] = self.salario_base
        return data

class VagaEstagio(Vaga):
    """Representa uma vaga de estágio."""
    def __init__(self, id_vaga, titulo, descricao, area, modalidade, bolsa_auxilio: float, instituicao_conveniada: str):
        super().__init__(id_vaga, titulo, descricao, area, modalidade, TipoVaga.ESTAGIO)
        if bolsa_auxilio <= 0:
            raise ValueError("Bolsa auxílio deve ser positiva")
        self.bolsa_auxilio = bolsa_auxilio
        self.instituicao_conveniada = instituicao_conveniada

    def calcular_custo_contratacao(self):
        """Calcula custo: Bolsa * 1.1"""
        return self.bolsa_auxilio * 1.1

    def to_dict(self):
        data = super().to_dict()
        data["bolsa_auxilio"] = self.bolsa_auxilio
        data["instituicao_conveniada"] = self.instituicao_conveniada
        return data