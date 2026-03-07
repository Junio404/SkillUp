from src.dominio.competencia import Competencia
from src.interfaces.interface_competencia import ICompetenciaRepositorio


class CompetenciaService:
    """Serviço de domínio para gerenciamento de competências.
    Contém a lógica de negócio e validações relacionadas às competências."""

    def __init__(self, repositorio: ICompetenciaRepositorio):
        self.repo = repositorio

    # ==========================================
    # CRUD
    # ==========================================

    def cadastrar(self, nome: str, descricao: str = None):
        """Cadastra uma nova competência. Valida duplicidade por nome."""
        existente = self.repo.buscar_por_nome(nome)
        if existente:
            raise ValueError("Já existe competência com este nome")

        todos = self.repo.listar_todos()
        novo_id = 1 if not todos else max(c.id for c in todos) + 1

        competencia = Competencia(
            id=novo_id,
            nome=nome,
            descricao=descricao,
        )

        self.repo.salvar(competencia)
        return competencia

    def listar_todos(self):
        """Lista todas as competências."""
        return self.repo.listar_todos()

    def buscar_por_id(self, id_competencia: int):
        """Busca uma competência pelo ID. Lança ValueError se não encontrada."""
        competencia = self.repo.buscar_por_id(id_competencia)
        if not competencia:
            raise ValueError("Competência não encontrada")
        return competencia

    def buscar_por_nome(self, nome: str):
        """Busca uma competência pelo nome exato."""
        competencia = self.repo.buscar_por_nome(nome)
        if not competencia:
            raise ValueError("Competência não encontrada")
        return competencia

    def buscar_por_nome_parcial(self, nome: str):
        """Busca competências cujo nome contém a string fornecida."""
        return self.repo.buscar_por_nome_parcial(nome)

    def buscar_por_filtros(self, **filtros):
        """Busca competências com filtros dinâmicos."""
        return self.repo.buscar_por_filtros(**filtros)

    def atualizar(self, id_competencia: int, campo: str, novo_valor):
        """Atualiza um campo específico de uma competência."""
        competencia = self.buscar_por_id(id_competencia)
        if not hasattr(competencia, campo):
            raise AttributeError(f"O campo '{campo}' não existe em Competencia")
        setattr(competencia, campo, novo_valor)
        self.repo.atualizar(competencia)
        return competencia

    def remover(self, id_competencia: int):
        """Remove uma competência pelo ID."""
        self.buscar_por_id(id_competencia)
        removido = self.repo.remover_por_id(id_competencia)
        if not removido:
            raise ValueError("Falha ao remover competência")

    def contar_total(self) -> int:
        """Retorna o total de competências cadastradas."""
        return self.repo.contar_total()

    # ==========================================
    # FORMATAÇÃO
    # ==========================================

    def listar_formatado(self):
        return [str(c) for c in self.listar_todos()]

    def buscar_por_id_formatado(self, id_competencia: int):
        return str(self.buscar_por_id(id_competencia))
