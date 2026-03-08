import unittest
from unittest.mock import Mock
from src.services.service_area_ensino import AreaEnsinoService
from src.interfaces.interface_area_ensino import IAreaEnsinoRepositorio


class TestServiceAreaEnsino(unittest.TestCase):
    """Testes do serviço de AreaEnsino."""

    def setUp(self):
        self.mock_repo = Mock(spec=IAreaEnsinoRepositorio)
        self.service = AreaEnsinoService(self.mock_repo)

    # -- CRUD --

    def test_cadastrar_sucesso(self):
        self.mock_repo.buscar_por_nome.return_value = None
        self.mock_repo.listar_todas.return_value = []
        area = self.service.cadastrar("Tecnologia da Informação")
        self.mock_repo.salvar.assert_called_once()
        self.assertEqual(area.id_area, 1)
        self.assertEqual(area.nome_area, "Tecnologia da Informação")

    def test_cadastrar_nome_duplicado(self):
        self.mock_repo.buscar_por_nome.return_value = Mock()
        with self.assertRaisesRegex(ValueError, "Já existe área de ensino"):
            self.service.cadastrar("TI")

    def test_cadastrar_id_incremental(self):
        existente = Mock()
        existente.id_area = 4
        self.mock_repo.buscar_por_nome.return_value = None
        self.mock_repo.listar_todas.return_value = [existente]
        area = self.service.cadastrar("Saúde")
        self.assertEqual(area.id_area, 5)

    def test_buscar_por_id_sucesso(self):
        obj = Mock()
        self.mock_repo.buscar_por_id.return_value = obj
        self.assertEqual(self.service.buscar_por_id(1), obj)

    def test_buscar_por_id_inexistente(self):
        self.mock_repo.buscar_por_id.return_value = None
        with self.assertRaisesRegex(ValueError, "não encontrada"):
            self.service.buscar_por_id(999)

    def test_buscar_por_nome_sucesso(self):
        obj = Mock()
        self.mock_repo.buscar_por_nome.return_value = obj
        self.assertEqual(self.service.buscar_por_nome("TI"), obj)

    def test_buscar_por_nome_inexistente(self):
        self.mock_repo.buscar_por_nome.return_value = None
        with self.assertRaisesRegex(ValueError, "não encontrada"):
            self.service.buscar_por_nome("Inexistente")

    def test_buscar_por_nome_parcial(self):
        self.mock_repo.buscar_por_nome_parcial.return_value = [Mock()]
        self.assertEqual(len(self.service.buscar_por_nome_parcial("Tec")), 1)

    def test_listar_todas(self):
        self.mock_repo.listar_todas.return_value = [Mock(), Mock()]
        self.assertEqual(len(self.service.listar_todas()), 2)

    def test_contar_total(self):
        self.mock_repo.contar_total.return_value = 7
        self.assertEqual(self.service.contar_total(), 7)

    # -- AÇÕES DE NEGÓCIO --

    def test_atualizar(self):
        area = Mock()
        self.mock_repo.buscar_por_id.return_value = area
        self.service.atualizar(1, "Novo Nome")
        self.assertEqual(area.nome_area, "Novo Nome")
        self.mock_repo.atualizar.assert_called_once_with(area)

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


if __name__ == "__main__":
    unittest.main()
