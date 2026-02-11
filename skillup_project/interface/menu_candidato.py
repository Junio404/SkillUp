import os

from src.dominio import Candidato

class Menu:
    """Gerencia o fluxo de interface (CLI) da aplicação."""

    def __init__(self):
        self.usuario_logado = None
        self.tipo_usuario = None

    # ===========================
    # FLUXOS PARA CANDIDATO
    # ===========================

    def fluxo_candidato(self):
        """Fluxo principal para candidatos."""
        opcao = input("\n1 - Entrar\n2 - Criar Perfil\nEscolha: ").strip()

        if opcao == "1":
            self.login_candidato()
        elif opcao == "2":
            self.cadastro_candidato()
        else:
            print("Opção inválida!")

    def cadastro_candidato(self):
        """Cadastro simples de candidato (sem CPF/email/validações por enquanto)."""
        self.limpar_tela()
        print("\n=== CADASTRO DE CANDIDATO ===\n")

        try:
            nome = input("Nome: ").strip()
            area_interesse = input("Área de interesse (ex: TI, RH, Vendas): ").strip()
            nivel_formacao = input("Nível de formação (Ensino Médio/Graduação/Pós): ").strip()

            # Placeholder para campos não usados agora (cpf/email/senha)
            candidato = Candidato(
                nome=nome,
                cpf="",
                email="",
                senha="",
                area_interesse=area_interesse,
                nivel_formacao=nivel_formacao,
            )

            self.usuario_logado = candidato
            self.tipo_usuario = "candidato"
            print(f"Perfil criado com sucesso! Bem-vindo, {nome}!")
            self.menu_candidato()

        except Exception as e:
            print(f"Erro ao cadastrar candidato: {e}")
            input("Pressione ENTER para continuar...")

    def login_candidato(self):
        """
        Login simplificado (sem autenticação real).
        Apenas seleciona um 'perfil' para navegar.
        """
        self.limpar_tela()
        print("\n=== ENTRAR COMO CANDIDATO ===\n")

        try:
            nome = input("Nome: ").strip()
            area_interesse = input("Área de interesse: ").strip()
            nivel_formacao = input("Nível de formação: ").strip()

            candidato = Candidato(
                nome=nome,
                cpf="",
                email="",
                senha="",
                area_interesse=area_interesse,
                nivel_formacao=nivel_formacao,
            )

            self.usuario_logado = candidato
            self.tipo_usuario = "candidato"
            print(f"Acesso realizado! Bem-vindo, {nome}!")
            self.menu_candidato()

        except Exception as e:
            print(f"Erro no acesso: {e}")
            input("Pressione ENTER para continuar...")

    def menu_candidato(self):
        """Menu de ações disponíveis para candidato (simplificado)."""
        while True:
            self.limpar_tela()
            print("\n=== MENU CANDIDATO ===")
            print(f"Usuário: {self.usuario_logado.nome}")
            print(f"Área: {self.usuario_logado.area_interesse}")
            print(f"Formação: {self.usuario_logado.nivel_formacao}\n")

            print("1. Buscar Vagas")
            print("2. Buscar Cursos")
            print("3. Atualizar Perfil")
            print("4. Sair da Conta")
            print("-" * 50)

            opcao = input("Escolha uma opção: ").strip()

            if opcao == "1":
                self.buscar_vagas()
            elif opcao == "2":
                self.buscar_cursos()
            elif opcao == "3":
                self.atualizar_perfil()
            elif opcao == "4":
                print("Saindo da conta...")
                self.usuario_logado = None
                self.tipo_usuario = None
                break
            else:
                print("Opção inválida!")
                input("Pressione ENTER para continuar...")

    def buscar_vagas(self):
        """Buscar vagas disponíveis (placeholder)."""
        self.limpar_tela()
        print("\n=== BUSCAR VAGAS ===\n")
        input("Filtrar por área (deixe em branco para ver todas): ").strip()
        input("Filtrar por modalidade (Presencial/Remoto/Híbrido): ").strip()

        print("Buscando vagas...")
        print("Espaço para vagas disponíveis")
        input("Pressione ENTER para continuar...")

    def buscar_cursos(self):
        """Buscar cursos disponíveis (placeholder)."""
        self.limpar_tela()
        print("\n=== BUSCAR CURSOS ===\n")
        input("Filtrar por área (deixe em branco para ver todos): ").strip()

        print("Buscando cursos...")
        print("Espaço para cursos disponíveis")
        input("Pressione ENTER para continuar...")

    def atualizar_perfil(self):
        """Atualizar área de interesse e nível de formação (sem email/senha)."""
        self.limpar_tela()
        print("\n=== ATUALIZAR PERFIL ===\n")

        try:
            print("O que deseja atualizar?\n")
            print("1. Área de interesse")
            print("2. Nível de formação")
            print("3. Voltar")

            opcao = input("\nEscolha uma opção: ").strip()

            if opcao == "1":
                nova_area = input("Nova área de interesse: ").strip()
                self.usuario_logado.atualizar_area_interesse(nova_area)
                print("Área atualizada com sucesso!")

            elif opcao == "2":
                novo_nivel = input("Novo nível de formação: ").strip()
                self.usuario_logado.atualizar_nivel_formacao(novo_nivel)
                print("Nível de formação atualizado com sucesso!")

        except Exception as e:
            print(f"Erro ao atualizar perfil: {e}")

        input("\nPressione ENTER para continuar...")
