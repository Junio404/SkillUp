import unittest
from datetime import date
from unittest.mock import Mock
from src.services.service_vaga_estagio import VagaEstagioService
from src.interfaces.interface_vaga import IVagaRepositorio
from src.dominio.vaga import Modalidade, TipoVaga


class TestServiceVagaEstagio(unittest.TestCase):
    """Testes do serviço de VagaEstagio."""

    def setUp(self):
        self.mock_repo = Mock(spec=IVagaRepositorio)
        self.service = VagaEstagioService(self.mock_repo)

    # -- CRUD --

    def test_cadastrar_sucesso(self):
        self.mock_repo.listar_todas.return_value = []
        vaga = self.service.cadastrar(
            titulo="Estágio TI",
            descricao="Estágio em TI",
            area="TI",
            modalidade=Modalidade.HIBRIDO,
            tipo=TipoVaga.ESTAGIO,
            bolsa_auxilio=1500.0,
            instituicao_conveniada="UFMG",
            localidade="Belo Horizonte",
            prazo_inscricao=date(2027, 12, 31),
        )
        self.mock_repo.salvar.assert_called_once()
        self.assertEqual(vaga.id, 1)
        self.assertEqual(vaga.titulo, "Estágio TI")
        self.assertEqual(vaga.bolsa_auxilio, 1500.0)
        self.assertEqual(vaga.instituicao_conveniada, "UFMG")

    def test_cadastrar_id_incremental(self):
        existente = Mock()
        existente.id = 3
        self.mock_repo.listar_todas.return_value = [existente]
        vaga = self.service.cadastrar(
            "Estágio Eng", "Desc", "Engenharia", Modalidade.PRESENCIAL,
            TipoVaga.ESTAGIO, 1200.0, "USP", "São Paulo", date(2027, 6, 1),
        )
        self.assertEqual(vaga.id, 4)

    def test_buscar_por_id_sucesso(self):
        obj = Mock()
        self.mock_repo.buscar_por_id.return_value = obj
        self.assertEqual(self.service.buscar_por_id(1), obj)

    def test_buscar_por_id_inexistente(self):
        self.mock_repo.buscar_por_id.return_value = None
        with self.assertRaisesRegex(ValueError, "Vaga de estágio não encontrada"):
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

    def test_listar_por_area(self):
        self.mock_repo.listar_por_area.return_value = [Mock()]
        self.assertEqual(len(self.service.listar_por_area("TI")), 1)

    # -- CONTAGEM --

    def test_contar_total(self):
        self.mock_repo.contar_total.return_value = 6
        self.assertEqual(self.service.contar_total(), 6)

    def test_contar_ativas(self):
        self.mock_repo.contar_ativas.return_value = 4
        self.assertEqual(self.service.contar_ativas(), 4)

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
