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
from src.dominio.inscricao_curso import InscricaoCurso, StatusInscricao
from src.dominio.validators import PrazoValidador
from src.services.service_candidato import CandidatoService
from src.services.service_busca_vaga import MotorBuscaVaga
from src.services.service_inscricao_curso import InscricaoCursoService
from src.services.service_recomendacao import (
    RecomendacaoService, ItemRankeado, PesoRecomendacao,
)
from src.interfaces.interface_candidato import ICandidatoRepositorio
from src.interfaces.interface_vaga import IVagaRepositorio
from src.interfaces.interface_curso import ICursoRepositorio
from src.interfaces.interface_inscricao_curso import IInscricaoCursoRepositorio

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
            salario_base=5000.0, prazo_inscricao=self.future_date,
            localidade="São Paulo"
        )
        
        vaga_estagio = VagaEstagio(
            id=2, titulo="Estágio Dev", descricao="Python", area="TI",
            modalidade=Modalidade.REMOTO, tipo=TipoVaga.ESTAGIO,
            bolsa_auxilio=1000.0, instituicao_conveniada="Univ",
            prazo_inscricao=self.future_date,
            localidade="Remoto"
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
            Candidato(1, "João", "1234567890a", "joao@email.com", ["TI"], "Superior", localidade="SP")

    def test_candidato_email_invalido(self):
        """Teste 8 - Exceção: Deve lançar ValueError para email inválido."""
        with self.assertRaises(ValueError):
            Candidato(1, "João", "12345678901", "email_sem_arroba", ["TI"], "Superior", localidade="SP")

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
            nivel_formacao="Superior",
            localidade="SP"
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
                nivel_formacao="Médio",
                localidade="RJ"
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


class TestMotorBuscaVaga(unittest.TestCase):
    """Testes do motor de busca de vagas."""

    def setUp(self):
        self.future_date = date(2027, 12, 31)
        self.mock_repo = Mock(spec=IVagaRepositorio)

        self.vaga_clt_sp = VagaCLT(
            id=1, titulo="Dev Python", descricao="Backend", area="TI",
            modalidade=Modalidade.PRESENCIAL, tipo=TipoVaga.EMPREGO,
            salario_base=8000.0, prazo_inscricao=self.future_date,
            localidade="São Paulo"
        )

        self.vaga_clt_rj = VagaCLT(
            id=2, titulo="Dev Java", descricao="Backend", area="TI",
            modalidade=Modalidade.REMOTO, tipo=TipoVaga.EMPREGO,
            salario_base=10000.0, prazo_inscricao=self.future_date,
            localidade="Rio de Janeiro"
        )

        self.vaga_estagio_sp = VagaEstagio(
            id=3, titulo="Estágio Data", descricao="Dados", area="Dados",
            modalidade=Modalidade.PRESENCIAL, tipo=TipoVaga.ESTAGIO,
            bolsa_auxilio=1500.0, instituicao_conveniada="USP",
            prazo_inscricao=self.future_date,
            localidade="São Paulo"
        )

        self.todas_vagas = [self.vaga_clt_sp, self.vaga_clt_rj, self.vaga_estagio_sp]
        self.mock_repo.listar_ativas.return_value = self.todas_vagas
        self.mock_repo.listar_todas.return_value = self.todas_vagas

        self.motor = MotorBuscaVaga(self.mock_repo)

    def test_buscar_por_area(self):
        """Motor de Busca: Filtra vagas por área."""
        resultado = self.motor.buscar(area="TI")
        self.assertEqual(len(resultado), 2)
        self.assertTrue(all(v.area == "TI" for v in resultado))

    def test_buscar_por_localidade(self):
        """Motor de Busca: Filtra vagas por localidade (remotas sempre incluídas)."""
        resultado = self.motor.buscar(localidade="São Paulo")
        # SP presencial (id=1) + RJ remoto (id=2, ignora localidade) + estágio SP (id=3)
        self.assertEqual(len(resultado), 3)

    def test_buscar_por_modalidade(self):
        """Motor de Busca: Filtra vagas por modalidade."""
        resultado = self.motor.buscar(modalidade=Modalidade.REMOTO)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].id, 2)

    def test_buscar_por_tipo(self):
        """Motor de Busca: Filtra vagas por tipo."""
        resultado = self.motor.buscar(tipo=TipoVaga.ESTAGIO)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].id, 3)

    def test_buscar_por_faixa_salarial(self):
        """Motor de Busca: Filtra vagas por faixa salarial."""
        resultado = self.motor.buscar(salario_min=5000.0, salario_max=9000.0)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].id, 1)

    def test_buscar_filtros_combinados(self):
        """Motor de Busca: Combina múltiplos filtros."""
        resultado = self.motor.buscar(area="TI", localidade="São Paulo", tipo=TipoVaga.EMPREGO)
        # Presencial SP (id=1) + Remoto RJ (id=2, remoto ignora localidade)
        self.assertEqual(len(resultado), 2)
        ids = [v.id for v in resultado]
        self.assertIn(1, ids)
        self.assertIn(2, ids)

    def test_buscar_sem_resultados(self):
        """Motor de Busca: Retorna lista vazia quando nenhuma vaga atende."""
        resultado = self.motor.buscar(area="Saúde")
        self.assertEqual(resultado, [])

    def test_buscar_por_candidato(self):
        """Motor de Busca: Filtra vagas compatíveis com perfil do candidato."""
        resultado = self.motor.buscar_por_candidato(
            areas_interesse=["TI"], localidade_candidato="São Paulo"
        )
        # Vaga presencial SP (localidade coincide) + Vaga remota RJ (remoto ignora localidade)
        self.assertEqual(len(resultado), 2)
        ids = [v.id for v in resultado]
        self.assertIn(1, ids)
        self.assertIn(2, ids)

    def test_buscar_vaga_remota_ignora_localidade(self):
        """Motor de Busca: Vaga remota é retornada independentemente da localidade do candidato."""
        resultado = self.motor.buscar(
            area="TI", localidade="Curitiba"
        )
        # Apenas a vaga remota (id=2) deve aparecer, pois a presencial SP não coincide com Curitiba
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].id, 2)


