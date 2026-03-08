import unittest
from src.dominio.curso_competencia import CursoCompetencia, CursoCompetenciaMapper


class TestCursoCompetencia(unittest.TestCase):
    """Testes da entidade CursoCompetencia."""

    def _criar(self, **kwargs):
        defaults = dict(id=1, id_curso=10, id_competencia=20, nivel_conferido="intermediario")
        defaults.update(kwargs)
        return CursoCompetencia(**defaults)

    def test_criacao_valida(self):
        c = self._criar()
        self.assertEqual(c.id_curso, 10)
        self.assertEqual(c.id_competencia, 20)
        self.assertEqual(c.nivel_conferido, "intermediario")

    def test_nivel_normaliza_lowercase(self):
        c = self._criar(nivel_conferido="AVANCADO")
        self.assertEqual(c.nivel_conferido, "avancado")

    def test_nivel_invalido(self):
        with self.assertRaises(ValueError):
            self._criar(nivel_conferido="expert")

    def test_atualizar_nivel(self):
        c = self._criar()
        c.atualizar_nivel("AVANCADO")
        self.assertEqual(c.nivel_conferido, "avancado")

    def test_nivel_como_inteiro(self):
        c = self._criar(nivel_conferido="INICIANTE")
        self.assertEqual(c.nivel_como_inteiro(), 0)

    def test_mapper_round_trip(self):
        original = self._criar()
        d = CursoCompetenciaMapper.to_dict(original)
        restaurado = CursoCompetenciaMapper.from_dict(d)
        self.assertEqual(restaurado.id, original.id)
        self.assertEqual(restaurado.id_curso, original.id_curso)
        self.assertEqual(restaurado.id_competencia, original.id_competencia)
        self.assertEqual(restaurado.nivel_conferido, original.nivel_conferido)


if __name__ == "__main__":
    unittest.main()