"""
Fluxo de Instituição de Ensino - Gerencia a navegação e ações da instituição na plataforma
"""

import os
from typing import Optional
from src.dominio.instituicao_ensino import InstituicaoEnsino
from src.services.service_instituicao_ensino import ServiceInstituicaoEnsino


class FluxoInstituicao:
    """Orquestra o fluxo completo de instituições de ensino na plataforma"""

    def __init__(self, service_instituicao: ServiceInstituicaoEnsino):
        """
        Inicializa o fluxo de instituição
        
        Args:
            service_instituicao: Serviço de instituições de ensino
        """
        self.service = service_instituicao
        self.instituicao_logada: Optional[InstituicaoEnsino] = None
        self.acoes_autenticacao = self._construir_acoes_autenticacao()
        self.acoes_menu_principal = self._construir_acoes_menu_principal()

    def _limpar_tela(self) -> None:
        """Limpa a tela do console"""
        os.system("clear" if os.name == "posix" else "cls")

    # ==========================
    # AUTENTICAÇÃO
    # ==========================

    def _construir_acoes_autenticacao(self) -> dict:
        """Constrói o dicionário de ações de autenticação"""
        return {
            1: self._login,
            2: self._cadastro,
            3: lambda: None  # Voltar
        }

    def _exibir_menu_autenticacao(self) -> str:
        """Exibe o menu de autenticação e retorna a opção"""
        self._limpar_tela()
        print("=" * 60)
        print("    INSTITUIÇÃO DE ENSINO - AUTENTICAÇÃO".center(60))
        print("=" * 60)
        print("\n1. Login")
        print("2. Cadastro")
        print("3. Voltar")
        print("\n" + "-" * 60)

        opcao = input("Digite a opção desejada (1-3): ").strip()
        return opcao

    def _login(self) -> None:
        """Fluxo de login de instituição"""
        self._limpar_tela()
        print("\n=== LOGIN DE INSTITUIÇÃO DE ENSINO ===\n")

        try:
            id_instituicao = int(input("Digite o ID da sua instituição: ").strip())
            # TODO: Implementar busca de instituição no repositório
            # instituicao = self.service.buscar_por_id(id_instituicao)
            # self.instituicao_logada = instituicao
            self._limpar_tela()
            print(f"\n⚠️  Login de instituição ainda não implementado no backend")
            input("Pressione ENTER para voltar...")

        except ValueError:
            self._limpar_tela()
            print("\n❌ ID inválido! Digite um número.")
            input("Pressione ENTER para tentar novamente...")

    def _cadastro(self) -> None:
        """Fluxo de cadastro de nova instituição"""
        self._limpar_tela()
        print("\n=== CADASTRO DE INSTITUIÇÃO DE ENSINO ===\n")

        try:
            razao_social = input("Razão Social: ").strip()
            nome_fantasia = input("Nome Fantasia: ").strip()
            cnpj = input("CNPJ (14 dígitos): ").strip()
            registro_educacional = input("Registro Educacional: ").strip()
            tipo = input("Tipo (Pública/Privada): ").strip().capitalize()
            modalidades = input("Modalidades (separadas por vírgula, ex: Presencial,EAD): ").strip().split(",")
            modalidades = [mod.strip() for mod in modalidades]

            # TODO: Implementar cadastro no repositório
            # instituicao = self.service.criar_conta(...)
            # self.instituicao_logada = instituicao

            self._limpar_tela()
            print(f"\n⚠️  Cadastro de instituição ainda não implementado no backend")
            input("Pressione ENTER para voltar...")

        except ValueError as e:
            self._limpar_tela()
            print(f"\n❌ Erro de validação: {e}")
            input("Pressione ENTER para tentar novamente...")
        except Exception as e:
            self._limpar_tela()
            print(f"\n❌ Erro ao cadastrar: {e}")
            input("Pressione ENTER para voltar...")

    def _processar_opcao_autenticacao(self, opcao: str) -> bool:
        """
        Processa opção de autenticação.
        Retorna True se deve continuar em autenticação, False se entrou ou saiu.
        """
        try:
            opcao_num = int(opcao)
            acao = self.acoes_autenticacao.get(opcao_num)

            if acao:
                acao()
                # Se fez login/cadastro com sucesso
                if self.instituicao_logada:
                    return False
                # Se clicou em voltar
                elif opcao_num == 3:
                    return False
                return True
            else:
                self._limpar_tela()
                print("\n❌ Opção inválida! Digite um número entre 1 e 3.")
                input("Pressione ENTER para continuar...")
                return True

        except ValueError:
            self._limpar_tela()
            print("\n❌ Entrada inválida! Digite um número entre 1 e 3.")
            input("Pressione ENTER para continuar...")
            return True

    # ==========================
    # MENU PRINCIPAL DA INSTITUIÇÃO
    # ==========================

    def _construir_acoes_menu_principal(self) -> dict:
        """Constrói o dicionário de ações do menu principal"""
        return {
            1: self._publicar_curso,
            2: self._gerenciar_cursos,
            3: self._ver_inscritos,
            4: self._gerenciar_competencias,
            5: self._ver_perfil,
            6: lambda: None  # Voltar
        }

    def _exibir_menu_principal(self) -> str:
        """Exibe o menu principal da instituição"""
        self._limpar_tela()
        print("=" * 60)
        print("BEM-VINDO À PLATAFORMA SKILLUP".center(60))
        print("=" * 60)
        print("\n1. Publicar Curso")
        print("2. Gerenciar Cursos")
        print("3. Ver Inscritos")
        print("4. Gerenciar Competências")
        print("5. Perfil da Instituição")
        print("6. Sair")
        print("\n" + "-" * 60)

        opcao = input("Digite a opção desejada (1-6): ").strip()
        return opcao

    def _publicar_curso(self) -> None:
        """Menu para publicar novo curso"""
        self._limpar_tela()
        print("\n=== PUBLICAR NOVO CURSO ===\n")
        print("⚠️  Funcionalidade em desenvolvimento")
        print("\nOpções planejadas:")
        print("  • Preencher dados do curso")
        print("  • Definir competências")
        print("  • Configurar modalidade (presencial/EAD)")
        print("  • Publicar curso")
        input("\nPressione ENTER para voltar...")

    def _gerenciar_cursos(self) -> None:
        """Menu para gerenciar cursos publicados"""
        self._limpar_tela()
        print("\n=== GERENCIAR CURSOS ===\n")
        print("⚠️  Funcionalidade em desenvolvimento")
        print("\nOpções planejadas:")
        print("  • Listar cursos publicados")
        print("  • Editar curso")
        print("  • Desativar/Ativar curso")
        print("  • Ver estatísticas")
        input("\nPressione ENTER para voltar...")

    def _ver_inscritos(self) -> None:
        """Menu para ver inscritos nos cursos"""
        self._limpar_tela()
        print("\n=== VER INSCRITOS ===\n")
        print("⚠️  Funcionalidade em desenvolvimento")
        print("\nOpções planejadas:")
        print("  • Listar inscritos por curso")
        print("  • Filtrar por status")
        print("  • Ver progresso do aluno")
        print("  • Gerar certificados")
        input("\nPressione ENTER para voltar...")

    def _gerenciar_competencias(self) -> None:
        """Menu para gerenciar competências dos cursos"""
        self._limpar_tela()
        print("\n=== GERENCIAR COMPETÊNCIAS ===\n")
        print("⚠️  Funcionalidade em desenvolvimento")
        print("\nOpções planejadas:")
        print("  • Listar competências oferecidas")
        print("  • Adicionar competência")
        print("  • Remover competência")
        print("  • Atualizar descrição")
        input("\nPressione ENTER para voltar...")

    def _ver_perfil(self) -> None:
        """Exibe o perfil da instituição"""
        self._limpar_tela()
        print("\n=== PERFIL DA INSTITUIÇÃO ===\n")
        print("⚠️  Instituição não autenticada")
        print("\nPerfil será exibido após login/cadastro.")
        input("\nPressione ENTER para voltar...")

    def _processar_opcao_menu_principal(self, opcao: str) -> bool:
        """
        Processa opção do menu principal.
        Retorna True se deve continuar, False se deve sair.
        """
        try:
            opcao_num = int(opcao)
            acao = self.acoes_menu_principal.get(opcao_num)

            if acao:
                acao()
                # Se clicou em sair
                if opcao_num == 6:
                    return False
                return True
            else:
                self._limpar_tela()
                print("\n❌ Opção inválida! Digite um número entre 1 e 6.")
                input("Pressione ENTER para continuar...")
                return True

        except ValueError:
            self._limpar_tela()
            print("\n❌ Entrada inválida! Digite um número entre 1 e 6.")
            input("Pressione ENTER para continuar...")
            return True

    # ==========================
    # EXECUÇÃO DO FLUXO
    # ==========================

    def executar(self) -> None:
        """Executa o fluxo completo da instituição"""
        # Fase 1: Autenticação
        while True:
            opcao = self._exibir_menu_autenticacao()
            if not self._processar_opcao_autenticacao(opcao):
                break

        # Se conseguiu fazer login/cadastro
        if self.instituicao_logada:
            # Fase 2: Menu principal autenticado
            while True:
                opcao = self._exibir_menu_principal()
                if not self._processar_opcao_menu_principal(opcao):
                    break

        # Despedida
        self._limpar_tela()
        print("\n" + "=" * 60)
        print("OBRIGADO POR USAR SKILLUP".center(60))
        print("=" * 60)
        print("\nAté logo!\n")