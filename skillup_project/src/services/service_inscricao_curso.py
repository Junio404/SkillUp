from datetime import date
from typing import Optional, List

from src.dominio.candidato import Candidato
from src.dominio.curso_abs import Curso
from src.dominio.curso_presencial import CursoPresencial
from src.dominio.inscricao_curso import InscricaoCurso, StatusInscricao
from src.dominio.competencia_candidato import CompetenciaCandidato
from src.interfaces.interface_inscricao_curso import IInscricaoCursoRepositorio
from src.interfaces.interface_curso import ICursoRepositorio
from src.interfaces.interface_candidato import ICandidatoRepositorio
from src.interfaces.interface_curso_competencia import ICursoCompetenciaRepositorio
from src.interfaces.interface_competencia_candidato import ICompetenciaCandidatoRepositorio


class InscricaoCursoService:
    """Serviço de inscrição em cursos.

    Regras de negócio:
    - O curso deve existir e estar ativo.
    - O candidato deve existir.
    - Se o curso for presencial, a localidade do candidato deve coincidir
    com a localidade do curso.
    - Não permite inscrição duplicada (mesmo candidato no mesmo curso).
    - Ao concluir um curso, as competências do curso são atribuídas ao candidato.
    """

    def __init__(
        self,
        repo_inscricao: IInscricaoCursoRepositorio,
        repo_curso: ICursoRepositorio,
        repo_candidato: ICandidatoRepositorio,
        repo_curso_competencia: Optional[ICursoCompetenciaRepositorio] = None,
        repo_competencia_candidato: Optional[ICompetenciaCandidatoRepositorio] = None,
    ):
        self._repo_inscricao = repo_inscricao
        self._repo_curso = repo_curso
        self._repo_candidato = repo_candidato
        self._repo_curso_competencia = repo_curso_competencia
        self._repo_competencia_candidato = repo_competencia_candidato

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

    def buscar_por_id(self, id_inscricao: int) -> InscricaoCurso:
        """Busca uma inscrição pelo ID. Lança ValueError se não encontrada."""
        inscricao = self._repo_inscricao.buscar_por_id(id_inscricao)
        if not inscricao:
            raise ValueError("Inscrição não encontrada.")
        return inscricao

    # ------------------------------------------------------------------
    # Conclusão de curso e atribuição de competências
    # ------------------------------------------------------------------

    def concluir_inscricao(self, id_inscricao: int) -> List[CompetenciaCandidato]:
        """Conclui uma inscrição e atribui as competências do curso ao candidato.

        Regras:
        - A inscrição deve existir e estar DEFERIDA.
        - Busca as competências oferecidas pelo curso.
        - Cria CompetenciaCandidato para cada competência do curso.
        - Se o candidato já possui a competência, atualiza o nível se for maior.
        - Marca a inscrição como CONCLUIDA.

        Returns:
            Lista de CompetenciaCandidato criadas ou atualizadas.
        """
        # 1. Buscar e validar inscrição
        inscricao = self.buscar_por_id(id_inscricao)

        if inscricao.status != StatusInscricao.DEFERIDO:
            raise ValueError("Somente inscrições deferidas podem ser concluídas.")

        # 2. Verificar se os repositórios de competência estão disponíveis
        if not self._repo_curso_competencia or not self._repo_competencia_candidato:
            # Conclui sem atribuir competências (repositórios não configurados)
            inscricao.concluir()
            self._repo_inscricao.salvar(inscricao)
            return []

        # 3. Buscar competências do curso
        competencias_curso = self._repo_curso_competencia.listar_por_curso(inscricao.id_curso)

        competencias_criadas: List[CompetenciaCandidato] = []

        # 4. Para cada competência do curso, criar ou atualizar competência do candidato
        for comp_curso in competencias_curso:
            # Verificar se candidato já possui essa competência
            comp_existente = self._repo_competencia_candidato.buscar_por_candidato_e_competencia(
                inscricao.id_aluno, comp_curso.id_competencia
            )

            if comp_existente:
                # Atualizar nível se o novo for maior
                nivel_curso = self._nivel_para_int(comp_curso.nivel_conferido)
                nivel_atual = self._nivel_para_int(comp_existente.nivel_atual)

                if nivel_curso > nivel_atual:
                    comp_existente.atualizar_nivel(comp_curso.nivel_conferido)
                    self._repo_competencia_candidato.atualizar(comp_existente)
                    competencias_criadas.append(comp_existente)
            else:
                # Criar nova competência para o candidato
                todas = self._repo_competencia_candidato.listar_todas()
                novo_id = 1 if not todas else max(c.id for c in todas) + 1

                nova_comp = CompetenciaCandidato(
                    id=novo_id,
                    id_candidato=inscricao.id_aluno,
                    id_competencia=comp_curso.id_competencia,
                    nivel_atual=comp_curso.nivel_conferido,
                )

                self._repo_competencia_candidato.salvar(nova_comp)
                competencias_criadas.append(nova_comp)

        # 5. Marcar inscrição como concluída
        inscricao.concluir()
        self._repo_inscricao.salvar(inscricao)

        return competencias_criadas

    @staticmethod
    def _nivel_para_int(nivel: str) -> int:
        """Converte um nível de competência para inteiro para comparação."""
        mapa = {"iniciante": 0, "intermediario": 1, "avancado": 2}
        return mapa.get(nivel.lower(), 0)

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