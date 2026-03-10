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
        # Opção 7 é sair
        result = fluxo._processar_opcao_menu_principal("7")
        assert result == False

    @patch('builtins.input', return_value='')
    @patch('os.system')
    def test_processar_opcao_invalida(self, mock_os, mock_input, fluxo):
        """Testa opção inválida"""
        result = fluxo._processar_opcao_menu_principal("99")
        assert result == True

    @patch('builtins.input', return_value='3')  # Voltar
    @patch('os.system')
    def test_publicar_curso_menu(self, mock_os, mock_input, fluxo):
        """Testa menu publicar curso"""
        fluxo._publicar_curso()
        assert mock_input.called


class TestFluxoInstituicaoPublicarCurso:
    """Testes de publicação de cursos"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_instituicao": MagicMock(),
            "service_curso_ead": MagicMock(),
            "service_curso_presencial": MagicMock(),
            "service_curso_competencia": MagicMock(),
            "service_competencia": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        fluxo = FluxoInstituicao(**mock_services)
        fluxo.instituicao_logada = MagicMock()
        fluxo.instituicao_logada.id = 1
        fluxo.instituicao_logada.nome = "Instituição Teste"
        return fluxo

    @patch('builtins.input', side_effect=['Curso Python', 'Tecnologia', '40', '30', 'http://plataforma.com', '', 'n', ''])
    @patch('os.system')
    def test_publicar_curso_ead_sucesso(self, mock_os, mock_input, fluxo, mock_services):
        """Testa publicação de curso EAD com sucesso"""
        mock_curso = MagicMock()
        mock_curso.id = 1
        mock_curso.nome = "Curso Python"
        mock_services["service_curso_ead"].cadastrar.return_value = mock_curso
        
        fluxo._publicar_curso_ead()
        
        mock_services["service_curso_ead"].cadastrar.assert_called_once()

    @patch('builtins.input', side_effect=['Curso Java', 'Tecnologia', '60', '25', 'São Paulo', '', 'n', ''])
    @patch('os.system')
    def test_publicar_curso_presencial_sucesso(self, mock_os, mock_input, fluxo, mock_services):
        """Testa publicação de curso presencial com sucesso"""
        mock_curso = MagicMock()
        mock_curso.id = 1
        mock_curso.nome = "Curso Java"
        mock_services["service_curso_presencial"].cadastrar.return_value = mock_curso
        
        fluxo._publicar_curso_presencial()
        
        mock_services["service_curso_presencial"].cadastrar.assert_called_once()

    @patch('builtins.input', side_effect=['Curso', 'Tech', 'abc', ''])
    @patch('os.system')
    def test_publicar_curso_ead_valor_invalido(self, mock_os, mock_input, fluxo):
        """Testa erro de validação na publicação"""
        fluxo._publicar_curso_ead()
        # Não deve quebrar

    def test_publicar_curso_ead_sem_servico(self, mock_services):
        """Testa publicação sem serviço de curso EAD"""
        fluxo = FluxoInstituicao(service_instituicao=mock_services["service_instituicao"])
        fluxo.instituicao_logada = MagicMock()
        fluxo.instituicao_logada.id = 1
        
        with patch('builtins.input', return_value=''):
            with patch('os.system'):
                fluxo._publicar_curso_ead()
                # Não deve quebrar


class TestFluxoInstituicaoGerenciarCursos:
    """Testes de gerenciamento de cursos"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_instituicao": MagicMock(),
            "service_curso_ead": MagicMock(),
            "service_curso_presencial": MagicMock(),
            "service_curso_competencia": MagicMock(),
            "service_competencia": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        fluxo = FluxoInstituicao(**mock_services)
        fluxo.instituicao_logada = MagicMock()
        fluxo.instituicao_logada.id = 1
        return fluxo

    @patch('builtins.input', side_effect=['8'])  # Voltar imediatamente
    @patch('os.system')
    def test_gerenciar_cursos_voltar(self, mock_os, mock_input, fluxo):
        """Testa voltar do menu gerenciar cursos"""
        fluxo._gerenciar_cursos()
        # Não deve quebrar

    @patch('builtins.input', side_effect=[''])
    @patch('os.system')
    def test_listar_cursos_ead_vazio(self, mock_os, mock_input, fluxo, mock_services):
        """Testa listar cursos EAD quando não há cursos"""
        mock_services["service_curso_ead"].listar_por_instituicao.return_value = []
        
        fluxo._listar_cursos_ead()
        
        mock_services["service_curso_ead"].listar_por_instituicao.assert_called_once_with(1)

    @patch('builtins.input', side_effect=[''])
    @patch('os.system')
    def test_listar_cursos_ead_com_cursos(self, mock_os, mock_input, fluxo, mock_services):
        """Testa listar cursos EAD existentes"""
        mock_curso = MagicMock()
        mock_curso.id = 1
        mock_curso.nome = "Python"
        mock_curso.carga_horaria = 40
        mock_curso.ativo = True
        mock_services["service_curso_ead"].listar_por_instituicao.return_value = [mock_curso]
        
        fluxo._listar_cursos_ead()
        
        assert mock_services["service_curso_ead"].listar_por_instituicao.called

    @patch('builtins.input', side_effect=[''])
    @patch('os.system')
    def test_listar_cursos_presenciais_vazio(self, mock_os, mock_input, fluxo, mock_services):
        """Testa listar cursos presenciais quando não há cursos"""
        mock_services["service_curso_presencial"].listar_por_instituicao.return_value = []
        
        fluxo._listar_cursos_presenciais()
        
        mock_services["service_curso_presencial"].listar_por_instituicao.assert_called_once_with(1)

    @patch('builtins.input', side_effect=['1', '', ''])
    @patch('os.system')
    def test_ver_detalhes_curso_ead_sucesso(self, mock_os, mock_input, fluxo, mock_services):
        """Testa ver detalhes de um curso EAD"""
        from src.dominio.curso_competencia import TipoCursoCompetencia
        mock_curso = MagicMock()
        mock_curso.id = 1
        mock_curso.nome = "Python"
        mock_curso.area = "Tecnologia"
        mock_curso.carga_horaria = 40
        mock_curso.capacidade = 30
        mock_curso.plataforma_url = "http://plataforma.com"
        mock_curso.prazo_inscricao = None
        mock_curso.ativo = True
        mock_curso.id_instituicao = 1
        mock_services["service_curso_ead"].buscar_por_id.return_value = mock_curso
        mock_services["service_curso_competencia"].listar_por_curso.return_value = []
        
        fluxo._ver_detalhes_curso_ead()
        
        mock_services["service_curso_ead"].buscar_por_id.assert_called_once()

    @patch('builtins.input', side_effect=['1', ''])
    @patch('os.system')
    def test_ver_detalhes_curso_nao_encontrado(self, mock_os, mock_input, fluxo, mock_services):
        """Testa ver detalhes de curso inexistente"""
        mock_services["service_curso_ead"].buscar_por_id.return_value = None
        
        fluxo._ver_detalhes_curso_ead()
        # Não deve quebrar


