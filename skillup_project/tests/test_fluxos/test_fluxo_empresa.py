"""
Testes automatizados para FluxoEmpresa
"""
import pytest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.aplicacao.fluxo_empresa import FluxoEmpresa

class TestFluxoEmpresaInicializacao:
    """Testes de inicialização"""

    @pytest.fixture
    def mock_service_empresa(self):
        return MagicMock()

    @pytest.fixture
    def fluxo(self, mock_service_empresa):
        return FluxoEmpresa(service_empresa=mock_service_empresa)

    def test_inicializacao_servicos(self, fluxo, mock_service_empresa):
        """Verifica inicialização dos serviços"""
        assert fluxo.service == mock_service_empresa

    def test_empresa_logada_inicial_none(self, fluxo):
        """Verifica estado inicial"""
        assert fluxo.empresa_logada is None


class TestFluxoEmpresaAutenticacao:
    """Testes do menu de autenticação"""

    @pytest.fixture
    def mock_service_empresa(self):
        return MagicMock()

    @pytest.fixture
    def fluxo(self, mock_service_empresa):
        return FluxoEmpresa(service_empresa=mock_service_empresa)

    def test_processar_opcao_voltar(self, fluxo):
        """Testa opção de voltar na autenticação"""
        # Opção 3 é voltar
        result = fluxo._processar_opcao_autenticacao("3")
        assert result == False

    @patch('builtins.input', return_value='')
    @patch('os.system')
    def test_processar_opcao_invalida(self, mock_os, mock_input, fluxo):
        """Testa opção inválida"""
        result = fluxo._processar_opcao_autenticacao("99")
        assert result == True


class TestFluxoEmpresaMenuPrincipal:
    """Testes do menu principal"""

    @pytest.fixture
    def mock_service_empresa(self):
        return MagicMock()

    @pytest.fixture
    def fluxo(self, mock_service_empresa):
        fluxo = FluxoEmpresa(service_empresa=mock_service_empresa)
        fluxo.empresa_logada = MagicMock()
        fluxo.empresa_logada.nome = "Empresa Teste"
        return fluxo

    def test_processar_opcao_sair(self, fluxo):
        """Testa opção de sair"""
        # Opção 7 é sair
        result = fluxo._processar_opcao_menu_principal("7")
        assert result == False

    @patch('builtins.input', return_value='')
    @patch('os.system')
    def test_processar_opcao_invalida(self, mock_os, mock_input, fluxo):
        """Testa opção inválida"""
        result = fluxo._processar_opcao_menu_principal("99")
        assert result == True

    @patch('builtins.input', return_value='')
    @patch('os.system')
    def test_ver_perfil(self, mock_os, mock_input, fluxo):
        """Testa visualização de perfil"""
        fluxo._ver_perfil()
        # Apenas verifica se não quebrou e chamou input
        assert mock_input.called
