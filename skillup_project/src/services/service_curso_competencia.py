from src.dominio.curso_competencia import CursoCompetencia, TipoCursoCompetencia
from src.interfaces.interface_curso_competencia import ICursoCompetenciaRepositorio


class CursoCompetenciaService:
    """Serviço de domínio para gerenciamento de competências oferecidas por cursos.
    Contém a lógica de negócio e validações relacionadas às competências de cursos."""

    def __init__(self, repositorio: ICursoCompetenciaRepositorio):
        self.repo = repositorio

    # ==========================================
    # CRUD
    # ==========================================

    def cadastrar(self, id_curso: int, id_competencia: int, nivel_conferido: str, tipo_curso: TipoCursoCompetencia):
        """Cadastra uma nova competência para um curso. Valida duplicidade."""
        existente = self.repo.buscar_por_curso_e_competencia(id_curso, id_competencia)
        if existente:
            raise ValueError("Curso já possui esta competência cadastrada")

        todas = self.repo.listar_todas()
        novo_id = 1 if not todas else max(c.id for c in todas) + 1

        curso_comp = CursoCompetencia(
            id=novo_id,
            id_curso=id_curso,
            id_competencia=id_competencia,
            nivel_conferido=nivel_conferido,
            tipo_curso=tipo_curso,
        )

        self.repo.salvar(curso_comp)
        return curso_comp

    def listar_todas(self):
        """Lista todas as competências de cursos."""
        return self.repo.listar_todas()

    def buscar_por_id(self, id_curso_competencia: int):
        """Busca uma competência de curso pelo ID. Lança ValueError se não encontrada."""
        comp = self.repo.buscar_por_id(id_curso_competencia)
        if not comp:
            raise ValueError("CursoCompetencia não encontrada")
        return comp

    # ==========================================
    # LISTAGENS
    # ==========================================

    def listar_por_curso(self, id_curso: int):
        """Retorna todas as competências oferecidas por um curso."""
        return self.repo.listar_por_curso(id_curso)

    def listar_por_competencia(self, id_competencia: int):
        """Retorna todos os cursos que oferecem uma competência."""
        return self.repo.listar_por_competencia(id_competencia)

    def listar_por_nivel(self, nivel: str):
        """Retorna todas as competências de cursos com um nível específico."""
        return self.repo.listar_por_nivel(nivel)

    def buscar_por_curso_e_competencia(self, id_curso: int, id_competencia: int):
        """Busca uma competência específica oferecida por um curso."""
        return self.repo.buscar_por_curso_e_competencia(id_curso, id_competencia)

    def contar_competencias_curso(self, id_curso: int) -> int:
        """Retorna a quantidade de competências oferecidas por um curso."""
        return self.repo.contar_competencias_curso(id_curso)

    # ==========================================
    # AÇÕES DE NEGÓCIO
    # ==========================================

    def atualizar_nivel(self, id_curso_competencia: int, novo_nivel: str):
        """Atualiza o nível conferido de uma competência de curso."""
        comp = self.buscar_por_id(id_curso_competencia)
        comp.atualizar_nivel(novo_nivel)
        self.repo.atualizar(comp)
        return comp

    def remover(self, id_curso_competencia: int):
        """Remove uma competência de curso pelo ID."""
        self.buscar_por_id(id_curso_competencia)
        removido = self.repo.remover_por_id(id_curso_competencia)
        if not removido:
            raise ValueError("Falha ao remover competência do curso")

    def remover_por_curso(self, id_curso: int):
        """Remove todas as competências de um curso."""
        return self.repo.remover_por_curso(id_curso)

    # ==========================================
    # FORMATAÇÃO
    # ==========================================

    def listar_formatado(self):
        return [str(c) for c in self.listar_todas()]

    def buscar_por_id_formatado(self, id_curso_competencia: int):
        return str(self.buscar_por_id(id_curso_competencia))