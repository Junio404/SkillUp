import unittest
from unittest.mock import Mock
from src.services.service_candidato import CandidatoService
from src.interfaces.interface_candidato import ICandidatoRepositorio


class TestServiceCandidato(unittest.TestCase):
    """Testes do serviço de Candidato."""

    def setUp(self):
        self.mock_repo = Mock(spec=ICandidatoRepositorio)
        self.service = CandidatoService(self.mock_repo)

    def test_cadastrar_sucesso(self):
        self.mock_repo.listar.return_value = []
        c = self.service.cadastrar("Maria", "11122233344", "maria@email.com", ["TI"], "Superior", "SP")
        self.mock_repo.salvar.assert_called_once()
        self.assertEqual(c.nome, "Maria")
        self.assertEqual(c.id, 1)
        self.assertEqual(c.localidade, "SP")

    def test_cadastrar_id_incremental(self):
        existente = Mock()
        existente.id = 5
        existente.cpf = "99988877766"
        self.mock_repo.listar.return_value = [existente]
        c = self.service.cadastrar("João", "22233344455", "joao@email.com", ["TI"], "Médio")
        self.assertEqual(c.id, 6)

    def test_cadastrar_cpf_duplicado(self):
        existente = Mock()
        existente.cpf = "11122233344"
        self.mock_repo.listar.return_value = [existente]
        with self.assertRaisesRegex(ValueError, "Já existe candidato com este CPF"):
            self.service.cadastrar("Maria", "11122233344", "maria@email.com", ["TI"], "Superior")

    def test_buscar_por_id_sucesso(self):
        candidato_mock = Mock()
        self.mock_repo.buscar_por_id.return_value = candidato_mock
        resultado = self.service.buscar_por_id(1)
        self.assertEqual(resultado, candidato_mock)

    def test_buscar_por_id_inexistente(self):
        self.mock_repo.buscar_por_id.return_value = None
        with self.assertRaisesRegex(ValueError, "Candidato não encontrado"):
            self.service.buscar_por_id(999)

    def test_listar(self):
        self.mock_repo.listar.return_value = [Mock(), Mock()]
        resultado = self.service.listar()
        self.assertEqual(len(resultado), 2)

    def test_buscar_por_cpf_sucesso(self):
        candidato_mock = Mock()
        self.mock_repo.buscar_por_cpf.return_value = candidato_mock
        resultado = self.service.buscar_por_cpf("11122233344")
        self.assertEqual(resultado, candidato_mock)

    def test_buscar_por_cpf_inexistente(self):
        self.mock_repo.buscar_por_cpf.return_value = None
        with self.assertRaisesRegex(ValueError, "Candidato não encontrado"):
            self.service.buscar_por_cpf("99999999999")

    def test_buscar_por_email_sucesso(self):
        candidato_mock = Mock()
        self.mock_repo.buscar_por_email.return_value = candidato_mock
        resultado = self.service.buscar_por_email("maria@email.com")
        self.assertEqual(resultado, candidato_mock)

    def test_buscar_por_email_inexistente(self):
        self.mock_repo.buscar_por_email.return_value = None
        with self.assertRaisesRegex(ValueError, "Candidato não encontrado"):
            self.service.buscar_por_email("nao@existe.com")

    def test_deletar(self):
        self.mock_repo.buscar_por_id.return_value = Mock()
        self.service.deletar(1)
        self.mock_repo.deletar.assert_called_once_with(1)

    def test_buscar_por_area_interesse(self):
        self.mock_repo.buscar_por_area_interesse.return_value = [Mock()]
        resultado = self.service.buscar_por_area_interesse("TI")
        self.assertEqual(len(resultado), 1)

    def test_buscar_por_nivel_formacao(self):
        self.mock_repo.buscar_por_nivel_formacao.return_value = [Mock(), Mock()]
        resultado = self.service.buscar_por_nivel_formacao("Superior")
        self.assertEqual(len(resultado), 2)

    def test_buscar_por_filtros(self):
        self.mock_repo.buscar_por_filtros.return_value = [Mock()]
        resultado = self.service.buscar_por_filtros(nome="Maria")
        self.assertEqual(len(resultado), 1)

    def test_listar_formatado(self):
        c1 = Mock()
        c1.__str__ = lambda self: "Candidato 1"
        c2 = Mock()
        c2.__str__ = lambda self: "Candidato 2"
        self.mock_repo.listar.return_value = [c1, c2]
        resultado = self.service.listar_formatado()
        self.assertEqual(len(resultado), 2)
        self.assertIsInstance(resultado[0], str)

    def test_contar_total(self):
        self.mock_repo.contar_total.return_value = 5
        self.assertEqual(self.service.contar_total(), 5)

    # --- Testes de Currículo ---

    def test_inicializar_curriculo(self):
        candidato = Mock()
        candidato.curriculo = None
        self.mock_repo.buscar_por_id.return_value = candidato
        self.service.inicializar_curriculo(1)
        candidato.inicializar_curriculo.assert_called_once()
        self.mock_repo.atualizar.assert_called_once_with(candidato)

    def test_obter_curriculo(self):
        candidato = Mock()
        candidato.curriculo = {"objetivo": "Dev", "experiencias": []}
        self.mock_repo.buscar_por_id.return_value = candidato
        resultado = self.service.obter_curriculo(1)
        self.assertEqual(resultado["objetivo"], "Dev")

    def test_atualizar_objetivo_curriculo(self):
        candidato = Mock()
        self.mock_repo.buscar_por_id.return_value = candidato
        self.service.atualizar_objetivo_curriculo(1, "Desenvolvedor Python")
        candidato.atualizar_objetivo_curriculo.assert_called_once_with("Desenvolvedor Python")
        self.mock_repo.atualizar.assert_called_once()

    def test_atualizar_resumo_curriculo(self):
        candidato = Mock()
        self.mock_repo.buscar_por_id.return_value = candidato
        self.service.atualizar_resumo_curriculo(1, "5 anos de experiência")
        candidato.atualizar_resumo_curriculo.assert_called_once_with("5 anos de experiência")
        self.mock_repo.atualizar.assert_called_once()

    def test_adicionar_experiencia(self):
        candidato = Mock()
        self.mock_repo.buscar_por_id.return_value = candidato
        self.service.adicionar_experiencia(1, "Tech Corp", "Dev", "Descrição", "2020-01", "2023-06")
        candidato.adicionar_experiencia.assert_called_once_with("Tech Corp", "Dev", "Descrição", "2020-01", "2023-06")
        self.mock_repo.atualizar.assert_called_once()

    def test_remover_experiencia(self):
        candidato = Mock()
        self.mock_repo.buscar_por_id.return_value = candidato
        self.service.remover_experiencia(1, 0)
        candidato.remover_experiencia.assert_called_once_with(0)
        self.mock_repo.atualizar.assert_called_once()

    def test_listar_experiencias(self):
        candidato = Mock()
        candidato.listar_experiencias.return_value = [{"empresa": "Tech", "cargo": "Dev"}]
        self.mock_repo.buscar_por_id.return_value = candidato
        resultado = self.service.listar_experiencias(1)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["empresa"], "Tech")

    def test_adicionar_formacao(self):
        candidato = Mock()
        self.mock_repo.buscar_por_id.return_value = candidato
        self.service.adicionar_formacao(1, "USP", "CC", "Graduação", "2015-03", "2019-12")
        candidato.adicionar_formacao.assert_called_once_with("USP", "CC", "Graduação", "2015-03", "2019-12")
        self.mock_repo.atualizar.assert_called_once()

    def test_remover_formacao(self):
        candidato = Mock()
        self.mock_repo.buscar_por_id.return_value = candidato
        self.service.remover_formacao(1, 0)
        candidato.remover_formacao.assert_called_once_with(0)
        self.mock_repo.atualizar.assert_called_once()

    def test_listar_formacoes(self):
        candidato = Mock()
        candidato.listar_formacoes.return_value = [{"instituicao": "USP", "curso": "CC"}]
        self.mock_repo.buscar_por_id.return_value = candidato
        resultado = self.service.listar_formacoes(1)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0]["instituicao"], "USP")


if __name__ == "__main__":
    unittest.main()
