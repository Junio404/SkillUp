from datetime import date
from typing import Optional
from src.dominio.curso_presencial import CursoPresencial
from src.dominio.vaga import Modalidade
from src.interfaces.interface_curso import ICursoRepositorio


class CursoPresencialService:
    """Serviço de domínio para gerenciamento de cursos presenciais.
    Contém a lógica de negócio e validações relacionadas aos cursos presenciais."""

    def __init__(self, repositorio: ICursoRepositorio):
        self.repo = repositorio

    # ==========================================
    # CRUD
    # ==========================================

    def cadastrar(
        self,
        nome: str,
        area: str,
        carga_horaria: int,
        capacidade: int,
        localidade: str,
        prazo_inscricao: Optional[date] = None,
        modalidade: Modalidade = Modalidade.PRESENCIAL,
    ):
        """Cadastra um novo curso presencial. Valida duplicidade por nome."""
        existentes = self.repo.listar_por_nome(nome)
        if existentes:
            raise ValueError("Já existe curso com este nome")

        todos = self.repo.listar_todos()
        novo_id = 1 if not todos else max(c.id for c in todos) + 1

        curso = CursoPresencial(
            id=novo_id,
            nome=nome,
            area=area,
            carga_horaria=carga_horaria,
            modalidade=modalidade,
            capacidade=capacidade,
            prazo_inscricao=prazo_inscricao,
            localidade=localidade,
        )

        self.repo.salvar(curso)
        return curso

    def listar_todos(self):
        """Lista todos os cursos presenciais."""
        return self.repo.listar_todos()

    def buscar_por_id(self, id_curso: int):
        """Busca um curso presencial pelo ID. Lança ValueError se não encontrado."""
        curso = self.repo.buscar_por_id(id_curso)
        if not curso:
            raise ValueError("Curso presencial não encontrado")
        return curso

    def remover(self, id_curso: int):
        """Remove um curso presencial pelo ID."""
        self.buscar_por_id(id_curso)
        removido = self.repo.remover_por_id(id_curso)
        if not removido:
            raise ValueError("Falha ao remover curso presencial")

    # ==========================================
    # LISTAGENS
    # ==========================================

    def listar_por_nome(self, nome: str):
        """Retorna cursos presenciais que correspondem ao nome."""
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
        """Atualiza um campo específico de um curso presencial."""
        curso = self.buscar_por_id(id_curso)
        if not hasattr(curso, campo):
            raise AttributeError(f"O campo '{campo}' não existe no curso presencial")
        setattr(curso, campo, novo_valor)
        self.repo.atualizar(curso)
        return curso

    def publicar(self, id_curso: int):
        """Torna um curso presencial ativo."""
        curso = self.buscar_por_id(id_curso)
        curso.publicar()
        self.repo.atualizar(curso)
        return curso

    def pausar(self, id_curso: int):
        """Pausa um curso presencial."""
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