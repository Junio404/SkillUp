import os
from typing import List, Optional
from src.dominio.instituicao_ensino import InstituicaoEnsino, InstituicaoEnsinoMapper
from src.interfaces.interface_instituicao_ensino import IInstituicaoEnsino
from src.repositorios.loader import JsonRepository

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_ARQUIVO = os.path.normpath(
    os.path.join(BASE_DIR, "..", "data", "instituicao_ensino.json")
)


class RepositorioInstituicaoEnsinoJSON(IInstituicaoEnsino):
    def __init__(self):
        self._json_repo = JsonRepository(CAMINHO_ARQUIVO)

    def salvar(self, instituicao: InstituicaoEnsino) -> None:
        dados = self._json_repo.carregar()
        dados.append(InstituicaoEnsinoMapper.to_dict(instituicao))
        self._json_repo.salvar(dados)

    def listar(self) -> List[InstituicaoEnsino]:
        dados = self._json_repo.carregar()
        return [InstituicaoEnsinoMapper.from_dict(d) for d in dados]

    def buscar_por_id(self, id_instituicao: int) -> Optional[InstituicaoEnsino]:
        dados = self._json_repo.carregar()
        for i in dados:
            if i["id"] == id_instituicao:
                return InstituicaoEnsinoMapper.from_dict(i)
        return None

    def buscar_por_cnpj(self, cnpj: str) -> Optional[InstituicaoEnsino]:
        for i in self.listar():
            if i.cnpj == cnpj:
                return i
        return None

    def buscar_por_nome(self, nome: str) -> List[InstituicaoEnsino]:
        return [i for i in self.listar() if nome.lower() in i.nome_fantasia.lower() or nome.lower() in i.razao_social.lower()]

    def buscar_por_tipo(self, tipo: str) -> List[InstituicaoEnsino]:
        return [i for i in self.listar() if i.tipo.lower() == tipo.lower()]

    def buscar_credenciadas(self) -> List[InstituicaoEnsino]:
        return [i for i in self.listar() if i.credenciada]

    def buscar_por_modalidade(self, modalidade: str) -> List[InstituicaoEnsino]:
        return [i for i in self.listar() if modalidade.lower() in [m.lower() for m in i.modalidades]]

    def buscar_por_filtros(self, **filtros) -> List[InstituicaoEnsino]:
        instituicoes = self.listar()
        resultado = []
        for inst in instituicoes:
            corresponde = True
            for campo, valor in filtros.items():
                if not hasattr(inst, campo):
                    raise AttributeError(f"O campo '{campo}' não existe na instituição")
                atributo = getattr(inst, campo)
                if isinstance(atributo, list):
                    if valor not in atributo:
                        corresponde = False
                        break
                else:
                    if atributo != valor:
                        corresponde = False
                        break
            if corresponde:
                resultado.append(inst)
        return resultado

    def atualizar(self, instituicao: InstituicaoEnsino) -> None:
        dados = self._json_repo.carregar()
        for i, inst in enumerate(dados):
            if inst["id"] == instituicao.id:
                dados[i] = InstituicaoEnsinoMapper.to_dict(instituicao)
                self._json_repo.salvar(dados)
                return
        raise ValueError("Instituição de ensino não encontrada")

    def deletar(self, id_instituicao: int) -> None:
        dados = self._json_repo.carregar()
        if not any(i["id"] == id_instituicao for i in dados):
            raise ValueError("Instituição de ensino não encontrada")
        dados = [i for i in dados if i["id"] != id_instituicao]
        self._json_repo.salvar(dados)

    def contar_total(self) -> int:
        return len(self.listar())

    def contar_credenciadas(self) -> int:
        return len(self.buscar_credenciadas())
