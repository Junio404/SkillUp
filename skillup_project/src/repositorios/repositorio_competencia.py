import os
from typing import List, Optional
from src.dominio.competencia import Competencia, CompetenciaMapper
from src.interfaces.interface_competencia import ICompetenciaRepositorio
from src.repositorios.loader import JsonRepository

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_ARQUIVO = os.path.normpath(
    os.path.join(BASE_DIR, "..", "data", "competencia.json")
)


class RepositorioCompetenciaJSON(ICompetenciaRepositorio):
    def __init__(self):
        self._json_repo = JsonRepository(CAMINHO_ARQUIVO)

    def salvar(self, competencia: Competencia) -> None:
        dados = self._json_repo.carregar()
        dados.append(CompetenciaMapper.to_dict(competencia))
        self._json_repo.salvar(dados)

    def buscar_por_id(self, id_competencia: int) -> Optional[Competencia]:
        dados = self._json_repo.carregar()
        for c in dados:
            if c["id"] == id_competencia:
                return CompetenciaMapper.from_dict(c)
        return None

    def buscar_por_nome(self, nome: str) -> Optional[Competencia]:
        for c in self.listar_todos():
            if c.nome == nome:
                return c
        return None

    def buscar_por_nome_parcial(self, nome: str) -> List[Competencia]:
        return [c for c in self.listar_todos() if nome.lower() in c.nome.lower()]

    def listar_todos(self) -> List[Competencia]:
        dados = self._json_repo.carregar()
        return [CompetenciaMapper.from_dict(d) for d in dados]

    def buscar_por_filtros(self, **filtros) -> List[Competencia]:
        competencias = self.listar_todos()
        resultado = []
        for comp in competencias:
            corresponde = True
            for campo, valor in filtros.items():
                if not hasattr(comp, campo):
                    raise AttributeError(f"O campo '{campo}' não existe em Competencia")
                atributo = getattr(comp, campo)
                if isinstance(atributo, list):
                    if valor not in atributo:
                        corresponde = False
                        break
                else:
                    if atributo != valor:
                        corresponde = False
                        break
            if corresponde:
                resultado.append(comp)
        return resultado

    def atualizar(self, competencia: Competencia) -> None:
        dados = self._json_repo.carregar()
        for i, c in enumerate(dados):
            if c["id"] == competencia.id:
                dados[i] = CompetenciaMapper.to_dict(competencia)
                self._json_repo.salvar(dados)
                return
        raise ValueError("Competência não encontrada")

    def remover_por_id(self, id_competencia: int) -> bool:
        dados = self._json_repo.carregar()
        tamanho_inicial = len(dados)
        dados = [c for c in dados if c["id"] != id_competencia]
        if len(dados) < tamanho_inicial:
            self._json_repo.salvar(dados)
            return True
        return False

    def contar_total(self) -> int:
        return len(self.listar_todos())
