import json
import os


class JsonRepository:
    def __init__(self, caminho_arquivo: str):
        self._caminho_arquivo = caminho_arquivo

    def carregar(self):
        if not os.path.exists(self._caminho_arquivo):
            return []

        try:
            with open(self._caminho_arquivo, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def salvar(self, lista):
        os.makedirs(os.path.dirname(self._caminho_arquivo), exist_ok=True)
        with open(self._caminho_arquivo, "w", encoding="utf-8") as f:
            json.dump(lista, f, indent=4, ensure_ascii=False)