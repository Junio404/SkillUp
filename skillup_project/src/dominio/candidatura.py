from datetime import datetime
from enum import Enum

class StatusCandidatura(Enum):
    ENVIADO = "Enviado"
    EM_ANALISE = "Em analise"
    ACEITO = "Aceito"
    RECUSADO = "Recusado"
    CANCELADO = "Cancelado"

class Candidatura:

    def __init__(
        self,
        id_candidatura: int,
        id_vaga: int,
        id_candidato: int,
        status: StatusCandidatura = StatusCandidatura.ENVIADO,
        data_candidatura: str = None
    ):

        self._validar_id(id_candidatura, "ID Candidatura")
        self._validar_id(id_vaga, "ID Vaga")
        self._validar_id(id_candidato, "ID Candidato")

        self._id_candidatura = id_candidatura
        self._id_vaga = id_vaga
        self._id_candidato = id_candidato
        
        # Define a data atual se nenhuma for passada
        if not data_candidatura:
            self._data_candidatura = datetime.now().date().isoformat()
        else:
            self._data_candidatura = data_candidatura

        # Garante que status seja do tipo Enum
        if isinstance(status, str):
            try:
                self._status = StatusCandidatura(status)
            except ValueError:
                self._status = StatusCandidatura.ENVIADO
        else:
            self._status = status

    # --------------------
    #     Validações
    # --------------------

    def _validar_id(self, valor, nome_campo):
        
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError(f"{nome_campo} deve ser um inteiro positivo.")

    # --------------------
    #     Properties
    # --------------------

    @property
    def id(self):
        
        return self._id_candidatura

    @property
    def id_vaga(self):
        
        return self._id_vaga

    @property
    def id_candidato(self):
        
        return self._id_candidato

    @property
    def data_candidatura(self):
        return self._data_candidatura

    @property
    def status(self):
        
        return self._status

    @status.setter
    def status(self, novo_status):
    
        if not isinstance(novo_status, StatusCandidatura):
            raise TypeError("O status deve ser do tipo StatusCandidatura.")
        self._status = novo_status

    # --------------------
    #     Métodos de Domínio
    # --------------------

    def aprovar(self):
        
        self.status = StatusCandidatura.ACEITO

    def reprovar(self):
        
        self.status = StatusCandidatura.RECUSADO

    def cancelar(self):
        
        if self.status in [StatusCandidatura.ACEITO, StatusCandidatura.RECUSADO]:
            raise ValueError("Não é possível cancelar uma candidatura já finalizada.")
        self.status = StatusCandidatura.CANCELADO

    def analisar(self):
        
        self.status = StatusCandidatura.EM_ANALISE

    # --------------------
    #     Serialização
    # --------------------

    def to_dict(self):
        return {
            "id_candidatura": self.id,
            "id_vaga": self.id_vaga,
            "id_candidato": self.id_candidato,
            "status": self.status.value,
            "data_candidatura": self.data_candidatura
        }

    @staticmethod
    def from_dict(d):
        
        return Candidatura(
            id_candidatura=d["id_candidatura"],
            id_vaga=d["id_vaga"],
            id_candidato=d["id_candidato"],
            status=StatusCandidatura(d.get("status", "Enviado")),
            data_candidatura=d.get("data_candidatura")
        )

    def __str__(self):
        return (
            f"Candidatura #{self.id}\n"
            f"Vaga ID: {self.id_vaga}\n"
            f"Candidato ID: {self.id_candidato}\n"
            f"Data: {self.data_candidatura}\n"
            f"Status: {self.status.value}\n"
            "-------------------------"
        )