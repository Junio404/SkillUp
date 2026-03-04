import os
from typing import List, Optional
from src.dominio.vaga import VagaEstagio, VagaEstagioMapper, Vaga
from src.interfaces.interface_vaga import IVagaRepositorio
from src.repositorios.loader import JsonRepository

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_ARQUIVO = os.path.normpath(
    os.path.join(BASE_DIR, "..", "data", "vaga_estagio.json")
)


class RepositorioVagaEstagioJSON(IVagaRepositorio):
    def __init__(self):
        self._json_repo = JsonRepository(CAMINHO_ARQUIVO)

    def salvar(self, vaga: VagaEstagio) -> None:
        dados = self._json_repo.carregar()
        dados.append(VagaEstagioMapper.to_dict(vaga))
        self._json_repo.salvar(dados)

    def buscar_por_id(self, id_vaga: int) -> Optional[VagaEstagio]:
        dados = self._json_repo.carregar()
        for v in dados:
            if v["id"] == id_vaga:
                return VagaEstagioMapper.from_dict(v)
        return None

    def listar_todas(self) -> List[VagaEstagio]:
        dados = self._json_repo.carregar()
        return [VagaEstagioMapper.from_dict(d) for d in dados]

    def listar_ativas(self) -> List[VagaEstagio]:
        return [v for v in self.listar_todas() if v.ativa]

    def listar_inativas(self) -> List[VagaEstagio]:
        return [v for v in self.listar_todas() if not v.ativa]

    def listar_por_area(self, area: str) -> List[VagaEstagio]:
        return [v for v in self.listar_todas() if v.area.lower() == area.lower()]

    def listar_por_modalidade(self, modalidade: str) -> List[VagaEstagio]:
        return [v for v in self.listar_todas() if v.modalidade.value.lower() == modalidade.lower()]

    def listar_por_tipo(self, tipo: str) -> List[VagaEstagio]:
        return [v for v in self.listar_todas() if v.tipo.value.lower() == tipo.lower()]

    def listar_por_titulo(self, titulo: str) -> List[VagaEstagio]:
        return [v for v in self.listar_todas() if titulo.lower() in v.titulo.lower()]

    def buscar_por_filtros(self, **filtros) -> List[VagaEstagio]:
        vagas = self.listar_todas()
        resultado = []
        for vaga in vagas:
            corresponde = True
            for campo, valor in filtros.items():
                if not hasattr(vaga, campo):
                    raise AttributeError(f"O campo '{campo}' não existe na vaga")
                atributo = getattr(vaga, campo)
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
                resultado.append(vaga)
        return resultado

    def atualizar(self, vaga: VagaEstagio) -> None:
        dados = self._json_repo.carregar()
        for i, v in enumerate(dados):
            if v["id"] == vaga.id:
                dados[i] = VagaEstagioMapper.to_dict(vaga)
                self._json_repo.salvar(dados)
                return
        raise ValueError("Vaga Estágio não encontrada")

    def excluir(self, id_vaga: int) -> None:
        dados = self._json_repo.carregar()
        if not any(v["id"] == id_vaga for v in dados):
            raise ValueError("Vaga Estágio não encontrada")
        dados = [v for v in dados if v["id"] != id_vaga]
        self._json_repo.salvar(dados)

    def contar_total(self) -> int:
        return len(self.listar_todas())

    def contar_ativas(self) -> int:
        return len(self.listar_ativas())

    def contar_por_area(self, area: str) -> int:
        return len(self.listar_por_area(area))

    # ==============================
    # MÉTODOS ESPECÍFICOS ESTÁGIO
    # ==============================

    def listar_por_instituicao(self, instituicao: str) -> List[VagaEstagio]:
        return [v for v in self.listar_todas() if instituicao.lower() in v.instituicao_conveniada.lower()]

    def listar_por_faixa_bolsa(self, bolsa_min: float, bolsa_max: float) -> List[VagaEstagio]:
        return [v for v in self.listar_todas() if bolsa_min <= v.bolsa_auxilio <= bolsa_max]

    def listar_por_bolsa_minima(self, bolsa_min: float) -> List[VagaEstagio]:
        return [v for v in self.listar_todas() if v.bolsa_auxilio >= bolsa_min]
