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
            "service_competencia_candidato": MagicMock(),
            "service_competencia": MagicMock(),
            "service_recomendacao": MagicMock(),
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
            "service_competencia_candidato": MagicMock(),
            "service_competencia": MagicMock(),
            "service_recomendacao": MagicMock(),
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
        # Opção 8 é sair, deve retornar False
        result = fluxo._processar_opcao_menu_principal("8")
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


class TestFluxoCandidatoCompetencias:
    """Testes de gerenciamento de competências do candidato"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_candidato": MagicMock(),
            "motor_busca_vagas": MagicMock(),
            "service_candidatura": MagicMock(),
            "service_inscricao_curso": MagicMock(),
            "service_curso_ead": MagicMock(),
            "service_curso_presencial": MagicMock(),
            "service_competencia_candidato": MagicMock(),
            "service_competencia": MagicMock(),
            "service_recomendacao": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        fluxo = FluxoCandidato(**mock_services)
        fluxo.candidato_logado = MagicMock()
        fluxo.candidato_logado.id = 1
        fluxo.candidato_logado.nome = "Teste"
        return fluxo

    @patch('builtins.input', return_value='5')  # Voltar
    @patch('os.system')
    def test_gerenciar_competencias_voltar(self, mock_os, mock_input, fluxo):
        """Testa menu de competências - opção voltar"""
        fluxo._gerenciar_competencias()
        # Deve encerrar sem erro

    @patch('builtins.input', side_effect=['1', '', '5'])  # Listar, enter, voltar
    @patch('os.system')
    def test_listar_competencias_candidato(self, mock_os, mock_input, fluxo, mock_services):
        """Testa listagem de competências do candidato"""
        mock_competencias = [MagicMock(competencia_id=1, nivel='Intermediário')]
        mock_competencias[0].competencia_id = 1
        mock_competencias[0].nivel = 'Intermediário'
        mock_services["service_competencia_candidato"].listar_por_candidato.return_value = mock_competencias
        mock_services["service_competencia"].obter_por_id.return_value = MagicMock(nome="Python")
        
        fluxo._gerenciar_competencias()
        
        mock_services["service_competencia_candidato"].listar_por_candidato.assert_called()

    @patch('builtins.input', side_effect=['2', '1', 'Avançado', '', '5'])  # Adicionar competência
    @patch('os.system')
    def test_adicionar_competencia(self, mock_os, mock_input, fluxo, mock_services):
        """Testa adição de competência ao candidato"""
        mock_competencia = MagicMock(id=1, nome="Python")
        mock_services["service_competencia"].listar_todas.return_value = [mock_competencia]
        mock_services["service_competencia_candidato"].cadastrar.return_value = MagicMock()
        
        fluxo._gerenciar_competencias()
        
        mock_services["service_competencia_candidato"].cadastrar.assert_called()

    @patch('builtins.input', side_effect=['4', '1', '', '5'])  # Remover competência
    @patch('os.system')
    def test_remover_competencia(self, mock_os, mock_input, fluxo, mock_services):
        """Testa remoção de competência do candidato"""
        mock_comp_cand = MagicMock(id=1, competencia_id=1, nivel='Básico')
        mock_competencia = MagicMock(id=1, nome="Python")
        mock_services["service_competencia_candidato"].listar_por_candidato.return_value = [mock_comp_cand]
        mock_services["service_competencia"].obter_por_id.return_value = mock_competencia
        
        fluxo._gerenciar_competencias()
        
        mock_services["service_competencia_candidato"].remover.assert_called()


class TestFluxoCandidatoRecomendacoes:
    """Testes de recomendações para o candidato"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_candidato": MagicMock(),
            "motor_busca_vagas": MagicMock(),
            "service_candidatura": MagicMock(),
            "service_inscricao_curso": MagicMock(),
            "service_curso_ead": MagicMock(),
            "service_curso_presencial": MagicMock(),
            "service_competencia_candidato": MagicMock(),
            "service_competencia": MagicMock(),
            "service_recomendacao": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        fluxo = FluxoCandidato(**mock_services)
        fluxo.candidato_logado = MagicMock()
        fluxo.candidato_logado.id = 1
        fluxo.candidato_logado.nome = "Teste"
        return fluxo

    @patch('builtins.input', return_value='')
    @patch('os.system')
    def test_ver_recomendacoes_com_resultados(self, mock_os, mock_input, fluxo, mock_services):
        """Testa visualização de recomendações com resultados"""
        mock_item_vaga = MagicMock()
        mock_item_vaga.pontuacao = 85
        mock_item_vaga.item.titulo = "Dev Python"
        mock_item_vaga.item.area = "Tecnologia"
        mock_item_vaga.item.modalidade.value = "Remoto"
        
        mock_item_curso = MagicMock()
        mock_item_curso.pontuacao = 75
        mock_item_curso.item.nome = "Curso Python"
        mock_item_curso.item.area = "Tecnologia"
        mock_item_curso.item.carga_horaria = 40
        
        mock_recomendacao = MagicMock()
        mock_recomendacao.vagas = [mock_item_vaga]
        mock_recomendacao.cursos = [mock_item_curso]
        mock_services["service_recomendacao"].recomendar.return_value = mock_recomendacao
        
        fluxo._ver_recomendacoes()
        
        mock_services["service_recomendacao"].recomendar.assert_called_once()

    @patch('builtins.input', return_value='')
    @patch('os.system')
    def test_ver_recomendacoes_sem_resultados(self, mock_os, mock_input, fluxo, mock_services):
        """Testa visualização de recomendações sem resultados"""
        mock_recomendacao = MagicMock()
        mock_recomendacao.vagas = []
        mock_recomendacao.cursos = []
        mock_services["service_recomendacao"].recomendar.return_value = mock_recomendacao
        
        fluxo._ver_recomendacoes()
        
        mock_services["service_recomendacao"].recomendar.assert_called_once()

    @patch('builtins.input', return_value='')
    @patch('os.system')
    def test_ver_recomendacoes_sem_servico(self, mock_os, mock_input, fluxo):
        """Testa visualização de recomendações sem serviço configurado"""
        fluxo.service_recomendacao = None
        
        fluxo._ver_recomendacoes()
        # Não deve quebrar, apenas exibir mensagem
