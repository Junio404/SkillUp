import unittest
from unittest.mock import Mock
from src.services.service_busca_vaga import MotorBuscaVaga
from src.interfaces.interface_vaga import IVagaRepositorio
from src.dominio.vaga import VagaCLT, VagaEstagio, Modalidade, TipoVaga


class TestServiceBuscaVaga(unittest.TestCase):
    """Testes do motor de busca de vagas."""

    def setUp(self):
        self.mock_repo = Mock(spec=IVagaRepositorio)
        self.motor = MotorBuscaVaga(self.mock_repo)

    def _criar_vaga_clt(self, id, area="TI", modalidade=Modalidade.PRESENCIAL,
                        localidade="São Paulo", salario=5000.0, ativo=True):
        vaga = Mock(spec=VagaCLT)
        vaga.id = id
        vaga.area = area
        vaga.modalidade = modalidade
        vaga.localidade = localidade
        vaga.salario_base = salario
        vaga.ativo = ativo
        vaga.tipo = TipoVaga.EMPREGO
        return vaga

    def _criar_vaga_estagio(self, id, area="TI", modalidade=Modalidade.PRESENCIAL,
                            localidade="São Paulo", bolsa=1500.0, ativo=True):
        vaga = Mock(spec=VagaEstagio)
        vaga.id = id
        vaga.area = area
        vaga.modalidade = modalidade
        vaga.localidade = localidade
        vaga.bolsa_auxilio = bolsa
        vaga.ativo = ativo
        vaga.tipo = TipoVaga.ESTAGIO
        return vaga

    # -- BUSCA COM FILTROS --

    def test_buscar_por_area(self):
        v1 = self._criar_vaga_clt(1, area="TI")
        v2 = self._criar_vaga_clt(2, area="Saúde")
        self.mock_repo.listar_ativas.return_value = [v1, v2]
        resultado = self.motor.buscar(area="TI")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].id, 1)

    def test_buscar_por_modalidade(self):
        v1 = self._criar_vaga_clt(1, modalidade=Modalidade.REMOTO, localidade="")
        v2 = self._criar_vaga_clt(2, modalidade=Modalidade.PRESENCIAL)
        self.mock_repo.listar_ativas.return_value = [v1, v2]
        resultado = self.motor.buscar(modalidade=Modalidade.REMOTO)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].modalidade, Modalidade.REMOTO)

    def test_buscar_por_localidade(self):
        v1 = self._criar_vaga_clt(1, localidade="São Paulo")
        v2 = self._criar_vaga_clt(2, localidade="Rio de Janeiro")
        self.mock_repo.listar_ativas.return_value = [v1, v2]
        resultado = self.motor.buscar(localidade="São Paulo")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].localidade, "São Paulo")

    def test_buscar_por_faixa_salarial(self):
        v1 = self._criar_vaga_clt(1, salario=3000.0)
        v2 = self._criar_vaga_clt(2, salario=8000.0)
        v3 = self._criar_vaga_clt(3, salario=15000.0)
        self.mock_repo.listar_ativas.return_value = [v1, v2, v3]
        resultado = self.motor.buscar(salario_min=5000.0, salario_max=10000.0)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].id, 2)

    def test_buscar_por_tipo(self):
        v1 = self._criar_vaga_clt(1)
        v2 = self._criar_vaga_estagio(2)
        self.mock_repo.listar_ativas.return_value = [v1, v2]
        resultado = self.motor.buscar(tipo=TipoVaga.EMPREGO)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].tipo, TipoVaga.EMPREGO)

    def test_buscar_sem_filtros_retorna_todas_ativas(self):
        vagas = [self._criar_vaga_clt(i) for i in range(5)]
        self.mock_repo.listar_ativas.return_value = vagas
        resultado = self.motor.buscar()
        self.assertEqual(len(resultado), 5)

    def test_buscar_vaga_remota_ignora_localidade(self):
        v_remota = self._criar_vaga_clt(1, modalidade=Modalidade.REMOTO, localidade="")
        v_presencial = self._criar_vaga_clt(2, localidade="Rio")
        self.mock_repo.listar_ativas.return_value = [v_remota, v_presencial]
        resultado = self.motor.buscar(localidade="São Paulo")
        # Vaga remota passa; vaga presencial em Rio não passa
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].modalidade, Modalidade.REMOTO)

    def test_buscar_filtros_combinados(self):
        v1 = self._criar_vaga_clt(1, area="TI", salario=8000.0)
        v2 = self._criar_vaga_clt(2, area="TI", salario=3000.0)
        v3 = self._criar_vaga_clt(3, area="Saúde", salario=8000.0)
        self.mock_repo.listar_ativas.return_value = [v1, v2, v3]
        resultado = self.motor.buscar(area="TI", salario_min=5000.0)
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].id, 1)

    def test_buscar_incluindo_inativas(self):
        v1 = self._criar_vaga_clt(1, ativo=True)
        v2 = self._criar_vaga_clt(2, ativo=False)
        self.mock_repo.listar_todas.return_value = [v1, v2]
        resultado = self.motor.buscar(apenas_ativas=False)
        self.assertEqual(len(resultado), 2)

    # -- BUSCA POR CANDIDATO --

    def test_buscar_por_candidato_area_correspondente(self):
        v1 = self._criar_vaga_clt(1, area="TI", localidade="São Paulo")
        v2 = self._criar_vaga_clt(2, area="Saúde", localidade="São Paulo")
        self.mock_repo.listar_ativas.return_value = [v1, v2]
        resultado = self.motor.buscar_por_candidato(["TI"], "São Paulo")
        self.assertEqual(len(resultado), 1)
        self.assertEqual(resultado[0].area, "TI")

    def test_buscar_por_candidato_localidade_diferente(self):
        v1 = self._criar_vaga_clt(1, area="TI", localidade="Rio")
        self.mock_repo.listar_ativas.return_value = [v1]
        resultado = self.motor.buscar_por_candidato(["TI"], "São Paulo")
        self.assertEqual(len(resultado), 0)

    def test_buscar_por_candidato_vaga_remota(self):
        v1 = self._criar_vaga_clt(1, area="TI", modalidade=Modalidade.REMOTO, localidade="")
        self.mock_repo.listar_ativas.return_value = [v1]
        resultado = self.motor.buscar_por_candidato(["TI"], "Qualquer Cidade")
        self.assertEqual(len(resultado), 1)

    def test_buscar_por_candidato_sem_area_interesse(self):
        v1 = self._criar_vaga_clt(1, area="TI")
        self.mock_repo.listar_ativas.return_value = [v1]
        resultado = self.motor.buscar_por_candidato(["Saúde"], "São Paulo")
        self.assertEqual(len(resultado), 0)


if __name__ == "__main__":
    unittest.main()
