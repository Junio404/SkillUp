import re
from dataclasses import dataclass, field
from typing import List, Protocol, Tuple, Dict, Any, Optional


# ==============================
# ABSTRAÇÕES (DIP)
# ==============================


class Validador(Protocol):
    def validar(self, valor) -> None:
        ...


# ==============================
# IMPLEMENTAÇÕES CONCRETAS
# ==============================

class IdValidador:
    def validar(self, valor: int) -> None:
        if not isinstance(valor, int) or valor <= 0:
            raise ValueError("ID deve ser inteiro positivo.")


class NomeValidador:
    def validar(self, valor: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError("Nome inválido.")


class CpfValidador:
    def validar(self, valor: str) -> None:
        if not isinstance(valor, str) or len(valor) != 11 or not valor.isdigit():
            raise ValueError("CPF inválido.")


class EmailValidador:
    EMAIL_REGEX = r"^[\w\.-]+@[\w\.-]+\.\w+$"

    def validar(self, valor: str) -> None:
        if not re.match(self.EMAIL_REGEX, valor):
            raise ValueError("Email inválido.")


class AreasValidador:
    def validar(self, valor: List[str]) -> None:
        if not isinstance(valor, list) or not valor:
            raise ValueError("Informe ao menos uma área.")

        for area in valor:
            if not isinstance(area, str) or not area.strip():
                raise ValueError("Área inválida.")


class NivelFormacaoValidador:
    def validar(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("Nível de formação inválido.")


# ==============================
# VALIDADORES DE CURRÍCULO
# ==============================


class ObjetivoCurriculoValidador:
    """Valida o objetivo profissional do currículo"""
    MIN_CARACTERES = 10
    MAX_CARACTERES = 500
    
    def validar(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("Objetivo deve ser texto.")
        valor = valor.strip()
        if len(valor) < self.MIN_CARACTERES:
            raise ValueError(f"Objetivo deve ter no mínimo {self.MIN_CARACTERES} caracteres.")
        if len(valor) > self.MAX_CARACTERES:
            raise ValueError(f"Objetivo deve ter no máximo {self.MAX_CARACTERES} caracteres.")


class ResumoCurriculoValidador:
    """Valida o resumo profissional do currículo"""
    MIN_CARACTERES = 20
    MAX_CARACTERES = 2000
    
    def validar(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("Resumo deve ser texto.")
        valor = valor.strip()
        if len(valor) < self.MIN_CARACTERES:
            raise ValueError(f"Resumo deve ter no mínimo {self.MIN_CARACTERES} caracteres.")
        if len(valor) > self.MAX_CARACTERES:
            raise ValueError(f"Resumo deve ter no máximo {self.MAX_CARACTERES} caracteres.")


class DataCurriculoValidador:
    """Valida datas no formato MM/AAAA"""
    DATA_REGEX = r"^(0[1-9]|1[0-2])/\d{4}$"
    
    def validar(self, valor: str, obrigatorio: bool = True) -> None:
        if not valor:
            if obrigatorio:
                raise ValueError("Data é obrigatória.")
            return  # Permite vazio se não obrigatório
        
        if not isinstance(valor, str):
            raise TypeError("Data deve ser texto.")
        
        if not re.match(self.DATA_REGEX, valor):
            raise ValueError("Data deve estar no formato MM/AAAA (ex: 01/2020).")


class NivelFormacaoCurriculoValidador:
    """Valida o nível de formação do currículo"""
    NIVEIS_VALIDOS = ["Técnico", "Graduação", "Pós-graduação", "Mestrado", "Doutorado"]
    
    def validar(self, valor: str) -> None:
        if not isinstance(valor, str):
            raise TypeError("Nível deve ser texto.")
        if valor.strip() not in self.NIVEIS_VALIDOS:
            raise ValueError(f"Nível inválido. Valores aceitos: {', '.join(self.NIVEIS_VALIDOS)}")


class CampoObrigatorioValidador:
    """Valida campos obrigatórios não vazios"""
    def validar(self, valor: str, nome_campo: str) -> None:
        if not isinstance(valor, str) or not valor.strip():
            raise ValueError(f"{nome_campo} é obrigatório(a).")


# ==============================
# ENTIDADE DE DOMÍNIO
# ==============================


@dataclass
class Candidato:
    id: int
    nome: str
    _cpf: str = field(repr=False)
    email: str
    _areas_interesse: List[str] = field(default_factory=list, repr=False)
    nivel_formacao: str = ""
    curriculo: Optional[Dict[str, Any]] = None  # {objetivo, resumo, experiencias, formacoes}
    localidade: str = ""

    # Dependências injetadas
    id_validador: Validador = field(default_factory=IdValidador, repr=False)
    nome_validador: Validador = field(default_factory=NomeValidador, repr=False)
    cpf_validador: Validador = field(default_factory=CpfValidador, repr=False)
    email_validador: Validador = field(default_factory=EmailValidador, repr=False)
    areas_validador: Validador = field(default_factory=AreasValidador, repr=False)
    nivel_validador: Validador = field(default_factory=NivelFormacaoValidador, repr=False)
    
    # Validadores de currículo
    objetivo_validador: Validador = field(default_factory=ObjetivoCurriculoValidador, repr=False)
    resumo_validador: Validador = field(default_factory=ResumoCurriculoValidador, repr=False)
    data_validador: DataCurriculoValidador = field(default_factory=DataCurriculoValidador, repr=False)
    nivel_curriculo_validador: Validador = field(default_factory=NivelFormacaoCurriculoValidador, repr=False)
    campo_obrigatorio_validador: CampoObrigatorioValidador = field(default_factory=CampoObrigatorioValidador, repr=False)

    def __post_init__(self):
        self.id_validador.validar(self.id)
        self.nome_validador.validar(self.nome)
        self.cpf_validador.validar(self._cpf)
        self.email_validador.validar(self.email)
        self.areas_validador.validar(self._areas_interesse)
        self.nivel_validador.validar(self.nivel_formacao)
        if not isinstance(self.localidade, str):
            raise TypeError("Localidade deve ser uma string.")
        self.localidade = self.localidade.strip()
        # Proteção contra mutação externa
        self._areas_interesse = [a.strip() for a in self._areas_interesse]


    # ==============================
    # PROPRIEDADES
    # ==============================

    @property
    def cpf(self) -> str:
        return self._cpf

    @property
    def areas_interesse(self) -> Tuple[str, ...]:
        return tuple(self._areas_interesse)


    # ==============================
    # REGRAS DE NEGÓCIO
    # ==============================

    def adicionar_area(self, area: str) -> None:
        area = area.strip()
        if not area:
            raise ValueError("Área inválida.")
        if area in self._areas_interesse:
            raise ValueError("Área já cadastrada.")
        self._areas_interesse.append(area)

    def remover_area(self, area: str) -> None:
        if area not in self._areas_interesse:
            raise ValueError("Área não encontrada.")
        if len(self._areas_interesse) <= 1:
            raise ValueError("Ao menos uma área é obrigatória.")
        self._areas_interesse.remove(area)

    def atualizar_dado(self, campo: str, novo_valor) -> None:
        """Atualiza um campo específico do candidato com validação"""
        if campo == "nome":
            self.nome_validador.validar(novo_valor)
            self.nome = novo_valor
        elif campo == "email":
            self.email_validador.validar(novo_valor)
            self.email = novo_valor
        elif campo == "nivel_formacao":
            self.nivel_validador.validar(novo_valor)
            self.nivel_formacao = novo_valor
        elif campo == "curriculo":
            if novo_valor is not None and not isinstance(novo_valor, dict):
                raise TypeError("Currículo deve ser um dicionário")
            self.curriculo = novo_valor
        elif campo == "localidade":
            if not isinstance(novo_valor, str):
                raise TypeError("Localidade deve ser uma string.")
            self.localidade = novo_valor.strip()
        else:
            raise ValueError(f"Campo '{campo}' não pode ser atualizado.")

    # ==============================
    # MÉTODOS DE CURRÍCULO
    # ==============================

    def inicializar_curriculo(self) -> None:
        """Inicializa um currículo vazio para o candidato"""
        if self.curriculo is None:
            self.curriculo = {
                "objetivo": "",
                "resumo": "",
                "experiencias": [],
                "formacoes": []
            }

    def atualizar_objetivo_curriculo(self, objetivo: str) -> None:
        """Atualiza o objetivo profissional do currículo"""
        self.objetivo_validador.validar(objetivo)
        self.inicializar_curriculo()
        self.curriculo["objetivo"] = objetivo.strip()

    def atualizar_resumo_curriculo(self, resumo: str) -> None:
        """Atualiza o resumo profissional do currículo"""
        self.resumo_validador.validar(resumo)
        self.inicializar_curriculo()
        self.curriculo["resumo"] = resumo.strip()

    def adicionar_experiencia(self, empresa: str, cargo: str, descricao: str = "",
                               data_inicio: str = "", data_fim: str = "") -> None:
        """Adiciona uma experiência profissional ao currículo"""
        # Validações
        self.campo_obrigatorio_validador.validar(empresa, "Empresa")
        self.campo_obrigatorio_validador.validar(cargo, "Cargo")
        self.data_validador.validar(data_inicio, obrigatorio=True)
        self.data_validador.validar(data_fim, obrigatorio=False)
        
        self.inicializar_curriculo()
        experiencia = {
            "empresa": empresa.strip(),
            "cargo": cargo.strip(),
            "descricao": descricao.strip(),
            "data_inicio": data_inicio,
            "data_fim": data_fim  # vazio = emprego atual
        }
        self.curriculo["experiencias"].append(experiencia)

    def remover_experiencia(self, indice: int) -> None:
        """Remove uma experiência pelo índice"""
        if self.curriculo is None or indice >= len(self.curriculo.get("experiencias", [])):
            raise ValueError("Experiência não encontrada")
        self.curriculo["experiencias"].pop(indice)

    def adicionar_formacao(self, instituicao: str, curso: str, nivel: str,
                           data_inicio: str = "", data_conclusao: str = "") -> None:
        """Adiciona uma formação acadêmica ao currículo"""
        # Validações
        self.campo_obrigatorio_validador.validar(instituicao, "Instituição")
        self.campo_obrigatorio_validador.validar(curso, "Curso")
        self.nivel_curriculo_validador.validar(nivel)
        self.data_validador.validar(data_inicio, obrigatorio=True)
        self.data_validador.validar(data_conclusao, obrigatorio=False)
        
        self.inicializar_curriculo()
        formacao = {
            "instituicao": instituicao.strip(),
            "curso": curso.strip(),
            "nivel": nivel.strip(),
            "data_inicio": data_inicio,
            "data_conclusao": data_conclusao  # vazio = em andamento
        }
        self.curriculo["formacoes"].append(formacao)

    def remover_formacao(self, indice: int) -> None:
        """Remove uma formação pelo índice"""
        if self.curriculo is None or indice >= len(self.curriculo.get("formacoes", [])):
            raise ValueError("Formação não encontrada")
        self.curriculo["formacoes"].pop(indice)

    def listar_experiencias(self) -> List[Dict[str, Any]]:
        """Lista todas as experiências do currículo"""
        if self.curriculo is None:
            return []
        return self.curriculo.get("experiencias", [])

    def listar_formacoes(self) -> List[Dict[str, Any]]:
        """Lista todas as formações do currículo"""
        if self.curriculo is None:
            return []
        return self.curriculo.get("formacoes", [])


# ==============================
# MAPPER (Responsabilidade isolada)
# ==============================


class CandidatoMapper:

    @staticmethod
    def to_dict(candidato: Candidato) -> dict:
        return {
            "id": candidato.id,
            "nome": candidato.nome,
            "cpf": candidato.cpf,
            "email": candidato.email,
            "areas_interesse": list(candidato.areas_interesse),
            "nivel_formacao": candidato.nivel_formacao,
            "curriculo": candidato.curriculo,
            "localidade": candidato.localidade
        }

    @staticmethod
    def from_dict(dados: dict) -> Candidato:
        return Candidato(
            id=dados["id"],
            nome=dados["nome"],
            _cpf=dados["cpf"],
            email=dados["email"],
            _areas_interesse=dados["areas_interesse"],
            nivel_formacao=dados["nivel_formacao"],
            curriculo=dados.get("curriculo"),
            localidade=dados.get("localidade", "")
        )
