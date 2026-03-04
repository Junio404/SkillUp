import os
from typing import List, Optional
from src.dominio.curso_competencia import CursoCompetencia, CursoCompetenciaMapper
from src.interfaces.interface_curso_competencia import ICursoCompetenciaRepositorio
from src.repositorios.loader import JsonRepository

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_ARQUIVO = os.path.normpath(
    os.path.join(BASE_DIR, "..", "data", "curso_competencia.json")
)


class RepositorioCursoCompetenciaJSON(ICursoCompetenciaRepositorio):
    def __init__(self):
        self._json_repo = JsonRepository(CAMINHO_ARQUIVO)

    def salvar(self, curso_competencia: CursoCompetencia) -> None:
        dados = self._json_repo.carregar()
        dados.append(CursoCompetenciaMapper.to_dict(curso_competencia))
        self._json_repo.salvar(dados)

    def buscar_por_id(self, id_curso_competencia: int) -> Optional[CursoCompetencia]:
        dados = self._json_repo.carregar()
        for c in dados:
            if c["id"] == id_curso_competencia:
                return CursoCompetenciaMapper.from_dict(c)
        return None

    def listar_todas(self) -> List[CursoCompetencia]:
        dados = self._json_repo.carregar()
        return [CursoCompetenciaMapper.from_dict(d) for d in dados]

    def listar_por_curso(self, id_curso: int) -> List[CursoCompetencia]:
        return [cc for cc in self.listar_todas() if cc.id_curso == id_curso]

    def listar_por_competencia(self, id_competencia: int) -> List[CursoCompetencia]:
        return [cc for cc in self.listar_todas() if cc.id_competencia == id_competencia]

    def listar_por_nivel(self, nivel: str) -> List[CursoCompetencia]:
        return [cc for cc in self.listar_todas() if cc.nivel_conferido == nivel.lower()]

    def buscar_por_curso_e_competencia(self, id_curso: int, id_competencia: int) -> Optional[CursoCompetencia]:
        for cc in self.listar_todas():
            if cc.id_curso == id_curso and cc.id_competencia == id_competencia:
                return cc
        return None

    def atualizar(self, curso_competencia: CursoCompetencia) -> None:
        dados = self._json_repo.carregar()
        for i, c in enumerate(dados):
            if c["id"] == curso_competencia.id:
                dados[i] = CursoCompetenciaMapper.to_dict(curso_competencia)
                self._json_repo.salvar(dados)
                return
        raise ValueError("CursoCompetencia não encontrado")

    def remover_por_id(self, id_curso_competencia: int) -> bool:
        dados = self._json_repo.carregar()
        tamanho_inicial = len(dados)
        dados = [c for c in dados if c["id"] != id_curso_competencia]
        if len(dados) < tamanho_inicial:
            self._json_repo.salvar(dados)
            return True
        return False

    def remover_por_curso(self, id_curso: int) -> bool:
        dados = self._json_repo.carregar()
        tamanho_inicial = len(dados)
        dados = [c for c in dados if c["curso_id"] != id_curso]
        if len(dados) < tamanho_inicial:
            self._json_repo.salvar(dados)
            return True
        return False

    def contar_competencias_curso(self, id_curso: int) -> int:
        return len(self.listar_por_curso(id_curso))
