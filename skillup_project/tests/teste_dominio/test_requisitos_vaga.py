import unittest
from src.dominio.requisitos_vaga import RequisitoVaga, RequisitoVagaMapper


class TestRequisitoVaga(unittest.TestCase):
    """Testes da entidade RequisitoVaga."""

    def _criar(self, **kwargs):
        defaults = dict(
            id=1, id_vaga=10, id_competencia=20,
            nivel_minimo="INTERMEDIARIO", obrigatorio=True,
        )
        defaults.update(kwargs)
        return RequisitoVaga(**defaults)

    def test_criacao_valida(self):
        r = self._criar()
        self.assertEqual(r.id_vaga, 10)
        self.assertEqual(r.id_competencia, 20)
        self.assertEqual(r.nivel_minimo, "INTERMEDIARIO")
        self.assertTrue(r.obrigatorio)

    def test_nivel_invalido(self):
        with self.assertRaises(ValueError):
            self._criar(nivel_minimo="expert")

    def test_obrigatorio_tipo_invalido(self):
        with self.assertRaises(TypeError):
            self._criar(obrigatorio="sim")

    # --- Regras de negócio ---

    def test_atualizar_nivel(self):
        r = self._criar()
        r.atualizar_nivel("AVANCADO")
        self.assertEqual(r.nivel_minimo, "AVANCADO")

    def test_tornar_opcional(self):
        r = self._criar(obrigatorio=True)
        r.tornar_opcional()
        self.assertFalse(r.obrigatorio)

    def test_tornar_obrigatorio(self):
        r = self._criar(obrigatorio=False)
        r.tornar_obrigatorio()
        self.assertTrue(r.obrigatorio)

    def test_nivel_como_inteiro(self):
        r = self._criar(nivel_minimo="INICIANTE")
        self.assertEqual(r.nivel_como_inteiro(), 0)
        r.atualizar_nivel("AVANCADO")
        self.assertEqual(r.nivel_como_inteiro(), 2)

    # --- Mapper ---

    def test_mapper_to_dict(self):
        r = self._criar()
        d = RequisitoVagaMapper.to_dict(r)
        self.assertEqual(d["vaga_id"], 10)
        self.assertEqual(d["competencia_id"], 20)
        self.assertEqual(d["nivel"], 1)  # INTERMEDIARIO = 1
        self.assertTrue(d["obrigatorio"])

    def test_mapper_round_trip(self):
        original = self._criar()
        d = RequisitoVagaMapper.to_dict(original)
        restaurado = RequisitoVagaMapper.from_dict(d)
        self.assertEqual(restaurado.id, original.id)
        self.assertEqual(restaurado.id_vaga, original.id_vaga)
        self.assertEqual(restaurado.id_competencia, original.id_competencia)
        self.assertTrue(restaurado.obrigatorio)


if __name__ == "__main__":
    unittest.main()