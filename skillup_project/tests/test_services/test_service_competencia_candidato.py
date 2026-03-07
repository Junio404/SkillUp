import unittest
from unittest.mock import Mock
from src.services.service_competencia_candidato import CompetenciaCandidatoService
from src.interfaces.interface_competencia_candidato import ICompetenciaCandidatoRepositorio


class TestServiceCompetenciaCandidato(unittest.TestCase):
    """Testes do serviço de CompetenciaCandidato."""

    def setUp(self):
        self.mock_repo = Mock(spec=ICompetenciaCandidatoRepositorio)
        self.service = CompetenciaCandidatoService(self.mock_repo)

    # -- CRUD --

    def test_cadastrar_sucesso(self):
        self.mock_repo.buscar_por_candidato_e_competencia.return_value = None
        self.mock_repo.listar_todas.return_value = []
        cc = self.service.cadastrar(1, 2, "intermediario")
        self.mock_repo.salvar.assert_called_once()
        self.assertEqual(cc.id, 1)
        self.assertEqual(cc.id_candidato, 1)
        self.assertEqual(cc.id_competencia, 2)

    def test_cadastrar_duplicado(self):
        self.mock_repo.buscar_por_candidato_e_competencia.return_value = Mock()
        with self.assertRaisesRegex(ValueError, "já possui esta competência"):
            self.service.cadastrar(1, 2, "avancado")

    def test_cadastrar_id_incremental(self):
        existente = Mock()
        existente.id = 5
        self.mock_repo.buscar_por_candidato_e_competencia.return_value = None
        self.mock_repo.listar_todas.return_value = [existente]
        cc = self.service.cadastrar(1, 3, "iniciante")
        self.assertEqual(cc.id, 6)

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

    def test_listar_por_candidato(self):
        self.mock_repo.listar_por_candidato.return_value = [Mock()]
        resultado = self.service.listar_por_candidato(1)
        self.assertEqual(len(resultado), 1)
        self.mock_repo.listar_por_candidato.assert_called_once_with(1)

    def test_listar_por_competencia(self):
        self.mock_repo.listar_por_competencia.return_value = [Mock()]
        resultado = self.service.listar_por_competencia(5)
        self.assertEqual(len(resultado), 1)
        self.mock_repo.listar_por_competencia.assert_called_once_with(5)

    def test_listar_por_nivel(self):
        self.mock_repo.listar_por_nivel.return_value = [Mock(), Mock()]
        resultado = self.service.listar_por_nivel("avancado")
        self.assertEqual(len(resultado), 2)

    def test_buscar_por_candidato_e_competencia(self):
        obj = Mock()
        self.mock_repo.buscar_por_candidato_e_competencia.return_value = obj
        self.assertEqual(self.service.buscar_por_candidato_e_competencia(1, 2), obj)

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

    def test_remover_por_candidato(self):
        self.service.remover_por_candidato(3)
        self.mock_repo.remover_por_candidato.assert_called_once_with(3)


if __name__ == "__main__":
    unittest.main()
