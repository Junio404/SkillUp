import unittest
from unittest.mock import Mock
from src.services.service_instituicao_ensino import ServiceInstituicaoEnsino
from src.interfaces.interface_instituicao_ensino import IInstituicaoEnsino


class TestServiceInstituicaoEnsino(unittest.TestCase):
    """Testes do serviço de InstituicaoEnsino."""

    def setUp(self):
        self.mock_repo = Mock(spec=IInstituicaoEnsino)
        self.service = ServiceInstituicaoEnsino(self.mock_repo)

    # -- CRUD --

    def test_cadastrar_sucesso(self):
        self.mock_repo.buscar_por_cnpj.return_value = None
        self.mock_repo.listar.return_value = []
        inst = self.service.cadastrar(
            razao_social="Instituto Alpha LTDA",
            nome_fantasia="Alpha",
            cnpj="12345678000190",
            registro_educacional="REG123",
            tipo="Universidade",
            modalidades=["presencial", "ead"],
            credenciada=True,
        )
        self.mock_repo.salvar.assert_called_once()
        self.assertEqual(inst.id, 1)
        self.assertEqual(inst.nome_fantasia, "Alpha")

    def test_cadastrar_cnpj_duplicado(self):
        self.mock_repo.buscar_por_cnpj.return_value = Mock()
        with self.assertRaisesRegex(ValueError, "Já existe instituição com este CNPJ"):
            self.service.cadastrar("X", "X", "12345678000190", "R", "U")

    def test_cadastrar_id_incremental(self):
        existente = Mock()
        existente.id = 5
        self.mock_repo.buscar_por_cnpj.return_value = None
        self.mock_repo.listar.return_value = [existente]
        inst = self.service.cadastrar("Beta", "Beta", "98765432000100", "R2", "Faculdade")
        self.assertEqual(inst.id, 6)

    def test_buscar_por_id_sucesso(self):
        obj = Mock()
        self.mock_repo.buscar_por_id.return_value = obj
        self.assertEqual(self.service.buscar_por_id(1), obj)

    def test_buscar_por_id_inexistente(self):
        self.mock_repo.buscar_por_id.return_value = None
        with self.assertRaisesRegex(ValueError, "não encontrada"):
            self.service.buscar_por_id(999)

    # -- BUSCAS --

    def test_buscar_por_cnpj_sucesso(self):
        obj = Mock()
        self.mock_repo.buscar_por_cnpj.return_value = obj
        self.assertEqual(self.service.buscar_por_cnpj("12345678000190"), obj)

    def test_buscar_por_cnpj_inexistente(self):
        self.mock_repo.buscar_por_cnpj.return_value = None
        with self.assertRaisesRegex(ValueError, "não encontrada"):
            self.service.buscar_por_cnpj("00000000000000")

    def test_buscar_por_nome(self):
        self.mock_repo.buscar_por_nome.return_value = [Mock()]
        self.assertEqual(len(self.service.buscar_por_nome("Alpha")), 1)

    def test_buscar_por_tipo(self):
        self.mock_repo.buscar_por_tipo.return_value = [Mock()]
        self.assertEqual(len(self.service.buscar_por_tipo("Universidade")), 1)

    def test_buscar_credenciadas(self):
        self.mock_repo.buscar_credenciadas.return_value = [Mock(), Mock()]
        self.assertEqual(len(self.service.buscar_credenciadas()), 2)

    def test_buscar_por_modalidade(self):
        self.mock_repo.buscar_por_modalidade.return_value = [Mock()]
        self.assertEqual(len(self.service.buscar_por_modalidade("ead")), 1)

    def test_listar(self):
        self.mock_repo.listar.return_value = [Mock(), Mock()]
        self.assertEqual(len(self.service.listar()), 2)

    # -- CONTAGEM --

    def test_contar_total(self):
        self.mock_repo.contar_total.return_value = 5
        self.assertEqual(self.service.contar_total(), 5)

    def test_contar_credenciadas(self):
        self.mock_repo.contar_credenciadas.return_value = 3
        self.assertEqual(self.service.contar_credenciadas(), 3)

    # -- AÇÕES DE NEGÓCIO --

    def test_deletar(self):
        self.mock_repo.buscar_por_id.return_value = Mock()
        self.service.deletar(1)
        self.mock_repo.deletar.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
