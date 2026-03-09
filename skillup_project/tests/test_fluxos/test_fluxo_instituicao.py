"""
Testes automatizados para FluxoInstituicao
"""
import pytest
from unittest.mock import MagicMock, patch
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.aplicacao.fluxo_instituicao import FluxoInstituicao

class TestFluxoInstituicaoInicializacao:
    """Testes de inicialização"""

    @pytest.fixture
    def mock_service_instituicao(self):
        return MagicMock()

    @pytest.fixture
    def fluxo(self, mock_service_instituicao):
        return FluxoInstituicao(service_instituicao=mock_service_instituicao)

    def test_inicializacao_servicos(self, fluxo, mock_service_instituicao):
        """Verifica inicialização dos serviços"""
        assert fluxo.service == mock_service_instituicao

    def test_instituicao_logada_inicial_none(self, fluxo):
        """Verifica estado inicial"""
        assert fluxo.instituicao_logada is None


class TestFluxoInstituicaoAutenticacao:
    """Testes do menu de autenticação"""

    @pytest.fixture
    def mock_service_instituicao(self):
        return MagicMock()

    @pytest.fixture
    def fluxo(self, mock_service_instituicao):
        return FluxoInstituicao(service_instituicao=mock_service_instituicao)

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


class TestFluxoInstituicaoMenuPrincipal:
    """Testes do menu principal"""

    @pytest.fixture
    def mock_service_instituicao(self):
        return MagicMock()

    @pytest.fixture
    def fluxo(self, mock_service_instituicao):
        fluxo = FluxoInstituicao(service_instituicao=mock_service_instituicao)
        fluxo.instituicao_logada = MagicMock() # Simula login
        return fluxo

    def test_processar_opcao_sair(self, fluxo):
        """Testa opção de sair"""
        # Opção 6 é sair
        result = fluxo._processar_opcao_menu_principal("6")
        assert result == False

    @patch('builtins.input', return_value='')
    @patch('os.system')
    def test_processar_opcao_invalida(self, mock_os, mock_input, fluxo):
        """Testa opção inválida"""
        result = fluxo._processar_opcao_menu_principal("99")
        assert result == True

    @patch('builtins.input', return_value='')
    @patch('os.system')
    def test_publicar_curso_em_desenvolvimento(self, mock_os, mock_input, fluxo):
        """Testa menu publicar curso (feature flag/TODO)"""
        fluxo._publicar_curso()
        # Confirma que input foi chamado (pausa na tela)
        assert mock_input.called
