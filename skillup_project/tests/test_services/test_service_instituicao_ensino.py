import unittest
from unittest.mock import Mock, MagicMock
from src.services.service_instituicao_ensino import ServiceInstituicaoEnsino
from src.dominio.instituicao_ensino import InstituicaoEnsino


class TestServiceInstituicaoEnsino(unittest.TestCase):
    """Testes do serviço de InstituicaoEnsino."""

    def setUp(self):
        self.mock_repo_instituicao = MagicMock()
        self.mock_repo_curso = MagicMock()
        self.service = ServiceInstituicaoEnsino(
            self.mock_repo_instituicao, 
            self.mock_repo_curso
        )

    # -- CRUD --

    def test_criar_conta_sucesso(self):
        """Testa criação de conta com sucesso"""
        self.mock_repo_instituicao.buscar_por_cnpj.return_value = None
        instituicao = MagicMock(spec=InstituicaoEnsino)
        instituicao.cnpj = "12345678000190"
        
        resultado = self.service.criar_conta(instituicao)
        
        self.mock_repo_instituicao.salvar.assert_called_once_with(instituicao)
        self.assertEqual(resultado, instituicao)

    def test_criar_conta_cnpj_duplicado(self):
        """Testa erro ao criar conta com CNPJ duplicado"""
        self.mock_repo_instituicao.buscar_por_cnpj.return_value = MagicMock()
        instituicao = MagicMock(spec=InstituicaoEnsino)
        instituicao.cnpj = "12345678000190"
        
        with self.assertRaisesRegex(ValueError, "Já existe uma instituição com este CNPJ"):
            self.service.criar_conta(instituicao)

    def test_buscar_por_id_sucesso(self):
        """Testa busca por ID com sucesso"""
        obj = MagicMock()
        self.mock_repo_instituicao.buscar_por_id.return_value = obj
        
        resultado = self.service.buscar_por_id(1)
        
        self.assertEqual(resultado, obj)
        self.mock_repo_instituicao.buscar_por_id.assert_called_once_with(1)

    def test_buscar_por_id_inexistente(self):
        """Testa busca por ID inexistente retorna None"""
        self.mock_repo_instituicao.buscar_por_id.return_value = None
        
        resultado = self.service.buscar_por_id(999)
        
        self.assertIsNone(resultado)

    def test_buscar_por_cnpj_sucesso(self):
        """Testa busca por CNPJ com sucesso"""
        obj = MagicMock()
        self.mock_repo_instituicao.buscar_por_cnpj.return_value = obj
        
        resultado = self.service.buscar_por_cnpj("12345678000190")
        
        self.assertEqual(resultado, obj)

    def test_buscar_por_cnpj_inexistente(self):
        """Testa busca por CNPJ inexistente retorna None"""
        self.mock_repo_instituicao.buscar_por_cnpj.return_value = None
        
        resultado = self.service.buscar_por_cnpj("00000000000000")
        
        self.assertIsNone(resultado)

    def test_listar(self):
        """Testa listagem de instituições"""
        instituicoes = [MagicMock(), MagicMock()]
        self.mock_repo_instituicao.listar.return_value = instituicoes
        
        resultado = self.service.listar()
        
        self.assertEqual(len(resultado), 2)

    def test_fazer_login_sucesso(self):
        """Testa login de instituição com sucesso"""
        instituicao = MagicMock()
        self.mock_repo_instituicao.buscar_por_id.return_value = instituicao
        
        resultado = self.service.fazer_login(1)
        
        self.assertEqual(resultado, instituicao)

    def test_fazer_login_instituicao_inexistente(self):
        """Testa login com instituição inexistente"""
        self.mock_repo_instituicao.buscar_por_id.return_value = None
        
        resultado = self.service.fazer_login(999)
        
        self.assertIsNone(resultado)

    def test_cadastrar_curso_sucesso(self):
        """Testa cadastro de curso com sucesso"""
        instituicao = MagicMock()
        instituicao.validar_publicacao.return_value = None
        curso = MagicMock()
        
        resultado = self.service.cadastrar_curso(instituicao, curso)
        
        self.assertTrue(resultado)
        self.mock_repo_curso.salvar.assert_called_once_with(curso)

    def test_cadastrar_curso_sem_permissao(self):
        """Testa cadastro de curso sem permissão"""
        instituicao = MagicMock()
        instituicao.validar_publicacao.side_effect = PermissionError("Não credenciada")
        curso = MagicMock()
        
        resultado = self.service.cadastrar_curso(instituicao, curso)
        
        self.assertFalse(resultado)
        self.mock_repo_curso.salvar.assert_not_called()

    def test_listar_cursos(self):
        """Testa listagem de cursos de uma instituição"""
        cursos = [MagicMock(), MagicMock()]
        self.mock_repo_curso.listar_por_instituicao.return_value = cursos
        
        resultado = self.service.listar_cursos(1)
        
        self.assertEqual(len(resultado), 2)
        self.mock_repo_curso.listar_por_instituicao.assert_called_once_with(1)


if __name__ == "__main__":
    unittest.main()
