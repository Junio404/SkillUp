from src.dominio.instituicao_ensino import InstituicaoAreaEnsino
from src.interfaces.interface_instituicao_area_ensino import IInstituicaoAreaEnsinoRepositorio


class InstituicaoAreaEnsinoService:
    """Serviço de domínio para gerenciamento de relações instituição-área de ensino.
    Contém a lógica de negócio e validações relacionadas às áreas oferecidas por instituições."""

    def __init__(self, repositorio: IInstituicaoAreaEnsinoRepositorio):
        self.repo = repositorio

    # ==========================================
    # CRUD
    # ==========================================

    def cadastrar(self, id_instituicao: int, id_area: int):
        """Cadastra uma nova relação instituição-área. Valida duplicidade."""
        existente = self.repo.buscar_por_instituicao_e_area(id_instituicao, id_area)
        if existente:
            raise ValueError("Instituição já possui esta área cadastrada")

        todas = self.repo.listar_todas()
        novo_id = 1 if not todas else max(ia.id_instituicao_area for ia in todas) + 1

        inst_area = InstituicaoAreaEnsino(
            id_instituicao_area=novo_id,
            id_instituicao=id_instituicao,
            id_area=id_area,
        )

        self.repo.salvar(inst_area)
        return inst_area

    def listar_todas(self):
        """Lista todas as relações instituição-área."""
        return self.repo.listar_todas()

    def buscar_por_id(self, id_instituicao_area: int):
        """Busca uma relação pelo ID. Lança ValueError se não encontrada."""
        rel = self.repo.buscar_por_id(id_instituicao_area)
        if not rel:
            raise ValueError("InstituicaoAreaEnsino não encontrada")
        return rel

    # ==========================================
    # LISTAGENS
    # ==========================================

    def listar_por_instituicao(self, id_instituicao: int):
        """Retorna todas as áreas de uma instituição."""
        return self.repo.listar_por_instituicao(id_instituicao)

    def listar_por_area(self, id_area: int):
        """Retorna todas as instituições que oferecem uma área."""
        return self.repo.listar_por_area(id_area)

    def buscar_por_instituicao_e_area(self, id_instituicao: int, id_area: int):
        """Busca uma relação específica entre instituição e área."""
        return self.repo.buscar_por_instituicao_e_area(id_instituicao, id_area)

    # ==========================================
    # CONTAGEM
    # ==========================================

    def contar_areas_por_instituicao(self, id_instituicao: int) -> int:
        return self.repo.contar_areas_por_instituicao(id_instituicao)

    def contar_instituicoes_por_area(self, id_area: int) -> int:
        return self.repo.contar_instituicoes_por_area(id_area)

    # ==========================================
    # AÇÕES DE NEGÓCIO
    # ==========================================

    def atualizar(self, id_instituicao_area: int, id_area_nova: int):
        """Atualiza a área de uma relação instituição-área."""
        rel = self.buscar_por_id(id_instituicao_area)
        rel.id_area = id_area_nova
        self.repo.atualizar(rel)
        return rel

    def remover(self, id_instituicao_area: int):
        """Remove uma relação instituição-área pelo ID."""
        self.buscar_por_id(id_instituicao_area)
        removido = self.repo.remover_por_id(id_instituicao_area)
        if not removido:
            raise ValueError("Falha ao remover relação instituição-área")

    def remover_por_instituicao(self, id_instituicao: int):
        """Remove todas as relações de uma instituição."""
        return self.repo.remover_por_instituicao(id_instituicao)

    # ==========================================
    # FORMATAÇÃO
    # ==========================================

    def listar_formatado(self):
        return [str(ia) for ia in self.listar_todas()]

    def buscar_por_id_formatado(self, id_instituicao_area: int):
        return str(self.buscar_por_id(id_instituicao_area))