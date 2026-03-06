from src.dominio.vaga import VagaEstagio, Modalidade, TipoVaga
from src.interfaces.interface_vaga import IVagaRepositorio


class VagaEstagioService:
    """Serviço de domínio para gerenciamento de vagas de estágio.
    Contém a lógica de negócio e validações relacionadas às vagas de estágio."""

    def __init__(self, repositorio: IVagaRepositorio):
        self.repo = repositorio

    # ==========================================
    # CRUD
    # ==========================================

    def cadastrar(
        self,
        titulo: str,
        descricao: str,
        area: str,
        modalidade: Modalidade,
        tipo: TipoVaga,
        bolsa_auxilio: float,
        instituicao_conveniada: str,
        localidade: str = "",
        prazo_inscricao=None,
    ):
        """Cadastra uma nova vaga de estágio. Gera ID automático."""
        todas = self.repo.listar_todas()
        novo_id = 1 if not todas else max(v.id for v in todas) + 1

        vaga = VagaEstagio(
            id=novo_id,
            titulo=titulo,
            descricao=descricao,
            area=area,
            modalidade=modalidade,
            tipo=tipo,
            bolsa_auxilio=bolsa_auxilio,
            instituicao_conveniada=instituicao_conveniada,
            localidade=localidade,
            prazo_inscricao=prazo_inscricao,
        )

        self.repo.salvar(vaga)
        return vaga

    def listar_todas(self):
        """Lista todas as vagas de estágio."""
        return self.repo.listar_todas()

    def buscar_por_id(self, id_vaga: int):
        """Busca uma vaga de estágio pelo ID. Lança ValueError se não encontrada."""
        vaga = self.repo.buscar_por_id(id_vaga)
        if not vaga:
            raise ValueError("Vaga de estágio não encontrada")
        return vaga

    def excluir(self, id_vaga: int):
        """Exclui uma vaga de estágio pelo ID."""
        self.buscar_por_id(id_vaga)
        self.repo.excluir(id_vaga)

    # ==========================================
    # LISTAGENS
    # ==========================================

    def listar_ativas(self):
        """Retorna apenas as vagas ativas."""
        return self.repo.listar_ativas()

    def listar_inativas(self):
        """Retorna apenas as vagas inativas."""
        return self.repo.listar_inativas()

    def listar_por_area(self, area: str):
        """Retorna vagas de uma área específica."""
        return self.repo.listar_por_area(area)

    def listar_por_modalidade(self, modalidade: str):
        """Retorna vagas de uma modalidade específica."""
        return self.repo.listar_por_modalidade(modalidade)

    def listar_por_tipo(self, tipo: str):
        """Retorna vagas de um tipo específico."""
        return self.repo.listar_por_tipo(tipo)

    def listar_por_titulo(self, titulo: str):
        """Retorna vagas cujo título contém a string fornecida."""
        return self.repo.listar_por_titulo(titulo)

    def buscar_por_filtros(self, **filtros):
        """Busca vagas com filtros dinâmicos."""
        return self.repo.buscar_por_filtros(**filtros)

    # ==========================================
    # CONTAGEM
    # ==========================================

    def contar_total(self) -> int:
        return self.repo.contar_total()

    def contar_ativas(self) -> int:
        return self.repo.contar_ativas()

    def contar_por_area(self, area: str) -> int:
        return self.repo.contar_por_area(area)

    # ==========================================
    # AÇÕES DE NEGÓCIO
    # ==========================================

    def atualizar(self, id_vaga: int, campo: str, novo_valor):
        """Atualiza um campo específico de uma vaga de estágio."""
        vaga = self.buscar_por_id(id_vaga)
        if not hasattr(vaga, campo):
            raise AttributeError(f"O campo '{campo}' não existe na vaga de estágio")
        setattr(vaga, campo, novo_valor)
        self.repo.atualizar(vaga)
        return vaga

    def publicar(self, id_vaga: int):
        """Torna uma vaga de estágio ativa."""
        vaga = self.buscar_por_id(id_vaga)
        vaga.publicar()
        self.repo.atualizar(vaga)
        return vaga

    def pausar(self, id_vaga: int):
        """Pausa uma vaga de estágio."""
        vaga = self.buscar_por_id(id_vaga)
        vaga.pausar()
        self.repo.atualizar(vaga)
        return vaga

    # ==========================================
    # FORMATAÇÃO
    # ==========================================

    def listar_formatado(self):
        return [str(v) for v in self.listar_todas()]

    def buscar_por_id_formatado(self, id_vaga: int):
        return str(self.buscar_por_id(id_vaga))