"""
Repositório JSON para CompetenciaCandidato
"""
import json
import os
from pathlib import Path
from typing import List, Optional

from src.dominio.competencia_candidato import CompetenciaCandidato
from src.interfaces.interface_competencia_candidato import ICompetenciaCandidatoRepositorio


class RepositorioCompetenciaCandidatoJSON(ICompetenciaCandidatoRepositorio):
    """Implementação do repositório de CompetenciaCandidato usando JSON."""

    def __init__(self, caminho_arquivo: str = None):
        if caminho_arquivo is None:
            base_dir = Path(__file__).parent.parent / "data"
            caminho_arquivo = str(base_dir / "competencia_candidato.json")
        self._caminho = caminho_arquivo
        self._garantir_arquivo()

    def _garantir_arquivo(self) -> None:
        """Garante que o arquivo JSON existe."""
        os.makedirs(os.path.dirname(self._caminho), exist_ok=True)
        if not os.path.exists(self._caminho):
            with open(self._caminho, "w", encoding="utf-8") as f:
                json.dump([], f)

    def _carregar(self) -> List[dict]:
        """Carrega dados do arquivo JSON."""
        with open(self._caminho, "r", encoding="utf-8") as f:
            return json.load(f)

    def _salvar_todos(self, dados: List[dict]) -> None:
        """Salva todos os dados no arquivo JSON."""
        with open(self._caminho, "w", encoding="utf-8") as f:
            json.dump(dados, f, indent=2, ensure_ascii=False)

    def _para_dict(self, comp: CompetenciaCandidato) -> dict:
        """Converte CompetenciaCandidato para dicionário."""
        return {
            "id": comp.id,
            "id_candidato": comp.id_candidato,
            "id_competencia": comp.id_competencia,
            "nivel_atual": comp.nivel_atual,
        }

    def _para_objeto(self, dados: dict) -> CompetenciaCandidato:
        """Converte dicionário para CompetenciaCandidato."""
        return CompetenciaCandidato(
            id=dados["id"],
            id_candidato=dados["id_candidato"],
            id_competencia=dados["id_competencia"],
            nivel_atual=dados["nivel_atual"],
        )

    def salvar(self, competencia_candidato: CompetenciaCandidato) -> None:
        """Salva ou atualiza uma competência do candidato."""
        dados = self._carregar()
        existente = next(
            (i for i, c in enumerate(dados) if c["id"] == competencia_candidato.id),
            None,
        )
        if existente is not None:
            dados[existente] = self._para_dict(competencia_candidato)
        else:
            dados.append(self._para_dict(competencia_candidato))
        self._salvar_todos(dados)

    def buscar_por_id(self, id_competencia_candidato: int) -> Optional[CompetenciaCandidato]:
        """Busca uma competência do candidato pelo ID."""
        dados = self._carregar()
        for c in dados:
            if c["id"] == id_competencia_candidato:
                return self._para_objeto(c)
        return None

    def listar_todas(self) -> List[CompetenciaCandidato]:
        """Retorna todas as competências de candidatos."""
        dados = self._carregar()
        return [self._para_objeto(c) for c in dados]

    def listar_por_candidato(self, id_candidato: int) -> List[CompetenciaCandidato]:
        """Retorna todas as competências de um candidato específico."""
        dados = self._carregar()
        return [self._para_objeto(c) for c in dados if c["id_candidato"] == id_candidato]

    def listar_por_competencia(self, id_competencia: int) -> List[CompetenciaCandidato]:
        """Retorna todos os candidatos que possuem uma competência específica."""
        dados = self._carregar()
        return [self._para_objeto(c) for c in dados if c["id_competencia"] == id_competencia]

    def listar_por_nivel(self, nivel: str) -> List[CompetenciaCandidato]:
        """Retorna todas as competências de candidatos com um nível específico."""
        dados = self._carregar()
        return [self._para_objeto(c) for c in dados if c["nivel_atual"] == nivel]

    def buscar_por_candidato_e_competencia(
        self, id_candidato: int, id_competencia: int
    ) -> Optional[CompetenciaCandidato]:
        """Busca a competência de um candidato específico."""
        dados = self._carregar()
        for c in dados:
            if c["id_candidato"] == id_candidato and c["id_competencia"] == id_competencia:
                return self._para_objeto(c)
        return None

    def atualizar(self, competencia_candidato: CompetenciaCandidato) -> None:
        """Atualiza uma competência do candidato."""
        self.salvar(competencia_candidato)

    def remover_por_id(self, id_competencia_candidato: int) -> bool:
        """Remove uma competência do candidato pelo ID."""
        dados = self._carregar()
        tamanho_original = len(dados)
        dados = [c for c in dados if c["id"] != id_competencia_candidato]
        if len(dados) < tamanho_original:
            self._salvar_todos(dados)
            return True
        return False

    def remover_por_candidato(self, id_candidato: int) -> bool:
        """Remove todas as competências de um candidato."""
        dados = self._carregar()
        tamanho_original = len(dados)
        dados = [c for c in dados if c["id_candidato"] != id_candidato]
        if len(dados) < tamanho_original:
            self._salvar_todos(dados)
            return True
        return False
