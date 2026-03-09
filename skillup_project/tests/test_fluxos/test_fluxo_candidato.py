"""
Testes automatizados para FluxoCandidato
"""
import pytest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.aplicacao.fluxo_candidato import FluxoCandidato

class TestFluxoCandidatoInicializacao:
    """Testes de inicialização"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_candidato": MagicMock(),
            "motor_busca_vagas": MagicMock(),
            "service_candidatura": MagicMock(),
            "service_inscricao_curso": MagicMock(),
            "service_curso_ead": MagicMock(),
            "service_curso_presencial": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        return FluxoCandidato(**mock_services)

    def test_inicializacao_servicos(self, fluxo, mock_services):
        """Verifica inicialização dos serviços"""
        assert fluxo.service == mock_services["service_candidato"]
        assert fluxo.motor_busca_vagas == mock_services["motor_busca_vagas"]
        assert fluxo.service_candidatura == mock_services["service_candidatura"]
        assert fluxo.service_inscricao_curso == mock_services["service_inscricao_curso"]
        assert fluxo.service_curso_ead == mock_services["service_curso_ead"]
        assert fluxo.service_curso_presencial == mock_services["service_curso_presencial"]

    def test_candidato_logado_inicial_none(self, fluxo):
        """Verifica estado inicial"""
        assert fluxo.candidato_logado is None


class TestFluxoCandidatoAutenticacao:
    """Testes do menu de autenticação"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_candidato": MagicMock(),
            "motor_busca_vagas": MagicMock(),
            "service_candidatura": MagicMock(),
            "service_inscricao_curso": MagicMock(),
            "service_curso_ead": MagicMock(),
            "service_curso_presencial": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        return FluxoCandidato(**mock_services)

    def test_processar_opcao_voltar(self, fluxo):
        """Testa opção de voltar na autenticação"""
        # Opção 3 é voltar, deve retornar False
        result = fluxo._processar_opcao_autenticacao("3")
        assert result == False

    @patch('builtins.input', return_value='')
    @patch('os.system')
    def test_processar_opcao_invalida(self, mock_os, mock_input, fluxo):
        """Testa opção inválida na autenticação"""
        result = fluxo._processar_opcao_autenticacao("99")
        assert result == True

    @patch('builtins.input', return_value='')
    @patch('os.system')
    def test_processar_entrada_nao_numerica(self, mock_os, mock_input, fluxo):
        """Testa entrada não numérica"""
        result = fluxo._processar_opcao_autenticacao("abc")
        assert result == True


class TestFluxoCandidatoMenuPrincipal:
    """Testes do menu principal"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_candidato": MagicMock(),
            "motor_busca_vagas": MagicMock(),
            "service_candidatura": MagicMock(),
            "service_inscricao_curso": MagicMock(),
            "service_curso_ead": MagicMock(),
            "service_curso_presencial": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        fluxo = FluxoCandidato(**mock_services)
        # Simula usuário logado
        fluxo.candidato_logado = MagicMock()
        fluxo.candidato_logado.nome = "Teste"
        return fluxo

    def test_processar_opcao_sair(self, fluxo):
        """Testa opção de sair"""
        # Opção 6 é sair, deve retornar False
        result = fluxo._processar_opcao_menu_principal("6")
        assert result == False

    @patch('builtins.input', return_value='')
    @patch('os.system')
    def test_processar_opcao_invalida(self, mock_os, mock_input, fluxo):
        """Testa opção inválida"""
        result = fluxo._processar_opcao_menu_principal("99")
        assert result == True

    @patch('builtins.input', side_effect=['', ''])
    @patch('os.system')
    def test_explorar_vagas_sem_vagas(self, mock_os, mock_input, fluxo):
        """Testa explorar vagas sem retorno"""
        fluxo.motor_busca_vagas.buscar_por_candidato.return_value = []
        fluxo._explorar_vagas()
        fluxo.motor_busca_vagas.buscar_por_candidato.assert_called_once()
