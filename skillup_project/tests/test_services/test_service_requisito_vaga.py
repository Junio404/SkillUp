import unittest
from unittest.mock import Mock
from src.services.service_requisito_vaga import RequisitoVagaService
from src.interfaces.interface_requisito_vaga import IRequisitoVagaRepositorio
from src.dominio.requisitos_vaga import TipoVagaRequisito


class TestServiceRequisitoVaga(unittest.TestCase):
    """Testes do serviço de RequisitoVaga."""

    def setUp(self):
        self.mock_repo = Mock(spec=IRequisitoVagaRepositorio)
        self.service = RequisitoVagaService(self.mock_repo)

    # -- CRUD --

    def test_cadastrar_sucesso(self):
        self.mock_repo.buscar_por_vaga_e_competencia.return_value = None
        self.mock_repo.listar_todos.return_value = []
        req = self.service.cadastrar(1, 2, "intermediario", TipoVagaRequisito.CLT, True)
        self.mock_repo.salvar.assert_called_once()
        self.assertEqual(req.id, 1)
        self.assertEqual(req.id_vaga, 1)
        self.assertEqual(req.id_competencia, 2)
        self.assertTrue(req.obrigatorio)

    def test_cadastrar_duplicado(self):
        self.mock_repo.buscar_por_vaga_e_competencia.return_value = Mock()
        with self.assertRaisesRegex(ValueError, "já possui este requisito"):
            self.service.cadastrar(1, 2, "avancado", TipoVagaRequisito.CLT)

    def test_cadastrar_id_incremental(self):
        existente = Mock()
        existente.id = 9
        self.mock_repo.buscar_por_vaga_e_competencia.return_value = None
        self.mock_repo.listar_todos.return_value = [existente]
        req = self.service.cadastrar(1, 3, "iniciante", TipoVagaRequisito.CLT, False)
        self.assertEqual(req.id, 10)

    def test_buscar_por_id_sucesso(self):
        obj = Mock()
        self.mock_repo.buscar_por_id.return_value = obj
        self.assertEqual(self.service.buscar_por_id(1), obj)

    def test_buscar_por_id_inexistente(self):
        self.mock_repo.buscar_por_id.return_value = None
        with self.assertRaisesRegex(ValueError, "não encontrado"):
            self.service.buscar_por_id(999)

    # -- LISTAGENS --

    def test_listar_todos(self):
        self.mock_repo.listar_todos.return_value = [Mock(), Mock()]
        self.assertEqual(len(self.service.listar_todos()), 2)

    def test_listar_por_vaga(self):
        self.mock_repo.listar_por_vaga.return_value = [Mock()]
        self.assertEqual(len(self.service.listar_por_vaga(1)), 1)

    def test_listar_por_competencia(self):
        self.mock_repo.listar_por_competencia.return_value = [Mock()]
        self.assertEqual(len(self.service.listar_por_competencia(2)), 1)

    def test_listar_obrigatorios_por_vaga(self):
        self.mock_repo.listar_obrigatorios_por_vaga.return_value = [Mock()]
        self.assertEqual(len(self.service.listar_obrigatorios_por_vaga(1)), 1)

    # -- CONTAGEM --

    def test_contar_requisitos_vaga(self):
        self.mock_repo.contar_requisitos_vaga.return_value = 5
        self.assertEqual(self.service.contar_requisitos_vaga(1), 5)

    def test_contar_requisitos_obrigatorios(self):
        self.mock_repo.contar_requisitos_obrigatorios.return_value = 3
        self.assertEqual(self.service.contar_requisitos_obrigatorios(1), 3)

    # -- AÇÕES DE NEGÓCIO --

    def test_atualizar_nivel(self):
        req = Mock()
        self.mock_repo.buscar_por_id.return_value = req
        self.service.atualizar_nivel(1, "avancado")
        req.atualizar_nivel.assert_called_once_with("avancado")
        self.mock_repo.atualizar.assert_called_once_with(req)

    def test_tornar_opcional(self):
        req = Mock()
        self.mock_repo.buscar_por_id.return_value = req
        self.service.tornar_opcional(1)
        req.tornar_opcional.assert_called_once()
        self.mock_repo.atualizar.assert_called_once_with(req)

    def test_tornar_obrigatorio(self):
        req = Mock()
        self.mock_repo.buscar_por_id.return_value = req
        self.service.tornar_obrigatorio(1)
        req.tornar_obrigatorio.assert_called_once()
        self.mock_repo.atualizar.assert_called_once_with(req)

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

    def test_remover_por_vaga(self):
        self.service.remover_por_vaga(3)
        self.mock_repo.remover_por_vaga.assert_called_once_with(3)


if __name__ == "__main__":
    unittest.main()
