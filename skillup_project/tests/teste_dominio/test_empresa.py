import unittest
from src.dominio.empresa import Empresa, EmpresaMapper


class TestEmpresa(unittest.TestCase):
    """Testes da entidade de domínio Empresa."""

    def _criar_empresa(self, **kwargs):
        defaults = dict(id=1, nome="Tech SA", _cnpj="12345678000199", porte="medio")
        defaults.update(kwargs)
        return Empresa(**defaults)

    # --- Criação válida ---

    def test_criacao_valida(self):
        e = self._criar_empresa()
        self.assertEqual(e.id, 1)
        self.assertEqual(e.nome, "Tech SA")
        self.assertEqual(e.cnpj, "12345678000199")
        self.assertEqual(e.porte, "medio")

    # --- Validações ---

    def test_cnpj_invalido_tamanho(self):
        with self.assertRaises(ValueError):
            self._criar_empresa(_cnpj="123")

    def test_cnpj_invalido_letras(self):
        with self.assertRaises(ValueError):
            self._criar_empresa(_cnpj="1234567800019X")

    def test_porte_invalido(self):
        with self.assertRaises(ValueError):
            self._criar_empresa(porte="enorme")

    def test_nome_vazio(self):
        with self.assertRaises(ValueError):
            self._criar_empresa(nome="")

    def test_id_negativo(self):
        with self.assertRaises(ValueError):
            self._criar_empresa(id=-1)

    # --- Regras de negócio ---

    def test_obter_limites_publicacao_pequeno(self):
        e = self._criar_empresa(porte="pequeno")
        self.assertEqual(e.obter_limites_publicacao(), 5)

    def test_obter_limites_publicacao_medio(self):
        e = self._criar_empresa(porte="medio")
        self.assertEqual(e.obter_limites_publicacao(), 15)

    def test_obter_limites_publicacao_grande(self):
        e = self._criar_empresa(porte="grande")
        self.assertEqual(e.obter_limites_publicacao(), 50)

    def test_validar_publicacao(self):
        e = self._criar_empresa()
        self.assertTrue(e.validar_publicacao(None))

    # --- Mapper ---

    def test_mapper_to_dict(self):
        e = self._criar_empresa()
        d = EmpresaMapper.to_dict(e)
        self.assertEqual(d["cnpj"], "12345678000199")
        self.assertEqual(d["porte"], "medio")

    def test_mapper_round_trip(self):
        original = self._criar_empresa()
        d = EmpresaMapper.to_dict(original)
        restaurado = EmpresaMapper.from_dict(d)
        self.assertEqual(restaurado.id, original.id)
        self.assertEqual(restaurado.cnpj, original.cnpj)
        self.assertEqual(restaurado.porte, original.porte)


if __name__ == "__main__":
    unittest.main()