class TestInscricaoCursoPresencial(unittest.TestCase):
    """Testes de inscrição em curso com validação de localidade."""

    def setUp(self):
        self.future_date = date(2027, 12, 31)

        self.mock_repo_inscricao = Mock(spec=IInscricaoCursoRepositorio)
        self.mock_repo_curso = Mock(spec=ICursoRepositorio)
        self.mock_repo_candidato = Mock(spec=ICandidatoRepositorio)

        self.mock_repo_inscricao.listar_todas.return_value = []
        self.mock_repo_inscricao.listar_por_aluno.return_value = []

        self.service = InscricaoCursoService(
            self.mock_repo_inscricao,
            self.mock_repo_curso,
            self.mock_repo_candidato,
        )

    def test_inscricao_presencial_localidade_compativel(self):
        """Inscrição: Aceita quando candidato e curso presencial têm mesma localidade."""
        curso = CursoPresencial(
            id=1, nome="Python Presencial", area="TI", carga_horaria=40,
            modalidade=Modalidade.PRESENCIAL, capacidade=30,
            prazo_inscricao=self.future_date, localidade="São Paulo"
        )
        candidato = Candidato(
            1, "Maria", "11122233344", "maria@email.com",
            ["TI"], "Superior", localidade="São Paulo"
        )

        self.mock_repo_curso.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = candidato

        inscricao = self.service.inscrever(id_candidato=1, id_curso=1)

        self.mock_repo_inscricao.salvar.assert_called_once()
        self.assertEqual(inscricao.id_curso, 1)
        self.assertEqual(inscricao.id_aluno, 1)

    def test_inscricao_presencial_localidade_incompativel(self):
        """Inscrição: Rejeita quando candidato e curso presencial têm localidades diferentes."""
        curso = CursoPresencial(
            id=1, nome="Python Presencial", area="TI", carga_horaria=40,
            modalidade=Modalidade.PRESENCIAL, capacidade=30,
            prazo_inscricao=self.future_date, localidade="São Paulo"
        )
        candidato = Candidato(
            2, "João", "22233344455", "joao@email.com",
            ["TI"], "Superior", localidade="Rio de Janeiro"
        )

        self.mock_repo_curso.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = candidato

        with self.assertRaisesRegex(ValueError, "Localidade incompatível"):
            self.service.inscrever(id_candidato=2, id_curso=1)

    def test_inscricao_presencial_candidato_sem_localidade(self):
        """Inscrição: Rejeita quando candidato não possui localidade para curso presencial."""
        curso = CursoPresencial(
            id=1, nome="Python Presencial", area="TI", carga_horaria=40,
            modalidade=Modalidade.PRESENCIAL, capacidade=30,
            prazo_inscricao=self.future_date, localidade="São Paulo"
        )
        candidato = Candidato(
            3, "Pedro", "33344455566", "pedro@email.com",
            ["TI"], "Superior", localidade=""
        )

        self.mock_repo_curso.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = candidato

        with self.assertRaisesRegex(ValueError, "não possui localidade"):
            self.service.inscrever(id_candidato=3, id_curso=1)

    def test_inscricao_ead_ignora_localidade(self):
        """Inscrição: Curso EAD não exige validação de localidade."""
        curso_ead = CursoEAD(
            id=2, nome="Python EAD", area="TI", carga_horaria=40,
            modalidade=Modalidade.REMOTO, capacidade=100,
            prazo_inscricao=self.future_date, plataforma_url="http://ead.com"
        )
        candidato = Candidato(
            4, "Ana", "44455566677", "ana@email.com",
            ["TI"], "Superior", localidade="Qualquer Cidade"
        )

        self.mock_repo_curso.buscar_por_id.return_value = curso_ead
        self.mock_repo_candidato.buscar_por_id.return_value = candidato

        inscricao = self.service.inscrever(id_candidato=4, id_curso=2)

        self.mock_repo_inscricao.salvar.assert_called_once()
        self.assertEqual(inscricao.id_curso, 2)

    def test_inscricao_curso_inexistente(self):
        """Inscrição: Rejeita quando curso não existe."""
        self.mock_repo_curso.buscar_por_id.return_value = None

        with self.assertRaisesRegex(ValueError, "Curso não encontrado"):
            self.service.inscrever(id_candidato=1, id_curso=999)

    def test_inscricao_candidato_inexistente(self):
        """Inscrição: Rejeita quando candidato não existe."""
        curso = CursoPresencial(
            id=1, nome="Curso", area="TI", carga_horaria=40,
            modalidade=Modalidade.PRESENCIAL, capacidade=30,
            prazo_inscricao=self.future_date, localidade="SP"
        )
        self.mock_repo_curso.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = None

        with self.assertRaisesRegex(ValueError, "Candidato não encontrado"):
            self.service.inscrever(id_candidato=999, id_curso=1)

    def test_inscricao_duplicada(self):
        """Inscrição: Rejeita inscrição duplicada no mesmo curso."""
        curso = CursoPresencial(
            id=1, nome="Curso", area="TI", carga_horaria=40,
            modalidade=Modalidade.PRESENCIAL, capacidade=30,
            prazo_inscricao=self.future_date, localidade="SP"
        )
        candidato = Candidato(
            1, "Maria", "11122233344", "maria@email.com",
            ["TI"], "Superior", localidade="SP"
        )
        inscricao_existente = Mock()
        inscricao_existente.id_curso = 1

        self.mock_repo_curso.buscar_por_id.return_value = curso
        self.mock_repo_candidato.buscar_por_id.return_value = candidato
        self.mock_repo_inscricao.listar_por_aluno.return_value = [inscricao_existente]

        with self.assertRaisesRegex(ValueError, "já está inscrito"):
            self.service.inscrever(id_candidato=1, id_curso=1)


