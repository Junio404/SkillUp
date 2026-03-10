import unittest
from datetime import date
from unittest.mock import Mock, PropertyMock
from src.services.service_inscricao_curso import InscricaoCursoService
from src.interfaces.interface_inscricao_curso import IInscricaoCursoRepositorio
from src.interfaces.interface_curso import ICursoRepositorio
from src.interfaces.interface_candidato import ICandidatoRepositorio
from src.interfaces.interface_curso_competencia import ICursoCompetenciaRepositorio
from src.interfaces.interface_competencia_candidato import ICompetenciaCandidatoRepositorio
from src.dominio.curso_presencial import CursoPresencial
from src.dominio.curso_ead import CursoEAD
from src.dominio.inscricao_curso import StatusInscricao, TipoCursoInscricao


class TestServiceInscricaoCurso(unittest.TestCase):
    """Testes do serviço de Inscrição em Curso."""

    def setUp(self):
        self.mock_repo_inscricao = Mock(spec=IInscricaoCursoRepositorio)
        self.mock_repo_curso_ead = Mock(spec=ICursoRepositorio)
        self.mock_repo_curso_presencial = Mock(spec=ICursoRepositorio)
        self.mock_repo_candidato = Mock(spec=ICandidatoRepositorio)
        self.service = InscricaoCursoService(
            repo_inscricao=self.mock_repo_inscricao,
            repo_curso_ead=self.mock_repo_curso_ead,
            repo_curso_presencial=self.mock_repo_curso_presencial,
            repo_candidato=self.mock_repo_candidato,
        )

    def _mock_candidato(self, id=1, localidade="São Paulo"):
        cand = Mock()
        cand.id = id
        cand.localidade = localidade
        return cand

    def _mock_curso_presencial(self, id=1, localidade="São Paulo", ativo=True):
        curso = Mock(spec=CursoPresencial)
        curso.id = id
        curso.localidade = localidade
        curso.ativo = ativo
        return curso

    def _mock_curso_ead(self, id=1, ativo=True):
        curso = Mock(spec=CursoEAD)
        curso.id = id
        curso.ativo = ativo
        return curso

    # -- INSCRIÇÃO --

    def test_inscrever_sucesso_presencial(self):
        curso = self._mock_curso_presencial(localidade="São Paulo")
        candidato = self._mock_candidato(localidade="São Paulo")
        self.mock_repo_curso_presencial.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = candidato
        self.mock_repo_inscricao.listar_por_aluno.return_value = []
        self.mock_repo_inscricao.listar_todas.return_value = []

        inscricao = self.service.inscrever(1, 1, TipoCursoInscricao.PRESENCIAL)
        self.mock_repo_inscricao.salvar.assert_called_once()
        self.assertEqual(inscricao.id, 1)
        self.assertEqual(inscricao.status, StatusInscricao.DEFERIDO)

    def test_inscrever_sucesso_ead(self):
        curso = self._mock_curso_ead()
        candidato = self._mock_candidato(localidade="Qualquer Cidade")
        self.mock_repo_curso_ead.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = candidato
        self.mock_repo_inscricao.listar_por_aluno.return_value = []
        self.mock_repo_inscricao.listar_todas.return_value = []

        inscricao = self.service.inscrever(1, 1, TipoCursoInscricao.EAD)
        self.mock_repo_inscricao.salvar.assert_called_once()

    def test_inscrever_curso_inexistente(self):
        self.mock_repo_curso_ead.buscar_por_id.return_value = None
        with self.assertRaisesRegex(ValueError, "não encontrado"):
            self.service.inscrever(1, 999, TipoCursoInscricao.EAD)

    def test_inscrever_curso_inativo(self):
        curso = self._mock_curso_presencial(ativo=False)
        self.mock_repo_curso_presencial.buscar_por_id.return_value = curso
        with self.assertRaisesRegex(ValueError, "não está ativo"):
            self.service.inscrever(1, 1, TipoCursoInscricao.PRESENCIAL)

    def test_inscrever_candidato_inexistente(self):
        curso = self._mock_curso_presencial()
        self.mock_repo_curso_presencial.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = None
        with self.assertRaisesRegex(ValueError, "não encontrado"):
            self.service.inscrever(999, 1, TipoCursoInscricao.PRESENCIAL)

    def test_inscrever_duplicada(self):
        curso = self._mock_curso_presencial()
        candidato = self._mock_candidato()
        inscricao_existente = Mock()
        inscricao_existente.id_curso = 1
        inscricao_existente.tipo_curso = TipoCursoInscricao.PRESENCIAL
        self.mock_repo_curso_presencial.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = candidato
        self.mock_repo_inscricao.listar_por_aluno.return_value = [inscricao_existente]

        with self.assertRaisesRegex(ValueError, "já está inscrito"):
            self.service.inscrever(1, 1, TipoCursoInscricao.PRESENCIAL)

    def test_inscrever_localidade_incompativel(self):
        curso = self._mock_curso_presencial(localidade="Rio de Janeiro")
        candidato = self._mock_candidato(localidade="São Paulo")
        self.mock_repo_curso_presencial.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = candidato
        self.mock_repo_inscricao.listar_por_aluno.return_value = []

        with self.assertRaisesRegex(ValueError, "Localidade incompatível"):
            self.service.inscrever(1, 1, TipoCursoInscricao.PRESENCIAL)

    def test_inscrever_candidato_sem_localidade_curso_presencial(self):
        curso = self._mock_curso_presencial(localidade="São Paulo")
        candidato = self._mock_candidato(localidade="")
        self.mock_repo_curso_presencial.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = candidato
        self.mock_repo_inscricao.listar_por_aluno.return_value = []

        with self.assertRaisesRegex(ValueError, "não possui localidade"):
            self.service.inscrever(1, 1, TipoCursoInscricao.PRESENCIAL)

    def test_inscrever_id_incremental(self):
        curso = self._mock_curso_ead()
        candidato = self._mock_candidato()
        existente = Mock()
        existente.id = 10
        existente.id_curso = 99
        self.mock_repo_curso_ead.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = candidato
        self.mock_repo_inscricao.listar_por_aluno.return_value = []
        self.mock_repo_inscricao.listar_todas.return_value = [existente]

        inscricao = self.service.inscrever(1, 1, TipoCursoInscricao.EAD)
        self.assertEqual(inscricao.id, 11)

    # -- LISTAGENS --

    def test_listar_por_candidato(self):
        self.mock_repo_inscricao.listar_por_aluno.return_value = [Mock()]
        resultado = self.service.listar_por_candidato(1)
        self.assertEqual(len(resultado), 1)
        self.mock_repo_inscricao.listar_por_aluno.assert_called_once_with(1)

    def test_listar_por_curso(self):
        self.mock_repo_inscricao.listar_por_curso.return_value = [Mock(), Mock()]
        resultado = self.service.listar_por_curso(1)
        self.assertEqual(len(resultado), 2)
        self.mock_repo_inscricao.listar_por_curso.assert_called_once_with(1)