class TestFluxoInstituicaoVerInscritos:
    """Testes de visualização de inscritos"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_instituicao": MagicMock(),
            "service_curso_ead": MagicMock(),
            "service_curso_presencial": MagicMock(),
            "service_inscricao_curso": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        fluxo = FluxoInstituicao(**mock_services)
        fluxo.instituicao_logada = MagicMock()
        fluxo.instituicao_logada.id = 1
        return fluxo

    @patch('builtins.input', side_effect=['4'])  # Voltar imediatamente
    @patch('os.system')
    def test_ver_inscritos_voltar(self, mock_os, mock_input, fluxo):
        """Testa voltar do menu de inscritos"""
        fluxo._ver_inscritos()
        # Não deve quebrar

    @patch('builtins.input', side_effect=['1', ''])
    @patch('os.system')
    def test_listar_inscritos_ead_sem_cursos(self, mock_os, mock_input, fluxo, mock_services):
        """Testa listar inscritos quando não há cursos"""
        mock_services["service_curso_ead"].listar_por_instituicao.return_value = []
        
        fluxo._listar_inscritos_ead()
        # Não deve quebrar

    @patch('builtins.input', side_effect=['1', ''])
    @patch('os.system')
    def test_listar_inscritos_ead_com_inscricoes(self, mock_os, mock_input, fluxo, mock_services):
        """Testa listar inscritos de um curso EAD"""
        mock_curso = MagicMock()
        mock_curso.id = 1
        mock_curso.nome = "Python"
        mock_services["service_curso_ead"].listar_por_instituicao.return_value = [mock_curso]
        
        mock_inscricao = MagicMock()
        mock_inscricao.id = 1
        mock_inscricao.id_candidato = 10
        mock_inscricao.data_inscricao = "2025-01-01"
        mock_inscricao.status = "ativo"
        mock_services["service_inscricao_curso"].listar_por_curso.return_value = [mock_inscricao]
        
        fluxo._listar_inscritos_ead()
        
        mock_services["service_inscricao_curso"].listar_por_curso.assert_called()

    @patch('builtins.input', side_effect=['1', ''])
    @patch('os.system')
    def test_ver_detalhes_inscricao_sucesso(self, mock_os, mock_input, fluxo, mock_services):
        """Testa ver detalhes de uma inscrição"""
        mock_inscricao = MagicMock()
        mock_inscricao.id = 1
        mock_inscricao.id_candidato = 10
        mock_inscricao.id_curso = 5
        mock_inscricao.data_inscricao = "2025-01-01"
        mock_inscricao.status = "ativo"
        mock_services["service_inscricao_curso"].buscar_por_id.return_value = mock_inscricao
        
        fluxo._ver_detalhes_inscricao()
        
        mock_services["service_inscricao_curso"].buscar_por_id.assert_called()

    @patch('builtins.input', side_effect=['abc', ''])
    @patch('os.system')
    def test_ver_detalhes_inscricao_id_invalido(self, mock_os, mock_input, fluxo):
        """Testa ver detalhes com ID inválido"""
        fluxo._ver_detalhes_inscricao()
        # Não deve quebrar


class TestFluxoInstituicaoGerenciarCompetencias:
    """Testes de gerenciamento de competências"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_instituicao": MagicMock(),
            "service_curso_ead": MagicMock(),
            "service_curso_presencial": MagicMock(),
            "service_curso_competencia": MagicMock(),
            "service_competencia": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        fluxo = FluxoInstituicao(**mock_services)
        fluxo.instituicao_logada = MagicMock()
        fluxo.instituicao_logada.id = 1
        return fluxo

    @patch('builtins.input', side_effect=['5'])  # Voltar imediatamente
    @patch('os.system')
    def test_gerenciar_competencias_voltar(self, mock_os, mock_input, fluxo):
        """Testa voltar do menu gerenciar competências"""
        fluxo._gerenciar_competencias()
        # Não deve quebrar

    @patch('builtins.input', side_effect=[''])
    @patch('os.system')
    def test_listar_todas_competencias_vazio(self, mock_os, mock_input, fluxo, mock_services):
        """Testa listar competências quando não há nenhuma"""
        mock_services["service_competencia"].listar_todos.return_value = []
        
        fluxo._listar_todas_competencias()
        
        mock_services["service_competencia"].listar_todos.assert_called_once()

    @patch('builtins.input', side_effect=[''])
    @patch('os.system')
    def test_listar_todas_competencias_com_dados(self, mock_os, mock_input, fluxo, mock_services):
        """Testa listar competências existentes"""
        mock_comp = MagicMock()
        mock_comp.id = 1
        mock_comp.nome = "Python"
        mock_comp.descricao = "Linguagem Python"
        mock_services["service_competencia"].listar_todos.return_value = [mock_comp]
        
        fluxo._listar_todas_competencias()
        
        assert mock_services["service_competencia"].listar_todos.called

    @patch('builtins.input', side_effect=['1', ''])
    @patch('os.system')
    def test_ver_competencias_curso_ead_sem_cursos(self, mock_os, mock_input, fluxo, mock_services):
        """Testa ver competências quando não há cursos"""
        mock_services["service_curso_ead"].listar_por_instituicao.return_value = []
        
        fluxo._ver_competencias_curso_ead()
        # Não deve quebrar

    @patch('builtins.input', side_effect=['1', ''])
    @patch('os.system')
    def test_ver_competencias_curso_ead_com_competencias(self, mock_os, mock_input, fluxo, mock_services):
        """Testa ver competências de um curso EAD"""
        from src.dominio.curso_competencia import TipoCursoCompetencia
        mock_curso = MagicMock()
        mock_curso.id = 1
        mock_curso.nome = "Python"
        mock_services["service_curso_ead"].listar_por_instituicao.return_value = [mock_curso]
        
        mock_cc = MagicMock()
        mock_cc.id_competencia = 1
        mock_cc.nivel_conferido = "avancado"
        mock_services["service_curso_competencia"].listar_por_curso.return_value = [mock_cc]
        
        fluxo._ver_competencias_curso_ead()
        
        mock_services["service_curso_competencia"].listar_por_curso.assert_called()


