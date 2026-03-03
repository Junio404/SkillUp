import os
from src.dominio.candidato import Candidato, CandidatoMapper
from src.interfaces.interface_candidato import ICandidatoRepositorio
from src.repositorios.loader import JsonRepository


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_ARQUIVO = os.path.normpath(
    os.path.join(BASE_DIR, "..", "data", "candidato.json")
)


class RepositorioCandidatoJSON(ICandidatoRepositorio):

    def __init__(self):
        self._json_repo = JsonRepository(CAMINHO_ARQUIVO)

    def salvar(self, candidato: Candidato):
        dados = self._json_repo.carregar()
        dados.append(CandidatoMapper.to_dict(candidato))
        self._json_repo.salvar(dados)

    def listar(self):
        dados = self._json_repo.carregar()
        return [CandidatoMapper.from_dict(d) for d in dados]

    def buscar_por_id(self, id_candidato: int):
        dados = self._json_repo.carregar()

        for c in dados:
            if c["id"] == id_candidato:
                return CandidatoMapper.from_dict(c)

        return None

    def buscar_por_filtros(self, **filtros):
        candidatos = self.listar()
        resultado = []

        for candidato in candidatos:
            corresponde = True

            for campo, valor in filtros.items():
                if not hasattr(candidato, campo):
                    raise AttributeError(f"O campo '{campo}' não existe no candidato")

                atributo = getattr(candidato, campo)

                if isinstance(atributo, (list, tuple)):
                    if valor not in atributo:
                        corresponde = False
                        break
                else:
                    if atributo != valor:
                        corresponde = False
                        break

            if corresponde:
                resultado.append(candidato)

        return resultado

    def atualizar(self, candidato: Candidato):
        dados = self._json_repo.carregar()

        for i, c in enumerate(dados):
            if c["id"] == candidato.id:
                dados[i] = CandidatoMapper.to_dict(candidato)
                self._json_repo.salvar(dados)
                return

        raise ValueError("Candidato não encontrado")

    def deletar(self, id_candidato: int):
        dados = self._json_repo.carregar()

        if not any(c["id"] == id_candidato for c in dados):
            raise ValueError("Candidato não encontrado")

        dados = [c for c in dados if c["id"] != id_candidato]
        self._json_repo.salvar(dados)

    def buscar_por_cpf(self, cpf: str):
        dados = self._json_repo.carregar()

        for c in dados:
            if c["cpf"] == cpf:
                return CandidatoMapper.from_dict(c)

        return None

    def buscar_por_email(self, email: str):
        dados = self._json_repo.carregar()

        for c in dados:
            if c["email"] == email:
                return CandidatoMapper.from_dict(c)

        return None

    def buscar_por_area_interesse(self, area: str):
        candidatos = self.listar()
        resultado = []

        for candidato in candidatos:
            if area in candidato.areas_interesse:
                resultado.append(candidato)

        return resultado

    def buscar_por_nivel_formacao(self, nivel: str):
        candidatos = self.listar()
        resultado = []

        for candidato in candidatos:
            if candidato.nivel_formacao == nivel:
                resultado.append(candidato)

        return resultado

    def contar_total(self) -> int:
        dados = self._json_repo.carregar()
        return len(dados)