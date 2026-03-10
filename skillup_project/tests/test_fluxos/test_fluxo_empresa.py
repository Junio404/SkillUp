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

    @patch('builtins.input', return_value='3')
    @patch('os.system')
    def test_ver_perfil(self, mock_os, mock_input, fluxo):
        """Testa visualização de perfil"""
        fluxo._ver_perfil()
        # Apenas verifica se não quebrou e chamou input
        assert mock_input.called


class TestFluxoEmpresaPublicarVaga:
    """Testes de publicação de vagas"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_empresa": MagicMock(),
            "service_vaga_clt": MagicMock(),
            "service_vaga_estagio": MagicMock(),
            "service_requisito_vaga": MagicMock(),
            "service_competencia": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        fluxo = FluxoEmpresa(**mock_services)
        fluxo.empresa_logada = MagicMock()
        fluxo.empresa_logada.id = 1
        fluxo.empresa_logada.nome = "Empresa Teste"
        return fluxo

    @patch('builtins.input', side_effect=['Desenvolvedor', 'Desenvolver sistemas', 'Tecnologia', '1', '1', '5000', 'SP', '', 'n', ''])
    @patch('os.system')
    def test_publicar_vaga_clt_sucesso(self, mock_os, mock_input, fluxo, mock_services):
        """Testa publicação de vaga CLT com sucesso"""
        mock_vaga = MagicMock()
        mock_vaga.id = 1
        mock_vaga.titulo = "Desenvolvedor"
        mock_services["service_vaga_clt"].cadastrar.return_value = mock_vaga
        
        fluxo._publicar_vaga()
        
        mock_services["service_vaga_clt"].cadastrar.assert_called_once()

    @patch('builtins.input', side_effect=['Titulo', 'Descricao', 'Area', '1', '1', 'abc', ''])
    @patch('os.system')
    def test_publicar_vaga_clt_valor_invalido(self, mock_os, mock_input, fluxo):
        """Testa erro de validação na publicação"""
        fluxo._publicar_vaga()
        # Não deve quebrar, apenas mostrar erro

    @patch('builtins.input', return_value='3')
    @patch('os.system')
    def test_publicar_vaga_menu_voltar(self, mock_os, mock_input, fluxo):
        """Testa voltar do menu de publicar vaga"""
        fluxo._publicar_vaga()
        # Opção 3 volta, não deve chamar cadastrar
        assert not fluxo.service_vaga_clt.cadastrar.called

    def test_publicar_vaga_sem_servico(self, mock_services):
        """Testa publicação sem serviço de vaga"""
        fluxo = FluxoEmpresa(service_empresa=mock_services["service_empresa"])
        fluxo.empresa_logada = MagicMock()
        fluxo.empresa_logada.id = 1
        
        with patch('builtins.input', side_effect=['', '']):
            with patch('os.system'):
                fluxo._publicar_vaga()
                # Não deve quebrar


class TestFluxoEmpresaGerenciarVagas:
    """Testes de gerenciamento de vagas"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_empresa": MagicMock(),
            "service_vaga_clt": MagicMock(),
            "service_requisito_vaga": MagicMock(),
            "service_competencia": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        fluxo = FluxoEmpresa(**mock_services)
        fluxo.empresa_logada = MagicMock()
        fluxo.empresa_logada.id = 1
        return fluxo

    @patch('builtins.input', side_effect=['1', ''])  # Listar e voltar
    @patch('os.system')
    def test_listar_vagas_empresa_vazia(self, mock_os, mock_input, fluxo, mock_services):
        """Testa listar vagas quando não há vagas"""
        mock_services["service_vaga_clt"].listar_por_empresa.return_value = []
        
        fluxo._listar_vagas_empresa()
        
        mock_services["service_vaga_clt"].listar_por_empresa.assert_called_once_with(1)

    @patch('builtins.input', side_effect=['1', ''])
    @patch('os.system')
    def test_listar_vagas_empresa_com_vagas(self, mock_os, mock_input, fluxo, mock_services):
        """Testa listar vagas existentes"""
        mock_vaga = MagicMock()
        mock_vaga.id = 1
        mock_vaga.titulo = "Dev Python"
        mock_vaga.ativo = True
        mock_services["service_vaga_clt"].listar_por_empresa.return_value = [mock_vaga]
        
        fluxo._listar_vagas_empresa()
        
        assert mock_services["service_vaga_clt"].listar_por_empresa.called

    @patch('builtins.input', side_effect=['5'])  # Voltar imediatamente
    @patch('os.system')
    def test_gerenciar_vagas_voltar(self, mock_os, mock_input, fluxo):
        """Testa voltar do menu gerenciar vagas"""
        fluxo._gerenciar_vagas()
        # Não deve quebrar

    @patch('builtins.input', side_effect=['1', '', ''])
    @patch('os.system')
    def test_ver_detalhes_vaga_sucesso(self, mock_os, mock_input, fluxo, mock_services):
        """Testa ver detalhes de uma vaga"""
        mock_modalidade = MagicMock()
        mock_modalidade.value = "presencial"
        mock_tipo = MagicMock()
        mock_tipo.value = "clt"
        
        mock_vaga = MagicMock()
        mock_vaga.id = 1
        mock_vaga.titulo = "Dev Python"
        mock_vaga.descricao = "Desenvolver sistemas"
        mock_vaga.area = "Tecnologia"
        mock_vaga.salario_base = 5000.0
        mock_vaga.localidade = "SP"
        mock_vaga.modalidade = mock_modalidade
        mock_vaga.tipo = mock_tipo
        mock_vaga.ativa = True
        mock_vaga.id_empresa = 1
        mock_services["service_vaga_clt"].buscar_por_id.return_value = mock_vaga
        mock_services["service_requisito_vaga"].listar_por_vaga.return_value = []
        
        fluxo._ver_detalhes_vaga()
        
        mock_services["service_vaga_clt"].buscar_por_id.assert_called_once()

    @patch('builtins.input', side_effect=['999', ''])
    @patch('os.system')
    def test_ver_detalhes_vaga_nao_encontrada(self, mock_os, mock_input, fluxo, mock_services):
        """Testa ver detalhes de vaga inexistente"""
        mock_services["service_vaga_clt"].buscar_por_id.side_effect = ValueError("Vaga não encontrada")
        
        fluxo._ver_detalhes_vaga()
        # Não deve quebrar

    @patch('builtins.input', side_effect=['1', ''])
    @patch('os.system')
    def test_pausar_ativar_vaga(self, mock_os, mock_input, fluxo, mock_services):
        """Testa pausar/ativar vaga"""
        mock_vaga = MagicMock()
        mock_vaga.id = 1
        mock_vaga.ativo = True
        mock_vaga.id_empresa = 1
        mock_services["service_vaga_clt"].buscar_por_id.return_value = mock_vaga
        
        fluxo._pausar_ativar_vaga()
        
        mock_services["service_vaga_clt"].pausar.assert_called_once_with(1)


