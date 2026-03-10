import unittest
from datetime import date
from unittest.mock import Mock
from src.services.service_curso_ead import CursoEADService
from src.interfaces.interface_curso import ICursoRepositorio
from src.dominio.vaga import Modalidade


class TestServiceCursoEAD(unittest.TestCase):
    """Testes do serviço de CursoEAD."""

    def setUp(self):
        self.mock_repo = Mock(spec=ICursoRepositorio)
        self.service = CursoEADService(self.mock_repo)

    # -- CRUD --

    def test_cadastrar_sucesso(self):
        self.mock_repo.listar_por_nome.return_value = []
        self.mock_repo.listar_todos.return_value = []
        curso = self.service.cadastrar(
            id_instituicao=1,
            nome="Python Avançado",
            area="TI",
            carga_horaria=40,
            capacidade=100,
            plataforma_url="https://plat.com/python",
            prazo_inscricao=date(2027, 12, 31),
        )
        self.mock_repo.salvar.assert_called_once()
        self.assertEqual(curso.id, 1)
        self.assertEqual(curso.nome, "Python Avançado")
        self.assertEqual(curso.modalidade, Modalidade.REMOTO)

    def test_cadastrar_nome_duplicado(self):
        self.mock_repo.listar_por_nome.return_value = [Mock()]
        with self.assertRaisesRegex(ValueError, "Já existe curso com este nome"):
            self.service.cadastrar(1, "Python", "TI", 40, 100, "https://x.com")

    def test_cadastrar_id_incremental(self):
        existente = Mock()
        existente.id = 3
        self.mock_repo.listar_por_nome.return_value = []
        self.mock_repo.listar_todos.return_value = [existente]
        curso = self.service.cadastrar(
            1, "Novo Curso", "TI", 20, 50, "https://x.com", date(2027, 6, 1)
        )
        self.assertEqual(curso.id, 4)

    def test_buscar_por_id_sucesso(self):
        obj = Mock()
        self.mock_repo.buscar_por_id.return_value = obj
        self.assertEqual(self.service.buscar_por_id(1), obj)

    def test_buscar_por_id_inexistente(self):
        self.mock_repo.buscar_por_id.return_value = None
        with self.assertRaisesRegex(ValueError, "Curso EAD não encontrado"):
            self.service.buscar_por_id(999)

    def test_remover_sucesso(self):
        self.mock_repo.buscar_por_id.return_value = Mock()
        self.mock_repo.remover_por_id.return_value = True
        self.service.remover(1)
        self.mock_repo.remover_por_id.assert_called_once_with(1)

    def test_remover_falha(self):
        self.mock_repo.buscar_por_id.return_value = Mock()
        self.mock_repo.remover_por_id.return_value = False
        with self.assertRaisesRegex(ValueError, "Falha ao remover"):
            self.service.remover(1)

    # -- LISTAGENS --

    def test_listar_todos(self):
        self.mock_repo.listar_todos.return_value = [Mock(), Mock()]
        self.assertEqual(len(self.service.listar_todos()), 2)

    def test_listar_por_nome(self):
        self.mock_repo.listar_por_nome.return_value = [Mock()]
        self.assertEqual(len(self.service.listar_por_nome("Python")), 1)

    def test_contar_total(self):
        self.mock_repo.contar_total.return_value = 5
        self.assertEqual(self.service.contar_total(), 5)

    # -- AÇÕES DE NEGÓCIO --

    def test_publicar(self):
        curso = Mock()
        self.mock_repo.buscar_por_id.return_value = curso
        self.service.publicar(1)
        curso.publicar.assert_called_once()
        self.mock_repo.atualizar.assert_called_once_with(curso)

    def test_pausar(self):
        curso = Mock()
        self.mock_repo.buscar_por_id.return_value = curso
        self.service.pausar(1)
        curso.pausar.assert_called_once()
        self.mock_repo.atualizar.assert_called_once_with(curso)

    def test_atualizar_campo_valido(self):
        curso = Mock(spec=["nome"])
        curso.nome = "Antigo"
        self.mock_repo.buscar_por_id.return_value = curso
        resultado = self.service.atualizar(1, "nome", "Novo")
        self.assertEqual(resultado.nome, "Novo")
        self.mock_repo.atualizar.assert_called_once()

    def test_atualizar_campo_inexistente(self):
        curso = Mock(spec=[])
        self.mock_repo.buscar_por_id.return_value = curso
        with self.assertRaises(AttributeError):
            self.service.atualizar(1, "campo_fake", "valor")


if __name__ == "__main__":
    unittest.main()
