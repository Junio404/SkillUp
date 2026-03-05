from typing import List, Optional

from src.dominio.vaga import Vaga, VagaCLT, VagaEstagio, Modalidade, TipoVaga
from src.interfaces.interface_vaga import IVagaRepositorio


class MotorBuscaVaga:
    """Motor de busca de vagas com filtros combinados.

    Permite buscar vagas por área, modalidade, tipo, localidade,
    faixa salarial e status (ativa/inativa), combinando critérios.
    """

    def __init__(self, repositorio: IVagaRepositorio):
        self._repo = repositorio

    # ------------------------------------------------------------------
    # Busca principal com múltiplos filtros
    # ------------------------------------------------------------------

    def buscar(
        self,
        *,
        area: Optional[str] = None,
        modalidade: Optional[Modalidade] = None,
        tipo: Optional[TipoVaga] = None,
        localidade: Optional[str] = None,
        salario_min: Optional[float] = None,
        salario_max: Optional[float] = None,
        apenas_ativas: bool = True,
    ) -> List[Vaga]:
        """Retorna vagas que atendem a **todos** os filtros fornecidos.

        Parâmetros opcionais — se omitidos, o critério não é aplicado.
        """
        vagas = self._repo.listar_ativas() if apenas_ativas else self._repo.listar_todas()
        resultado: List[Vaga] = []

        for vaga in vagas:
            if area and vaga.area.lower() != area.lower():
                continue

            if modalidade and vaga.modalidade != modalidade:
                continue

            if tipo and vaga.tipo != tipo:
                continue

            if localidade and vaga.modalidade != Modalidade.REMOTO \
                    and not self._localidade_coincide(vaga, localidade):
                continue

            if salario_min is not None or salario_max is not None:
                salario = self._extrair_salario(vaga)
                if salario is None:
                    continue
                if salario_min is not None and salario < salario_min:
                    continue
                if salario_max is not None and salario > salario_max:
                    continue

            resultado.append(vaga)

        return resultado

    # ------------------------------------------------------------------
    # Busca por compatibilidade com candidato
    # ------------------------------------------------------------------

    def buscar_por_candidato(
        self,
        areas_interesse: List[str],
        localidade_candidato: str = "",
        apenas_ativas: bool = True,
    ) -> List[Vaga]:
        """Retorna vagas compatíveis com o perfil do candidato.

        Critérios:
        - A área da vaga deve estar nas áreas de interesse do candidato.
        - Se a vaga possui localidade, ela deve coincidir com a do candidato.
        """
        vagas = self._repo.listar_ativas() if apenas_ativas else self._repo.listar_todas()
        areas_lower = [a.lower() for a in areas_interesse]
        resultado: List[Vaga] = []

        for vaga in vagas:
            if vaga.area.lower() not in areas_lower:
                continue

            if vaga.modalidade != Modalidade.REMOTO \
                    and localidade_candidato \
                    and hasattr(vaga, "localidade") and vaga.localidade:
                if vaga.localidade.lower() != localidade_candidato.lower():
                    continue

            resultado.append(vaga)

        return resultado

    # ------------------------------------------------------------------
    # Helpers privados
    # ------------------------------------------------------------------

    @staticmethod
    def _localidade_coincide(vaga: Vaga, localidade: str) -> bool:
        """Verifica se a vaga possui localidade e se coincide.

        Vagas remotas são compatíveis com qualquer localidade.
        """
        if vaga.modalidade == Modalidade.REMOTO:
            return True
        if hasattr(vaga, "localidade") and vaga.localidade:
            return vaga.localidade.lower() == localidade.lower()
        return False

    @staticmethod
    def _extrair_salario(vaga: Vaga) -> Optional[float]:
        """Extrai o valor salarial da vaga (salário ou bolsa)."""
        if isinstance(vaga, VagaCLT):
            return vaga.salario_base
        if isinstance(vaga, VagaEstagio):
            return vaga.bolsa_auxilio
        return None
