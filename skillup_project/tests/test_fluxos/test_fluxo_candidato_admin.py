"""
Testes automatizados para FluxoCandidatoAdmin
"""
import pytest
from unittest.mock import MagicMock, patch

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.aplicacao.fluxo_candidato_admin import FluxoCandidatoAdmin


class TestFluxoCandidatoAdminInicializacao:
    """Testes de inicialização"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_candidato": MagicMock(),
            "service_candidatura": MagicMock(),
            "service_inscricao_curso": MagicMock(),
            "service_curso_ead": MagicMock(),
            "service_curso_presencial": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        return FluxoCandidatoAdmin(**mock_services)

    def test_inicializacao_servicos(self, fluxo, mock_services):
        """Verifica inicialização dos serviços"""
        assert fluxo.service == mock_services["service_candidato"]
        assert fluxo.service_candidatura == mock_services["service_candidatura"]

    def test_candidato_selecionado_inicial_none(self, fluxo):
        """Verifica estado inicial"""
        assert fluxo.candidato_selecionado is None


class TestFluxoCandidatoAdminMenu:
    """Testes do menu principal"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_candidato": MagicMock(),
            "service_candidatura": MagicMock(),
            "service_inscricao_curso": MagicMock(),
            "service_curso_ead": MagicMock(),
            "service_curso_presencial": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        return FluxoCandidatoAdmin(**mock_services)

    def test_processar_opcao_sair(self, fluxo):
        """Testa opção de sair"""
        result = fluxo._processar_opcao_principal("7")
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
        candidato = MagicMock(id=1, nome="Teste")
        fluxo.service.buscar_por_id.return_value = candidato
        fluxo._buscar_por_id()
        fluxo.service.buscar_por_id.assert_called_once_with(1)