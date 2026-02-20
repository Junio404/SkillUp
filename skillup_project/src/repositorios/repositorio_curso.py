import json
import os
from typing import List
# from src.dominio.curso import Curso # Descomente se a classe Curso já estiver definida corretamente

class RepositorioCurso:
    CAMINHO_ARQUIVO = os.path.join("src", "data", "curso.json")

    def __init__(self):
        self._garantir_arquivo()

    def _garantir_arquivo(self):
        os.makedirs(os.path.dirname(self.CAMINHO_ARQUIVO), exist_ok=True)
        if not os.path.exists(self.CAMINHO_ARQUIVO):
            with open(self.CAMINHO_ARQUIVO, "w", encoding='utf-8') as f:
                json.dump([], f)

    def salvar(self, curso):
        cursos = self._ler_arquivo()
        # Assume que o objeto curso tem to_dict()
        if hasattr(curso, "to_dict"):
            cursos.append(curso.to_dict())
        else:
            cursos.append(curso._dict_)
        
        self._salvar_arquivo(cursos)

    def listar_por_instituicao(self, id_instituicao: int) -> List[dict]:
        cursos = self._ler_arquivo()
        # Filtra cursos onde o id da instituicao corresponde
        return [c for c in cursos if c.get("id_instituicao") == id_instituicao]

    def _ler_arquivo(self):
        try:
            with open(self.CAMINHO_ARQUIVO, "r", encoding='utf-8') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def _salvar_arquivo(self, dados):
        with open(self.CAMINHO_ARQUIVO, "w", encoding='utf-8') as f:
            json.dump(dados, f, indent=4, ensure_ascii=False)