import unittest
from src.dominio.competencia import Competencia, CompetenciaNivelada, Nivel, CompetenciaMapper, CompetenciaNiveladaMapper


class TestCompetencia(unittest.TestCase):
    """Testes da entidade Competencia."""

    def test_criacao_valida(self):
        c = Competencia(id=1, nome="Python", descricao="Linguagem de programação")
        self.assertEqual(c.id, 1)
        self.assertEqual(c.nome, "Python")
        self.assertEqual(c.descricao, "Linguagem de programação")

    def test_criacao_sem_descricao(self):
        c = Competencia(id=1, nome="Python")
        self.assertIsNone(c.descricao)

    def test_nome_vazio(self):
        with self.assertRaises(ValueError):
            Competencia(id=1, nome="")

    def test_id_negativo(self):
        with self.assertRaises(ValueError):
            Competencia(id=-1, nome="Python")

    def test_descricao_tipo_invalido(self):
        with self.assertRaises(TypeError):
            Competencia(id=1, nome="Python", descricao=123)

    def test_mapper_round_trip(self):
        original = Competencia(id=1, nome="Python", descricao="Backend")
        d = CompetenciaMapper.to_dict(original)
        restaurado = CompetenciaMapper.from_dict(d)
        self.assertEqual(restaurado.id, original.id)
        self.assertEqual(restaurado.nome, original.nome)
        self.assertEqual(restaurado.descricao, original.descricao)


class TestCompetenciaNivelada(unittest.TestCase):
    """Testes da entidade CompetenciaNivelada."""

    def test_criacao_valida(self):
        c = CompetenciaNivelada(id=1, nome="Python", nivel=Nivel.AVANCADO)
        self.assertEqual(c.nivel, Nivel.AVANCADO)

    def test_criacao_nivel_default(self):
        c = CompetenciaNivelada(id=1, nome="Python")
        self.assertEqual(c.nivel, Nivel.INICIANTE)

    def test_mapper_round_trip(self):
        original = CompetenciaNivelada(id=1, nome="Python", nivel=Nivel.INTERMEDIARIO)
        d = CompetenciaNiveladaMapper.to_dict(original)
        restaurado = CompetenciaNiveladaMapper.from_dict(d)
        self.assertEqual(restaurado.nivel, original.nivel)


class TestNivelEnum(unittest.TestCase):
    """Testes do enum Nivel."""

    def test_valores(self):
        self.assertEqual(Nivel.INICIANTE.value, 0)
        self.assertEqual(Nivel.INTERMEDIARIO.value, 1)
        self.assertEqual(Nivel.AVANCADO.value, 2)


if __name__ == "__main__":
    unittest.main()