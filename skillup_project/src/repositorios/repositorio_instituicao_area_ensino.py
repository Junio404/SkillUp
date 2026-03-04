import os
from typing import List, Optional
from src.dominio.instituicao_ensino import InstituicaoAreaEnsino, InstituicaoAreaEnsinoMapper
from src.interfaces.interface_instituicao_area_ensino import IInstituicaoAreaEnsinoRepositorio
from src.repositorios.loader import JsonRepository

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_ARQUIVO = os.path.normpath(
    os.path.join(BASE_DIR, "..", "data", "instituicao_area_ensino.json")
)


class RepositorioInstituicaoAreaEnsinoJSON(IInstituicaoAreaEnsinoRepositorio):
    def __init__(self):
        self._json_repo = JsonRepository(CAMINHO_ARQUIVO)

    def salvar(self, inst_area: InstituicaoAreaEnsino) -> None:
        dados = self._json_repo.carregar()
        dados.append(InstituicaoAreaEnsinoMapper.to_dict(inst_area))
        self._json_repo.salvar(dados)

    def buscar_por_id(self, id_instituicao_area: int) -> Optional[InstituicaoAreaEnsino]:
        dados = self._json_repo.carregar()
        for ia in dados:
            if ia["id_instituicao_area"] == id_instituicao_area:
                return InstituicaoAreaEnsinoMapper.from_dict(ia)
        return None

    def listar_todas(self) -> List[InstituicaoAreaEnsino]:
        dados = self._json_repo.carregar()
        return [InstituicaoAreaEnsinoMapper.from_dict(d) for d in dados]

    def listar_por_instituicao(self, id_instituicao: int) -> List[InstituicaoAreaEnsino]:
        return [ia for ia in self.listar_todas() if ia.id_instituicao == id_instituicao]

    def listar_por_area(self, id_area: int) -> List[InstituicaoAreaEnsino]:
        return [ia for ia in self.listar_todas() if ia.id_area == id_area]

    def buscar_por_instituicao_e_area(self, id_instituicao: int, id_area: int) -> Optional[InstituicaoAreaEnsino]:
        for ia in self.listar_todas():
            if ia.id_instituicao == id_instituicao and ia.id_area == id_area:
                return ia
        return None

    def atualizar(self, inst_area: InstituicaoAreaEnsino) -> None:
        dados = self._json_repo.carregar()
        for i, ia in enumerate(dados):
            if ia["id_instituicao_area"] == inst_area.id_instituicao_area:
                dados[i] = InstituicaoAreaEnsinoMapper.to_dict(inst_area)
                self._json_repo.salvar(dados)
                return
        raise ValueError("InstituicaoAreaEnsino não encontrada")

    def remover_por_id(self, id_instituicao_area: int) -> bool:
        dados = self._json_repo.carregar()
        tamanho_inicial = len(dados)
        dados = [ia for ia in dados if ia["id_instituicao_area"] != id_instituicao_area]
        if len(dados) < tamanho_inicial:
            self._json_repo.salvar(dados)
            return True
        return False

    def remover_por_instituicao(self, id_instituicao: int) -> bool:
        dados = self._json_repo.carregar()
        tamanho_inicial = len(dados)
        dados = [ia for ia in dados if ia["id_instituicao"] != id_instituicao]
        if len(dados) < tamanho_inicial:
            self._json_repo.salvar(dados)
            return True
        return False

    def contar_areas_por_instituicao(self, id_instituicao: int) -> int:
        return len(self.listar_por_instituicao(id_instituicao))

    def contar_instituicoes_por_area(self, id_area: int) -> int:
        return len(self.listar_por_area(id_area))
