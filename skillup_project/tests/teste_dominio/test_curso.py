import unittest
from datetime import date
from src.dominio.curso_ead import CursoEAD, CursoEADMapper
from src.dominio.curso_presencial import CursoPresencial, CursoPresencialMapper
from src.dominio.vaga import Modalidade


class TestCursoEAD(unittest.TestCase):
    """Testes da entidade CursoEAD."""

    def _criar(self, **kwargs):
        defaults = dict(
            id=1, nome="Python EAD", area="TI", carga_horaria=40,
            modalidade=Modalidade.REMOTO, capacidade=100,
            prazo_inscricao=date(2027, 12, 31), plataforma_url="http://ead.com",
            id_instituicao=1,
        )
        defaults.update(kwargs)
        return CursoEAD(**defaults)

    def test_criacao_valida(self):
        c = self._criar()
        self.assertEqual(c.nome, "Python EAD")
        self.assertEqual(c.plataforma_url, "http://ead.com")
        self.assertTrue(c.ativo)

    def test_exibir_detalhes(self):
        c = self._criar()
        detalhes = c.exibir_detalhes()
        self.assertIn("Curso EAD", detalhes)
        self.assertIn("Python EAD", detalhes)
        self.assertIn("http://ead.com", detalhes)

    def test_publicar_pausar(self):
        c = self._criar()
        c.pausar()
        self.assertFalse(c.ativo)
        c.publicar()
        self.assertTrue(c.ativo)

    def test_prazo_passado_invalido(self):
        with self.assertRaises(ValueError):
            self._criar(prazo_inscricao=date(2020, 1, 1))

    def test_url_vazia_invalida(self):
        with self.assertRaises(ValueError):
            self._criar(plataforma_url="")

    def test_mapper_round_trip(self):
        original = self._criar()
        d = CursoEADMapper.to_dict(original)
        restaurado = CursoEADMapper.from_dict(d)
        self.assertEqual(restaurado.id, original.id)
        self.assertEqual(restaurado.nome, original.nome)
        self.assertEqual(restaurado.plataforma_url, original.plataforma_url)


class TestCursoPresencial(unittest.TestCase):
    """Testes da entidade CursoPresencial."""

    def _criar(self, **kwargs):
        defaults = dict(
            id=1, nome="Python Presencial", area="TI", carga_horaria=40,
            modalidade=Modalidade.PRESENCIAL, capacidade=30,
            prazo_inscricao=date(2027, 12, 31), localidade="São Paulo",
            id_instituicao=1,
        )
        defaults.update(kwargs)
        return CursoPresencial(**defaults)

    def test_criacao_valida(self):
        c = self._criar()
        self.assertEqual(c.localidade, "São Paulo")

    def test_exibir_detalhes(self):
        c = self._criar()
        detalhes = c.exibir_detalhes()
        self.assertIn("Curso Presencial", detalhes)
        self.assertIn("São Paulo", detalhes)

    def test_localidade_vazia_invalida(self):
        with self.assertRaises(ValueError):
            self._criar(localidade="")

    def test_editar_curso(self):
        c = self._criar()
        c.editar(nome="Java Presencial", carga_horaria=60)
        self.assertEqual(c.nome, "Java Presencial")
        self.assertEqual(c.carga_horaria, 60)

    def test_mapper_round_trip(self):
        original = self._criar()
        d = CursoPresencialMapper.to_dict(original)
        restaurado = CursoPresencialMapper.from_dict(d)
        self.assertEqual(restaurado.id, original.id)
        self.assertEqual(restaurado.localidade, original.localidade)
        self.assertEqual(restaurado.modalidade, original.modalidade)


if __name__ == "__main__":
    unittest.main()