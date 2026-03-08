"""
Fluxo de Candidato - Gerencia a navegação e ações do candidato na plataforma
"""

import os
from typing import Optional, List
from src.dominio.candidato import Candidato
from src.dominio.vaga import Modalidade
from src.services.service_candidato import CandidatoService
from src.services.service_busca_vaga import MotorBuscaVaga
from src.services.service_candidatura import CandidaturaService
from src.services.service_inscricao_curso import InscricaoCursoService
from src.services.service_curso_ead import CursoEADService
from src.services.service_curso_presencial import CursoPresencialService


class FluxoCandidato:
    """Orquestra o fluxo completo de candidatos na plataforma"""

    def __init__(
        self,
        service_candidato: CandidatoService,
        motor_busca_vagas: MotorBuscaVaga,
        service_candidatura: CandidaturaService,
        service_inscricao_curso: InscricaoCursoService,
        service_curso_ead: CursoEADService,
        service_curso_presencial: CursoPresencialService
    ):
        """
        Inicializa o fluxo de candidato com todos os serviços necessários
        """
        self.service = service_candidato
        self.motor_busca_vagas = motor_busca_vagas
        self.service_candidatura = service_candidatura
        self.service_inscricao_curso = service_inscricao_curso
        self.service_curso_ead = service_curso_ead
        self.service_curso_presencial = service_curso_presencial

        self.candidato_logado: Optional[Candidato] = None
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
        print("         CANDIDATO - AUTENTICAÇÃO".center(60))
        print("=" * 60)
        print("\n1. Login")
        print("2. Cadastro")
        print("3. Voltar")
        print("\n" + "-" * 60)

        opcao = input("Digite a opção desejada (1-3): ").strip()
        return opcao

    def _login(self) -> None:
        """Fluxo de login de candidato"""
        self._limpar_tela()
        print("\n=== LOGIN DE CANDIDATO ===\n")

        try:
            id_candidato = int(input("Digite seu ID: ").strip())
            candidato = self.service.buscar_por_id(id_candidato)
            self.candidato_logado = candidato
            self._limpar_tela()
            print(f"\n✅ Login realizado com sucesso!")
            print(f"Bem-vindo, {candidato.nome}!\n")
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
        """Fluxo de cadastro de novo candidato"""
        self._limpar_tela()
        print("\n=== CADASTRO DE CANDIDATO ===\n")

        try:
            nome = input("Nome completo: ").strip()
            cpf = input("CPF (11 dígitos): ").strip()
            email = input("Email: ").strip()
            areas = input("Áreas de interesse (separadas por vírgula): ").strip().split(",")
            areas = [a.strip() for a in areas]
            nivel = input("Nível de formação: ").strip()
            localidade = input("Localidade (Cidade/UF): ").strip()

            candidato = self.service.cadastrar(
                nome=nome,
                cpf=cpf,
                email=email,
                areas_interesse=areas,
                nivel_formacao=nivel,
                localidade=localidade
            )

            self.candidato_logado = candidato
            self._limpar_tela()
            print(f"\n✅ Cadastro realizado com sucesso!")
            print(f"Seu ID é: {candidato.id}")
            print(f"Bem-vindo, {candidato.nome}!\n")
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
                if self.candidato_logado:
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
    # MENU PRINCIPAL DO CANDIDATO
    # ==========================

    def _construir_acoes_menu_principal(self) -> dict:
        """Constrói o dicionário de ações do menu principal"""
        return {
            1: self._explorar_vagas,
            2: self._explorar_cursos,
            3: self._gerenciar_candidaturas,
            4: self._gerenciar_inscricoes_cursos,
            5: self._ver_perfil,
            6: lambda: None  # Voltar
        }

    def _exibir_menu_principal(self) -> str:
        """Exibe o menu principal do candidato"""
        self._limpar_tela()
        print("=" * 60)
        print(f"         BEM-VINDO, {self.candidato_logado.nome.upper()}".center(60))
        print("=" * 60)
        print("\n1. Explorar Vagas")
        print("2. Explorar Cursos")
        print("3. Minhas Candidaturas")
        print("4. Minhas Inscrições em Cursos")
        print("5. Perfil")
        print("6. Sair")
        print("\n" + "-" * 60)

        opcao = input("Digite a opção desejada (1-6): ").strip()
        return opcao

    def _explorar_vagas(self) -> None:
        self._limpar_tela()
        print("\n=== VAGAS RECOMENDADAS ===\n")
        
        # Busca vagas compatíveis
        vagas = self.motor_busca_vagas.buscar_por_candidato(
            areas_interesse=self.candidato_logado._areas_interesse,
            localidade_candidato=self.candidato_logado.localidade
        )

        if not vagas:
            print("Nenhuma vaga encontrada para o seu perfil no momento.")
        else:
            print(f"Encontramos {len(vagas)} vagas para você:\n")
            for v in vagas:
                empresa_nome = v.empresa_nome if hasattr(v, 'empresa_nome') else 'Empresa Parceira'
                print(f"ID: {v.id} | {v.titulo} ({v.modalidade.value}) - {empresa_nome}")
                # Verifica se 'salario' existe antes de acessar
                salario = f"R$ {v.salario:.2f}" if hasattr(v, 'salario') else "A combinar"
                print(f"   Salário: {salario} | Área: {v.area}")
                print("-" * 40)
            
            escolha = input("\nDigite o ID da vaga para se candidatar (ou ENTER para voltar): ").strip()
            if escolha:
                try:
                    id_vaga = int(escolha)
                    self.service_candidatura.cadastrar(id_vaga, self.candidato_logado.id)
                    print("✅ Candidatura enviada com sucesso!")
                except Exception as e:
                    print(f"❌ Erro ao candidatar: {e}")
                input("Pressione ENTER para continuar...")
        
        if not vagas:
            input("\nPressione ENTER para voltar...")

    def _explorar_cursos(self) -> None:
        self._limpar_tela()
        print("\n=== CURSOS DISPONÍVEIS ===\n")
        
        # Combinar cursos EAD e Presenciais
        cursos_ead = self.service_curso_ead.repo.listar_todos()
        cursos_pres = self.service_curso_presencial.repo.listar_todos()
        todos_cursos = cursos_ead + cursos_pres

        if not todos_cursos:
            print("Nenhum curso disponível no momento.")
        else:
            for c in todos_cursos:
                modalidade = "EAD" if hasattr(c, 'plataforma_url') else "Presencial"
                print(f"ID: {c.id} | {c.nome} ({modalidade})")
                print(f"   Área: {c.area} | Carga: {c.carga_horaria}h")
                print("-" * 40)

            escolha = input("\nDigite o ID do curso para se inscrever (ou ENTER para voltar): ").strip()
            if escolha:
                try:
                    id_curso = int(escolha)
                    self.service_inscricao_curso.inscrever(self.candidato_logado.id, id_curso)
                    print("✅ Inscrição realizada com sucesso!")
                except Exception as e:
                    print(f"❌ Erro ao inscrever: {e}")
                input("Pressione ENTER para continuar...")
        
        if not todos_cursos:
            input("\nPressione ENTER para voltar...")

    def _gerenciar_candidaturas(self) -> None:
        self._limpar_tela()
        print("\n=== MINHAS CANDIDATURAS ===\n")
        try:
            candidaturas = self.service_candidatura.listar_por_candidato(self.candidato_logado.id)
            if not candidaturas:
                print("Você ainda não se candidatou a nenhuma vaga.")
            else:
                for c in candidaturas:
                    print(f"Candidatura #{c.id} - Vaga ID: {c.id_vaga}")
                    print(f"Status: {c.status.value}")
                    print("-" * 30)
        except Exception as e:
            print(f"Erro ao listar candidaturas: {e}")
        
        input("\nPressione ENTER para voltar...")

    def _gerenciar_inscricoes_cursos(self) -> None:
        self._limpar_tela()
        print("\n=== MINHAS INSCRIÇÕES EM CURSOS ===\n")
        try:
            inscricoes = self.service_inscricao_curso.listar_por_candidato(self.candidato_logado.id)
            if not inscricoes:
                print("Você não possui inscrições em cursos.")
            else:
                for i in inscricoes:
                    print(f"Inscrição #{i.id} - Curso ID: {i.id_curso}")
                    print(f"Data: {i.data_inscricao}") if hasattr(i, 'data_inscricao') else print(f"Data: N/A")
                    print(f"Status: {i.status.value}")
                    print("-" * 30)
        except Exception as e:
            print(f"Erro ao listar inscrições: {e}")
            
        input("\nPressione ENTER para voltar...")

    def _ver_perfil(self) -> None:
        """Exibe o perfil do candidato"""
        self._limpar_tela()
        print("\n=== MEU PERFIL ===\n")
        print(f"ID: {self.candidato_logado.id}")
        print(f"Nome: {self.candidato_logado.nome}")
        print(f"Email: {self.candidato_logado.email}")
        print(f"Áreas de Interesse: {', '.join(self.candidato_logado._areas_interesse)}")
        print(f"Nível de Formação: {self.candidato_logado.nivel_formacao}")
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
        """Executa o fluxo completo do candidato"""
        # Fase 1: Autenticação
        while True:
            opcao = self._exibir_menu_autenticacao()
            if not self._processar_opcao_autenticacao(opcao):
                break

        # Se conseguiu fazer login/cadastro
        if self.candidato_logado:
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