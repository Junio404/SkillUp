import unittest
from unittest.mock import Mock, patch
from src.services.service_candidatura import CandidaturaService
from src.interfaces.interface_candidatura import ICandidaturaRepositorio
from src.dominio.candidatura import StatusCandidatura, TipoVagaCandidatura
from src.dominio.validators import PrazoValidador


class TestServiceCandidatura(unittest.TestCase):
    """Testes do serviço de Candidatura."""

    def setUp(self):
        self.mock_repo = Mock(spec=ICandidaturaRepositorio)
        self.service = CandidaturaService(self.mock_repo)

    @patch.object(PrazoValidador, "validar", return_value=None)
    def test_cadastrar_sucesso(self, _mock_prazo):
        self.mock_repo.listar_por_candidato.return_value = []
        self.mock_repo.listar_todas.return_value = []
        c = self.service.cadastrar(id_vaga=10, id_candidato=20, tipo_vaga=TipoVagaCandidatura.CLT)
        self.mock_repo.salvar.assert_called_once()
        self.assertEqual(c.id_vaga, 10)
        self.assertEqual(c.id_candidato, 20)
        self.assertEqual(c.status, StatusCandidatura.ENVIADO)

    @patch.object(PrazoValidador, "validar", return_value=None)
    def test_cadastrar_duplicado(self, _mock_prazo):
        existente = Mock()
        existente.id_vaga = 10
        existente.tipo_vaga = TipoVagaCandidatura.CLT
        self.mock_repo.listar_por_candidato.return_value = [existente]
        self.mock_repo.listar_todas.return_value = []
        with self.assertRaisesRegex(ValueError, "já possui candidatura"):
            self.service.cadastrar(id_vaga=10, id_candidato=20, tipo_vaga=TipoVagaCandidatura.CLT)

    def test_buscar_por_id_sucesso(self):
        candidatura = Mock()
        self.mock_repo.buscar_por_id.return_value = candidatura
        resultado = self.service.buscar_por_id(1)
        self.assertEqual(resultado, candidatura)

    def test_buscar_por_id_inexistente(self):
        self.mock_repo.buscar_por_id.return_value = None
        with self.assertRaisesRegex(ValueError, "Candidatura não encontrada"):
            self.service.buscar_por_id(999)

    def test_excluir(self):
        self.mock_repo.buscar_por_id.return_value = Mock()
        self.service.excluir(1)
        self.mock_repo.excluir.assert_called_once_with(1)

    def test_listar_todas(self):
        self.mock_repo.listar_todas.return_value = [Mock(), Mock()]
        resultado = self.service.listar_todas()
        self.assertEqual(len(resultado), 2)

    def test_listar_por_candidato(self):
        self.mock_repo.listar_por_candidato.return_value = [Mock()]
        resultado = self.service.listar_por_candidato(20)
        self.assertEqual(len(resultado), 1)

    def test_listar_por_vaga(self):
        self.mock_repo.listar_por_vaga.return_value = [Mock(), Mock()]
        resultado = self.service.listar_por_vaga(10)
        self.assertEqual(len(resultado), 2)

    def test_listar_por_status(self):
        self.mock_repo.listar_por_status.return_value = [Mock()]
        resultado = self.service.listar_por_status("Enviado")
        self.assertEqual(len(resultado), 1)

    def test_contar_por_candidato(self):
        self.mock_repo.contar_por_candidato.return_value = 3
        self.assertEqual(self.service.contar_por_candidato(20), 3)

    def test_contar_por_vaga(self):
        self.mock_repo.contar_por_vaga.return_value = 5
        self.assertEqual(self.service.contar_por_vaga(10), 5)

    def test_aprovar(self):
        candidatura = Mock()
        self.mock_repo.buscar_por_id.return_value = candidatura
        self.service.aprovar(1)
        candidatura.aprovar.assert_called_once()
        self.mock_repo.atualizar_status.assert_called_once_with(1, StatusCandidatura.ACEITO.value)

    def test_reprovar(self):
        candidatura = Mock()
        self.mock_repo.buscar_por_id.return_value = candidatura
        self.service.reprovar(1)
        candidatura.reprovar.assert_called_once()
        self.mock_repo.atualizar_status.assert_called_once_with(1, StatusCandidatura.RECUSADO.value)

    def test_cancelar(self):
        candidatura = Mock()
        self.mock_repo.buscar_por_id.return_value = candidatura
        self.service.cancelar(1)
        candidatura.cancelar.assert_called_once()


if __name__ == "__main__":
    unittest.main()
