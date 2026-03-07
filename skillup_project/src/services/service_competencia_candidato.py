from src.dominio.competencia_candidato import CompetenciaCandidato
from src.interfaces.interface_competencia_candidato import ICompetenciaCandidatoRepositorio


class CompetenciaCandidatoService:
    """Serviço de domínio para gerenciamento de competências de candidatos.
    Contém a lógica de negócio e validações relacionadas às competências dos candidatos."""

    def __init__(self, repositorio: ICompetenciaCandidatoRepositorio):
        self.repo = repositorio

    # ==========================================
    # CRUD
    # ==========================================

    def cadastrar(self, id_candidato: int, id_competencia: int, nivel_atual: str):
        """Cadastra uma nova competência para um candidato. Valida duplicidade."""
        existente = self.repo.buscar_por_candidato_e_competencia(id_candidato, id_competencia)
        if existente:
            raise ValueError("Candidato já possui esta competência cadastrada")

        todas = self.repo.listar_todas()
        novo_id = 1 if not todas else max(c.id for c in todas) + 1

        comp_candidato = CompetenciaCandidato(
            id=novo_id,
            id_candidato=id_candidato,
            id_competencia=id_competencia,
            nivel_atual=nivel_atual,
        )

        self.repo.salvar(comp_candidato)
        return comp_candidato

    def listar_todas(self):
        """Lista todas as competências de candidatos."""
        return self.repo.listar_todas()

    def buscar_por_id(self, id_competencia_candidato: int):
        """Busca uma competência do candidato pelo ID. Lança ValueError se não encontrada."""
        comp = self.repo.buscar_por_id(id_competencia_candidato)
        if not comp:
            raise ValueError("CompetenciaCandidato não encontrada")
        return comp

    # ==========================================
    # LISTAGENS
    # ==========================================

    def listar_por_candidato(self, id_candidato: int):
        """Retorna todas as competências de um candidato."""
        return self.repo.listar_por_candidato(id_candidato)

    def listar_por_competencia(self, id_competencia: int):
        """Retorna todos os candidatos que possuem uma competência."""
        return self.repo.listar_por_competencia(id_competencia)

    def listar_por_nivel(self, nivel: str):
        """Retorna todas as competências de candidatos com um nível específico."""
        return self.repo.listar_por_nivel(nivel)

    def buscar_por_candidato_e_competencia(self, id_candidato: int, id_competencia: int):
        """Busca a competência de um candidato específico."""
        return self.repo.buscar_por_candidato_e_competencia(id_candidato, id_competencia)

    # ==========================================
    # AÇÕES DE NEGÓCIO
    # ==========================================

    def atualizar_nivel(self, id_competencia_candidato: int, novo_nivel: str):
        """Atualiza o nível de uma competência do candidato."""
        comp = self.buscar_por_id(id_competencia_candidato)
        comp.atualizar_nivel(novo_nivel)
        self.repo.atualizar(comp)
        return comp

    def remover(self, id_competencia_candidato: int):
        """Remove uma competência do candidato pelo ID."""
        self.buscar_por_id(id_competencia_candidato)
        removido = self.repo.remover_por_id(id_competencia_candidato)
        if not removido:
            raise ValueError("Falha ao remover competência do candidato")

    def remover_por_candidato(self, id_candidato: int):
        """Remove todas as competências de um candidato."""
        return self.repo.remover_por_candidato(id_candidato)

    # ==========================================
    # FORMATAÇÃO
    # ==========================================

    def listar_formatado(self):
        return [str(c) for c in self.listar_todas()]

    def buscar_por_id_formatado(self, id_competencia_candidato: int):
        return str(self.buscar_por_id(id_competencia_candidato))
