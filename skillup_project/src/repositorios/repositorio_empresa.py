import os
from typing import List, Optional
from src.dominio.empresa import Empresa, EmpresaMapper
from src.interfaces.interface_empresa import IEmpresa
from src.repositorios.loader import JsonRepository

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_ARQUIVO = os.path.normpath(
    os.path.join(BASE_DIR, "..", "data", "empresa.json")
)


class RepositorioEmpresaJSON(IEmpresa):
    def __init__(self):
        self._json_repo = JsonRepository(CAMINHO_ARQUIVO)

    def salvar(self, empresa: Empresa) -> None:
        dados = self._json_repo.carregar()
        dados.append(EmpresaMapper.to_dict(empresa))
        self._json_repo.salvar(dados)

    def listar(self) -> List[Empresa]:
        dados = self._json_repo.carregar()
        return [EmpresaMapper.from_dict(d) for d in dados]

    def buscar_por_id(self, id_empresa: int) -> Optional[Empresa]:
        dados = self._json_repo.carregar()
        for e in dados:
            if e["id"] == id_empresa:
                return EmpresaMapper.from_dict(e)
        return None

    def buscar_por_cnpj(self, cnpj: str) -> Optional[Empresa]:
        for e in self.listar():
            if e.cnpj == cnpj:
                return e
        return None

    def buscar_por_nome(self, nome: str) -> List[Empresa]:
        return [e for e in self.listar() if nome.lower() in e.nome.lower()]

    def buscar_por_porte(self, porte: str) -> List[Empresa]:
        return [e for e in self.listar() if e.porte.lower() == porte.lower()]

    def buscar_por_filtros(self, **filtros) -> List[Empresa]:
        empresas = self.listar()
        resultado = []
        for empresa in empresas:
            corresponde = True
            for campo, valor in filtros.items():
                if not hasattr(empresa, campo):
                    raise AttributeError(f"O campo '{campo}' não existe na empresa")
                atributo = getattr(empresa, campo)
                if isinstance(atributo, list):
                    if valor not in atributo:
                        corresponde = False
                        break
                else:
                    if atributo != valor:
                        corresponde = False
                        break
            if corresponde:
                resultado.append(empresa)
        return resultado

    def atualizar(self, empresa: Empresa) -> None:
        dados = self._json_repo.carregar()
        for i, e in enumerate(dados):
            if e["id"] == empresa.id:
                dados[i] = EmpresaMapper.to_dict(empresa)
                self._json_repo.salvar(dados)
                return
        raise ValueError("Empresa não encontrada")

    def deletar(self, id_empresa: int) -> None:
        dados = self._json_repo.carregar()
        if not any(e["id"] == id_empresa for e in dados):
            raise ValueError("Empresa não encontrada")
        dados = [e for e in dados if e["id"] != id_empresa]
        self._json_repo.salvar(dados)

    def contar_total(self) -> int:
        return len(self.listar())

    def contar_por_porte(self, porte: str) -> int:
        return len(self.buscar_por_porte(porte))