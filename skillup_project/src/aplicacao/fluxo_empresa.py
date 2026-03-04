"""
Fluxo de Empresa - Gerencia a navegação e ações da empresa na plataforma
"""

import os
from typing import Optional
from src.dominio.empresa import Empresa
from src.services.services_empresa import EmpresaService


class FluxoEmpresa:
    """Orquestra o fluxo completo de empresas na plataforma"""

    def __init__(self, service_empresa: EmpresaService):
        """
        Inicializa o fluxo de empresa
        
        Args:
            service_empresa: Serviço de empresas
        """
        self.service = service_empresa
        self.empresa_logada: Optional[Empresa] = None
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
        print("         EMPRESA - AUTENTICAÇÃO".center(60))
        print("=" * 60)
        print("\n1. Login")
        print("2. Cadastro")
        print("3. Voltar")
        print("\n" + "-" * 60)

        opcao = input("Digite a opção desejada (1-3): ").strip()
        return opcao

    def _login(self) -> None:
        """Fluxo de login de empresa"""
        self._limpar_tela()
        print("\n=== LOGIN DE EMPRESA ===\n")

        try:
            id_empresa = int(input("Digite o ID da sua empresa: ").strip())
            empresa = self.service.buscar_por_id(id_empresa)
            self.empresa_logada = empresa
            self._limpar_tela()
            print(f"\n✅ Login realizado com sucesso!")
            print(f"Bem-vindo, {empresa.nome}!\n")
            input("Pressione ENTER para continuar...")

        except ValueError:
            self._limpar_tela()
            print("\n❌ ID inválido! Digite um número.")
            input("Pressione ENTER para tentar novamente...")
        except Exception as e:
            self._limpar_tela()
            print(f"\n❌ Erro ao fazer login: {e}")
            input("Pressione ENTER para voltar...")

    def _cadastro(self) -> None:
        """Fluxo de cadastro de nova empresa"""
        self._limpar_tela()
        print("\n=== CADASTRO DE EMPRESA ===\n")

        try:
            nome = input("Nome da empresa: ").strip()
            cnpj = input("CNPJ (14 dígitos): ").strip()
            porte = input("Porte da empresa (pequeno/médio/grande): ").strip().lower()

            if porte not in ["pequeno", "médio", "grande"]:
                raise ValueError("Porte deve ser: pequeno, médio ou grande")

            empresa = self.service.cadastrar(
                nome=nome,
                cnpj=cnpj,
                porte=porte
            )

            self.empresa_logada = empresa
            self._limpar_tela()
            print(f"\n✅ Cadastro realizado com sucesso!")
            print(f"ID da empresa: {empresa.id}")
            print(f"Bem-vindo, {empresa.nome}!\n")
            input("Pressione ENTER para continuar...")

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
                if self.empresa_logada:
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
    # MENU PRINCIPAL DA EMPRESA
    # ==========================

    def _construir_acoes_menu_principal(self) -> dict:
        """Constrói o dicionário de ações do menu principal"""
        return {
            1: self._publicar_vaga,
            2: self._publicar_curso,
            3: self._gerenciar_vagas,
            4: self._gerenciar_cursos,
            5: self._ver_candidaturas,
            6: self._ver_perfil,
            7: lambda: None  # Voltar
        }

    def _exibir_menu_principal(self) -> str:
        """Exibe o menu principal da empresa"""
        self._limpar_tela()
        print("=" * 60)
        print(f"         BEM-VINDO, {self.empresa_logada.nome.upper()}".center(60))
        print("=" * 60)
        print("\n1. Publicar Vaga de Emprego")
        print("2. Publicar Curso")
        print("3. Gerenciar Vagas")
        print("4. Gerenciar Cursos")
        print("5. Ver Candidaturas Recebidas")
        print("6. Perfil da Empresa")
        print("7. Sair")
        print("\n" + "-" * 60)

        opcao = input("Digite a opção desejada (1-7): ").strip()
        return opcao

    def _publicar_vaga(self) -> None:
        """Menu para publicar nova vaga"""
        self._limpar_tela()
        print("\n=== PUBLICAR VAGA DE EMPREGO ===\n")
        print("⚠️  Funcionalidade em desenvolvimento")
        print("\nOpções planejadas:")
        print("  • Preencher dados da vaga")
        print("  • Definir requisitos")
        print("  • Definir pré-requisitos (cursos)")
        print("  • Publicar vaga")
        input("\nPressione ENTER para voltar...")

    def _publicar_curso(self) -> None:
        """Menu para publicar novo curso"""
        self._limpar_tela()
        print("\n=== PUBLICAR CURSO ===\n")
        print("⚠️  Funcionalidade em desenvolvimento")
        print("\nOpções planejadas:")
        print("  • Preencher dados do curso")
        print("  • Definir competências")
        print("  • Configurar tipo (presencial/EAD)")
        print("  • Publicar curso")
        input("\nPressione ENTER para voltar...")

    def _gerenciar_vagas(self) -> None:
        """Menu para gerenciar vagas publicadas"""
        self._limpar_tela()
        print("\n=== GERENCIAR VAGAS ===\n")
        print("⚠️  Funcionalidade em desenvolvimento")
        print("\nOpções planejadas:")
        print("  • Listar vagas publicadas")
        print("  • Editar vaga")
        print("  • Encerrar vaga")
        print("  • Ver detalhes de candidaturas")
        input("\nPressione ENTER para voltar...")

    def _gerenciar_cursos(self) -> None:
        """Menu para gerenciar cursos publicados"""
        self._limpar_tela()
        print("\n=== GERENCIAR CURSOS ===\n")
        print("⚠️  Funcionalidade em desenvolvimento")
        print("\nOpções planejadas:")
        print("  • Listar cursos publicados")
        print("  • Editar curso")
        print("  • Desativar curso")
        print("  • Ver inscritos")
        input("\nPressione ENTER para voltar...")

    def _ver_candidaturas(self) -> None:
        """Menu para ver candidaturas recebidas"""
        self._limpar_tela()
        print("\n=== CANDIDATURAS RECEBIDAS ===\n")
        print("⚠️  Funcionalidade em desenvolvimento")
        print("\nOpções planejadas:")
        print("  • Listar todas as candidaturas")
        print("  • Filtrar por vaga")
        print("  • Filtrar por status")
        print("  • Ver perfil do candidato")
        input("\nPressione ENTER para voltar...")

    def _ver_perfil(self) -> None:
        """Exibe o perfil da empresa"""
        self._limpar_tela()
        print("\n=== PERFIL DA EMPRESA ===\n")
        print(f"ID: {self.empresa_logada.id}")
        print(f"Nome: {self.empresa_logada.nome}")
        print(f"CNPJ: {self.empresa_logada.cnpj}")
        print(f"Porte: {self.empresa_logada.porte}")
        print(f"Limite de publicações: {self.empresa_logada.obter_limites_publicacao()}")
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
                if opcao_num == 7:
                    return False
                return True
            else:
                self._limpar_tela()
                print("\n❌ Opção inválida! Digite um número entre 1 e 7.")
                input("Pressione ENTER para continuar...")
                return True

        except ValueError:
            self._limpar_tela()
            print("\n❌ Entrada inválida! Digite um número entre 1 e 7.")
            input("Pressione ENTER para continuar...")
            return True

    # ==========================
    # EXECUÇÃO DO FLUXO
    # ==========================

    def executar(self) -> None:
        """Executa o fluxo completo da empresa"""
        # Fase 1: Autenticação
        while True:
            opcao = self._exibir_menu_autenticacao()
            if not self._processar_opcao_autenticacao(opcao):
                break

        # Se conseguiu fazer login/cadastro
        if self.empresa_logada:
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
