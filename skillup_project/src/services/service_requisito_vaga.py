from src.dominio.requisitos_vaga import RequisitoVaga
from src.interfaces.interface_requisito_vaga import IRequisitoVagaRepositorio


class RequisitoVagaService:
    """Serviço de domínio para gerenciamento de requisitos de vagas.
    Contém a lógica de negócio e validações relacionadas aos requisitos de vagas."""

    def __init__(self, repositorio: IRequisitoVagaRepositorio):
        self.repo = repositorio

    # ==========================================
    # CRUD
    # ==========================================

    def cadastrar(
        self,
        id_vaga: int,
        id_competencia: int,
        nivel_minimo: str,
        obrigatorio: bool = True,
    ):
        """Cadastra um novo requisito para uma vaga. Valida duplicidade."""
        existente = self.repo.buscar_por_vaga_e_competencia(id_vaga, id_competencia)
        if existente:
            raise ValueError("Vaga já possui este requisito de competência")

        todos = self.repo.listar_todos()
        novo_id = 1 if not todos else max(r.id for r in todos) + 1

        requisito = RequisitoVaga(
            id=novo_id,
            id_vaga=id_vaga,
            id_competencia=id_competencia,
            nivel_minimo=nivel_minimo,
            obrigatorio=obrigatorio,
        )

        self.repo.salvar(requisito)
        return requisito

    def listar_todos(self):
        """Lista todos os requisitos de vagas."""
        return self.repo.listar_todos()

    def buscar_por_id(self, id_requisito: int):
        """Busca um requisito pelo ID. Lança ValueError se não encontrado."""
        requisito = self.repo.buscar_por_id(id_requisito)
        if not requisito:
            raise ValueError("Requisito de vaga não encontrado")
        return requisito

    # ==========================================
    # LISTAGENS
    # ==========================================

    def listar_por_vaga(self, id_vaga: int):
        """Retorna todos os requisitos de uma vaga."""
        return self.repo.listar_por_vaga(id_vaga)

    def listar_por_competencia(self, id_competencia: int):
        """Retorna todas as vagas que exigem uma competência."""
        return self.repo.listar_por_competencia(id_competencia)

    def listar_obrigatorios_por_vaga(self, id_vaga: int):
        """Retorna todos os requisitos obrigatórios de uma vaga."""
        return self.repo.listar_obrigatorios_por_vaga(id_vaga)

    def listar_por_nivel_minimo(self, nivel: str):
        """Retorna todos os requisitos com um nível mínimo específico."""
        return self.repo.listar_por_nivel_minimo(nivel)

    def buscar_por_vaga_e_competencia(self, id_vaga: int, id_competencia: int):
        """Busca um requisito específico de uma vaga para uma competência."""
        return self.repo.buscar_por_vaga_e_competencia(id_vaga, id_competencia)

    # ==========================================
    # CONTAGEM
    # ==========================================

    def contar_requisitos_vaga(self, id_vaga: int) -> int:
        return self.repo.contar_requisitos_vaga(id_vaga)

    def contar_requisitos_obrigatorios(self, id_vaga: int) -> int:
        return self.repo.contar_requisitos_obrigatorios(id_vaga)

    # ==========================================
    # AÇÕES DE NEGÓCIO
    # ==========================================

    def atualizar_nivel(self, id_requisito: int, novo_nivel: str):
        """Atualiza o nível mínimo de um requisito."""
        requisito = self.buscar_por_id(id_requisito)
        requisito.atualizar_nivel(novo_nivel)
        self.repo.atualizar(requisito)
        return requisito

    def tornar_opcional(self, id_requisito: int):
        """Torna um requisito opcional."""
        requisito = self.buscar_por_id(id_requisito)
        requisito.tornar_opcional()
        self.repo.atualizar(requisito)
        return requisito

    def tornar_obrigatorio(self, id_requisito: int):
        """Torna um requisito obrigatório."""
        requisito = self.buscar_por_id(id_requisito)
        requisito.tornar_obrigatorio()
        self.repo.atualizar(requisito)
        return requisito

    def remover(self, id_requisito: int):
        """Remove um requisito pelo ID."""
        self.buscar_por_id(id_requisito)
        removido = self.repo.remover_por_id(id_requisito)
        if not removido:
            raise ValueError("Falha ao remover requisito de vaga")

    def remover_por_vaga(self, id_vaga: int):
        """Remove todos os requisitos de uma vaga."""
        return self.repo.remover_por_vaga(id_vaga)

    # ==========================================
    # FORMATAÇÃO
    # ==========================================

    def listar_formatado(self):
        return [str(r) for r in self.listar_todos()]

    def buscar_por_id_formatado(self, id_requisito: int):
        return str(self.buscar_por_id(id_requisito))