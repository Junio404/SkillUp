import unittest
from datetime import date
from src.dominio.inscricao_curso import InscricaoCurso, StatusInscricao, InscricaoCursoMapper


class TestInscricaoCurso(unittest.TestCase):
    """Testes da entidade InscricaoCurso."""

    def _criar(self, **kwargs):
        defaults = dict(id=1, id_curso=10, id_aluno=20, data_inscricao=date.today())
        defaults.update(kwargs)
        return InscricaoCurso(**defaults)

    def test_criacao_valida(self):
        i = self._criar()
        self.assertEqual(i.id_curso, 10)
        self.assertEqual(i.id_aluno, 20)
        self.assertEqual(i.status, StatusInscricao.DEFERIDO)

    def test_deferir(self):
        i = self._criar(status=StatusInscricao.INDEFERIDO)
        i.deferir()
        self.assertEqual(i.status, StatusInscricao.DEFERIDO)

    def test_indeferir(self):
        i = self._criar()
        i.indeferir()
        self.assertEqual(i.status, StatusInscricao.INDEFERIDO)

    def test_data_invalida(self):
        with self.assertRaises(TypeError):
            self._criar(data_inscricao="2026-03-05")

    def test_mapper_round_trip(self):
        original = self._criar()
        d = InscricaoCursoMapper.to_dict(original)
        restaurado = InscricaoCursoMapper.from_dict(d)
        self.assertEqual(restaurado.id, original.id)
        self.assertEqual(restaurado.id_curso, original.id_curso)
        self.assertEqual(restaurado.id_aluno, original.id_aluno)
        self.assertEqual(restaurado.status, original.status)


class TestStatusInscricao(unittest.TestCase):
    """Testes do enum StatusInscricao."""

    def test_valores(self):
        self.assertEqual(StatusInscricao.DEFERIDO.value, 0)
        self.assertEqual(StatusInscricao.INDEFERIDO.value, 1)


if __name__ == "__main__":
    unittest.main()