class TestFluxoEmpresaCandidaturas:
    """Testes de visualização de candidaturas"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_empresa": MagicMock(),
            "service_vaga_clt": MagicMock(),
            "service_candidatura": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        fluxo = FluxoEmpresa(**mock_services)
        fluxo.empresa_logada = MagicMock()
        fluxo.empresa_logada.id = 1
        return fluxo

    @patch('builtins.input', side_effect=['5'])  # Voltar imediatamente
    @patch('os.system')
    def test_ver_candidaturas_voltar(self, mock_os, mock_input, fluxo):
        """Testa voltar do menu de candidaturas"""
        fluxo._ver_candidaturas()
        # Não deve quebrar

    @patch('builtins.input', side_effect=['1', ''])  # Listar por vaga
    @patch('os.system')
    def test_listar_candidaturas_por_vaga(self, mock_os, mock_input, fluxo, mock_services):
        """Testa listar candidaturas de uma vaga"""
        mock_vaga = MagicMock()
        mock_vaga.id = 1
        mock_vaga.titulo = "Dev Python"
        mock_services["service_vaga_clt"].listar_por_empresa.return_value = [mock_vaga]
        mock_services["service_candidatura"].listar_por_vaga.return_value = []
        
        fluxo._listar_candidaturas_por_vaga()
        
        mock_services["service_vaga_clt"].listar_por_empresa.assert_called()

    @patch('builtins.input', side_effect=['1', ''])
    @patch('os.system')
    def test_aprovar_candidatura_sucesso(self, mock_os, mock_input, fluxo, mock_services):
        """Testa aprovação de candidatura"""
        mock_candidatura = MagicMock()
        mock_candidatura.id = 1
        mock_services["service_candidatura"].buscar_por_id.return_value = mock_candidatura
        
        fluxo._aprovar_candidatura()
        
        mock_services["service_candidatura"].aprovar.assert_called_once_with(1)

    @patch('builtins.input', side_effect=['1', ''])
    @patch('os.system')
    def test_reprovar_candidatura_sucesso(self, mock_os, mock_input, fluxo, mock_services):
        """Testa reprovação de candidatura"""
        mock_candidatura = MagicMock()
        mock_candidatura.id = 1
        mock_services["service_candidatura"].buscar_por_id.return_value = mock_candidatura
        
        fluxo._reprovar_candidatura()
        
        mock_services["service_candidatura"].reprovar.assert_called_once_with(1)

    @patch('builtins.input', side_effect=['abc', ''])
    @patch('os.system')
    def test_aprovar_candidatura_id_invalido(self, mock_os, mock_input, fluxo):
        """Testa aprovação com ID inválido"""
        fluxo._aprovar_candidatura()
        # Não deve quebrar

    @patch('builtins.input', side_effect=['1', ''])
    @patch('os.system')
    def test_ver_detalhes_candidatura(self, mock_os, mock_input, fluxo, mock_services):
        """Testa visualizar detalhes de candidatura"""
        mock_status = MagicMock()
        mock_status.value = "pendente"
        mock_tipo = MagicMock()
        mock_tipo.value = "clt"
        
        mock_cand = MagicMock()
        mock_cand.id = 1
        mock_cand.id_candidato = 10
        mock_cand.id_vaga = 5
        mock_cand.data_candidatura = "2025-01-01"
        mock_cand.status = mock_status
        mock_cand.tipo_vaga = mock_tipo
        mock_services["service_candidatura"].buscar_por_id.return_value = mock_cand
        
        fluxo._ver_detalhes_candidatura()
        
        mock_services["service_candidatura"].buscar_por_id.assert_called()
