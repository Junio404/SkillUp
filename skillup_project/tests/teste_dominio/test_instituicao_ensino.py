import unittest
from src.dominio.instituicao_ensino import (
    InstituicaoEnsino, InstituicaoEnsinoMapper,
    AreaEnsino, AreaEnsinoMapper,
    InstituicaoAreaEnsino, InstituicaoAreaEnsinoMapper,
)


class TestInstituicaoEnsino(unittest.TestCase):
    """Testes da entidade InstituicaoEnsino."""

    def _criar(self, **kwargs):
        defaults = dict(
            id=1, razao_social="Escola Tech LTDA", nome_fantasia="Escola Tech",
            _cnpj="12345678000199", registro_educacional="REG123",
            tipo="Universidade", modalidades=["Presencial", "EAD"],
            credenciada=True,
        )
        defaults.update(kwargs)
        return InstituicaoEnsino(**defaults)

    def test_criacao_valida(self):
        i = self._criar()
        self.assertEqual(i.razao_social, "Escola Tech LTDA")
        self.assertEqual(i.cnpj, "12345678000199")
        self.assertTrue(i.credenciada)

    def test_cnpj_invalido(self):
        with self.assertRaises(ValueError):
            self._criar(_cnpj="123")

    def test_validar_publicacao_credenciada(self):
        i = self._criar(credenciada=True)
        self.assertTrue(i.validar_publicacao())

    def test_validar_publicacao_nao_credenciada(self):
        i = self._criar(credenciada=False)
        with self.assertRaises(PermissionError):
            i.validar_publicacao()

    def test_mapper_round_trip(self):
        original = self._criar()
        d = InstituicaoEnsinoMapper.to_dict(original)
        restaurado = InstituicaoEnsinoMapper.from_dict(d)
        self.assertEqual(restaurado.id, original.id)
        self.assertEqual(restaurado.cnpj, original.cnpj)
        self.assertEqual(restaurado.credenciada, original.credenciada)
        self.assertEqual(restaurado.modalidades, original.modalidades)


class TestAreaEnsino(unittest.TestCase):
    """Testes da entidade AreaEnsino."""

    def test_criacao_valida(self):
        a = AreaEnsino(id_area=1, nome_area="Tecnologia")
        self.assertEqual(a.id_area, 1)
        self.assertEqual(a.nome_area, "Tecnologia")

    def test_nome_vazio(self):
        with self.assertRaises(ValueError):
            AreaEnsino(id_area=1, nome_area="")

    def test_id_invalido(self):
        with self.assertRaises(ValueError):
            AreaEnsino(id_area=-1, nome_area="Tecnologia")

    def test_mapper_round_trip(self):
        original = AreaEnsino(id_area=1, nome_area="Saúde")
        d = AreaEnsinoMapper.to_dict(original)
        restaurado = AreaEnsinoMapper.from_dict(d)
        self.assertEqual(restaurado.id_area, original.id_area)
        self.assertEqual(restaurado.nome_area, original.nome_area)


class TestInstituicaoAreaEnsino(unittest.TestCase):
    """Testes da entidade InstituicaoAreaEnsino."""

    def test_criacao_valida(self):
        ia = InstituicaoAreaEnsino(id_instituicao_area=1, id_instituicao=10, id_area=20)
        self.assertEqual(ia.id_instituicao_area, 1)
        self.assertEqual(ia.id_instituicao, 10)
        self.assertEqual(ia.id_area, 20)

    def test_id_invalido(self):
        with self.assertRaises(ValueError):
            InstituicaoAreaEnsino(id_instituicao_area=-1, id_instituicao=10, id_area=20)

    def test_mapper_round_trip(self):
        original = InstituicaoAreaEnsino(id_instituicao_area=1, id_instituicao=10, id_area=20)
        d = InstituicaoAreaEnsinoMapper.to_dict(original)
        restaurado = InstituicaoAreaEnsinoMapper.from_dict(d)
        self.assertEqual(restaurado.id_instituicao_area, original.id_instituicao_area)
        self.assertEqual(restaurado.id_instituicao, original.id_instituicao)
        self.assertEqual(restaurado.id_area, original.id_area)


if __name__ == "__main__":
    unittest.main()