class TestConclusaoInscricao(unittest.TestCase):
    """Testes da funcionalidade de conclusão de inscrição e atribuição de competências."""

    def setUp(self):
        self.mock_repo_inscricao = Mock(spec=IInscricaoCursoRepositorio)
        self.mock_repo_curso_ead = Mock(spec=ICursoRepositorio)
        self.mock_repo_curso_presencial = Mock(spec=ICursoRepositorio)
        self.mock_repo_candidato = Mock(spec=ICandidatoRepositorio)
        self.mock_repo_curso_competencia = Mock(spec=ICursoCompetenciaRepositorio)
        self.mock_repo_competencia_candidato = Mock(spec=ICompetenciaCandidatoRepositorio)

        self.service = InscricaoCursoService(
            repo_inscricao=self.mock_repo_inscricao,
            repo_curso_ead=self.mock_repo_curso_ead,
            repo_curso_presencial=self.mock_repo_curso_presencial,
            repo_candidato=self.mock_repo_candidato,
            repo_curso_competencia=self.mock_repo_curso_competencia,
            repo_competencia_candidato=self.mock_repo_competencia_candidato,
        )

    def _mock_inscricao(self, id=1, id_curso=1, id_aluno=1, status=StatusInscricao.DEFERIDO):
        inscricao = Mock()
        inscricao.id = id
        inscricao.id_curso = id_curso
        inscricao.id_aluno = id_aluno
        inscricao.status = status
        return inscricao

    def _mock_curso_competencia(self, id=1, id_curso=1, id_competencia=1, nivel_conferido="intermediario"):
        comp = Mock()
        comp.id = id
        comp.id_curso = id_curso
        comp.id_competencia = id_competencia
        comp.nivel_conferido = nivel_conferido
        return comp

    def _mock_competencia_candidato(self, id=1, id_candidato=1, id_competencia=1, nivel_atual="iniciante"):
        comp = Mock()
        comp.id = id
        comp.id_candidato = id_candidato
        comp.id_competencia = id_competencia
        comp.nivel_atual = nivel_atual
        return comp

    # -- CONCLUSÃO DE INSCRIÇÃO --

    def test_concluir_inscricao_sucesso_sem_competencias(self):
        """Conclui inscrição quando o curso não tem competências associadas."""
        inscricao = self._mock_inscricao()
        self.mock_repo_inscricao.buscar_por_id.return_value = inscricao
        self.mock_repo_curso_competencia.listar_por_curso.return_value = []

        competencias = self.service.concluir_inscricao(1)

        self.assertEqual(len(competencias), 0)
        inscricao.concluir.assert_called_once()
        self.mock_repo_inscricao.salvar.assert_called_once_with(inscricao)

    def test_concluir_inscricao_cria_competencias(self):
        """Conclui inscrição e cria competências para o candidato."""
        inscricao = self._mock_inscricao(id_aluno=5, id_curso=10)
        comp_curso = self._mock_curso_competencia(id_competencia=100, nivel_conferido="avancado")

        self.mock_repo_inscricao.buscar_por_id.return_value = inscricao
        self.mock_repo_curso_competencia.listar_por_curso.return_value = [comp_curso]
        self.mock_repo_competencia_candidato.buscar_por_candidato_e_competencia.return_value = None
        self.mock_repo_competencia_candidato.listar_todas.return_value = []

        competencias = self.service.concluir_inscricao(1)

        self.assertEqual(len(competencias), 1)
        self.mock_repo_competencia_candidato.salvar.assert_called_once()
        inscricao.concluir.assert_called_once()

    def test_concluir_inscricao_atualiza_nivel_maior(self):
        """Atualiza nível da competência quando o curso confere nível maior."""
        inscricao = self._mock_inscricao(id_aluno=5, id_curso=10)
        comp_curso = self._mock_curso_competencia(id_competencia=100, nivel_conferido="avancado")
        comp_existente = self._mock_competencia_candidato(
            id_candidato=5, id_competencia=100, nivel_atual="iniciante"
        )

        self.mock_repo_inscricao.buscar_por_id.return_value = inscricao
        self.mock_repo_curso_competencia.listar_por_curso.return_value = [comp_curso]
        self.mock_repo_competencia_candidato.buscar_por_candidato_e_competencia.return_value = comp_existente
        self.mock_repo_competencia_candidato.listar_todas.return_value = []

        competencias = self.service.concluir_inscricao(1)

        self.assertEqual(len(competencias), 1)
        comp_existente.atualizar_nivel.assert_called_once_with("avancado")
        self.mock_repo_competencia_candidato.atualizar.assert_called_once()

    def test_concluir_inscricao_nao_atualiza_nivel_menor(self):
        """Não atualiza competência quando o candidato já tem nível maior."""
        inscricao = self._mock_inscricao(id_aluno=5, id_curso=10)
        comp_curso = self._mock_curso_competencia(id_competencia=100, nivel_conferido="iniciante")
        comp_existente = self._mock_competencia_candidato(
            id_candidato=5, id_competencia=100, nivel_atual="avancado"
        )

        self.mock_repo_inscricao.buscar_por_id.return_value = inscricao
        self.mock_repo_curso_competencia.listar_por_curso.return_value = [comp_curso]
        self.mock_repo_competencia_candidato.buscar_por_candidato_e_competencia.return_value = comp_existente

        competencias = self.service.concluir_inscricao(1)

        self.assertEqual(len(competencias), 0)
        comp_existente.atualizar_nivel.assert_not_called()
        self.mock_repo_competencia_candidato.salvar.assert_not_called()

    def test_concluir_inscricao_multiplas_competencias(self):
        """Conclui inscrição com múltiplas competências."""
        inscricao = self._mock_inscricao(id_aluno=5, id_curso=10)
        comp1 = self._mock_curso_competencia(id=1, id_competencia=100, nivel_conferido="intermediario")
        comp2 = self._mock_curso_competencia(id=2, id_competencia=200, nivel_conferido="avancado")
        comp3 = self._mock_curso_competencia(id=3, id_competencia=300, nivel_conferido="iniciante")

        self.mock_repo_inscricao.buscar_por_id.return_value = inscricao
        self.mock_repo_curso_competencia.listar_por_curso.return_value = [comp1, comp2, comp3]
        self.mock_repo_competencia_candidato.buscar_por_candidato_e_competencia.return_value = None
        self.mock_repo_competencia_candidato.listar_todas.return_value = []

        competencias = self.service.concluir_inscricao(1)

        self.assertEqual(len(competencias), 3)
        self.assertEqual(self.mock_repo_competencia_candidato.salvar.call_count, 3)

    def test_concluir_inscricao_inexistente(self):
        """Erro ao concluir inscrição inexistente."""
        self.mock_repo_inscricao.buscar_por_id.return_value = None

        with self.assertRaisesRegex(ValueError, "Inscrição não encontrada"):
            self.service.concluir_inscricao(999)

    def test_concluir_inscricao_nao_deferida(self):
        """Erro ao concluir inscrição que não está deferida."""
        inscricao = self._mock_inscricao(status=StatusInscricao.INDEFERIDO)
        self.mock_repo_inscricao.buscar_por_id.return_value = inscricao

        with self.assertRaisesRegex(ValueError, "Somente inscrições deferidas"):
            self.service.concluir_inscricao(1)

    def test_concluir_inscricao_ja_concluida(self):
        """Erro ao concluir inscrição que já foi concluída."""
        inscricao = self._mock_inscricao(status=StatusInscricao.CONCLUIDO)
        self.mock_repo_inscricao.buscar_por_id.return_value = inscricao

        with self.assertRaisesRegex(ValueError, "Somente inscrições deferidas"):
            self.service.concluir_inscricao(1)

    def test_concluir_inscricao_sem_repositorios_competencia(self):
        """Conclui inscrição mesmo sem repositórios de competência configurados."""
        service_sem_repos = InscricaoCursoService(
            repo_inscricao=self.mock_repo_inscricao,
            repo_curso_ead=self.mock_repo_curso_ead,
            repo_curso_presencial=self.mock_repo_curso_presencial,
            repo_candidato=self.mock_repo_candidato,
            repo_curso_competencia=None,  # Sem repo_curso_competencia
            repo_competencia_candidato=None,  # Sem repo_competencia_candidato
        )
        inscricao = self._mock_inscricao()
        self.mock_repo_inscricao.buscar_por_id.return_value = inscricao

        competencias = service_sem_repos.concluir_inscricao(1)

        self.assertEqual(len(competencias), 0)
        inscricao.concluir.assert_called_once()
        self.mock_repo_inscricao.salvar.assert_called_once()


if __name__ == "__main__":
    unittest.main()
