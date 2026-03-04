import os
from typing import List, Optional
from src.dominio.instituicao_ensino import AreaEnsino, AreaEnsinoMapper
from src.interfaces.interface_area_ensino import IAreaEnsinoRepositorio
from src.repositorios.loader import JsonRepository

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_ARQUIVO = os.path.normpath(
    os.path.join(BASE_DIR, "..", "data", "area_ensino.json")
)


class RepositorioAreaEnsinoJSON(IAreaEnsinoRepositorio):
    def __init__(self):
        self._json_repo = JsonRepository(CAMINHO_ARQUIVO)

    def salvar(self, area: AreaEnsino) -> None:
        dados = self._json_repo.carregar()
        dados.append(AreaEnsinoMapper.to_dict(area))
        self._json_repo.salvar(dados)

    def buscar_por_id(self, id_area: int) -> Optional[AreaEnsino]:
        dados = self._json_repo.carregar()
        for a in dados:
            if a["id_area"] == id_area:
                return AreaEnsinoMapper.from_dict(a)
        return None

    def buscar_por_nome(self, nome: str) -> Optional[AreaEnsino]:
        for a in self.listar_todas():
            if a.nome_area == nome:
                return a
        return None

    def buscar_por_nome_parcial(self, nome: str) -> List[AreaEnsino]:
        return [a for a in self.listar_todas() if nome.lower() in a.nome_area.lower()]

    def listar_todas(self) -> List[AreaEnsino]:
        dados = self._json_repo.carregar()
        return [AreaEnsinoMapper.from_dict(d) for d in dados]

    def atualizar(self, area: AreaEnsino) -> None:
        dados = self._json_repo.carregar()
        for i, a in enumerate(dados):
            if a["id_area"] == area.id_area:
                dados[i] = AreaEnsinoMapper.to_dict(area)
                self._json_repo.salvar(dados)
                return
        raise ValueError("Área de ensino não encontrada")

    def remover_por_id(self, id_area: int) -> bool:
        dados = self._json_repo.carregar()
        tamanho_inicial = len(dados)
        dados = [a for a in dados if a["id_area"] != id_area]
        if len(dados) < tamanho_inicial:
            self._json_repo.salvar(dados)
            return True
        return False

    def contar_total(self) -> int:
        return len(self.listar_todas())
