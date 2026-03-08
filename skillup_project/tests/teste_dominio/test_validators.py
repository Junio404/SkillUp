import unittest
from datetime import date
from src.dominio.validators import (
    IdValidador, StrValidador, CpfValidador, CnpjValidador,
    EmailValidador, AreasValidador, PorteValidador,
    PrazoValidador, SalarioValidador, BooleanValidador,
    CargaHorariaValidador, CapacidadeValidador,
    NivelAtualizavelValidador, NivelMinimoValidador,
)


class TestIdValidador(unittest.TestCase):
    def test_valido(self):
        IdValidador().validar(1)

    def test_zero(self):
        with self.assertRaises(ValueError):
            IdValidador().validar(0)

    def test_negativo(self):
        with self.assertRaises(ValueError):
            IdValidador().validar(-5)

    def test_tipo_invalido(self):
        with self.assertRaises(ValueError):
            IdValidador().validar("abc")


class TestStrValidador(unittest.TestCase):
    def test_valido(self):
        StrValidador().validar("teste")

    def test_vazio(self):
        with self.assertRaises(ValueError):
            StrValidador().validar("")

    def test_espacos(self):
        with self.assertRaises(ValueError):
            StrValidador().validar("   ")

    def test_tipo_invalido(self):
        with self.assertRaises(ValueError):
            StrValidador().validar(123)


class TestCpfValidador(unittest.TestCase):
    def test_valido(self):
        CpfValidador().validar("11122233344")

    def test_tamanho_errado(self):
        with self.assertRaises(ValueError):
            CpfValidador().validar("123")

    def test_com_letras(self):
        with self.assertRaises(ValueError):
            CpfValidador().validar("1112223334a")


class TestCnpjValidador(unittest.TestCase):
    def test_valido(self):
        CnpjValidador().validar("12345678000199")

    def test_tamanho_errado(self):
        with self.assertRaises(ValueError):
            CnpjValidador().validar("12345")


class TestEmailValidador(unittest.TestCase):
    def test_valido(self):
        EmailValidador().validar("user@email.com")

    def test_sem_arroba(self):
        with self.assertRaises(ValueError):
            EmailValidador().validar("sem_arroba")


class TestPorteValidador(unittest.TestCase):
    def test_validos(self):
        for porte in ["pequeno", "medio", "grande"]:
            PorteValidador().validar(porte)

    def test_invalido(self):
        with self.assertRaises(ValueError):
            PorteValidador().validar("gigante")


class TestPrazoValidador(unittest.TestCase):
    def test_futuro_valido(self):
        PrazoValidador().validar(date(2027, 12, 31))

    def test_none_valido(self):
        PrazoValidador().validar(None)

    def test_passado_invalido(self):
        with self.assertRaises(ValueError):
            PrazoValidador().validar(date(2020, 1, 1))

    def test_tipo_invalido(self):
        with self.assertRaises(TypeError):
            PrazoValidador().validar("2027-12-31")


class TestSalarioValidador(unittest.TestCase):
    def test_valido(self):
        SalarioValidador().validar(3000.0)

    def test_negativo(self):
        with self.assertRaises(ValueError):
            SalarioValidador().validar(-100)

    def test_zero(self):
        with self.assertRaises(ValueError):
            SalarioValidador().validar(0)


class TestBooleanValidador(unittest.TestCase):
    def test_valido(self):
        BooleanValidador().validar(True)
        BooleanValidador().validar(False)

    def test_tipo_invalido(self):
        with self.assertRaises(TypeError):
            BooleanValidador().validar("sim")


class TestCargaHorariaValidador(unittest.TestCase):
    def test_valido(self):
        CargaHorariaValidador().validar(40)

    def test_zero(self):
        with self.assertRaises(ValueError):
            CargaHorariaValidador().validar(0)


class TestCapacidadeValidador(unittest.TestCase):
    def test_valido(self):
        CapacidadeValidador().validar(30)

    def test_negativo(self):
        with self.assertRaises(ValueError):
            CapacidadeValidador().validar(-1)


class TestNivelAtualizavelValidador(unittest.TestCase):
    def test_validos(self):
        v = NivelAtualizavelValidador()
        for nivel in ["iniciante", "intermediario", "avancado"]:
            v.validar(nivel)

    def test_invalido(self):
        with self.assertRaises(ValueError):
            NivelAtualizavelValidador().validar("expert")


class TestNivelMinimoValidador(unittest.TestCase):
    def test_validos(self):
        v = NivelMinimoValidador()
        for nivel in ["INICIANTE", "INTERMEDIARIO", "AVANCADO"]:
            v.validar(nivel)

    def test_invalido(self):
        with self.assertRaises(ValueError):
            NivelMinimoValidador().validar("MASTER")


if __name__ == "__main__":
    unittest.main()