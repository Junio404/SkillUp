"""
SkillUp - Plataforma de Gestão de Vagas e Capacitação Profissional
Ponto de entrada principal da aplicação
"""

import os
import sys
from typing import Optional

# Adiciona o diretório skillup_project ao PATH para importações relativas
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Repositórios
from src.repositorios.repositorio_candidato import RepositorioCandidatoJSON
from src.repositorios.repositorio_empresa import RepositorioEmpresaJSON
from src.repositorios.repositorio_instituicao_ensino import RepositorioInstituicaoEnsinoJSON
from src.repositorios.repositorio_vaga_clt import RepositorioVagaCLTJSON
from src.repositorios.repositorio_vaga_estagio import RepositorioVagaEstagioJSON
from src.repositorios.repositorio_candidatura import RepositorioCandidaturaJSON
from src.repositorios.repositorio_inscricao_curso import RepositorioInscricaoCursoJSON
from src.repositorios.repositorio_curso_ead import RepositorioCursoEADJSON
from src.repositorios.repositorio_curso_presencial import RepositorioCursoPresencialJSON
from src.repositorios.repositorio_competencia import RepositorioCompetenciaJSON
from src.repositorios.repositorio_competencia_candidato import RepositorioCompetenciaCandidatoJSON
from src.repositorios.repositorio_requisitos_vaga import RepositorioRequisitoVagaJSON
from src.repositorios.repositorio_curso_competencia import RepositorioCursoCompetenciaJSON
from src.repositorios.repositorio_area_ensino import RepositorioAreaEnsinoJSON
from src.repositorios.repositorio_instituicao_area_ensino import RepositorioInstituicaoAreaEnsinoJSON

# Services
from src.services.service_candidato import CandidatoService
from src.services.service_instituicao_ensino import ServiceInstituicaoEnsino
from src.services.services_empresa import EmpresaService
from src.services.service_busca_vaga import MotorBuscaVaga
from src.services.service_candidatura import CandidaturaService
from src.services.service_inscricao_curso import InscricaoCursoService
from src.services.service_curso_ead import CursoEADService
from src.services.service_curso_presencial import CursoPresencialService
from src.services.service_competencia import CompetenciaService
from src.services.service_competencia_candidato import CompetenciaCandidatoService
from src.services.service_recomendacao import RecomendacaoService
from src.services.service_vaga_clt import VagaCLTService
from src.services.service_vaga_estagio import VagaEstagioService
from src.services.service_requisito_vaga import RequisitoVagaService
from src.services.service_curso_competencia import CursoCompetenciaService
from src.services.service_area_ensino import AreaEnsinoService
from src.services.service_instituicao_area_ensino import InstituicaoAreaEnsinoService

# Fluxos
from src.aplicacao.fluxo_candidato import FluxoCandidato
from src.aplicacao.fluxo_empresa import FluxoEmpresa
from src.aplicacao.fluxo_instituicao import FluxoInstituicao


