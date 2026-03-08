import unittest
from unittest.mock import Mock
from src.services.service_instituicao_area_ensino import InstituicaoAreaEnsinoService
from src.interfaces.interface_instituicao_area_ensino import IInstituicaoAreaEnsinoRepositorio


class TestServiceInstituicaoAreaEnsino(unittest.TestCase):
    """Testes do serviço de InstituicaoAreaEnsino."""

    def setUp(self):
        self.mock_repo = Mock(spec=IInstituicaoAreaEnsinoRepositorio)
        self.service = InstituicaoAreaEnsinoService(self.mock_repo)

    # -- CRUD --

    def test_cadastrar_sucesso(self):
        self.mock_repo.buscar_por_instituicao_e_area.return_value = None
        self.mock_repo.listar_todas.return_value = []
        rel = self.service.cadastrar(1, 2)
        self.mock_repo.salvar.assert_called_once()
        self.assertEqual(rel.id_instituicao_area, 1)
        self.assertEqual(rel.id_instituicao, 1)
        self.assertEqual(rel.id_area, 2)

    def test_cadastrar_duplicado(self):
        self.mock_repo.buscar_por_instituicao_e_area.return_value = Mock()
        with self.assertRaisesRegex(ValueError, "já possui esta área"):
            self.service.cadastrar(1, 2)

    def test_cadastrar_id_incremental(self):
        existente = Mock()
        existente.id_instituicao_area = 7
        self.mock_repo.buscar_por_instituicao_e_area.return_value = None
        self.mock_repo.listar_todas.return_value = [existente]
        rel = self.service.cadastrar(2, 3)
        self.assertEqual(rel.id_instituicao_area, 8)

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

    def test_listar_por_instituicao(self):
        self.mock_repo.listar_por_instituicao.return_value = [Mock()]
        resultado = self.service.listar_por_instituicao(1)
        self.assertEqual(len(resultado), 1)

    def test_listar_por_area(self):
        self.mock_repo.listar_por_area.return_value = [Mock(), Mock()]
        resultado = self.service.listar_por_area(2)
        self.assertEqual(len(resultado), 2)

    # -- CONTAGEM --

    def test_contar_areas_por_instituicao(self):
        self.mock_repo.contar_areas_por_instituicao.return_value = 3
        self.assertEqual(self.service.contar_areas_por_instituicao(1), 3)

    def test_contar_instituicoes_por_area(self):
        self.mock_repo.contar_instituicoes_por_area.return_value = 2
        self.assertEqual(self.service.contar_instituicoes_por_area(1), 2)

    # -- AÇÕES DE NEGÓCIO --

    def test_atualizar(self):
        rel = Mock()
        self.mock_repo.buscar_por_id.return_value = rel
        resultado = self.service.atualizar(1, 5)
        self.assertEqual(rel.id_area, 5)
        self.mock_repo.atualizar.assert_called_once_with(rel)

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

    def test_remover_por_instituicao(self):
        self.service.remover_por_instituicao(3)
        self.mock_repo.remover_por_instituicao.assert_called_once_with(3)


if __name__ == "__main__":
    unittest.main()
