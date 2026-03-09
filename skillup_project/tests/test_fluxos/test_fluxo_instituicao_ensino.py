"""
Testes automatizados para FluxoInstituicaoAdmin
"""
import pytest
from unittest.mock import MagicMock, patch

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from src.aplicacao.fluxo_instituicao_admin import FluxoInstituicaoAdmin


class TestFluxoInstituicaoAdminInicializacao:
    """Testes de inicialização"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_area_ensino": MagicMock(),
            "service_instituicao_area": MagicMock(),
            "service_curso_ead": MagicMock(),
            "service_curso_presencial": MagicMock(),
            "service_curso_competencia": MagicMock(),
            "service_inscricao_curso": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        return FluxoInstituicaoAdmin(**mock_services)

    def test_inicializacao_servicos(self, fluxo, mock_services):
        """Verifica inicialização dos serviços"""
        assert fluxo.service_area_ensino == mock_services["service_area_ensino"]
        assert fluxo.service_curso_ead == mock_services["service_curso_ead"]


class TestFluxoInstituicaoAdminMenu:
    """Testes do menu principal"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_area_ensino": MagicMock(),
            "service_instituicao_area": MagicMock(),
            "service_curso_ead": MagicMock(),
            "service_curso_presencial": MagicMock(),
            "service_curso_competencia": MagicMock(),
            "service_inscricao_curso": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        return FluxoInstituicaoAdmin(**mock_services)

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

    @patch('builtins.input', return_value='')
    @patch('os.system')
    def test_listar_areas(self, mock_os, mock_input, fluxo):
        """Testa listagem de áreas"""
        fluxo.service_area_ensino.listar_todas.return_value = []
        fluxo._listar_areas()
        fluxo.service_area_ensino.listar_todas.assert_called_once()