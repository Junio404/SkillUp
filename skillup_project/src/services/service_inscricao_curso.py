from datetime import date

from src.dominio.candidato import Candidato
from src.dominio.curso_abs import Curso
from src.dominio.curso_presencial import CursoPresencial
from src.dominio.inscricao_curso import InscricaoCurso, StatusInscricao
from src.interfaces.interface_inscricao_curso import IInscricaoCursoRepositorio
from src.interfaces.interface_curso import ICursoRepositorio
from src.interfaces.interface_candidato import ICandidatoRepositorio


class InscricaoCursoService:
    """Serviço de inscrição em cursos.

    Regras de negócio:
    - O curso deve existir e estar ativo.
    - O candidato deve existir.
    - Se o curso for presencial, a localidade do candidato deve coincidir
      com a localidade do curso.
    - Não permite inscrição duplicada (mesmo candidato no mesmo curso).
    """

    def __init__(
        self,
        repo_inscricao: IInscricaoCursoRepositorio,
        repo_curso: ICursoRepositorio,
        repo_candidato: ICandidatoRepositorio,
    ):
        self._repo_inscricao = repo_inscricao
        self._repo_curso = repo_curso
        self._repo_candidato = repo_candidato

    def inscrever(self, id_candidato: int, id_curso: int) -> InscricaoCurso:
        """Inscreve um candidato em um curso, validando todas as regras de negócio."""
        # 1. Buscar curso
        curso = self._repo_curso.buscar_por_id(id_curso)
        if not curso:
            raise ValueError("Curso não encontrado.")

        if not curso.ativo:
            raise ValueError("Curso não está ativo para inscrições.")

        # 2. Buscar candidato
        candidato = self._repo_candidato.buscar_por_id(id_candidato)
        if not candidato:
            raise ValueError("Candidato não encontrado.")

        # 3. Verificar duplicidade
        inscricoes_aluno = self._repo_inscricao.listar_por_aluno(id_candidato)
        if any(i.id_curso == id_curso for i in inscricoes_aluno):
            raise ValueError("Candidato já está inscrito neste curso.")

        # 4. Regra de localidade para cursos presenciais
        if isinstance(curso, CursoPresencial):
            self._validar_localidade(candidato, curso)

        # 5. Gerar ID e criar inscrição
        todas = self._repo_inscricao.listar_todas()
        novo_id = 1 if not todas else max(i.id for i in todas) + 1

        inscricao = InscricaoCurso(
            id=novo_id,
            id_curso=id_curso,
            id_aluno=id_candidato,
            data_inscricao=date.today(),
            status=StatusInscricao.DEFERIDO,
        )

        self._repo_inscricao.salvar(inscricao)
        return inscricao

    def listar_por_candidato(self, id_candidato: int):
        """Lista todas as inscrições de um candidato."""
        return self._repo_inscricao.listar_por_aluno(id_candidato)

    def listar_por_curso(self, id_curso: int):
        """Lista todas as inscrições em um curso."""
        return self._repo_inscricao.listar_por_curso(id_curso)

    # ------------------------------------------------------------------
    # Validação de localidade
    # ------------------------------------------------------------------

    @staticmethod
    def _validar_localidade(candidato: Candidato, curso: CursoPresencial) -> None:
        """Valida que a localidade do candidato coincide com a do curso presencial."""
        localidade_candidato = candidato.localidade.strip().lower()
        localidade_curso = curso.localidade.strip().lower()

        if not localidade_candidato:
            raise ValueError(
                "Candidato não possui localidade cadastrada. "
                "Cursos presenciais exigem localidade compatível."
            )

        if localidade_candidato != localidade_curso:
            raise ValueError(
                f"Localidade incompatível: candidato em '{candidato.localidade}', "
                f"curso presencial em '{curso.localidade}'. "
                "Inscrição permitida somente para candidatos da mesma região."
            )
