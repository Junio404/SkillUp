"""
SkillUp - Plataforma de Gestão de Vagas e Capacitação Profissional
Ponto de entrada principal da aplicação
"""

import os
import sys
from typing import Optional

# Adiciona o diretório skillup_project ao PATH para importações relativas
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.services.service_candidato import CandidatoService
from src.services.service_instituicao_ensino import ServiceInstituicaoEnsino
from src.services.services_empresa import EmpresaService
from src.repositorios.repositorio_candidato import RepositorioCandidatoJSON
from src.repositorios.repositorio_empresa import RepositorioEmpresaJSON


class AplicacaoSkillUp:
    """Orquestradora principal da aplicação SkillUp"""

    def __init__(self):
        """Inicializa a aplicação e suas dependências"""
        self._inicializar_servicos()
        self.acoes = self._construir_acoes()

    def _inicializar_servicos(self) -> None:
        """Inicializa todos os serviços e repositórios"""
        # Repositórios
        self.repo_candidato = RepositorioCandidatoJSON()
        self.repo_empresa = RepositorioEmpresaJSON()

        # Serviços
        self.service_candidato = CandidatoService(self.repo_candidato)
        self.service_empresa = EmpresaService(self.repo_empresa)
        self.service_instituicao = ServiceInstituicaoEnsino(
            None, None  # TODO: implementar repositórios da instituição
        )

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
        self._limpar_tela()
        print("\nMódulo de Candidato ainda não implementado.")
        print("\nFuncionalidades em desenvolvimento:")
        print("  • Login/Cadastro de Candidato")
        print("  • Exploração de Vagas")
        print("  • Exploração de Cursos")
        print("  • Gestão de Candidaturas")
        input("\nPressione ENTER para retornar...")

    def _executar_fluxo_empresa(self) -> None:
        """Executa o fluxo de empresa"""
        self._limpar_tela()
        print("\nMódulo de Empresa ainda não implementado.")
        print("\nFuncionalidades em desenvolvimento:")
        print("  • Login/Cadastro de Empresa")
        print("  • Publicação de Vagas")
        print("  • Gestão de Candidaturas")
        input("\nPressione ENTER para retornar...")

    def _executar_fluxo_instituicao(self) -> None:
        """Executa o fluxo de instituição de ensino"""
        self._limpar_tela()
        print("\nMódulo de Instituição de Ensino ainda não implementado.")
        print("\nFuncionalidades em desenvolvimento:")
        print("  • Login/Cadastro de Instituição")
        print("  • Publicação de Cursos")
        print("  • Gestão de Inscrições")
        input("\nPressione ENTER para retornar...")

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
                print("\n❌ Opção inválida! Digite um número entre 1 e 4.")
                input("Pressione ENTER para continuar...")
                return True

        except ValueError:
            self._limpar_tela()
            print("\n❌ Entrada inválida! Digite um número entre 1 e 4.")
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
        print(f"\n❌ Erro fatal na aplicação: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
