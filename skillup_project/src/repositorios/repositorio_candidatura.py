import os
from src.dominio.candidatura import Candidatura
from src.interfaces.interface_candidatura import ICandidaturaRepositorio
from src.repositorios.loader import JsonRepository

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_ARQUIVO = os.path.normpath(
    os.path.join(BASE_DIR, "..", "data", "candidatura.json")
)

class RepositorioCandidaturaJSON(ICandidaturaRepositorio):
    def __init__(self):
        self._json_repo = JsonRepository(CAMINHO_ARQUIVO)

    def salvar(self, candidatura: Candidatura) -> None:
        dados = self._json_repo.carregar()
        dados.append(candidatura.to_dict())
        self._json_repo.salvar(dados)

    def buscar_por_id(self, id_candidatura: int):
        dados = self._json_repo.carregar()
        for c in dados:
            if c["id"] == id_candidatura:
                return Candidatura.from_dict(c)
        return None

    def listar_todas(self):
        dados = self._json_repo.carregar()
        return [Candidatura.from_dict(d) for d in dados]

    def listar_por_candidato(self, id_candidato: int):
        return [c for c in self.listar_todas() if c.id_candidato == id_candidato]

    def listar_por_vaga(self, id_vaga: int):
        return [c for c in self.listar_todas() if c.id_vaga == id_vaga]

    def listar_por_status(self, status: str):
        return [c for c in self.listar_todas() if c.status == status]

    def contar_por_candidato(self, id_candidato: int) -> int:
        return len(self.listar_por_candidato(id_candidato))

    def contar_por_vaga(self, id_vaga: int) -> int:
        return len(self.listar_por_vaga(id_vaga))

    def contar_por_status(self, status: str) -> int:
        return len(self.listar_por_status(status))

    def atualizar_status(self, id_candidatura: int, novo_status: str) -> bool:
        dados = self._json_repo.carregar()
        for i, c in enumerate(dados):
            if c["id"] == id_candidatura:
                dados[i]["status"] = novo_status
                self._json_repo.salvar(dados)
                return True
        return False

    def excluir(self, id_candidatura: int) -> None:
        dados = self._json_repo.carregar()
        dados = [c for c in dados if c["id"] != id_candidatura]
        self._json_repo.salvar(dados)
