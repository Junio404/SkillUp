from datetime import date
from typing import Optional
from src.dominio.curso_ead import CursoEAD
from src.interfaces.interface_curso import ICursoRepositorio
from src.interfaces.interface_instituicao_ensino import IInstituicaoEnsino


class CursoEADService:
    """Serviço de domínio para gerenciamento de cursos EAD.
    Contém a lógica de negócio e validações relacionadas aos cursos EAD."""

    def __init__(
        self,
        repositorio: ICursoRepositorio,
        repo_instituicao: Optional[IInstituicaoEnsino] = None
    ):
        self.repo = repositorio
        self._repo_instituicao = repo_instituicao

    # ==========================================
    # CRUD
    # ==========================================

    def cadastrar(
        self,
        id_instituicao: int,
        nome: str,
        area: str,
        carga_horaria: int,
        capacidade: int,
        plataforma_url: str,
        prazo_inscricao: Optional[date] = None,
    ):
        """Cadastra um novo curso EAD. Valida existência da instituição."""
        from src.dominio.vaga import Modalidade
        
        # Validação de integridade referencial: instituição deve existir
        if self._repo_instituicao:
            instituicao = self._repo_instituicao.buscar_por_id(id_instituicao)
            if not instituicao:
                raise ValueError(f"Instituição com ID {id_instituicao} não encontrada.")
        
        existentes = self.repo.listar_por_nome(nome)
        if existentes:
            raise ValueError("Já existe curso com este nome")

        todos = self.repo.listar_todos()
        novo_id = 1 if not todos else max(c.id for c in todos) + 1

        curso = CursoEAD(
            id=novo_id,
            id_instituicao=id_instituicao,
            nome=nome,
            area=area,
            carga_horaria=carga_horaria,
            modalidade=Modalidade.REMOTO,
            capacidade=capacidade,
            prazo_inscricao=prazo_inscricao,
            plataforma_url=plataforma_url,
        )

        self.repo.salvar(curso)
        return curso

    def listar_por_instituicao(self, id_instituicao: int):
        """Retorna todos os cursos EAD de uma instituição específica."""
        return [c for c in self.repo.listar_todos() if c.id_instituicao == id_instituicao]

    def listar_todos(self):
        """Lista todos os cursos EAD."""
        return self.repo.listar_todos()

    def buscar_por_id(self, id_curso: int):
        """Busca um curso EAD pelo ID. Lança ValueError se não encontrado."""
        curso = self.repo.buscar_por_id(id_curso)
        if not curso:
            raise ValueError("Curso EAD não encontrado")
        return curso

    def remover(self, id_curso: int):
        """Remove um curso EAD pelo ID."""
        self.buscar_por_id(id_curso)
        removido = self.repo.remover_por_id(id_curso)
        if not removido:
            raise ValueError("Falha ao remover curso EAD")

    # ==========================================
    # LISTAGENS
    # ==========================================

    def listar_por_nome(self, nome: str):
        """Retorna cursos EAD que correspondem ao nome."""
        return self.repo.listar_por_nome(nome)

    def listar_por_tipo(self, tipo: str):
        """Retorna cursos de um tipo específico."""
        return self.repo.listar_por_tipo(tipo)

    def listar_por_carga_horaria_minima(self, carga_horaria: int):
        """Retorna cursos com carga horária mínima especificada."""
        return self.repo.listar_por_carga_horaria_minima(carga_horaria)

    def buscar_por_filtros(self, **filtros):
        """Busca cursos com filtros dinâmicos."""
        return self.repo.buscar_por_filtros(**filtros)

    def contar_total(self) -> int:
        """Retorna o total de cursos cadastrados."""
        return self.repo.contar_total()

    # ==========================================
    # AÇÕES DE NEGÓCIO
    # ==========================================

    def atualizar(self, id_curso: int, campo: str, novo_valor):
        """Atualiza um campo específico de um curso EAD."""
        curso = self.buscar_por_id(id_curso)
        if not hasattr(curso, campo):
            raise AttributeError(f"O campo '{campo}' não existe no curso EAD")
        setattr(curso, campo, novo_valor)
        self.repo.atualizar(curso)
        return curso

    def publicar(self, id_curso: int):
        """Torna um curso EAD ativo."""
        curso = self.buscar_por_id(id_curso)
        curso.publicar()
        self.repo.atualizar(curso)
        return curso

    def pausar(self, id_curso: int):
        """Pausa um curso EAD."""
        curso = self.buscar_por_id(id_curso)
        curso.pausar()
        self.repo.atualizar(curso)
        return curso

    # ==========================================
    # FORMATAÇÃO
    # ==========================================

    def listar_formatado(self):
        return [c.exibir_detalhes() for c in self.listar_todos()]

    def buscar_por_id_formatado(self, id_curso: int):
        return self.buscar_por_id(id_curso).exibir_detalhes()