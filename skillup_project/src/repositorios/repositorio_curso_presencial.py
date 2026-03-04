import os
from typing import List, Optional
from src.dominio.curso_presencial import CursoPresencial, CursoPresencialMapper
from src.interfaces.interface_curso import ICursoRepositorio
from src.repositorios.loader import JsonRepository

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_ARQUIVO = os.path.normpath(
    os.path.join(BASE_DIR, "..", "data", "curso_presencial.json")
)


class RepositorioCursoPresencialJSON(ICursoRepositorio):
    def __init__(self):
        self._json_repo = JsonRepository(CAMINHO_ARQUIVO)

    def salvar(self, curso: CursoPresencial) -> None:
        dados = self._json_repo.carregar()
        dados.append(CursoPresencialMapper.to_dict(curso))
        self._json_repo.salvar(dados)

    def buscar_por_id(self, id_curso: int) -> Optional[CursoPresencial]:
        dados = self._json_repo.carregar()
        for c in dados:
            if c["id"] == id_curso:
                return CursoPresencialMapper.from_dict(c)
        return None

    def listar_todos(self) -> List[CursoPresencial]:
        dados = self._json_repo.carregar()
        return [CursoPresencialMapper.from_dict(d) for d in dados]

    def listar_por_nome(self, nome: str) -> List[CursoPresencial]:
        return [c for c in self.listar_todos() if nome.lower() in c.nome.lower()]

    def listar_por_tipo(self, tipo: str) -> List[CursoPresencial]:
        if tipo.lower() == "presencial":
            return self.listar_todos()
        return []

    def listar_por_carga_horaria_minima(self, carga_horaria: int) -> List[CursoPresencial]:
        return [c for c in self.listar_todos() if c.carga_horaria >= carga_horaria]

    def buscar_por_filtros(self, **filtros) -> List[CursoPresencial]:
        cursos = self.listar_todos()
        resultado = []
        for curso in cursos:
            corresponde = True
            for campo, valor in filtros.items():
                if not hasattr(curso, campo):
                    raise AttributeError(f"O campo '{campo}' não existe no curso")
                atributo = getattr(curso, campo)
                if isinstance(atributo, list):
                    if valor not in atributo:
                        corresponde = False
                        break
                elif hasattr(atributo, 'value'):
                    if atributo.value != valor:
                        corresponde = False
                        break
                else:
                    if atributo != valor:
                        corresponde = False
                        break
            if corresponde:
                resultado.append(curso)
        return resultado

    def atualizar(self, curso: CursoPresencial) -> None:
        dados = self._json_repo.carregar()
        for i, c in enumerate(dados):
            if c["id"] == curso.id:
                dados[i] = CursoPresencialMapper.to_dict(curso)
                self._json_repo.salvar(dados)
                return
        raise ValueError("Curso Presencial não encontrado")

    def remover_por_id(self, id_curso: int) -> bool:
        dados = self._json_repo.carregar()
        tamanho_inicial = len(dados)
        dados = [c for c in dados if c["id"] != id_curso]
        if len(dados) < tamanho_inicial:
            self._json_repo.salvar(dados)
            return True
        return False

    def contar_total(self) -> int:
        return len(self.listar_todos())

    # ==============================
    # MÉTODOS ESPECÍFICOS PRESENCIAL
    # ==============================

    def listar_ativos(self) -> List[CursoPresencial]:
        return [c for c in self.listar_todos() if c.ativo]

    def listar_inativos(self) -> List[CursoPresencial]:
        return [c for c in self.listar_todos() if not c.ativo]

    def listar_por_area(self, area: str) -> List[CursoPresencial]:
        return [c for c in self.listar_todos() if c.area.lower() == area.lower()]

    def listar_por_localidade(self, localidade: str) -> List[CursoPresencial]:
        return [c for c in self.listar_todos() if localidade.lower() in c.localidade.lower()]

    def listar_por_modalidade(self, modalidade: str) -> List[CursoPresencial]:
        return [c for c in self.listar_todos() if c.modalidade.value.lower() == modalidade.lower()]

    def contar_ativos(self) -> int:
        return len(self.listar_ativos())

    def contar_por_area(self, area: str) -> int:
        return len(self.listar_por_area(area))

    def contar_por_localidade(self, localidade: str) -> int:
        return len(self.listar_por_localidade(localidade))
