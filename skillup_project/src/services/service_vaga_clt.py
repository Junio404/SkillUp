from typing import Optional
from src.dominio.vaga import VagaCLT, Modalidade, TipoVaga
from src.interfaces.interface_vaga import IVagaRepositorio
from src.interfaces.interface_empresa import IEmpresa


class VagaCLTService:
    """Serviço de domínio para gerenciamento de vagas CLT.
    Contém a lógica de negócio e validações relacionadas às vagas CLT."""

    def __init__(
        self,
        repositorio: IVagaRepositorio,
        repo_empresa: Optional[IEmpresa] = None
    ):
        self.repo = repositorio
        self._repo_empresa = repo_empresa

    # ==========================================
    # CRUD
    # ==========================================

    def cadastrar(
        self,
        id_empresa: int,
        titulo: str,
        descricao: str,
        area: str,
        modalidade: Modalidade,
        tipo: TipoVaga,
        salario_base: float,
        localidade: str = "",
        prazo_inscricao=None,
    ):
        """Cadastra uma nova vaga CLT. Valida existência da empresa."""
        # Validação de integridade referencial: empresa deve existir
        if self._repo_empresa:
            empresa = self._repo_empresa.buscar_por_id(id_empresa)
            if not empresa:
                raise ValueError(f"Empresa com ID {id_empresa} não encontrada.")
        
        todas = self.repo.listar_todas()
        novo_id = 1 if not todas else max(v.id for v in todas) + 1

        vaga = VagaCLT(
            id=novo_id,
            id_empresa=id_empresa,
            titulo=titulo,
            descricao=descricao,
            area=area,
            modalidade=modalidade,
            tipo=tipo,
            salario_base=salario_base,
            localidade=localidade,
            prazo_inscricao=prazo_inscricao,
        )

        self.repo.salvar(vaga)
        return vaga

    def listar_por_empresa(self, id_empresa: int):
        """Retorna todas as vagas CLT de uma empresa específica."""
        return [v for v in self.repo.listar_todas() if v.id_empresa == id_empresa]

    def listar_todas(self):
        """Lista todas as vagas CLT."""
        return self.repo.listar_todas()

    def buscar_por_id(self, id_vaga: int):
        """Busca uma vaga CLT pelo ID. Lança ValueError se não encontrada."""
        vaga = self.repo.buscar_por_id(id_vaga)
        if not vaga:
            raise ValueError("Vaga CLT não encontrada")
        return vaga

    def excluir(self, id_vaga: int):
        """Exclui uma vaga CLT pelo ID."""
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
        """Atualiza um campo específico de uma vaga CLT."""
        vaga = self.buscar_por_id(id_vaga)
        if not hasattr(vaga, campo):
            raise AttributeError(f"O campo '{campo}' não existe na vaga CLT")
        setattr(vaga, campo, novo_valor)
        self.repo.atualizar(vaga)
        return vaga

    def publicar(self, id_vaga: int):
        """Torna uma vaga CLT ativa."""
        vaga = self.buscar_por_id(id_vaga)
        vaga.publicar()
        self.repo.atualizar(vaga)
        return vaga

    def pausar(self, id_vaga: int):
        """Pausa uma vaga CLT."""
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