from enum import Enum

class Nivel(Enum):
    """Enumeração para os níveis de competência."""
    BAIXA = "Baixa"
    MEDIA = "Media"
    ALTA = "Alta"

class Competencia:
    """
    Entidade base representando uma habilidade ou conhecimento.
    """
    def __init__(self, id_competencia: int, nome: str, descricao: str = None):
        """
        Cria uma nova competência.
        param id_competencia: Identificador único.
        param nome: Nome da competência (ex: Python, Gestão).
        param descricao: Detalhamento do que é esperado.
        """
        self._validar_id(id_competencia)
        self._validar_texto(nome, "Nome")
        
        self._id = id_competencia
        self._nome = nome
        self._descricao = descricao

    # --------------------
    #     Validações
    # --------------------
    def _validar_id(self, valor):
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("ID deve ser um inteiro positivo.")

    def _validar_texto(self, valor, campo):
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{campo} inválido.")

    # --------------------
    #     Properties
    # --------------------
    @property
    def id(self): return self._id

    @property
    def nome(self): return self._nome

    @nome.setter
    def nome(self, valor):
        self._validar_texto(valor, "Nome")
        self._nome = valor

    @property
    def descricao(self): return self._descricao

    @descricao.setter
    def descricao(self, valor):
        if valor is not None and not isinstance(valor, str):
            raise TypeError("Descrição deve ser texto.")
        self._descricao = valor

    # --------------------
    #     Serialização
    # --------------------
    def to_dict(self):
        """Converte a competência para dicionário."""
        return {
            "id": self.id,
            "nome": self.nome,
            "descricao": self.descricao
        }
    
    @staticmethod
    def from_dict(d):
        return Competencia(d["id"], d["nome"], d.get("descricao"))

    def __str__(self):
        return f"{self.nome} ({self.descricao or 'Sem descrição'})"


class CompetenciaNivelada(Competencia):
    """Classe base para competências que possuem um nível associado."""
    def __init__(self, id_competencia: int, nome: str, nivel: Nivel, descricao: str = None):
        super().__init__(id_competencia, nome, descricao)
        self.nivel = nivel # Usa o setter para validar

    @property
    def nivel(self):
        return self._nivel
    
    @nivel.setter
    def nivel(self, valor):
        if isinstance(valor, str):
            try:
                self._nivel = Nivel(valor)
            except ValueError:
                raise ValueError(f"Nível inválido: {valor}")
        elif isinstance(valor, Nivel):
            self._nivel = valor
        else:
            raise TypeError("Nível deve ser do tipo Enum Nivel.")

    def to_dict(self):
        data = super().to_dict()
        data["nivel"] = self.nivel.value
        return data

class CompetenciaCandidato(CompetenciaNivelada):
    """Competência possuída por um candidato."""
    pass

class CursoCompetencia(CompetenciaNivelada):
    """Competência exigida por um curso ou vaga."""
    pass