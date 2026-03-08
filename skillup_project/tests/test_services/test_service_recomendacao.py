import unittest
from unittest.mock import Mock
from src.services.service_recomendacao import (
    RecomendacaoService, PesoRecomendacao, ItemRankeado, Recomendacao,
)
from src.interfaces.interface_vaga import IVagaRepositorio
from src.interfaces.interface_curso import ICursoRepositorio
from src.dominio.vaga import VagaCLT, VagaEstagio, Modalidade, TipoVaga
from src.dominio.curso_presencial import CursoPresencial
from src.dominio.curso_ead import CursoEAD


class TestServiceRecomendacao(unittest.TestCase):
    """Testes do serviço de Recomendação."""

    def setUp(self):
        self.mock_repo_vaga = Mock(spec=IVagaRepositorio)
        self.mock_repo_curso = Mock(spec=ICursoRepositorio)
        self.service = RecomendacaoService(self.mock_repo_vaga, self.mock_repo_curso)

    def _mock_candidato(self, areas=None, localidade="São Paulo"):
        cand = Mock()
        cand.areas_interesse = areas or ["TI"]
        cand.localidade = localidade
        return cand

    def _mock_vaga_clt(self, id=1, area="TI", modalidade=Modalidade.PRESENCIAL,
                        localidade="São Paulo", salario=5000.0):
        vaga = Mock(spec=VagaCLT)
        vaga.id = id
        vaga.area = area
        vaga.modalidade = modalidade
        vaga.localidade = localidade
        vaga.salario_base = salario
        vaga.ativo = True
        type(vaga).tipo = TipoVaga.EMPREGO
        return vaga

    def _mock_curso_presencial(self, id=1, area="TI", localidade="São Paulo", ativo=True):
        curso = Mock(spec=CursoPresencial)
        curso.id = id
        curso.area = area
        curso.localidade = localidade
        curso.modalidade = Modalidade.PRESENCIAL
        curso.ativo = ativo
        return curso

    def _mock_curso_ead(self, id=1, area="TI", ativo=True):
        curso = Mock(spec=CursoEAD)
        curso.id = id
        curso.area = area
        curso.modalidade = Modalidade.REMOTO
        curso.ativo = ativo
        return curso

    # -- PESOS --

    def test_peso_area(self):
        self.assertEqual(PesoRecomendacao.AREA, 50)

    def test_peso_localidade(self):
        self.assertEqual(PesoRecomendacao.LOCALIDADE, 30)

    def test_peso_remoto(self):
        self.assertEqual(PesoRecomendacao.REMOTO, 20)

    def test_peso_hibrido(self):
        self.assertEqual(PesoRecomendacao.HIBRIDO, 10)

    # -- RECOMENDAÇÃO DE VAGAS --

    def test_recomendar_vagas_area_localidade(self):
        """Vaga presencial com área e localidade correspondentes = AREA + LOCALIDADE."""
        vaga = self._mock_vaga_clt(area="TI", localidade="São Paulo")
        self.mock_repo_vaga.listar_ativas.return_value = [vaga]
        candidato = self._mock_candidato(["TI"], "São Paulo")

        resultado = self.service.recomendar_vagas(candidato)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].pontuacao, PesoRecomendacao.AREA + PesoRecomendacao.LOCALIDADE)

    def test_recomendar_vagas_remota(self):
        """Vaga remota com área correspondente = AREA + REMOTO."""
        vaga = self._mock_vaga_clt(area="TI", modalidade=Modalidade.REMOTO, localidade="")
        self.mock_repo_vaga.listar_ativas.return_value = [vaga]
        candidato = self._mock_candidato(["TI"], "Qualquer Cidade")

        resultado = self.service.recomendar_vagas(candidato)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].pontuacao, PesoRecomendacao.AREA + PesoRecomendacao.REMOTO)

    def test_recomendar_vagas_hibrida(self):
        """Vaga híbrida com localidade correspondente = AREA + LOCALIDADE + HIBRIDO."""
        vaga = self._mock_vaga_clt(area="TI", modalidade=Modalidade.HIBRIDO, localidade="São Paulo")
        self.mock_repo_vaga.listar_ativas.return_value = [vaga]
        candidato = self._mock_candidato(["TI"], "São Paulo")

        resultado = self.service.recomendar_vagas(candidato)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(
            resultado[0].pontuacao,
            PesoRecomendacao.AREA + PesoRecomendacao.LOCALIDADE + PesoRecomendacao.HIBRIDO,
        )

    def test_recomendar_vagas_area_diferente_excluida(self):
        """Vagas de área diferente são excluídas."""
        vaga = self._mock_vaga_clt(area="Saúde")
        self.mock_repo_vaga.listar_ativas.return_value = [vaga]
        candidato = self._mock_candidato(["TI"])

        resultado = self.service.recomendar_vagas(candidato)
        self.assertEqual(len(resultado), 0)

    def test_recomendar_vagas_localidade_diferente_presencial_excluida(self):
        """Vaga presencial com localidade diferente e candidato com localidade é excluída."""
        vaga = self._mock_vaga_clt(area="TI", localidade="Rio de Janeiro")
        self.mock_repo_vaga.listar_ativas.return_value = [vaga]
        candidato = self._mock_candidato(["TI"], "São Paulo")

        resultado = self.service.recomendar_vagas(candidato)
        self.assertEqual(len(resultado), 0)

    def test_recomendar_vagas_candidato_sem_localidade_presencial_excluida(self):
        """Candidato sem localidade não recebe vagas presenciais com localidade."""
        vaga = self._mock_vaga_clt(area="TI", localidade="São Paulo")
        self.mock_repo_vaga.listar_ativas.return_value = [vaga]
        candidato = self._mock_candidato(["TI"], "")

        resultado = self.service.recomendar_vagas(candidato)
        self.assertEqual(len(resultado), 0)

    def test_recomendar_vagas_ordenacao_por_pontuacao(self):
        """Vagas são ordenadas por pontuação decrescente."""
        v_presencial = self._mock_vaga_clt(1, "TI", Modalidade.PRESENCIAL, "São Paulo")
        v_remoto = self._mock_vaga_clt(2, "TI", Modalidade.REMOTO, "")
        self.mock_repo_vaga.listar_ativas.return_value = [v_remoto, v_presencial]
        candidato = self._mock_candidato(["TI"], "São Paulo")

        resultado = self.service.recomendar_vagas(candidato)
        self.assertEqual(len(resultado), 2)
        # Presencial com localidade: 50+30=80 > Remoto: 50+20=70
        self.assertGreaterEqual(resultado[0].pontuacao, resultado[1].pontuacao)

    # -- RECOMENDAÇÃO DE CURSOS --

    def test_recomendar_cursos_presencial_mesma_localidade(self):
        curso = self._mock_curso_presencial(area="TI", localidade="São Paulo")
        self.mock_repo_curso.listar_todos.return_value = [curso]
        candidato = self._mock_candidato(["TI"], "São Paulo")

        resultado = self.service.recomendar_cursos(candidato)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(
            resultado[0].pontuacao, PesoRecomendacao.AREA + PesoRecomendacao.LOCALIDADE
        )

    def test_recomendar_cursos_ead(self):
        curso = self._mock_curso_ead(area="TI")
        self.mock_repo_curso.listar_todos.return_value = [curso]
        candidato = self._mock_candidato(["TI"], "Qualquer")

        resultado = self.service.recomendar_cursos(candidato)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].pontuacao, PesoRecomendacao.AREA + PesoRecomendacao.REMOTO)

    def test_recomendar_cursos_inativo_excluido(self):
        curso = self._mock_curso_ead(area="TI", ativo=False)
        self.mock_repo_curso.listar_todos.return_value = [curso]
        candidato = self._mock_candidato(["TI"])

        resultado = self.service.recomendar_cursos(candidato)
        self.assertEqual(len(resultado), 0)

    def test_recomendar_cursos_area_diferente_excluida(self):
        curso = self._mock_curso_ead(area="Saúde")
        self.mock_repo_curso.listar_todos.return_value = [curso]
        candidato = self._mock_candidato(["TI"])

        resultado = self.service.recomendar_cursos(candidato)
        self.assertEqual(len(resultado), 0)

    # -- RECOMENDAR (VAGAS + CURSOS) --

    def test_recomendar_retorna_recomendacao(self):
        vaga = self._mock_vaga_clt(area="TI", modalidade=Modalidade.REMOTO, localidade="")
        curso = self._mock_curso_ead(area="TI")
        self.mock_repo_vaga.listar_ativas.return_value = [vaga]
        self.mock_repo_curso.listar_todos.return_value = [curso]
        candidato = self._mock_candidato(["TI"])

        resultado = self.service.recomendar(candidato)
        self.assertIsInstance(resultado, Recomendacao)
        self.assertEqual(len(resultado.vagas), 1)
        self.assertEqual(len(resultado.cursos), 1)

    def test_recomendar_sem_correspondencias(self):
        self.mock_repo_vaga.listar_ativas.return_value = []
        self.mock_repo_curso.listar_todos.return_value = []
        candidato = self._mock_candidato(["TI"])

        resultado = self.service.recomendar(candidato)
        self.assertEqual(len(resultado.vagas), 0)
        self.assertEqual(len(resultado.cursos), 0)


if __name__ == "__main__":
    unittest.main()
