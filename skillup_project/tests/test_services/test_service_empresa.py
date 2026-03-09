import unittest
from unittest.mock import Mock
from src.services.services_empresa import EmpresaService
from src.interfaces.interface_empresa import IEmpresa


class TestServiceEmpresa(unittest.TestCase):
    """Testes do serviço de Empresa."""

    def setUp(self):
        self.mock_repo = Mock(spec=IEmpresa)
        self.service = EmpresaService(self.mock_repo)

    def test_cadastrar_sucesso(self):
        self.mock_repo.listar.return_value = []
        e = self.service.cadastrar("Tech SA", "12345678000199", "medio")
        self.mock_repo.salvar.assert_called_once()
        self.assertEqual(e.nome, "Tech SA")
        self.assertEqual(e.id, 1)

    def test_cadastrar_cnpj_duplicado(self):
        existente = Mock()
        existente.cnpj = "12345678000199"
        self.mock_repo.listar.return_value = [existente]
        with self.assertRaisesRegex(ValueError, "Já existe empresa com este CNPJ"):
            self.service.cadastrar("Outra SA", "12345678000199", "grande")

    def test_cadastrar_id_incremental(self):
        existente = Mock()
        existente.id = 3
        existente.cnpj = "99999999000100"
        self.mock_repo.listar.return_value = [existente]
        e = self.service.cadastrar("Nova SA", "12345678000199", "pequeno")
        self.assertEqual(e.id, 4)

    def test_buscar_por_id_sucesso(self):
        empresa_mock = Mock()
        self.mock_repo.buscar_por_id.return_value = empresa_mock
        resultado = self.service.buscar_por_id(1)
        self.assertEqual(resultado, empresa_mock)

    def test_buscar_por_id_inexistente(self):
        self.mock_repo.buscar_por_id.return_value = None
        with self.assertRaisesRegex(ValueError, "Empresa não encontrada"):
            self.service.buscar_por_id(999)

    def test_listar(self):
        self.mock_repo.listar.return_value = [Mock(), Mock()]
        resultado = self.service.listar()
        self.assertEqual(len(resultado), 2)

    def test_buscar_por_filtros(self):
        """Testa busca por filtros dinâmicos"""
        self.mock_repo.buscar_por_filtros.return_value = [Mock()]
        resultado = self.service.buscar_por_filtros(porte="medio")
        self.assertEqual(len(resultado), 1)
        self.mock_repo.buscar_por_filtros.assert_called_once_with(porte="medio")

    def test_deletar(self):
        self.mock_repo.buscar_por_id.return_value = Mock()
        self.service.deletar(1)
        self.mock_repo.deletar.assert_called_once_with(1)

    def test_listar_formatado(self):
        e = Mock()
        e.__str__ = lambda self: "Empresa X"
        self.mock_repo.listar.return_value = [e]
        resultado = self.service.listar_formatado()
        self.assertEqual(len(resultado), 1)
        self.assertIsInstance(resultado[0], str)

    def test_atualizar(self):
        """Testa atualização de empresa"""
        empresa = Mock()
        self.mock_repo.buscar_por_id.return_value = empresa
        self.service.atualizar(1, "nome", "Novo Nome")
        empresa.atualizar_dado.assert_called_once_with("nome", "Novo Nome")
        self.mock_repo.atualizar.assert_called_once()


if __name__ == "__main__":
    unittest.main()
