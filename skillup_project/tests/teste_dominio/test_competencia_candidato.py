import unittest
from src.dominio.competencia_candidato import CompetenciaCandidato, CompetenciaCandidatoMapper


class TestCompetenciaCandidato(unittest.TestCase):
    """Testes da entidade CompetenciaCandidato."""

    def _criar(self, **kwargs):
        defaults = dict(id=1, id_candidato=10, id_competencia=20, nivel_atual="intermediario")
        defaults.update(kwargs)
        return CompetenciaCandidato(**defaults)

    def test_criacao_valida(self):
        c = self._criar()
        self.assertEqual(c.id, 1)
        self.assertEqual(c.id_candidato, 10)
        self.assertEqual(c.id_competencia, 20)
        self.assertEqual(c.nivel_atual, "intermediario")

    def test_nivel_normaliza_lowercase(self):
        c = self._criar(nivel_atual="AVANCADO")
        self.assertEqual(c.nivel_atual, "avancado")

    def test_nivel_invalido(self):
        with self.assertRaises(ValueError):
            self._criar(nivel_atual="expert")

    def test_atualizar_nivel(self):
        c = self._criar()
        c.atualizar_nivel("avancado")
        self.assertEqual(c.nivel_atual, "avancado")

    def test_atualizar_nivel_invalido(self):
        c = self._criar()
        with self.assertRaises(ValueError):
            c.atualizar_nivel("master")

    def test_nivel_como_inteiro(self):
        c = self._criar(nivel_atual="iniciante")
        self.assertEqual(c.nivel_como_inteiro(), 0)
        c.atualizar_nivel("intermediario")
        self.assertEqual(c.nivel_como_inteiro(), 1)
        c.atualizar_nivel("avancado")
        self.assertEqual(c.nivel_como_inteiro(), 2)

    def test_mapper_round_trip(self):
        original = self._criar()
        d = CompetenciaCandidatoMapper.to_dict(original)
        restaurado = CompetenciaCandidatoMapper.from_dict(d)
        self.assertEqual(restaurado.id, original.id)
        self.assertEqual(restaurado.id_candidato, original.id_candidato)
        self.assertEqual(restaurado.id_competencia, original.id_competencia)
        self.assertEqual(restaurado.nivel_atual, original.nivel_atual)


if __name__ == "__main__":
    unittest.main()