import unittest
from unittest.mock import Mock, patch
from datetime import date
import sys
import os

# Permitir importação dos módulos src
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.dominio.candidato import Candidato
from src.dominio.vaga import Modalidade, TipoVaga, VagaCLT, VagaEstagio
from src.dominio.curso_ead import CursoEAD
from src.dominio.curso_presencial import CursoPresencial
from src.dominio.validators import PrazoValidador
from src.services.service_candidato import CandidatoService
from src.interfaces.interface_candidato import ICandidatoRepositorio

class TestSkillUpSuite(unittest.TestCase):

    def setUp(self):
        self.future_date = date(2027, 12, 31)
        self.past_date = date(2020, 1, 1)

    # ==========================================
    # 1. TESTES DE POLIMORFISMO
    # ==========================================

    def test_polimorfismo_cursos_exibir_detalhes(self):
        """Teste 1 - Polimorfismo: Teste se diferentes tipos de curso implementam exibir_detalhes corretamente."""
        curso_ead = CursoEAD(
            id=1, nome="Python EAD", area="TI", carga_horaria=40,
            modalidade=Modalidade.REMOTO, capacidade=100, 
            prazo_inscricao=self.future_date, plataforma_url="http://ead.com"
        )
        curso_presencial = CursoPresencial(
            id=2, nome="Python Presencial", area="TI", carga_horaria=40,
            modalidade=Modalidade.PRESENCIAL, capacidade=30, 
            prazo_inscricao=self.future_date, localidade="Sala 1"
        )
        
        cursos = [curso_ead, curso_presencial]
        detalhes = [c.exibir_detalhes() for c in cursos]
        
        self.assertTrue(any("Curso EAD" in d for d in detalhes))
        self.assertTrue(any("Curso Presencial" in d for d in detalhes))

    def test_polimorfismo_vagas_custo_contratacao(self):
        """Teste 2 - Polimorfismo: Teste se subclasses de Vaga calculam custo de forma diferente."""
        vaga_clt = VagaCLT(
            id=1, titulo="Dev Jr", descricao="Python", area="TI",
            modalidade=Modalidade.REMOTO, tipo=TipoVaga.EMPREGO,
            salario_base=5000.0, prazo_inscricao=self.future_date
        )
        
        vaga_estagio = VagaEstagio(
            id=2, titulo="Estágio Dev", descricao="Python", area="TI",
            modalidade=Modalidade.REMOTO, tipo=TipoVaga.ESTAGIO,
            bolsa_auxilio=1000.0, instituicao_conveniada="Univ",
            prazo_inscricao=self.future_date
        )

        # Regra: CLT * 1.8 | Estágio * 1.1
        self.assertAlmostEqual(vaga_clt.calcular_custo_contratacao(), 9000.0)
        self.assertAlmostEqual(vaga_estagio.calcular_custo_contratacao(), 1100.0)

    # ==========================================
    # 2. TESTES DE REGRAS DE NEGÓCIO
    # ==========================================

    def test_curso_prazo_futuro_valido(self):
        """Teste 3 - Regra de Negócio: Valida criação de curso com prazo no futuro."""
        curso = CursoEAD(
            id=1, nome="Curso Futuro", area="TI", carga_horaria=10,
            modalidade=Modalidade.REMOTO, capacidade=10,
            prazo_inscricao=self.future_date, plataforma_url="http://test.com"
        )
        self.assertEqual(curso.prazo_inscricao, self.future_date)

    def test_vaga_clt_salario_positivo(self):
        """Teste 4 - Regra de Negócio: Valida que salário deve ser validado na criação."""
        vaga = VagaCLT(
            id=1, titulo="Dev", descricao="Desc", area="TI",
            modalidade=Modalidade.REMOTO, tipo=TipoVaga.EMPREGO,
            salario_base=3000.0, prazo_inscricao=self.future_date
        )
        self.assertEqual(vaga.salario_base, 3000.0)

    # ==========================================
    # 3. TESTES DE EXCEÇÕES E ERROS
    # ==========================================

    def test_curso_prazo_passado_invalido(self):
        """Teste 5 - Exceção: Deve lançar ValueError se o prazo for no passado."""
        with self.assertRaises(ValueError):
            CursoEAD(
                id=1, nome="Curso Passado", area="TI", carga_horaria=10,
                modalidade=Modalidade.REMOTO, capacidade=10,
                prazo_inscricao=self.past_date, 
                plataforma_url="http://test.com"
            )

    def test_prazo_validador_tipo_invalido(self):
        """Teste 6 - Exceção: Deve lançar TypeError se prazo não for date ou None."""
        validador = PrazoValidador()
        with self.assertRaises(TypeError):
            validador.validar("2027-12-31")  # Passando string ao invés de date

    def test_candidato_cpf_invalido(self):
        """Teste 7 - Exceção: Deve lançar ValueError para CPF com formato inválido."""
        with self.assertRaises(ValueError):
            # CPF com letras
            Candidato(1, "João", "1234567890a", "joao@email.com", ["TI"], "Superior")

    def test_candidato_email_invalido(self):
        """Teste 8 - Exceção: Deve lançar ValueError para email inválido."""
        with self.assertRaises(ValueError):
            Candidato(1, "João", "12345678901", "email_sem_arroba", ["TI"], "Superior")

    def test_vaga_adicionar_requisito_vazio(self):
        """Teste 9 - Exceção: Valida se adicionar requisito vazio lança erro."""
        vaga = VagaCLT(
            id=1, titulo="Dev", descricao="Desc", area="TI",
            modalidade=Modalidade.REMOTO, tipo=TipoVaga.EMPREGO,
            salario_base=3000.0, prazo_inscricao=self.future_date
        )
        with self.assertRaises(ValueError):
            vaga.adicionar_requisito("   ")

    def test_service_candidato_buscar_inexistente_mock(self):
        """Teste 10 - Exceção (Mock): Mock do repositório para testar busca de candidato inexistente."""
        mock_repo = Mock(spec=ICandidatoRepositorio)
        mock_repo.buscar_por_id.return_value = None
        
        service = CandidatoService(mock_repo)
        
        with self.assertRaisesRegex(ValueError, "Candidato não encontrado"):
            service.buscar_por_id(999)

    # ==========================================
    # 4. TESTES COM MOCKS
    # ==========================================

    def test_service_candidato_cadastro_sucesso_mock(self):
        """Teste 11 - Mock: Mock do repositório para testar fluxo de sucesso no serviço."""
        # Cria mock do repositório
        mock_repo = Mock(spec=ICandidatoRepositorio)
        
        # Simula que não existem candidatos (para gerar ID 1 e não dar conflito de CPF)
        mock_repo.listar.return_value = []
        
        service = CandidatoService(mock_repo)
        
        candidato = service.cadastrar(
            nome="Maria Mock", 
            cpf="11122233344", 
            email="maria@mock.com", 
            areas_interesse=["Dados"], 
            nivel_formacao="Superior"
        )
        
        # Verifica se o repositório foi chamado corretamente
        mock_repo.salvar.assert_called_once()
        self.assertEqual(candidato.nome, "Maria Mock")
        self.assertEqual(candidato.id, 1)

    def test_service_candidato_cpf_duplicado_mock(self):
        """Teste 12 - Mock: Mock do repositório para simular conflito de CPF."""
        mock_repo = Mock(spec=ICandidatoRepositorio)
        
        # Simula um candidato já existente no retorno do listar
        candidato_existente = Mock()
        candidato_existente.cpf = "11122233344"
        mock_repo.listar.return_value = [candidato_existente]
        
        service = CandidatoService(mock_repo)
        
        # Deve falhar ao tentar cadastrar mesmo CPF
        with self.assertRaisesRegex(ValueError, "Já existe candidato com este CPF"):
            service.cadastrar(
                nome="João Duplicado", 
                cpf="11122233344", 
                email="joao@mock.com", 
                areas_interesse=["TI"], 
                nivel_formacao="Médio"
            )

    def test_prazo_validador_com_mock_data(self):
        """Teste 13 - Mock: Mock de 'date.today' usando uma classe derivada fake para contornar limitações de mock de built-in."""
        
        # classe fake que se comporta como date, mas com today controlavel
        class FakeDate(date):
            @classmethod
            def today(cls):
                return cls(2026, 1, 1)

        # Patching o objeto 'date' dentro do módulo validators
        with patch('src.dominio.validators.date', FakeDate):
            validador = PrazoValidador()
            
            
            # Data no passado
            data_passada = FakeDate(2025, 12, 31)
            with self.assertRaises(ValueError):
                validador.validar(data_passada)
            
            # Data no futuro
            data_futura = FakeDate(2026, 1, 2)
            try:
                validador.validar(data_futura)
            except ValueError:
                self.fail("Validador rejeitou data futura válida com mock.")

if __name__ == '__main__':
    unittest.main()