class TestRecomendacaoService(unittest.TestCase):
    """Testes do serviço de recomendação de vagas e cursos."""

    def setUp(self):
        self.future_date = date(2027, 12, 31)
        self.mock_repo_vaga = Mock(spec=IVagaRepositorio)
        self.mock_repo_curso = Mock(spec=ICursoRepositorio)

        # --- Vagas ---
        self.vaga_ti_sp_presencial = VagaCLT(
            id=1, titulo="Dev Python", descricao="Backend", area="TI",
            modalidade=Modalidade.PRESENCIAL, tipo=TipoVaga.EMPREGO,
            salario_base=8000.0, prazo_inscricao=self.future_date,
            localidade="São Paulo"
        )
        self.vaga_ti_remoto = VagaCLT(
            id=2, titulo="Dev Java", descricao="Backend", area="TI",
            modalidade=Modalidade.REMOTO, tipo=TipoVaga.EMPREGO,
            salario_base=10000.0, prazo_inscricao=self.future_date,
            localidade="Rio de Janeiro"
        )
        self.vaga_dados_sp = VagaEstagio(
            id=3, titulo="Estágio Data", descricao="Dados", area="Dados",
            modalidade=Modalidade.PRESENCIAL, tipo=TipoVaga.ESTAGIO,
            bolsa_auxilio=1500.0, instituicao_conveniada="USP",
            prazo_inscricao=self.future_date, localidade="São Paulo"
        )
        self.vaga_ti_hibrido_rj = VagaCLT(
            id=4, titulo="Dev Full", descricao="Fullstack", area="TI",
            modalidade=Modalidade.HIBRIDO, tipo=TipoVaga.EMPREGO,
            salario_base=9000.0, prazo_inscricao=self.future_date,
            localidade="Rio de Janeiro"
        )

        self.mock_repo_vaga.listar_ativas.return_value = [
            self.vaga_ti_sp_presencial,
            self.vaga_ti_remoto,
            self.vaga_dados_sp,
            self.vaga_ti_hibrido_rj,
        ]

        # --- Cursos ---
        self.curso_ti_presencial_sp = CursoPresencial(
            id=1, nome="Python Presencial", area="TI", carga_horaria=40,
            modalidade=Modalidade.PRESENCIAL, capacidade=30,
            prazo_inscricao=self.future_date, localidade="São Paulo"
        )
        self.curso_ti_ead = CursoEAD(
            id=2, nome="Python EAD", area="TI", carga_horaria=40,
            modalidade=Modalidade.REMOTO, capacidade=100,
            prazo_inscricao=self.future_date, plataforma_url="http://ead.com"
        )
        self.curso_dados_presencial_rj = CursoPresencial(
            id=3, nome="Data Science", area="Dados", carga_horaria=60,
            modalidade=Modalidade.PRESENCIAL, capacidade=25,
            prazo_inscricao=self.future_date, localidade="Rio de Janeiro"
        )

        self.mock_repo_curso.listar_todos.return_value = [
            self.curso_ti_presencial_sp,
            self.curso_ti_ead,
            self.curso_dados_presencial_rj,
        ]

        self.service = RecomendacaoService(
            self.mock_repo_vaga, self.mock_repo_curso
        )

    # --- Vagas ---

    def test_recomenda_vagas_por_area_e_localidade(self):
        """Recomendação: Candidato de SP em TI recebe presencial SP + remoto + não híbrido RJ."""
        candidato = Candidato(
            1, "Maria", "11122233344", "maria@email.com",
            ["TI"], "Superior", localidade="São Paulo"
        )
        vagas = self.service.recomendar_vagas(candidato)
        ids = [v.item.id for v in vagas]
        self.assertIn(1, ids)  # presencial SP — match
        self.assertIn(2, ids)  # remoto — sempre
        self.assertNotIn(3, ids)  # área Dados — não coincide
        self.assertNotIn(4, ids)  # híbrido RJ — localidade diferente
        # Verifica que são ItemRankeado
        self.assertTrue(all(isinstance(v, ItemRankeado) for v in vagas))
        # Presencial SP (area+localidade=80) > Remoto (area+remoto=70)
        self.assertGreaterEqual(vagas[0].pontuacao, vagas[1].pontuacao)

    def test_recomenda_vaga_remota_qualquer_localidade(self):
        """Recomendação: Vaga remota é recomendada independente da localidade."""
        candidato = Candidato(
            2, "João", "22233344455", "joao@email.com",
            ["TI"], "Superior", localidade="Manaus"
        )
        vagas = self.service.recomendar_vagas(candidato)
        ids = [v.item.id for v in vagas]
        self.assertIn(2, ids)  # remoto
        self.assertNotIn(1, ids)  # presencial SP != Manaus
        self.assertNotIn(4, ids)  # híbrido RJ != Manaus
        # Remoto ganha pontuação PesoRecomendacao.AREA + PesoRecomendacao.REMOTO
        self.assertEqual(vagas[0].pontuacao, PesoRecomendacao.AREA + PesoRecomendacao.REMOTO)

    def test_recomenda_vaga_hibrida_localidade_coincide(self):
        """Recomendação: Vaga híbrida é recomendada se localidade coincide."""
        candidato = Candidato(
            3, "Pedro", "33344455566", "pedro@email.com",
            ["TI"], "Superior", localidade="Rio de Janeiro"
        )
        vagas = self.service.recomendar_vagas(candidato)
        ids = [v.item.id for v in vagas]
        self.assertIn(4, ids)  # híbrido RJ — match
        self.assertIn(2, ids)  # remoto — sempre
        self.assertNotIn(1, ids)  # presencial SP != RJ
        # Híbrido RJ (area+localidade+hibrido=90) > Remoto (area+remoto=70)
        pontuacoes = {v.item.id: v.pontuacao for v in vagas}
        self.assertGreater(pontuacoes[4], pontuacoes[2])

    def test_candidato_sem_localidade_nao_recebe_presencial(self):
        """Recomendação: Candidato sem localidade não recebe vagas presenciais/híbridas."""
        candidato = Candidato(
            4, "Ana", "44455566677", "ana@email.com",
            ["TI"], "Superior", localidade=""
        )
        vagas = self.service.recomendar_vagas(candidato)
        ids = [v.item.id for v in vagas]
        self.assertIn(2, ids)  # remoto — sempre
        self.assertNotIn(1, ids)  # presencial SP — sem localidade
        self.assertNotIn(4, ids)  # híbrido RJ — sem localidade

    # --- Cursos ---

    def test_recomenda_cursos_por_area_e_localidade(self):
        """Recomendação: Candidato de SP em TI recebe presencial SP + EAD."""
        candidato = Candidato(
            1, "Maria", "11122233344", "maria@email.com",
            ["TI"], "Superior", localidade="São Paulo"
        )
        cursos = self.service.recomendar_cursos(candidato)
        ids = [c.item.id for c in cursos]
        self.assertIn(1, ids)  # presencial SP — match
        self.assertIn(2, ids)  # EAD — sempre
        self.assertNotIn(3, ids)  # área Dados
        # Presencial SP (area+localidade=80) > EAD (area+remoto=70)
        self.assertGreaterEqual(cursos[0].pontuacao, cursos[1].pontuacao)

    def test_recomenda_curso_ead_qualquer_localidade(self):
        """Recomendação: Curso EAD é recomendado independente da localidade."""
        candidato = Candidato(
            2, "João", "22233344455", "joao@email.com",
            ["TI"], "Superior", localidade="Manaus"
        )
        cursos = self.service.recomendar_cursos(candidato)
        ids = [c.item.id for c in cursos]
        self.assertIn(2, ids)  # EAD
        self.assertNotIn(1, ids)  # presencial SP != Manaus
        self.assertEqual(cursos[0].pontuacao, PesoRecomendacao.AREA + PesoRecomendacao.REMOTO)

    def test_recomenda_curso_presencial_localidade_diferente(self):
        """Recomendação: Curso presencial de RJ não é recomendado para candidato de SP."""
        candidato = Candidato(
            1, "Maria", "11122233344", "maria@email.com",
            ["Dados"], "Superior", localidade="São Paulo"
        )
        cursos = self.service.recomendar_cursos(candidato)
        ids = [c.item.id for c in cursos]
        self.assertNotIn(3, ids)  # presencial RJ != SP

    # --- Recomendação completa ---

    def test_recomendar_retorna_vagas_e_cursos(self):
        """Recomendação: Método recomendar retorna vagas e cursos agrupados com pontuação."""
        candidato = Candidato(
            1, "Maria", "11122233344", "maria@email.com",
            ["TI"], "Superior", localidade="São Paulo"
        )
        rec = self.service.recomendar(candidato)
        self.assertGreater(len(rec.vagas), 0)
        self.assertGreater(len(rec.cursos), 0)
        # Cada item é um ItemRankeado
        self.assertTrue(all(isinstance(v, ItemRankeado) for v in rec.vagas))
        self.assertTrue(all(isinstance(c, ItemRankeado) for c in rec.cursos))

    def test_recomendacao_vazia_sem_area_compativel(self):
        """Recomendação: Nenhum resultado se área do candidato não existe."""
        candidato = Candidato(
            5, "Carlos", "55566677788", "carlos@email.com",
            ["Saúde"], "Superior", localidade="São Paulo"
        )
        rec = self.service.recomendar(candidato)
        self.assertEqual(len(rec.vagas), 0)
        self.assertEqual(len(rec.cursos), 0)

    def test_ranking_ordem_decrescente_pontuacao(self):
        """Recomendação: O ranking retorna itens ordenados do maior para o menor score."""
        candidato = Candidato(
            3, "Pedro", "33344455566", "pedro@email.com",
            ["TI"], "Superior", localidade="Rio de Janeiro"
        )
        vagas = self.service.recomendar_vagas(candidato)
        # Deve conter híbrido RJ e remoto
        self.assertEqual(len(vagas), 2)
        # Híbrido RJ: AREA(50) + LOCALIDADE(30) + HIBRIDO(10) = 90
        # Remoto:     AREA(50) + REMOTO(20) = 70
        self.assertEqual(vagas[0].pontuacao, 90)
        self.assertEqual(vagas[0].item.id, 4)
        self.assertEqual(vagas[1].pontuacao, 70)
        self.assertEqual(vagas[1].item.id, 2)

    def test_pontuacao_presencial_localidade_match(self):
        """Recomendação: Verifica pontuação correta para vaga presencial com localidade."""
        candidato = Candidato(
            1, "Maria", "11122233344", "maria@email.com",
            ["TI"], "Superior", localidade="São Paulo"
        )
        vagas = self.service.recomendar_vagas(candidato)
        pontuacoes = {v.item.id: v.pontuacao for v in vagas}
        # Presencial SP: AREA(50) + LOCALIDADE(30) = 80
        self.assertEqual(pontuacoes[1], 80)
        # Remoto: AREA(50) + REMOTO(20) = 70
        self.assertEqual(pontuacoes[2], 70)


if __name__ == '__main__':
    unittest.main()