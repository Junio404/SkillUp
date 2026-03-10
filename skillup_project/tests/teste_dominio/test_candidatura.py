import unittest
from unittest.mock import patch
from src.dominio.candidatura import Candidatura, StatusCandidatura, CandidaturaMapper, TipoVagaCandidatura
from src.dominio.validators import PrazoValidador


class TestCandidatura(unittest.TestCase):
    """Testes da entidade Candidatura.

    Nota: Candidatura usa PrazoValidador que espera date, mas data_candidatura
    é string. Usamos patch no PrazoValidador para contornar essa incompatibilidade.
    """

    def _criar(self, **kwargs):
        defaults = dict(id=1, id_vaga=10, id_candidato=20, tipo_vaga=TipoVagaCandidatura.CLT)
        defaults.update(kwargs)
        with patch.object(PrazoValidador, "validar", return_value=None):
            return Candidatura(**defaults)

    def test_criacao_valida(self):
        c = self._criar()
        self.assertEqual(c.id, 1)
        self.assertEqual(c.id_vaga, 10)
        self.assertEqual(c.id_candidato, 20)
        self.assertEqual(c.status, StatusCandidatura.ENVIADO)
        self.assertIsNotNone(c.data_candidatura)

    def test_criacao_com_status(self):
        c = self._criar(status=StatusCandidatura.EM_ANALISE)
        self.assertEqual(c.status, StatusCandidatura.EM_ANALISE)

    def test_id_vaga_invalido(self):
        with self.assertRaises(ValueError):
            self._criar(id_vaga=-1)

    def test_id_candidato_invalido(self):
        with self.assertRaises(ValueError):
            self._criar(id_candidato=0)

    # --- Regras de negócio ---

    def test_aprovar(self):
        c = self._criar()
        c.aprovar()
        self.assertEqual(c.status, StatusCandidatura.ACEITO)

    def test_reprovar(self):
        c = self._criar()
        c.reprovar()
        self.assertEqual(c.status, StatusCandidatura.RECUSADO)

    def test_cancelar(self):
        c = self._criar()
        c.cancelar()
        self.assertEqual(c.status, StatusCandidatura.CANCELADO)

    def test_cancelar_aceita_falha(self):
        c = self._criar()
        c.aprovar()
        with self.assertRaises(ValueError):
            c.cancelar()

    def test_cancelar_recusada_falha(self):
        c = self._criar()
        c.reprovar()
        with self.assertRaises(ValueError):
            c.cancelar()

    def test_analisar(self):
        c = self._criar()
        c.analisar()
        self.assertEqual(c.status, StatusCandidatura.EM_ANALISE)

    # --- Mapper ---

    def test_mapper_to_dict(self):
        c = self._criar()
        d = CandidaturaMapper.to_dict(c)
        self.assertEqual(d["id_candidatura"], 1)
        self.assertEqual(d["id_vaga"], 10)
        self.assertEqual(d["id_candidato"], 20)
        self.assertEqual(d["status"], "Enviado")

    def test_mapper_round_trip(self):
        original = self._criar()
        d = CandidaturaMapper.to_dict(original)
        with patch.object(PrazoValidador, "validar", return_value=None):
            restaurado = CandidaturaMapper.from_dict(d)
        self.assertEqual(restaurado.id, original.id)
        self.assertEqual(restaurado.id_vaga, original.id_vaga)
        self.assertEqual(restaurado.status, original.status)


class TestStatusCandidatura(unittest.TestCase):
    """Testes do enum StatusCandidatura."""

    def test_valores(self):
        self.assertEqual(StatusCandidatura.ENVIADO.value, "Enviado")
        self.assertEqual(StatusCandidatura.EM_ANALISE.value, "Em analise")
        self.assertEqual(StatusCandidatura.ACEITO.value, "Aceito")
        self.assertEqual(StatusCandidatura.RECUSADO.value, "Recusado")
        self.assertEqual(StatusCandidatura.CANCELADO.value, "Cancelado")


if __name__ == "__main__":
    unittest.main()