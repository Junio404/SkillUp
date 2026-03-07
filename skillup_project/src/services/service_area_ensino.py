from src.dominio.instituicao_ensino import AreaEnsino
from src.interfaces.interface_area_ensino import IAreaEnsinoRepositorio


class AreaEnsinoService:
    """Serviço de domínio para gerenciamento de áreas de ensino.
    Contém a lógica de negócio e validações relacionadas às áreas de ensino."""

    def __init__(self, repositorio: IAreaEnsinoRepositorio):
        self.repo = repositorio

    # ==========================================
    # CRUD
    # ==========================================

    def cadastrar(self, nome_area: str):
        """Cadastra uma nova área de ensino. Valida duplicidade por nome."""
        existente = self.repo.buscar_por_nome(nome_area)
        if existente:
            raise ValueError("Já existe área de ensino com este nome")

        todas = self.repo.listar_todas()
        novo_id = 1 if not todas else max(a.id_area for a in todas) + 1

        area = AreaEnsino(
            id_area=novo_id,
            nome_area=nome_area,
        )

        self.repo.salvar(area)
        return area

    def listar_todas(self):
        """Lista todas as áreas de ensino."""
        return self.repo.listar_todas()

    def buscar_por_id(self, id_area: int):
        """Busca uma área de ensino pelo ID. Lança ValueError se não encontrada."""
        area = self.repo.buscar_por_id(id_area)
        if not area:
            raise ValueError("Área de ensino não encontrada")
        return area

    def buscar_por_nome(self, nome: str):
        """Busca uma área de ensino pelo nome exato."""
        area = self.repo.buscar_por_nome(nome)
        if not area:
            raise ValueError("Área de ensino não encontrada")
        return area

    def buscar_por_nome_parcial(self, nome: str):
        """Busca áreas de ensino cujo nome contém a string fornecida."""
        return self.repo.buscar_por_nome_parcial(nome)

    def contar_total(self) -> int:
        """Retorna o total de áreas de ensino cadastradas."""
        return self.repo.contar_total()

    # ==========================================
    # AÇÕES DE NEGÓCIO
    # ==========================================

    def atualizar(self, id_area: int, novo_nome: str):
        """Atualiza o nome de uma área de ensino."""
        area = self.buscar_por_id(id_area)
        area.nome_area = novo_nome
        self.repo.atualizar(area)
        return area

    def remover(self, id_area: int):
        """Remove uma área de ensino pelo ID."""
        self.buscar_por_id(id_area)
        removido = self.repo.remover_por_id(id_area)
        if not removido:
            raise ValueError("Falha ao remover área de ensino")

    # ==========================================
    # FORMATAÇÃO
    # ==========================================

    def listar_formatado(self):
        return [str(a) for a in self.listar_todas()]

    def buscar_por_id_formatado(self, id_area: int):
        return str(self.buscar_por_id(id_area))
