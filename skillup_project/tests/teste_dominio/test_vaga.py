import unittest
from datetime import date
from src.dominio.vaga import VagaCLT, VagaEstagio, Modalidade, TipoVaga, VagaCLTMapper, VagaEstagioMapper


class TestVagaCLT(unittest.TestCase):
    """Testes da entidade VagaCLT."""

    def _criar_vaga_clt(self, **kwargs):
        defaults = dict(
            id=1, id_empresa=1, titulo="Dev Python", descricao="Backend",
            area="TI", modalidade=Modalidade.REMOTO, tipo=TipoVaga.EMPREGO,
            salario_base=8000.0, prazo_inscricao=date(2027, 12, 31),
            localidade="São Paulo",
        )
        defaults.update(kwargs)
        return VagaCLT(**defaults)

    def test_criacao_valida(self):
        v = self._criar_vaga_clt()
        self.assertEqual(v.titulo, "Dev Python")
        self.assertEqual(v.salario_base, 8000.0)
        self.assertEqual(v.localidade, "São Paulo")
        self.assertTrue(v.ativa)

    def test_custo_contratacao(self):
        v = self._criar_vaga_clt(salario_base=5000.0)
        self.assertAlmostEqual(v.calcular_custo_contratacao(), 9000.0)

    def test_adicionar_requisito(self):
        v = self._criar_vaga_clt()
        v.adicionar_requisito("Python 3+")
        self.assertIn("Python 3+", v.requisitos)

    def test_adicionar_requisito_vazio(self):
        v = self._criar_vaga_clt()
        with self.assertRaises(ValueError):
            v.adicionar_requisito("   ")

    def test_pausar_publicar(self):
        v = self._criar_vaga_clt()
        v.pausar()
        self.assertFalse(v.ativa)
        v.publicar()
        self.assertTrue(v.ativa)

    def test_editar(self):
        v = self._criar_vaga_clt()
        v.editar(titulo="Dev Senior", descricao="Full-stack")
        self.assertEqual(v.titulo, "Dev Senior")
        self.assertEqual(v.descricao, "Full-stack")

    def test_localidade_tipo_invalido(self):
        with self.assertRaises(TypeError):
            self._criar_vaga_clt(localidade=123)

    def test_mapper_round_trip(self):
        original = self._criar_vaga_clt()
        d = VagaCLTMapper.to_dict(original)
        restaurado = VagaCLTMapper.from_dict(d)
        self.assertEqual(restaurado.id, original.id)
        self.assertEqual(restaurado.salario_base, original.salario_base)
        self.assertEqual(restaurado.localidade, original.localidade)
        self.assertEqual(restaurado.modalidade, original.modalidade)


class TestVagaEstagio(unittest.TestCase):
    """Testes da entidade VagaEstagio."""

    def _criar_vaga_estagio(self, **kwargs):
        defaults = dict(
            id=1, id_empresa=1, titulo="Estágio Dev", descricao="Python", area="TI",
            modalidade=Modalidade.PRESENCIAL, tipo=TipoVaga.ESTAGIO,
            bolsa_auxilio=1500.0, id_instituicao_conveniada=1,
            prazo_inscricao=date(2027, 12, 31), localidade="São Paulo",
        )
        defaults.update(kwargs)
        return VagaEstagio(**defaults)

    def test_criacao_valida(self):
        v = self._criar_vaga_estagio()
        self.assertEqual(v.bolsa_auxilio, 1500.0)
        self.assertEqual(v.id_instituicao_conveniada, 1)
        self.assertEqual(v.localidade, "São Paulo")

    def test_custo_contratacao(self):
        v = self._criar_vaga_estagio(bolsa_auxilio=1000.0)
        self.assertAlmostEqual(v.calcular_custo_contratacao(), 1100.0)

    def test_mapper_round_trip(self):
        original = self._criar_vaga_estagio()
        d = VagaEstagioMapper.to_dict(original)
        restaurado = VagaEstagioMapper.from_dict(d)
        self.assertEqual(restaurado.id, original.id)
        self.assertEqual(restaurado.bolsa_auxilio, original.bolsa_auxilio)
        self.assertEqual(restaurado.localidade, original.localidade)
        self.assertEqual(restaurado.id_instituicao_conveniada, original.id_instituicao_conveniada)


class TestModalidadeEnum(unittest.TestCase):
    """Testes dos enums de Vaga."""

    def test_modalidade_values(self):
        self.assertEqual(Modalidade.PRESENCIAL.value, "Presencial")
        self.assertEqual(Modalidade.REMOTO.value, "Remoto")
        self.assertEqual(Modalidade.HIBRIDO.value, "Híbrido")

    def test_tipo_vaga_values(self):
        self.assertEqual(TipoVaga.EMPREGO.value, "Emprego")
        self.assertEqual(TipoVaga.ESTAGIO.value, "Estágio")
        self.assertEqual(TipoVaga.TRAINEE.value, "Trainee")


if __name__ == "__main__":
    unittest.main()