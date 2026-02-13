from src.dominio.empresa import Empresa
from src.dominio.candidato import Candidato
from src.dominio.vaga import VagaCLT, VagaEstagio
from src.dominio.candidatura import Candidatura
from src.dominio.competencia import Competencia
from src.dominio.curso import Curso
import os
from datetime import datetime


class Menu:
    """Classe responsável por gerenciar o fluxo de interface da aplicação."""
    
    def __init__(self):
        self.usuario_logado = None
        self.tipo_usuario = None
    
    def limpar_tela(self):
        """Limpa a tela do terminal."""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def exibir_menu_principal(self):
        """Menu principal da aplicação."""
        self.limpar_tela()
        print("=" * 50)
        print("        BEM-VINDO AO SKILLUP")
        print("=" * 50)
        print("\nEscolha seu papel na plataforma:\n")
        print("1. Sou uma Empresa")
        print("2. Sou um Candidato")
        print("3. Sair")
        print("-" * 50)
        
        opcao = input("Digite a opção desejada (1, 2 ou 3): ").strip()
        return opcao
    
    # ===========================
    # FLUXOS PARA EMPRESA
    # ===========================
    
    def fluxo_empresa(self):
        """Fluxo principal para empresas."""
        opcao = input("\n1. Fazer Login\n2. Criar Nova Conta\nEscolha: ").strip()
        
        if opcao == "1":
            self.login_empresa()
        elif opcao == "2":
            self.cadastro_empresa()
        else:
            print("Opção inválida!")
    
    def cadastro_empresa(self):
        """Cadastro de nova empresa."""
        self.limpar_tela()
        print("\n=== CADASTRO DE EMPRESA ===\n")
        
        try:
            id_empresa = input("ID da empresa: ").strip()
            nome = input("Nome da empresa: ").strip()
            cnpj = input("CNPJ: ").strip()
            porte = input("Porte (pequeno/medio/grande): ").strip().lower()
            
            if porte not in ["pequeno", "medio", "grande"]:
                print("Porte inválido!")
                return
            
            empresa = Empresa(id_empresa, nome, cnpj, porte)
            self.usuario_logado = empresa
            self.tipo_usuario = "empresa"
            print(f"\n✓ Empresa '{nome}' cadastrada com sucesso!")
            self.menu_empresa()
            
        except Exception as e:
            print(f"Erro ao cadastrar empresa: {e}")
    
    def login_empresa(self):
        """Login de empresa existente."""
        self.limpar_tela()
        print("\n=== LOGIN EMPRESA ===\n")
        
        try:
            cnpj = input("Digite o CNPJ: ").strip()
            nome = input("Digite o nome da empresa: ").strip()
            porte = input("Porte (pequeno/medio/grande): ").strip().lower()
            
            empresa = Empresa(cnpj, nome, cnpj, porte)
            self.usuario_logado = empresa
            self.tipo_usuario = "empresa"
            print(f"\n✓ Login realizado com sucesso! Bem-vindo, {nome}!")
            self.menu_empresa()
            
        except Exception as e:
            print(f"Erro no login: {e}")
    
    def menu_empresa(self):
        """Menu de ações disponíveis para empresa."""
        while True:
            self.limpar_tela()
            print(f"\n=== MENU EMPRESA ===")
            print(f"Empresa: {self.usuario_logado.nome}")
            print(f"Limite de publicações: {self.usuario_logado.obter_limites_publicacao()}\n")
            
            print("1. Publicar Vaga CLT")
            print("2. Publicar Vaga de Estágio")
            print("3. Validar Publicação")
            print("4. Ver Minhas Vagas")
            print("5. Sair da Conta")
            print("-" * 50)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.publicar_vaga_clt()
            elif opcao == "2":
                self.publicar_vaga_estagio()
            elif opcao == "3":
                self.validar_publicacao()
            elif opcao == "4":
                self.ver_minhas_vagas()
            elif opcao == "5":
                print("\n✓ Saindo da conta...")
                self.usuario_logado = None
                break
            else:
                print("Opção inválida!")
                input("Pressione ENTER para continuar...")
    
    def publicar_vaga_clt(self):
        """Publicar vaga de emprego CLT."""
        self.limpar_tela()
        print("\n=== PUBLICAR VAGA CLT ===\n")
        
        try:
            id_vaga = input("ID da vaga: ").strip()
            titulo = input("Título da vaga: ").strip()
            descricao = input("Descrição: ").strip()
            area = input("Área (ex: TI, RH, Vendas): ").strip()
            modalidade = input("Modalidade (Presencial/Remoto/Híbrido): ").strip()
            salario_base = float(input("Salário base (R$): "))
            
            vaga = VagaCLT(id_vaga, titulo, descricao, area, modalidade, salario_base)
            
            if self.usuario_logado.validar_publicacao(vaga):
                custo = vaga.calcular_custo_contratacao()
                print(f"\n✓ Vaga publicada com sucesso!")
                print(f"Custo estimado de contratação: R$ {custo:,.2f}")
            else:
                print("\n✗ Não foi possível publicar a vaga")
                
        except ValueError:
            print("Erro: Digite um valor numérico válido para o salário")
        except Exception as e:
            print(f"Erro ao publicar vaga: {e}")
        
        input("\nPressione ENTER para continuar...")
    
    def publicar_vaga_estagio(self):
        """Publicar vaga de estágio."""
        self.limpar_tela()
        print("\n=== PUBLICAR VAGA DE ESTÁGIO ===\n")
        
        try:
            id_vaga = input("ID da vaga: ").strip()
            titulo = input("Título da vaga: ").strip()
            descricao = input("Descrição: ").strip()
            area = input("Área (ex: TI, RH, Vendas): ").strip()
            modalidade = input("Modalidade (Presencial/Remoto/Híbrido): ").strip()
            bolsa_auxilio = float(input("Bolsa auxílio (R$): "))
            instituicao_conveniada = input("Instituição conveniada: ").strip()
            
            vaga = VagaEstagio(id_vaga, titulo, descricao, area, modalidade, 
                              bolsa_auxilio, instituicao_conveniada)
            
            if self.usuario_logado.validar_publicacao(vaga):
                custo = vaga.calcular_custo_contratacao()
                print(f"\n✓ Vaga de estágio publicada com sucesso!")
                print(f"Custo estimado: R$ {custo:,.2f}")
            else:
                print("\n✗ Não foi possível publicar a vaga")
                
        except ValueError:
            print("Erro: Digite um valor numérico válido")
        except Exception as e:
            print(f"Erro ao publicar vaga: {e}")
        
        input("\nPressione ENTER para continuar...")
    
    def validar_publicacao(self):
        """Validar uma publicação."""
        self.limpar_tela()
        print("\n=== VALIDAR PUBLICAÇÃO ===\n")
        print("Validação de publicações da empresa")
        print("Sua empresa pode publicar vagas e cursos.")
        print("Limite máximo: ", self.usuario_logado.obter_limites_publicacao(), " publicações")
        input("\nPressione ENTER para continuar...")
    
    def ver_minhas_vagas(self):
        """Ver vagas publicadas pela empresa."""
        self.limpar_tela()
        print("\n=== MINHAS VAGAS ===\n")
        print("Vagas publicadas pela empresa:")
        print("(Funcionalidade em desenvolvimento...)")
        input("\nPressione ENTER para continuar...")
    
    # ===========================
    # FLUXOS PARA CANDIDATO
    # ===========================
    
    def fluxo_candidato(self):
        """Fluxo principal para candidatos."""
        opcao = input("\n1. Fazer Login\n2. Criar Nova Conta\nEscolha: ").strip()
        
        if opcao == "1":
            self.login_candidato()
        elif opcao == "2":
            self.cadastro_candidato()
        else:
            print("Opção inválida!")
    
    def cadastro_candidato(self):
        """Cadastro de novo candidato."""
        self.limpar_tela()
        print("\n=== CADASTRO DE CANDIDATO ===\n")
        
        try:
            nome = input("Nome completo: ").strip()
            cpf = input("CPF: ").strip()
            email = input("Email: ").strip()
            senha = input("Senha: ").strip()
            area_interesse = input("Área de interesse (ex: TI, RH, Vendas): ").strip()
            nivel_formacao = input("Nível de formação (Ensino Médio/Graduação/Pós-graduação): ").strip()
            
            candidato = Candidato(nome, cpf, email, senha, area_interesse, nivel_formacao)
            self.usuario_logado = candidato
            self.tipo_usuario = "candidato"
            print(f"\n✓ Candidato '{nome}' cadastrado com sucesso!")
            self.menu_candidato()
            
        except Exception as e:
            print(f"Erro ao cadastrar candidato: {e}")
    
    def login_candidato(self):
        """Login de candidato existente."""
        self.limpar_tela()
        print("\n=== LOGIN CANDIDATO ===\n")
        
        try:
            email = input("Digite seu email: ").strip()
            senha = input("Digite sua senha: ").strip()
            
            # Simular validação de credenciais
            nome = input("Digite seu nome: ").strip()
            cpf = input("Digite seu CPF: ").strip()
            area_interesse = input("Área de interesse: ").strip()
            nivel_formacao = input("Nível de formação: ").strip()
            
            candidato = Candidato(nome, cpf, email, senha, area_interesse, nivel_formacao)
            self.usuario_logado = candidato
            self.tipo_usuario = "candidato"
            print(f"\n✓ Login realizado com sucesso! Bem-vindo, {nome}!")
            self.menu_candidato()
            
        except Exception as e:
            print(f"Erro no login: {e}")
    
    def menu_candidato(self):
        """Menu de ações disponíveis para candidato."""
        while True:
            self.limpar_tela()
            print(f"\n=== MENU CANDIDATO ===")
            print(f"Usuário: {self.usuario_logado.nome}")
            print(f"Email: {self.usuario_logado.email}")
            print(f"Área: {self.usuario_logado.area_interesse}\n")
            
            print("1. Buscar Vagas")
            print("2. Minhas Candidaturas")
            print("3. Buscar Cursos")
            print("4. Atualizar Perfil")
            print("5. Alterar Senha")
            print("6. Sair da Conta")
            print("-" * 50)
            
            opcao = input("Escolha uma opção: ").strip()
            
            if opcao == "1":
                self.buscar_vagas()
            elif opcao == "2":
                self.minhas_candidaturas()
            elif opcao == "3":
                self.buscar_cursos()
            elif opcao == "4":
                self.atualizar_perfil()
            elif opcao == "5":
                self.alterar_senha()
            elif opcao == "6":
                print("\n✓ Saindo da conta...")
                self.usuario_logado = None
                break
            else:
                print("Opção inválida!")
                input("Pressione ENTER para continuar...")
    
    def buscar_vagas(self):
        """Buscar vagas disponíveis."""
        self.limpar_tela()
        print("\n=== BUSCAR VAGAS ===\n")
        
        try:
            filtro_area = input("Filtrar por área (deixe em branco para ver todas): ").strip()
            filtro_modalidade = input("Filtrar por modalidade (Presencial/Remoto/Híbrido): ").strip()
            
            print("\n✓ Buscando vagas...")
            print("(Vagas disponíveis seriam listadas aqui)")
            print(f"Sua área de interesse: {self.usuario_logado.area_interesse}")
            print(f"Seu nível de formação: {self.usuario_logado.nivel_formacao}")
            
        except Exception as e:
            print(f"Erro ao buscar vagas: {e}")
        
        input("\nPressione ENTER para continuar...")
    
    def candidatar_a_vaga(self, vaga):
        """Candidatar-se a uma vaga."""
        try:
            candidatura = self.usuario_logado.candidatar_se(vaga)
            print(f"✓ Candidatura enviada com sucesso para a vaga: {vaga.titulo}")
            return candidatura
        except Exception as e:
            print(f"Erro ao enviar candidatura: {e}")
    
    def minhas_candidaturas(self):
        """Ver candidaturas do candidato."""
        self.limpar_tela()
        print("\n=== MINHAS CANDIDATURAS ===\n")
        print("Histórico de candidaturas:")
        print("(Funcionalidade em desenvolvimento...)")
        input("\nPressione ENTER para continuar...")
    
    def buscar_cursos(self):
        """Buscar cursos disponíveis."""
        self.limpar_tela()
        print("\n=== BUSCAR CURSOS ===\n")
        
        try:
            filtro_area = input("Filtrar por área (deixe em branco para ver todos): ").strip()
            
            print("\n✓ Buscando cursos...")
            print("(Cursos disponíveis seriam listados aqui)")
            print(f"Sua área de interesse: {self.usuario_logado.area_interesse}")
            
        except Exception as e:
            print(f"Erro ao buscar cursos: {e}")
        
        input("\nPressione ENTER para continuar...")
    
    def inscrever_em_curso(self, curso):
        """Inscrever-se em um curso."""
        try:
            inscricao = self.usuario_logado.inscrever_em_curso(curso)
            print(f"✓ Inscrição realizada com sucesso no curso: {curso.nome}")
            return inscricao
        except Exception as e:
            print(f"Erro ao se inscrever no curso: {e}")
    
    def atualizar_perfil(self):
        """Atualizar informações do perfil."""
        self.limpar_tela()
        print("\n=== ATUALIZAR PERFIL ===\n")
        
        try:
            print("O que deseja atualizar?\n")
            print("1. Área de interesse")
            print("2. Nível de formação")
            print("3. Email")
            print("4. Voltar")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                nova_area = input("Nova área de interesse: ").strip()
                self.usuario_logado.atualizar_area_interesse(nova_area)
                print("✓ Área atualizada com sucesso!")
                
            elif opcao == "2":
                novo_nivel = input("Novo nível de formação: ").strip()
                self.usuario_logado.atualizar_nivel_formacao(novo_nivel)
                print("✓ Nível de formação atualizado com sucesso!")
                
            elif opcao == "3":
                novo_email = input("Novo email: ").strip()
                self.usuario_logado.atualizar_email(novo_email)
                print("✓ Email atualizado com sucesso!")
            
        except Exception as e:
            print(f"Erro ao atualizar perfil: {e}")
        
        input("\nPressione ENTER para continuar...")
    
    def alterar_senha(self):
        """Alterar senha do candidato."""
        self.limpar_tela()
        print("\n=== ALTERAR SENHA ===\n")
        
        try:
            senha_atual = input("Digite sua senha atual: ").strip()
            nova_senha = input("Digite sua nova senha: ").strip()
            confirma_senha = input("Confirme a nova senha: ").strip()
            
            if nova_senha != confirma_senha:
                print("✗ As senhas não conferem!")
            else:
                self.usuario_logado.alterar_senha(senha_atual, nova_senha)
                print("✓ Senha alterada com sucesso!")
                
        except ValueError as e:
            print(f"✗ Erro: {e}")
        except Exception as e:
            print(f"Erro ao alterar senha: {e}")
        
        input("\nPressione ENTER para continuar...")
    
    def executar(self):
        """Executa o fluxo principal da aplicação."""
        while True:
            opcao = self.exibir_menu_principal()
            
            if opcao == "1":
                self.fluxo_empresa()
            elif opcao == "2":
                self.fluxo_candidato()
            elif opcao == "3":
                self.limpar_tela()
                print("\n=== OBRIGADO POR USAR SKILLUP ===\n")
                print("Até logo!")
                break
            else:
                print("Opção inválida! Tente novamente.")
                input("Pressione ENTER para continuar...")


def main():
    """Função principal que inicia a aplicação."""
    menu = Menu()
    menu.executar()


if __name__ == "__main__":
    main()