class TestFluxoInstituicaoVerPerfil:
    """Testes de visualização de perfil"""

    @pytest.fixture
    def mock_service_instituicao(self):
        return MagicMock()

    @pytest.fixture
    def fluxo(self, mock_service_instituicao):
        return FluxoInstituicao(service_instituicao=mock_service_instituicao)

    @patch('builtins.input', return_value='3')
    @patch('os.system')
    def test_ver_perfil_sem_login(self, mock_os, mock_input, fluxo):
        """Testa ver perfil sem estar logado"""
        fluxo._ver_perfil()
        assert mock_input.called

    @patch('builtins.input', return_value='3')
    @patch('os.system')
    def test_ver_perfil_logado(self, mock_os, mock_input, fluxo):
        """Testa ver perfil estando logado"""
        fluxo.instituicao_logada = MagicMock()
        fluxo.instituicao_logada.id = 1
        fluxo.instituicao_logada.nome = "Instituição Teste"
        fluxo.instituicao_logada.cnpj = "12345678901234"
        fluxo.instituicao_logada.email = "teste@inst.com"
        fluxo.instituicao_logada.telefone = "11999999999"
        fluxo.instituicao_logada.endereco = "Rua Teste, 123"
        fluxo.instituicao_logada.website = "http://teste.com"
        
        fluxo._ver_perfil()
        
        assert mock_input.called


