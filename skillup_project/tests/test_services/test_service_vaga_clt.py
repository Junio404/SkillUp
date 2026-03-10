import unittest
from datetime import date
from unittest.mock import Mock
from src.services.service_vaga_clt import VagaCLTService
from src.interfaces.interface_vaga import IVagaRepositorio
from src.dominio.vaga import Modalidade, TipoVaga


class TestServiceVagaCLT(unittest.TestCase):
    """Testes do serviço de VagaCLT."""

    def setUp(self):
        self.mock_repo = Mock(spec=IVagaRepositorio)
        self.service = VagaCLTService(self.mock_repo)

    # -- CRUD --

    def test_cadastrar_sucesso(self):
        self.mock_repo.listar_todas.return_value = []
        vaga = self.service.cadastrar(
            id_empresa=1,
            titulo="Dev Python",
            descricao="Vaga para dev",
            area="TI",
            modalidade=Modalidade.REMOTO,
            tipo=TipoVaga.EMPREGO,
            salario_base=8000.0,
            prazo_inscricao=date(2027, 12, 31),
        )
        self.mock_repo.salvar.assert_called_once()
        self.assertEqual(vaga.id, 1)
        self.assertEqual(vaga.id_empresa, 1)
        self.assertEqual(vaga.titulo, "Dev Python")
        self.assertEqual(vaga.salario_base, 8000.0)

    def test_cadastrar_id_incremental(self):
        existente = Mock()
        existente.id = 5
        self.mock_repo.listar_todas.return_value = [existente]
        vaga = self.service.cadastrar(
            1, "Dev Java", "Vaga", "TI", Modalidade.PRESENCIAL, TipoVaga.EMPREGO,
            10000.0, "São Paulo", date(2027, 12, 31),
        )
        self.assertEqual(vaga.id, 6)

    def test_buscar_por_id_sucesso(self):
        obj = Mock()
        self.mock_repo.buscar_por_id.return_value = obj
        self.assertEqual(self.service.buscar_por_id(1), obj)

    def test_buscar_por_id_inexistente(self):
        self.mock_repo.buscar_por_id.return_value = None
        with self.assertRaisesRegex(ValueError, "Vaga CLT não encontrada"):
            self.service.buscar_por_id(999)

    def test_excluir(self):
        self.mock_repo.buscar_por_id.return_value = Mock()
        self.service.excluir(1)
        self.mock_repo.excluir.assert_called_once_with(1)

    # -- LISTAGENS --

    def test_listar_todas(self):
        self.mock_repo.listar_todas.return_value = [Mock(), Mock()]
        self.assertEqual(len(self.service.listar_todas()), 2)

    def test_listar_ativas(self):
        self.mock_repo.listar_ativas.return_value = [Mock()]
        self.assertEqual(len(self.service.listar_ativas()), 1)

    def test_listar_inativas(self):
        self.mock_repo.listar_inativas.return_value = []
        self.assertEqual(len(self.service.listar_inativas()), 0)

    def test_listar_por_area(self):
        self.mock_repo.listar_por_area.return_value = [Mock()]
        self.assertEqual(len(self.service.listar_por_area("TI")), 1)

    def test_listar_por_modalidade(self):
        self.mock_repo.listar_por_modalidade.return_value = [Mock()]
        self.assertEqual(len(self.service.listar_por_modalidade("remoto")), 1)

    # -- CONTAGEM --

    def test_contar_total(self):
        self.mock_repo.contar_total.return_value = 12
        self.assertEqual(self.service.contar_total(), 12)

    def test_contar_ativas(self):
        self.mock_repo.contar_ativas.return_value = 8
        self.assertEqual(self.service.contar_ativas(), 8)

    def test_contar_por_area(self):
        self.mock_repo.contar_por_area.return_value = 3
        self.assertEqual(self.service.contar_por_area("TI"), 3)

    # -- AÇÕES DE NEGÓCIO --

    def test_publicar(self):
        vaga = Mock()
        self.mock_repo.buscar_por_id.return_value = vaga
        self.service.publicar(1)
        vaga.publicar.assert_called_once()
        self.mock_repo.atualizar.assert_called_once_with(vaga)

    def test_pausar(self):
        vaga = Mock()
        self.mock_repo.buscar_por_id.return_value = vaga
        self.service.pausar(1)
        vaga.pausar.assert_called_once()
        self.mock_repo.atualizar.assert_called_once_with(vaga)


if __name__ == "__main__":
    unittest.main()
