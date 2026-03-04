import os
from typing import List, Optional
from src.dominio.requisitos_vaga import RequisitoVaga, RequisitoVagaMapper
from src.interfaces.interface_requisito_vaga import IRequisitoVagaRepositorio
from src.repositorios.loader import JsonRepository

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_ARQUIVO = os.path.normpath(
    os.path.join(BASE_DIR, "..", "data", "requisitos_vaga.json")
)


class RepositorioRequisitoVagaJSON(IRequisitoVagaRepositorio):
    def __init__(self):
        self._json_repo = JsonRepository(CAMINHO_ARQUIVO)

    def salvar(self, requisito: RequisitoVaga) -> None:
        dados = self._json_repo.carregar()
        dados.append(RequisitoVagaMapper.to_dict(requisito))
        self._json_repo.salvar(dados)

    def buscar_por_id(self, id_requisito: int) -> Optional[RequisitoVaga]:
        dados = self._json_repo.carregar()
        for r in dados:
            if r["id"] == id_requisito:
                return RequisitoVagaMapper.from_dict(r)
        return None

    def listar_todos(self) -> List[RequisitoVaga]:
        dados = self._json_repo.carregar()
        return [RequisitoVagaMapper.from_dict(d) for d in dados]

    def listar_por_vaga(self, id_vaga: int) -> List[RequisitoVaga]:
        return [r for r in self.listar_todos() if r.id_vaga == id_vaga]

    def listar_por_competencia(self, id_competencia: int) -> List[RequisitoVaga]:
        return [r for r in self.listar_todos() if r.id_competencia == id_competencia]

    def listar_obrigatorios_por_vaga(self, id_vaga: int) -> List[RequisitoVaga]:
        return [r for r in self.listar_por_vaga(id_vaga) if r.obrigatorio]

    def listar_por_nivel_minimo(self, nivel: str) -> List[RequisitoVaga]:
        return [r for r in self.listar_todos() if r.nivel_minimo.lower() == nivel.lower()]

    def buscar_por_vaga_e_competencia(self, id_vaga: int, id_competencia: int) -> Optional[RequisitoVaga]:
        for r in self.listar_todos():
            if r.id_vaga == id_vaga and r.id_competencia == id_competencia:
                return r
        return None

    def atualizar(self, requisito: RequisitoVaga) -> None:
        dados = self._json_repo.carregar()
        for i, r in enumerate(dados):
            if r["id"] == requisito.id:
                dados[i] = RequisitoVagaMapper.to_dict(requisito)
                self._json_repo.salvar(dados)
                return
        raise ValueError("RequisitoVaga não encontrado")

    def remover_por_id(self, id_requisito: int) -> bool:
        dados = self._json_repo.carregar()
        tamanho_inicial = len(dados)
        dados = [r for r in dados if r["id"] != id_requisito]
        if len(dados) < tamanho_inicial:
            self._json_repo.salvar(dados)
            return True
        return False

    def remover_por_vaga(self, id_vaga: int) -> bool:
        dados = self._json_repo.carregar()
        tamanho_inicial = len(dados)
        dados = [r for r in dados if r["vaga_id"] != id_vaga]
        if len(dados) < tamanho_inicial:
            self._json_repo.salvar(dados)
            return True
        return False

    def contar_requisitos_vaga(self, id_vaga: int) -> int:
        return len(self.listar_por_vaga(id_vaga))

    def contar_requisitos_obrigatorios(self, id_vaga: int) -> int:
        return len(self.listar_obrigatorios_por_vaga(id_vaga))
