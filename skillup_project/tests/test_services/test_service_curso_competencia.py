import unittest
from unittest.mock import Mock
from src.services.service_curso_competencia import CursoCompetenciaService
from src.interfaces.interface_curso_competencia import ICursoCompetenciaRepositorio
from src.dominio.curso_competencia import TipoCursoCompetencia


class TestServiceCursoCompetencia(unittest.TestCase):
    """Testes do serviço de CursoCompetencia."""

    def setUp(self):
        self.mock_repo = Mock(spec=ICursoCompetenciaRepositorio)
        self.service = CursoCompetenciaService(self.mock_repo)

    # -- CRUD --

    def test_cadastrar_sucesso(self):
        self.mock_repo.buscar_por_curso_e_competencia.return_value = None
        self.mock_repo.listar_todas.return_value = []
        cc = self.service.cadastrar(1, 2, "intermediario", TipoCursoCompetencia.EAD)
        self.mock_repo.salvar.assert_called_once()
        self.assertEqual(cc.id, 1)
        self.assertEqual(cc.id_curso, 1)
        self.assertEqual(cc.id_competencia, 2)

    def test_cadastrar_duplicado(self):
        self.mock_repo.buscar_por_curso_e_competencia.return_value = Mock()
        with self.assertRaisesRegex(ValueError, "já possui esta competência"):
            self.service.cadastrar(1, 2, "avancado", TipoCursoCompetencia.EAD)

    def test_cadastrar_id_incremental(self):
        existente = Mock()
        existente.id = 10
        self.mock_repo.buscar_por_curso_e_competencia.return_value = None
        self.mock_repo.listar_todas.return_value = [existente]
        cc = self.service.cadastrar(1, 3, "iniciante", TipoCursoCompetencia.EAD)
        self.assertEqual(cc.id, 11)

    def test_buscar_por_id_sucesso(self):
        obj = Mock()
        self.mock_repo.buscar_por_id.return_value = obj
        self.assertEqual(self.service.buscar_por_id(1), obj)

    def test_buscar_por_id_inexistente(self):
        self.mock_repo.buscar_por_id.return_value = None
        with self.assertRaisesRegex(ValueError, "não encontrada"):
            self.service.buscar_por_id(999)

    # -- LISTAGENS --

    def test_listar_todas(self):
        self.mock_repo.listar_todas.return_value = [Mock(), Mock()]
        self.assertEqual(len(self.service.listar_todas()), 2)

    def test_listar_por_curso(self):
        self.mock_repo.listar_por_curso.return_value = [Mock()]
        resultado = self.service.listar_por_curso(1)
        self.assertEqual(len(resultado), 1)
        self.mock_repo.listar_por_curso.assert_called_once_with(1)

    def test_listar_por_competencia(self):
        self.mock_repo.listar_por_competencia.return_value = [Mock()]
        resultado = self.service.listar_por_competencia(5)
        self.assertEqual(len(resultado), 1)

    def test_listar_por_nivel(self):
        self.mock_repo.listar_por_nivel.return_value = [Mock()]
        self.assertEqual(len(self.service.listar_por_nivel("avancado")), 1)

    def test_contar_competencias_curso(self):
        self.mock_repo.contar_competencias_curso.return_value = 4
        self.assertEqual(self.service.contar_competencias_curso(1), 4)

    # -- AÇÕES DE NEGÓCIO --

    def test_atualizar_nivel(self):
        comp = Mock()
        self.mock_repo.buscar_por_id.return_value = comp
        self.service.atualizar_nivel(1, "avancado")
        comp.atualizar_nivel.assert_called_once_with("avancado")
        self.mock_repo.atualizar.assert_called_once_with(comp)

    def test_remover_sucesso(self):
        self.mock_repo.buscar_por_id.return_value = Mock()
        self.mock_repo.remover_por_id.return_value = True
        self.service.remover(1)
        self.mock_repo.remover_por_id.assert_called_once_with(1)

    def test_remover_falha(self):
        self.mock_repo.buscar_por_id.return_value = Mock()
        self.mock_repo.remover_por_id.return_value = False
        with self.assertRaisesRegex(ValueError, "Falha ao remover"):
            self.service.remover(1)

    def test_remover_por_curso(self):
        self.service.remover_por_curso(5)
        self.mock_repo.remover_por_curso.assert_called_once_with(5)


if __name__ == "__main__":
    unittest.main()
