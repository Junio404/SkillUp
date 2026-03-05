from dataclasses import dataclass, field
from typing import List, Tuple

from src.dominio.candidato import Candidato
from src.dominio.curso_abs import Curso
from src.dominio.curso_presencial import CursoPresencial
from src.dominio.vaga import Vaga, VagaCLT, VagaEstagio, Modalidade
from src.interfaces.interface_vaga import IVagaRepositorio
from src.interfaces.interface_curso import ICursoRepositorio


# ==============================
# PESOS DE PONTUAÇÃO
# ==============================

PESO_AREA = 50           # área de interesse coincide
PESO_LOCALIDADE = 30     # localidade coincide (presencial/híbrido)
PESO_REMOTO = 20         # bônus por ser remoto (máxima flexibilidade)
PESO_HIBRIDO = 10        # bônus menor por ser híbrido


# ==============================
# RESULTADO DA RECOMENDAÇÃO
# ==============================

@dataclass
class ItemRankeado:
    """Wrapper genérico que associa uma pontuação a um item."""
    item: object
    pontuacao: int = 0


@dataclass
class Recomendacao:
    """Resultado agrupado de recomendações para um candidato, ordenadas por pontuação."""
    vagas: List[ItemRankeado] = field(default_factory=list)
    cursos: List[ItemRankeado] = field(default_factory=list)


# ==============================
# SERVIÇO DE RECOMENDAÇÃO
# ==============================

class RecomendacaoService:
    """Recomenda vagas e cursos compatíveis com o perfil do candidato.

    Regras:
    - Área de interesse: a área da vaga/curso deve estar nas áreas do candidato.
    - Localidade:
        • Vagas/cursos REMOTOS → sempre recomendados (ignora localidade).
        • Vagas/cursos PRESENCIAIS ou HÍBRIDOS → recomendados apenas se a
          localidade coincidir com a do candidato.
    - Apenas itens ativos são recomendados por padrão.
    """

    def __init__(
        self,
        repo_vaga: IVagaRepositorio,
        repo_curso: ICursoRepositorio,
    ):
        self._repo_vaga = repo_vaga
        self._repo_curso = repo_curso

    # ------------------------------------------------------------------
    # API pública
    # ------------------------------------------------------------------

    def recomendar(self, candidato: Candidato) -> Recomendacao:
        """Retorna vagas e cursos recomendados para o candidato, ordenados por pontuação."""
        vagas = self._recomendar_vagas(candidato)
        cursos = self._recomendar_cursos(candidato)
        return Recomendacao(vagas=vagas, cursos=cursos)

    def recomendar_vagas(self, candidato: Candidato) -> List[ItemRankeado]:
        """Retorna vagas recomendadas ordenadas por pontuação (maior primeiro)."""
        return self._recomendar_vagas(candidato)

    def recomendar_cursos(self, candidato: Candidato) -> List[ItemRankeado]:
        """Retorna cursos recomendados ordenados por pontuação (maior primeiro)."""
        return self._recomendar_cursos(candidato)

    # ------------------------------------------------------------------
    # Lógica interna
    # ------------------------------------------------------------------

    def _recomendar_vagas(self, candidato: Candidato) -> List[ItemRankeado]:
        vagas = self._repo_vaga.listar_ativas()
        areas_lower = [a.lower() for a in candidato.areas_interesse]
        rankeados: List[ItemRankeado] = []

        for vaga in vagas:
            pontuacao = 0

            # 1. Área deve corresponder (obrigatório)
            if vaga.area.lower() not in areas_lower:
                continue

            pontuacao += PESO_AREA

            # 2. Localidade: presencial/híbrido exige match
            localidade_vaga = getattr(vaga, "localidade", "")
            if not self._localidade_compativel(
                vaga.modalidade, localidade_vaga, candidato.localidade
            ):
                continue

            # 3. Pontuação de modalidade e localidade
            pontuacao += self._pontuar_modalidade_localidade(
                vaga.modalidade, localidade_vaga, candidato.localidade
            )

            rankeados.append(ItemRankeado(item=vaga, pontuacao=pontuacao))

        # Ordenar por pontuação decrescente
        rankeados.sort(key=lambda r: r.pontuacao, reverse=True)
        return rankeados

    def _recomendar_cursos(self, candidato: Candidato) -> List[ItemRankeado]:
        cursos = self._repo_curso.listar_todos()
        areas_lower = [a.lower() for a in candidato.areas_interesse]
        rankeados: List[ItemRankeado] = []

        for curso in cursos:
            # Apenas cursos ativos
            if not curso.ativo:
                continue

            pontuacao = 0

            # 1. Área deve corresponder (obrigatório)
            if curso.area.lower() not in areas_lower:
                continue

            pontuacao += PESO_AREA

            # 2. Localidade: presencial/híbrido exige match
            localidade_curso = ""
            if isinstance(curso, CursoPresencial):
                localidade_curso = curso.localidade

            if not self._localidade_compativel(
                curso.modalidade, localidade_curso, candidato.localidade
            ):
                continue

            # 3. Pontuação de modalidade e localidade
            pontuacao += self._pontuar_modalidade_localidade(
                curso.modalidade, localidade_curso, candidato.localidade
            )

            rankeados.append(ItemRankeado(item=curso, pontuacao=pontuacao))

        # Ordenar por pontuação decrescente
        rankeados.sort(key=lambda r: r.pontuacao, reverse=True)
        return rankeados

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    @staticmethod
    def _pontuar_modalidade_localidade(
        modalidade: Modalidade,
        localidade_item: str,
        localidade_candidato: str,
    ) -> int:
        """Calcula pontos extras com base em modalidade e localidade.

        - REMOTO: +PESO_REMOTO (flexibilidade total).
        - PRESENCIAL com localidade coincidente: +PESO_LOCALIDADE.
        - HÍBRIDO com localidade coincidente: +PESO_LOCALIDADE + PESO_HIBRIDO.
        """
        pontos = 0

        if modalidade == Modalidade.REMOTO:
            pontos += PESO_REMOTO
            return pontos

        # Presencial ou Híbrido — verificar localidade
        if localidade_item and localidade_candidato:
            if localidade_item.strip().lower() == localidade_candidato.strip().lower():
                pontos += PESO_LOCALIDADE

        if modalidade == Modalidade.HIBRIDO:
            pontos += PESO_HIBRIDO

        return pontos

    @staticmethod
    def _localidade_compativel(
        modalidade: Modalidade,
        localidade_item: str,
        localidade_candidato: str,
    ) -> bool:
        """Verifica compatibilidade de localidade.

        - REMOTO: sempre compatível.
        - PRESENCIAL / HÍBRIDO: compatível apenas se localidades coincidem
          (ou se o item não tem localidade definida).
        """
        if modalidade == Modalidade.REMOTO:
            return True

        # Se o item não tem localidade, aceita qualquer candidato
        if not localidade_item:
            return True

        # Se o candidato não tem localidade, não pode recomendar presencial/híbrido
        if not localidade_candidato:
            return False

        return localidade_item.strip().lower() == localidade_candidato.strip().lower()