class AplicacaoSkillUp:
    """Orquestradora principal da aplicação SkillUp"""

    def __init__(self):
        """Inicializa a aplicação e suas dependências"""
        self._inicializar_servicos()
        self.acoes = self._construir_acoes()

    def _inicializar_servicos(self) -> None:
        """Inicializa todos os serviços e repositórios"""
        # ==========================================
        # Repositórios
        # ==========================================
        self.repo_candidato = RepositorioCandidatoJSON()
        self.repo_empresa = RepositorioEmpresaJSON()
        self.repo_instituicao = RepositorioInstituicaoEnsinoJSON()
        self.repo_vaga_clt = RepositorioVagaCLTJSON()
        self.repo_vaga_estagio = RepositorioVagaEstagioJSON()
        self.repo_candidatura = RepositorioCandidaturaJSON()
        self.repo_inscricao_curso = RepositorioInscricaoCursoJSON()
        self.repo_curso_ead = RepositorioCursoEADJSON()
        self.repo_curso_presencial = RepositorioCursoPresencialJSON()
        self.repo_competencia = RepositorioCompetenciaJSON()
        self.repo_competencia_candidato = RepositorioCompetenciaCandidatoJSON()
        self.repo_requisito_vaga = RepositorioRequisitoVagaJSON()
        self.repo_curso_competencia = RepositorioCursoCompetenciaJSON()
        self.repo_area_ensino = RepositorioAreaEnsinoJSON()
        self.repo_instituicao_area = RepositorioInstituicaoAreaEnsinoJSON()

        # ==========================================
        # Serviços
        # ==========================================
        # Candidato
        self.service_candidato = CandidatoService(self.repo_candidato)
        
        # Empresa
        self.service_empresa = EmpresaService(self.repo_empresa)
        
        # Instituição
        self.service_instituicao = ServiceInstituicaoEnsino(
            self.repo_instituicao, self.repo_curso_ead
        )
        
        # Vagas
        self.service_vaga_clt = VagaCLTService(self.repo_vaga_clt, self.repo_empresa)
        self.service_vaga_estagio = VagaEstagioService(self.repo_vaga_estagio, self.repo_empresa)
        self.motor_busca_vagas = MotorBuscaVaga(self.repo_vaga_clt)  # Busca em vagas CLT
        
        # Candidatura
        self.service_candidatura = CandidaturaService(
            self.repo_candidatura,
            self.repo_vaga_clt,
            self.repo_vaga_estagio,
            self.repo_candidato
        )
        
        # Cursos
        self.service_curso_ead = CursoEADService(self.repo_curso_ead, self.repo_instituicao)
        self.service_curso_presencial = CursoPresencialService(self.repo_curso_presencial, self.repo_instituicao)
        self.service_curso_competencia = CursoCompetenciaService(self.repo_curso_competencia)
        
        # Inscrição em cursos
        self.service_inscricao_curso = InscricaoCursoService(
            self.repo_inscricao_curso,
            self.repo_curso_ead,
            self.repo_curso_presencial,
            self.repo_candidato,
            self.repo_curso_competencia,
            self.repo_competencia_candidato
        )
        
        # Competências
        self.service_competencia = CompetenciaService(self.repo_competencia)
        self.service_competencia_candidato = CompetenciaCandidatoService(self.repo_competencia_candidato)
        
        # Requisitos de vaga
        self.service_requisito_vaga = RequisitoVagaService(self.repo_requisito_vaga)
        
        # Recomendação
        self.service_recomendacao = RecomendacaoService(self.repo_vaga_clt, self.repo_curso_ead)
        
        # Áreas de ensino
        self.service_area_ensino = AreaEnsinoService(self.repo_area_ensino)
        self.service_instituicao_area = InstituicaoAreaEnsinoService(self.repo_instituicao_area)

    def _limpar_tela(self) -> None:
        """Limpa a tela do console"""
        os.system("clear" if os.name == "posix" else "cls")

    def _exibir_menu_principal(self) -> str:
        """Exibe o menu principal e retorna a opção escolhida"""
        self._limpar_tela()
        print("=" * 60)
        print("         BEM-VINDO AO SKILLUP".center(60))
        print("  Plataforma de Gestão de Vagas e Capacitação".center(60))
        print("=" * 60)
        print("\nEscolha seu perfil na plataforma:\n")
        print("  1. Candidato")
        print("  2. Empresa")
        print("  3. Instituição de Ensino")
        print("  4. Sair")
        print("\n" + "-" * 60)

        opcao = input("Digite a opção desejada (1-4): ").strip()
        return opcao

    def _executar_fluxo_candidato(self) -> None:
        """Executa o fluxo de candidato"""
        try:
            fluxo = FluxoCandidato(
                service_candidato=self.service_candidato,
                motor_busca_vagas=self.motor_busca_vagas,
                service_candidatura=self.service_candidatura,
                service_inscricao_curso=self.service_inscricao_curso,
                service_curso_ead=self.service_curso_ead,
                service_curso_presencial=self.service_curso_presencial,
                service_competencia_candidato=self.service_competencia_candidato,
                service_competencia=self.service_competencia,
                service_recomendacao=self.service_recomendacao,
            )
            fluxo.executar()
        except Exception as e:
            self._limpar_tela()
            print(f"\nErro ao executar fluxo de candidato: {e}")
            input("Pressione ENTER para continuar...")

    def _executar_fluxo_empresa(self) -> None:
        """Executa o fluxo de empresa"""
        try:
            fluxo = FluxoEmpresa(
                service_empresa=self.service_empresa,
                service_vaga_clt=self.service_vaga_clt,
                service_vaga_estagio=self.service_vaga_estagio,
                service_requisito_vaga=self.service_requisito_vaga,
                service_candidatura=self.service_candidatura,
                service_competencia=self.service_competencia,
            )
            fluxo.executar()
        except Exception as e:
            self._limpar_tela()
            print(f"\nErro ao executar fluxo de empresa: {e}")
            input("Pressione ENTER para continuar...")

    def _executar_fluxo_instituicao(self) -> None:
        """Executa o fluxo de instituição de ensino"""
        try:
            fluxo = FluxoInstituicao(
                service_instituicao=self.service_instituicao,
                service_curso_ead=self.service_curso_ead,
                service_curso_presencial=self.service_curso_presencial,
                service_curso_competencia=self.service_curso_competencia,
                service_inscricao_curso=self.service_inscricao_curso,
                service_competencia=self.service_competencia,
                service_area_ensino=self.service_area_ensino,
                service_instituicao_area=self.service_instituicao_area,
            )
            fluxo.executar()
        except Exception as e:
            self._limpar_tela()
            print(f"\n❌ Erro ao executar fluxo de instituição: {e}")
            input("Pressione ENTER para continuar...")

    def _exibir_despedida(self) -> None:
        """Exibe mensagem de despedida"""
        self._limpar_tela()
        print("\n" + "=" * 60)
        print("OBRIGADO POR USAR SKILLUP".center(60))
        print("=" * 60)
        print("\nAté logo!\n")

    def _construir_acoes(self) -> dict:
        """Constrói o dicionário de ações disponíveis"""
        return {
            1: self._executar_fluxo_candidato,
            2: self._executar_fluxo_empresa,
            3: self._executar_fluxo_instituicao,
            4: self._exibir_despedida
        }

    def _processar_opcao(self, opcao: str, acoes: dict) -> bool:
        """
        Processa a opção escolhida pelo usuário.
        Retorna True se deve continuar, False se deve sair.
        """
        try:
            opcao_num = int(opcao)
            acao = acoes.get(opcao_num)

            if acao:
                if opcao_num == 4:  # Opção de sair
                    acao()
                    return False
                else:
                    acao()
                    return True
            else:
                self._limpar_tela()
                print("\nOpção inválida! Digite um número entre 1 e 4.")
                input("Pressione ENTER para continuar...")
                return True

        except ValueError:
            self._limpar_tela()
            print("\nEntrada inválida! Digite um número entre 1 e 4.")
            input("Pressione ENTER para continuar...")
            return True

    def executar(self) -> None:
        """Loop principal da aplicação"""
        while True:
            opcao = self._exibir_menu_principal()

            if not self._processar_opcao(opcao, self.acoes):
                break


def main():
    """Função de entrada da aplicação"""
    try:
        app = AplicacaoSkillUp()
        app.executar()
    except KeyboardInterrupt:
        print("\n\nAplicação interrompida pelo usuário.")
        sys.exit(0)
    except Exception as e:
        print(f"\nErro fatal na aplicação: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()