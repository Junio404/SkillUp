import os
from src.dominio.inscricao_curso import InscricaoCurso
from src.interfaces.interface_inscricao_curso import IInscricaoCursoRepositorio
from src.repositorios.loader import JsonRepository

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_ARQUIVO = os.path.normpath(
    os.path.join(BASE_DIR, "..", "data", "inscricao_curso.json")
)

class RepositorioInscricaoCursoJSON(IInscricaoCursoRepositorio):
    def __init__(self):
        self._json_repo = JsonRepository(CAMINHO_ARQUIVO)

    def salvar(self, inscricao: InscricaoCurso) -> None:
        dados = self._json_repo.carregar()
        dados.append(inscricao.to_dict())
        self._json_repo.salvar(dados)

    def buscar_por_id(self, id_inscricao: int):
        dados = self._json_repo.carregar()
        for i in dados:
            if i["id"] == id_inscricao:
                return InscricaoCurso.from_dict(i)
        return None

    def listar_todas(self):
        dados = self._json_repo.carregar()
        return [InscricaoCurso.from_dict(d) for d in dados]

    def listar_por_aluno(self, id_aluno: int):
        return [i for i in self.listar_todas() if i.id_aluno == id_aluno]

    def listar_por_curso(self, id_curso: int):
        return [i for i in self.listar_todas() if i.id_curso == id_curso]

    def listar_por_status(self, status: str):
        return [i for i in self.listar_todas() if str(i.status) == status]

    def contar_por_aluno(self, id_aluno: int) -> int:
        return len(self.listar_por_aluno(id_aluno))

    def contar_por_curso(self, id_curso: int) -> int:
        return len(self.listar_por_curso(id_curso))

    def contar_por_status(self, status: str) -> int:
        return len(self.listar_por_status(status))

    def atualizar_status(self, id_inscricao: int, novo_status: str) -> bool:
        dados = self._json_repo.carregar()
        for i, insc in enumerate(dados):
            if insc["id"] == id_inscricao:
                dados[i]["status"] = novo_status
                self._json_repo.salvar(dados)
                return True
        return False

    def excluir(self, id_inscricao: int) -> None:
        dados = self._json_repo.carregar()
        dados = [i for i in dados if i["id"] != id_inscricao]
        self._json_repo.salvar(dados)
