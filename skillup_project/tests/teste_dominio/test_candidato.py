import unittest
from src.dominio.candidato import Candidato, CandidatoMapper


class TestCandidato(unittest.TestCase):
    """Testes da entidade de domínio Candidato."""

    def _criar_candidato(self, **kwargs):
        defaults = dict(
            id=1, nome="Maria Silva", _cpf="11122233344",
            email="maria@email.com", _areas_interesse=["TI"],
            nivel_formacao="Superior", localidade="São Paulo",
        )
        defaults.update(kwargs)
        return Candidato(**defaults)

    # --- Criação válida ---

    def test_criacao_valida(self):
        c = self._criar_candidato()
        self.assertEqual(c.id, 1)
        self.assertEqual(c.nome, "Maria Silva")
        self.assertEqual(c.cpf, "11122233344")
        self.assertEqual(c.email, "maria@email.com")
        self.assertEqual(c.areas_interesse, ("TI",))
        self.assertEqual(c.nivel_formacao, "Superior")
        self.assertEqual(c.localidade, "São Paulo")

    def test_criacao_sem_localidade(self):
        c = self._criar_candidato(localidade="")
        self.assertEqual(c.localidade, "")

    # --- Validações ---

    def test_cpf_invalido_letras(self):
        with self.assertRaises(ValueError):
            self._criar_candidato(_cpf="1234567890a")

    def test_cpf_invalido_tamanho(self):
        with self.assertRaises(ValueError):
            self._criar_candidato(_cpf="123")

    def test_email_invalido(self):
        with self.assertRaises(ValueError):
            self._criar_candidato(email="sem_arroba")

    def test_nome_vazio(self):
        with self.assertRaises(ValueError):
            self._criar_candidato(nome="")

    def test_areas_interesse_vazia(self):
        with self.assertRaises(ValueError):
            self._criar_candidato(_areas_interesse=[])

    def test_id_negativo(self):
        with self.assertRaises(ValueError):
            self._criar_candidato(id=-1)

    def test_localidade_tipo_invalido(self):
        with self.assertRaises(TypeError):
            self._criar_candidato(localidade=123)

    # --- Regras de negócio ---

    def test_adicionar_area(self):
        c = self._criar_candidato()
        c.adicionar_area("Dados")
        self.assertIn("Dados", c.areas_interesse)

    def test_adicionar_area_duplicada(self):
        c = self._criar_candidato()
        with self.assertRaises(ValueError):
            c.adicionar_area("TI")

    def test_adicionar_area_vazia(self):
        c = self._criar_candidato()
        with self.assertRaises(ValueError):
            c.adicionar_area("   ")

    def test_remover_area(self):
        c = self._criar_candidato(_areas_interesse=["TI", "Dados"])
        c.remover_area("TI")
        self.assertNotIn("TI", c.areas_interesse)

    def test_remover_area_unica_falha(self):
        c = self._criar_candidato()
        with self.assertRaises(ValueError):
            c.remover_area("TI")

    def test_atualizar_nome(self):
        c = self._criar_candidato()
        c.atualizar_dado("nome", "João Pedro")
        self.assertEqual(c.nome, "João Pedro")

    def test_atualizar_email(self):
        c = self._criar_candidato()
        c.atualizar_dado("email", "novo@email.com")
        self.assertEqual(c.email, "novo@email.com")

    def test_atualizar_localidade(self):
        c = self._criar_candidato()
        c.atualizar_dado("localidade", "Rio de Janeiro")
        self.assertEqual(c.localidade, "Rio de Janeiro")

    def test_atualizar_campo_invalido(self):
        c = self._criar_candidato()
        with self.assertRaises(ValueError):
            c.atualizar_dado("cpf", "99988877766")

    # --- Mapper ---

    def test_mapper_to_dict(self):
        c = self._criar_candidato()
        d = CandidatoMapper.to_dict(c)
        self.assertEqual(d["id"], 1)
        self.assertEqual(d["cpf"], "11122233344")
        self.assertEqual(d["areas_interesse"], ["TI"])
        self.assertEqual(d["localidade"], "São Paulo")

    def test_mapper_round_trip(self):
        original = self._criar_candidato()
        d = CandidatoMapper.to_dict(original)
        restaurado = CandidatoMapper.from_dict(d)
        self.assertEqual(restaurado.id, original.id)
        self.assertEqual(restaurado.cpf, original.cpf)
        self.assertEqual(restaurado.email, original.email)
        self.assertEqual(restaurado.localidade, original.localidade)


if __name__ == "__main__":
    unittest.main()