import json
import os

from src.dominio.empresa import Empresa
from src.interfaces.interface_empresa import IEmpresaRepositorio  # ajuste se o nome for diferente


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_ARQUIVO = os.path.normpath(
    os.path.join(BASE_DIR, "..", "data", "empresa.json")
)


class RepositorioEmpresaJSON(IEmpresaRepositorio):
    """
    Repositório de empresas que utiliza um arquivo JSON para armazenar os dados.
    Implementa os métodos definidos na interface IEmpresaRepositorio.
    """

    def _carregar_dados(self):
        """Carrega os dados do arquivo JSON. Retorna uma lista de dicionários representando as empresas."""
        if not os.path.exists(CAMINHO_ARQUIVO):
            return []

        try:
            with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _salvar_dados(self, lista):
        """Salva a lista de empresas no arquivo JSON."""
        os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
        with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(lista, f, indent=4, ensure_ascii=False)

    def salvar(self, empresa: Empresa):
        """Salva uma empresa no arquivo JSON."""
        dados = self._carregar_dados()
        dados.append(empresa.to_dict())
        self._salvar_dados(dados)

    def listar(self):
        """Lista todas as empresas armazenadas no arquivo JSON."""
        dados = self._carregar_dados()
        return [Empresa.from_dict(d) for d in dados]

    def buscar_por_id(self, id_empresa: int):
        """Busca uma empresa pelo ID. Retorna Empresa ou None."""
        for empresa in self.listar():
            if empresa.id == id_empresa:
                return empresa
        return None

    def buscar_por_filtros(self, **filtros):
        """
        Busca empresas que correspondam aos filtros fornecidos.
        Os filtros podem incluir qualquer atributo de Empresa (ex: nome, cnpj, porte).
        """
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

    def atualizar(self, empresa: Empresa):
        """
        Atualiza uma empresa existente no arquivo JSON.
        A empresa é identificada pelo ID.
        """
        dados = self._carregar_dados()

        for i, e in enumerate(dados):
            if e["id"] == empresa.id:
                dados[i] = empresa.to_dict()
                self._salvar_dados(dados)
                return

        raise ValueError("Empresa não encontrada")

    def deletar(self, id_empresa: int):
        """Deleta uma empresa do arquivo JSON pelo ID."""
        dados = self._carregar_dados()

        if not any(e["id"] == id_empresa for e in dados):
            raise ValueError("Empresa não encontrada")

        dados = [e for e in dados if e["id"] != id_empresa]
        self._salvar_dados(dados)