class TestFluxoInstituicaoAreasEnsino:
    """Testes de gerenciamento de áreas de ensino"""

    @pytest.fixture
    def mock_services(self):
        return {
            "service_instituicao": MagicMock(),
            "service_curso_ead": MagicMock(),
            "service_curso_presencial": MagicMock(),
            "service_curso_competencia": MagicMock(),
            "service_competencia": MagicMock(),
            "service_area_ensino": MagicMock(),
            "service_instituicao_area": MagicMock(),
        }

    @pytest.fixture
    def fluxo(self, mock_services):
        fluxo = FluxoInstituicao(**mock_services)
        fluxo.instituicao_logada = MagicMock()
        fluxo.instituicao_logada.id = 1
        fluxo.instituicao_logada.nome = "Instituição Teste"
        return fluxo

    @patch('builtins.input', return_value='4')  # Voltar
    @patch('os.system')
    def test_gerenciar_areas_voltar(self, mock_os, mock_input, fluxo):
        """Testa menu de áreas de ensino - opção voltar"""
        fluxo._gerenciar_areas_ensino()
        # Deve encerrar sem erro

    @patch('builtins.input', side_effect=['1', '', '4'])  # Listar todas, enter, voltar
    @patch('os.system')
    def test_listar_todas_areas(self, mock_os, mock_input, fluxo, mock_services):
        """Testa listagem de todas as áreas de ensino"""
        mock_area = MagicMock()
        mock_area.id = 1
        mock_area.nome = "Tecnologia"
        mock_area.descricao = "Área de tecnologia"
        mock_services["service_area_ensino"].listar_todas.return_value = [mock_area]
        
        fluxo._gerenciar_areas_ensino()
        
        mock_services["service_area_ensino"].listar_todas.assert_called()

    @patch('builtins.input', side_effect=['1', '', '4'])  # Listar todas, enter, voltar
    @patch('os.system')
    def test_listar_todas_areas_vazio(self, mock_os, mock_input, fluxo, mock_services):
        """Testa listagem quando não há áreas cadastradas"""
        mock_services["service_area_ensino"].listar_todas.return_value = []
        
        fluxo._gerenciar_areas_ensino()
        
        mock_services["service_area_ensino"].listar_todas.assert_called()

    @patch('builtins.input', side_effect=['2', '', '4'])  # Ver minhas áreas, enter, voltar
    @patch('os.system')
    def test_listar_minhas_areas(self, mock_os, mock_input, fluxo, mock_services):
        """Testa listagem das áreas da instituição"""
        mock_inst_area = MagicMock()
        mock_inst_area.area_ensino_id = 1
        mock_area = MagicMock()
        mock_area.nome = "Tecnologia"
        mock_services["service_instituicao_area"].listar_por_instituicao.return_value = [mock_inst_area]
        mock_services["service_area_ensino"].obter_por_id.return_value = mock_area
        
        fluxo._gerenciar_areas_ensino()
        
        mock_services["service_instituicao_area"].listar_por_instituicao.assert_called()

    @patch('builtins.input', side_effect=['3', '1', '', '4'])  # Adicionar área, id=1, enter, voltar
    @patch('os.system')
    def test_adicionar_area_instituicao(self, mock_os, mock_input, fluxo, mock_services):
        """Testa adição de área de ensino à instituição"""
        mock_area = MagicMock()
        mock_area.id = 1
        mock_area.nome = "Tecnologia"
        mock_services["service_area_ensino"].listar_todas.return_value = [mock_area]
        mock_services["service_instituicao_area"].cadastrar.return_value = MagicMock()
        
        fluxo._gerenciar_areas_ensino()
        
        mock_services["service_instituicao_area"].cadastrar.assert_called()

    @patch('builtins.input', side_effect=['3', '1', '', '4'])  # Adicionar área duplicada
    @patch('os.system')
    def test_adicionar_area_duplicada(self, mock_os, mock_input, fluxo, mock_services):
        """Testa tentativa de adicionar área duplicada"""
        mock_area = MagicMock()
        mock_area.id = 1
        mock_area.nome = "Tecnologia"
        mock_services["service_area_ensino"].listar_todas.return_value = [mock_area]
        mock_services["service_instituicao_area"].cadastrar.side_effect = ValueError("Já existe")
        
        fluxo._gerenciar_areas_ensino()
        # Não deve quebrar, apenas exibir erro

    def test_gerenciar_areas_sem_servico(self, fluxo):
        """Testa gerenciamento de áreas sem serviço configurado"""
        fluxo.service_area_ensino = None
        fluxo.service_instituicao_area = None
        
        # Não deve quebrar
        with patch('builtins.input', return_value='4'):
            with patch('os.system'):
                fluxo._gerenciar_areas_ensino()
