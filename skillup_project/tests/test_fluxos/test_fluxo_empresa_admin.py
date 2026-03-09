"""
Testes automatizados para FluxoEmpresaAdmin
"""
import pytest
from unittest.mock import MagicMock, patch

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.aplicacao.fluxo_empresa_admin import FluxoEmpresaAdmin


class TestFluxoEmpresaAdminInicializacao:
    """Testes de inicialização"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_empresa": MagicMock(),
            "service_vaga_clt": MagicMock(),
            "service_vaga_estagio": MagicMock(),
            "service_requisito_vaga": MagicMock(),
            "service_candidatura": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        return FluxoEmpresaAdmin(**mock_services)

    def test_inicializacao_servicos(self, fluxo, mock_services):
        """Verifica inicialização dos serviços"""
        assert fluxo.service_empresa == mock_services["service_empresa"]
        assert fluxo.service_vaga_clt == mock_services["service_vaga_clt"]

    def test_empresa_selecionada_inicial_none(self, fluxo):
        """Verifica estado inicial"""
        assert fluxo.empresa_selecionada is None


class TestFluxoEmpresaAdminMenu:
    """Testes do menu principal"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_empresa": MagicMock(),
            "service_vaga_clt": MagicMock(),
            "service_vaga_estagio": MagicMock(),
            "service_requisito_vaga": MagicMock(),
            "service_candidatura": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        return FluxoEmpresaAdmin(**mock_services)

    def test_processar_opcao_sair(self, fluxo):
        """Testa opção de sair"""
        result = fluxo._processar_opcao_principal("8")
        assert result == False

    @patch('builtins.input', return_value='')
    @patch('os.system')
    def test_processar_opcao_invalida(self, mock_os, mock_input, fluxo):
        """Testa opção inválida"""
        result = fluxo._processar_opcao_principal("99")
        assert result == True

    @patch('builtins.input', side_effect=['1', ''])
    @patch('os.system')
    def test_buscar_por_id(self, mock_os, mock_input, fluxo):
        """Testa busca por ID"""
        empresa = MagicMock(id=1, nome="Empresa Teste")
        fluxo.service_empresa.buscar_por_id.return_value = empresa
        fluxo._buscar_por_id()
        fluxo.service_empresa.buscar_por_id.assert_called_once_with(1)