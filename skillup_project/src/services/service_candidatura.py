from src.dominio.candidatura import Candidatura, StatusCandidatura
from src.interfaces.interface_candidatura import ICandidaturaRepositorio


class CandidaturaService:
    """Serviço de domínio para gerenciamento de candidaturas.
    Contém a lógica de negócio e validações relacionadas às candidaturas."""

    def __init__(self, repositorio: ICandidaturaRepositorio):
        self.repo = repositorio

    # ==========================================
    # CRUD
    # ==========================================

    def cadastrar(self, id_vaga: int, id_candidato: int, status: str = "Enviado"):
        """Cadastra uma nova candidatura. Valida duplicidade (candidato + vaga)."""
        existentes = self.repo.listar_por_candidato(id_candidato)
        if any(c.id_vaga == id_vaga for c in existentes):
            raise ValueError("Candidato já possui candidatura para esta vaga")

        todas = self.repo.listar_todas()
        novo_id = 1 if not todas else max(c.id for c in todas) + 1

        candidatura = Candidatura(
            id=novo_id,
            id_vaga=id_vaga,
            id_candidato=id_candidato,
            status=StatusCandidatura(status),
        )

        self.repo.salvar(candidatura)
        return candidatura

    def listar_todas(self):
        """Lista todas as candidaturas."""
        return self.repo.listar_todas()

    def buscar_por_id(self, id_candidatura: int):
        """Busca uma candidatura pelo ID. Lança ValueError se não encontrada."""
        candidatura = self.repo.buscar_por_id(id_candidatura)
        if not candidatura:
            raise ValueError("Candidatura não encontrada")
        return candidatura

    def excluir(self, id_candidatura: int):
        """Exclui uma candidatura pelo ID."""
        self.buscar_por_id(id_candidatura)
        self.repo.excluir(id_candidatura)

    # ==========================================
    # LISTAGENS
    # ==========================================

    def listar_por_candidato(self, id_candidato: int):
        """Retorna todas as candidaturas de um candidato."""
        return self.repo.listar_por_candidato(id_candidato)

    def listar_por_vaga(self, id_vaga: int):
        """Retorna todas as candidaturas de uma vaga."""
        return self.repo.listar_por_vaga(id_vaga)

    def listar_por_status(self, status: str):
        """Retorna todas as candidaturas com um status específico."""
        return self.repo.listar_por_status(status)

    # ==========================================
    # CONTAGEM
    # ==========================================

    def contar_por_candidato(self, id_candidato: int) -> int:
        return self.repo.contar_por_candidato(id_candidato)

    def contar_por_vaga(self, id_vaga: int) -> int:
        return self.repo.contar_por_vaga(id_vaga)

    def contar_por_status(self, status: str) -> int:
        return self.repo.contar_por_status(status)

    # ==========================================
    # AÇÕES DE NEGÓCIO
    # ==========================================

    def atualizar_status(self, id_candidatura: int, novo_status: str) -> bool:
        """Atualiza o status de uma candidatura."""
        self.buscar_por_id(id_candidatura)
        return self.repo.atualizar_status(id_candidatura, novo_status)

    def aprovar(self, id_candidatura: int):
        """Aprova uma candidatura."""
        candidatura = self.buscar_por_id(id_candidatura)
        candidatura.aprovar()
        return self.repo.atualizar_status(id_candidatura, StatusCandidatura.ACEITO.value)

    def reprovar(self, id_candidatura: int):
        """Reprova uma candidatura."""
        candidatura = self.buscar_por_id(id_candidatura)
        candidatura.reprovar()
        return self.repo.atualizar_status(id_candidatura, StatusCandidatura.RECUSADO.value)

    def cancelar(self, id_candidatura: int):
        """Cancela uma candidatura (apenas se não finalizada)."""
        candidatura = self.buscar_por_id(id_candidatura)
        candidatura.cancelar()
        return self.repo.atualizar_status(id_candidatura, StatusCandidatura.CANCELADO.value)

    # ==========================================
    # FORMATAÇÃO
    # ==========================================

    def listar_formatado(self):
        return [str(c) for c in self.listar_todas()]

    def buscar_por_id_formatado(self, id_candidatura: int):
        return str(self.buscar_por_id(id_candidatura))
