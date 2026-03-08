import unittest
from datetime import date
from unittest.mock import Mock, PropertyMock
from src.service.service_inscricao_curso import InscricaoCursoService
from src.interfaces.interface_inscricao_curso import IInscricaoCursoRepositorio
from src.interfaces.interface_curso import ICursoRepositorio
from src.interfaces.interface_candidato import ICandidatoRepositorio
from src.dominio.curso_presencial import CursoPresencial
from src.dominio.curso_ead import CursoEAD
from src.dominio.inscricao_curso import StatusInscricao


class TestServiceInscricaoCurso(unittest.TestCase):
    """Testes do serviço de Inscrição em Curso."""

    def setUp(self):
        self.mock_repo_inscricao = Mock(spec=IInscricaoCursoRepositorio)
        self.mock_repo_curso = Mock(spec=ICursoRepositorio)
        self.mock_repo_candidato = Mock(spec=ICandidatoRepositorio)
        self.service = InscricaoCursoService(
            self.mock_repo_inscricao,
            self.mock_repo_curso,
            self.mock_repo_candidato,
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
        self.mock_repo_curso.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = candidato
        self.mock_repo_inscricao.listar_por_aluno.return_value = []
        self.mock_repo_inscricao.listar_todas.return_value = []

        inscricao = self.service.inscrever(1, 1)
        self.mock_repo_inscricao.salvar.assert_called_once()
        self.assertEqual(inscricao.id, 1)
        self.assertEqual(inscricao.status, StatusInscricao.DEFERIDO)

    def test_inscrever_sucesso_ead(self):
        curso = self._mock_curso_ead()
        candidato = self._mock_candidato(localidade="Qualquer Cidade")
        self.mock_repo_curso.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = candidato
        self.mock_repo_inscricao.listar_por_aluno.return_value = []
        self.mock_repo_inscricao.listar_todas.return_value = []

        inscricao = self.service.inscrever(1, 1)
        self.mock_repo_inscricao.salvar.assert_called_once()

    def test_inscrever_curso_inexistente(self):
        self.mock_repo_curso.buscar_por_id.return_value = None
        with self.assertRaisesRegex(ValueError, "Curso não encontrado"):
            self.service.inscrever(1, 999)

    def test_inscrever_curso_inativo(self):
        curso = self._mock_curso_presencial(ativo=False)
        self.mock_repo_curso.buscar_por_id.return_value = curso
        with self.assertRaisesRegex(ValueError, "não está ativo"):
            self.service.inscrever(1, 1)

    def test_inscrever_candidato_inexistente(self):
        curso = self._mock_curso_presencial()
        self.mock_repo_curso.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = None
        with self.assertRaisesRegex(ValueError, "Candidato não encontrado"):
            self.service.inscrever(999, 1)

    def test_inscrever_duplicada(self):
        curso = self._mock_curso_presencial()
        candidato = self._mock_candidato()
        inscricao_existente = Mock()
        inscricao_existente.id_curso = 1
        self.mock_repo_curso.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = candidato
        self.mock_repo_inscricao.listar_por_aluno.return_value = [inscricao_existente]

        with self.assertRaisesRegex(ValueError, "já está inscrito"):
            self.service.inscrever(1, 1)

    def test_inscrever_localidade_incompativel(self):
        curso = self._mock_curso_presencial(localidade="Rio de Janeiro")
        candidato = self._mock_candidato(localidade="São Paulo")
        self.mock_repo_curso.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = candidato
        self.mock_repo_inscricao.listar_por_aluno.return_value = []

        with self.assertRaisesRegex(ValueError, "Localidade incompatível"):
            self.service.inscrever(1, 1)

    def test_inscrever_candidato_sem_localidade_curso_presencial(self):
        curso = self._mock_curso_presencial(localidade="São Paulo")
        candidato = self._mock_candidato(localidade="")
        self.mock_repo_curso.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = candidato
        self.mock_repo_inscricao.listar_por_aluno.return_value = []

        with self.assertRaisesRegex(ValueError, "não possui localidade"):
            self.service.inscrever(1, 1)

    def test_inscrever_id_incremental(self):
        curso = self._mock_curso_ead()
        candidato = self._mock_candidato()
        existente = Mock()
        existente.id = 10
        existente.id_curso = 99
        self.mock_repo_curso.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = candidato
        self.mock_repo_inscricao.listar_por_aluno.return_value = []
        self.mock_repo_inscricao.listar_todas.return_value = [existente]

        inscricao = self.service.inscrever(1, 1)
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


if __name__ == "__main__":
    unittest.main()
