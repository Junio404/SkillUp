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
from src.services.service_competencia_candidato import CompetenciaCandidatoService
from src.services.service_competencia import CompetenciaService
from src.services.service_recomendacao import RecomendacaoService


class FluxoCandidato:
    """Orquestra o fluxo completo de candidatos na plataforma"""

    def __init__(
        self,
        service_candidato: CandidatoService,
        motor_busca_vagas: MotorBuscaVaga,
        service_candidatura: CandidaturaService,
        service_inscricao_curso: InscricaoCursoService,
        service_curso_ead: CursoEADService,
        service_curso_presencial: CursoPresencialService,
        service_competencia_candidato: Optional[CompetenciaCandidatoService] = None,
        service_competencia: Optional[CompetenciaService] = None,
        service_recomendacao: Optional[RecomendacaoService] = None,
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
        self.service_competencia_candidato = service_competencia_candidato
        self.service_competencia = service_competencia
        self.service_recomendacao = service_recomendacao

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
            5: self._gerenciar_competencias,
            6: self._ver_recomendacoes,
            7: self._ver_perfil,
            8: lambda: None  # Sair
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
        print("5. Minhas Competências")
        print("6. Recomendações para Mim")
        print("7. Perfil")
        print("8. Sair")
        print("\n" + "-" * 60)

        opcao = input("Digite a opção desejada (1-8): ").strip()
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
                    from src.dominio.candidatura import TipoVagaCandidatura
                    id_vaga = int(escolha)
                    # Por padrão, vagas listadas são CLT
                    self.service_candidatura.cadastrar(id_vaga, TipoVagaCandidatura.CLT, self.candidato_logado.id)
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
        from src.dominio.inscricao_curso import TipoCursoInscricao
        
        cursos_ead = self.service_curso_ead.repo.listar_todos()
        cursos_pres = self.service_curso_presencial.repo.listar_todos()
        
        # Mapeia ID -> tipo do curso
        cursos_por_id = {}
        for c in cursos_ead:
            cursos_por_id[(c.id, TipoCursoInscricao.EAD)] = c
        for c in cursos_pres:
            cursos_por_id[(c.id, TipoCursoInscricao.PRESENCIAL)] = c
        
        todos_cursos = cursos_ead + cursos_pres

        if not todos_cursos:
            print("Nenhum curso disponível no momento.")
        else:
            for c in cursos_ead:
                print(f"ID: {c.id} | {c.nome} (EAD)")
                print(f"   Área: {c.area} | Carga: {c.carga_horaria}h")
                print("-" * 40)
            for c in cursos_pres:
                print(f"ID: {c.id} | {c.nome} (Presencial)")
                print(f"   Área: {c.area} | Carga: {c.carga_horaria}h")
                print("-" * 40)

            escolha = input("\nDigite o ID do curso para se inscrever (ou ENTER para voltar): ").strip()
            if escolha:
                try:
                    id_curso = int(escolha)
                    # Determina o tipo do curso pelo ID
                    tipo_curso = None
                    if any(c.id == id_curso for c in cursos_ead):
                        tipo_curso = TipoCursoInscricao.EAD
                    elif any(c.id == id_curso for c in cursos_pres):
                        tipo_curso = TipoCursoInscricao.PRESENCIAL
                    else:
                        raise ValueError("Curso não encontrado.")
                    
                    self.service_inscricao_curso.inscrever(self.candidato_logado.id, id_curso, tipo_curso)
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

    def _gerenciar_competencias(self) -> None:
        """Menu para gerenciar competências do candidato"""
        while True:
            self._limpar_tela()
            print("\n=== MINHAS COMPETÊNCIAS ===")
            print("\n1. Listar minhas competências")
            print("2. Adicionar competência")
            print("3. Atualizar nível de competência")
            print("4. Remover competência")
            print("5. Voltar")
            
            opcao = input("\nEscolha (1-5): ").strip()
            
            if opcao == "1":
                self._listar_competencias_candidato()
            elif opcao == "2":
                self._adicionar_competencia()
            elif opcao == "3":
                self._atualizar_nivel_competencia()
            elif opcao == "4":
                self._remover_competencia()
            elif opcao == "5":
                break

    def _listar_competencias_candidato(self) -> None:
        """Lista competências do candidato logado"""
        if not self.service_competencia_candidato:
            print("\n❌ Serviço de competências não disponível")
            input("Pressione ENTER...")
            return
        
        self._limpar_tela()
        print("\n=== MINHAS COMPETÊNCIAS ===")
        
        try:
            competencias = self.service_competencia_candidato.listar_por_candidato(self.candidato_logado.id)
            if not competencias:
                print("\nVocê ainda não possui competências cadastradas.")
            else:
                for c in competencias:
                    print(f"\n  ID: {c.id} | Competência ID: {c.id_competencia} | Nível: {c.nivel_atual}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        input("\nPressione ENTER para voltar...")

    def _adicionar_competencia(self) -> None:
        """Adiciona uma nova competência ao candidato"""
        if not self.service_competencia_candidato or not self.service_competencia:
            print("\n❌ Serviços não disponíveis")
            input("Pressione ENTER...")
            return
        
        self._limpar_tela()
        print("\n=== ADICIONAR COMPETÊNCIA ===")
        
        try:
            competencias = self.service_competencia.listar_todos()
            if not competencias:
                print("\n⚠️ Nenhuma competência disponível no sistema.")
                input("Pressione ENTER...")
                return
            
            print("\n--- Competências disponíveis ---")
            for c in competencias:
                print(f"  {c.id}. {c.nome}")
            
            id_comp = int(input("\nID da competência: ").strip())
            print("\nNível atual:")
            print("  1. Iniciante")
            print("  2. Intermediário")
            print("  3. Avançado")
            opt_nivel = input("Escolha (1-3): ").strip()
            niveis = {"1": "iniciante", "2": "intermediario", "3": "avancado"}
            nivel = niveis.get(opt_nivel, "iniciante")
            
            self.service_competencia_candidato.cadastrar(
                id_candidato=self.candidato_logado.id,
                id_competencia=id_comp,
                nivel_atual=nivel
            )
            print("\n✅ Competência adicionada com sucesso!")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        input("Pressione ENTER para continuar...")

    def _atualizar_nivel_competencia(self) -> None:
        """Atualiza nível de uma competência"""
        if not self.service_competencia_candidato:
            print("\n❌ Serviço não disponível")
            input("Pressione ENTER...")
            return
        
        try:
            competencias = self.service_competencia_candidato.listar_por_candidato(self.candidato_logado.id)
            if not competencias:
                print("\nVocê não possui competências cadastradas.")
                input("Pressione ENTER...")
                return
            
            print("\n--- Suas competências ---")
            for c in competencias:
                print(f"  ID: {c.id} | Comp. ID: {c.id_competencia} | Nível: {c.nivel_atual}")
            
            id_comp_cand = int(input("\nID da competência a atualizar: ").strip())
            print("\nNovo nível:")
            print("  1. Iniciante")
            print("  2. Intermediário")
            print("  3. Avançado")
            opt_nivel = input("Escolha (1-3): ").strip()
            niveis = {"1": "iniciante", "2": "intermediario", "3": "avancado"}
            nivel = niveis.get(opt_nivel, "iniciante")
            
            self.service_competencia_candidato.atualizar_nivel(id_comp_cand, nivel)
            print("\n✅ Nível atualizado com sucesso!")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        input("Pressione ENTER para continuar...")

    def _remover_competencia(self) -> None:
        """Remove uma competência do candidato"""
        if not self.service_competencia_candidato:
            print("\n❌ Serviço não disponível")
            input("Pressione ENTER...")
            return
        
        try:
            competencias = self.service_competencia_candidato.listar_por_candidato(self.candidato_logado.id)
            if not competencias:
                print("\nVocê não possui competências cadastradas.")
                input("Pressione ENTER...")
                return
            
            print("\n--- Suas competências ---")
            for c in competencias:
                print(f"  ID: {c.id} | Comp. ID: {c.id_competencia} | Nível: {c.nivel_atual}")
            
            id_comp_cand = int(input("\nID da competência a remover: ").strip())
            self.service_competencia_candidato.remover(id_comp_cand)
            print("\n✅ Competência removida com sucesso!")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        input("Pressione ENTER para continuar...")

    def _ver_recomendacoes(self) -> None:
        """Exibe recomendações de vagas e cursos para o candidato"""
        if not self.service_recomendacao:
            self._limpar_tela()
            print("\n=== RECOMENDAÇÕES ===")
            print("\n❌ Serviço de recomendações não disponível")
            input("Pressione ENTER para voltar...")
            return
        
        self._limpar_tela()
        print("\n=== RECOMENDAÇÕES PARA VOCÊ ===")
        
        try:
            recomendacao = self.service_recomendacao.recomendar(self.candidato_logado)
            
            print("\n--- VAGAS RECOMENDADAS ---")
            if not recomendacao.vagas:
                print("  Nenhuma vaga recomendada no momento.")
            else:
                for item in recomendacao.vagas[:10]:  # Top 10
                    vaga = item.item
                    print(f"\n  [⭐ {item.pontuacao}pts] {vaga.titulo}")
                    print(f"     Área: {vaga.area} | Modalidade: {vaga.modalidade.value}")
            
            print("\n--- CURSOS RECOMENDADOS ---")
            if not recomendacao.cursos:
                print("  Nenhum curso recomendado no momento.")
            else:
                for item in recomendacao.cursos[:10]:  # Top 10
                    curso = item.item
                    print(f"\n  [⭐ {item.pontuacao}pts] {curso.nome}")
                    print(f"     Área: {curso.area} | Carga: {curso.carga_horaria}h")
        except Exception as e:
            print(f"\n❌ Erro ao obter recomendações: {e}")
        
        input("\nPressione ENTER para voltar...")

    def _ver_perfil(self) -> None:
        """Menu de gerenciamento do perfil do candidato"""
        while True:
            self._limpar_tela()
            print("\n=== MEU PERFIL ===\n")
            print(f"ID: {self.candidato_logado.id}")
            print(f"Nome: {self.candidato_logado.nome}")
            print(f"Email: {self.candidato_logado.email}")
            print(f"Áreas de Interesse: {', '.join(self.candidato_logado._areas_interesse)}")
            print(f"Nível de Formação: {self.candidato_logado.nivel_formacao}")
            print("\n" + "-" * 40)
            print("\n1. Editar perfil")
            print("2. Excluir conta")
            print("3. Voltar")
            
            opcao = input("\nEscolha (1-3): ").strip()
            
            if opcao == "1":
                self._editar_perfil()
            elif opcao == "2":
                if self._excluir_conta():
                    return  # Sai do loop se a conta foi excluída
            elif opcao == "3":
                break

    def _editar_perfil(self) -> None:
        """Edita dados do perfil do candidato"""
        self._limpar_tela()
        print("\n=== EDITAR PERFIL ===\n")
        print("Qual campo deseja editar?")
        print("1. Nome")
        print("2. Email")
        print("3. Áreas de Interesse")
        print("4. Nível de Formação")
        print("5. Voltar")
        
        opcao = input("\nEscolha (1-5): ").strip()
        
        try:
            if opcao == "1":
                novo_nome = input("Novo nome: ").strip()
                self.service.atualizar(self.candidato_logado.id, "nome", novo_nome)
                self.candidato_logado.nome = novo_nome
                print("\n✅ Nome atualizado!")
            elif opcao == "2":
                novo_email = input("Novo email: ").strip()
                self.service.atualizar(self.candidato_logado.id, "email", novo_email)
                self.candidato_logado.email = novo_email
                print("\n✅ Email atualizado!")
            elif opcao == "3":
                novas_areas = input("Novas áreas de interesse (separadas por vírgula): ").strip()
                areas_lista = [a.strip() for a in novas_areas.split(",")]
                self.service.atualizar(self.candidato_logado.id, "areas_interesse", areas_lista)
                self.candidato_logado._areas_interesse = areas_lista
                print("\n✅ Áreas de interesse atualizadas!")
            elif opcao == "4":
                print("\nNíveis disponíveis:")
                print("1. Ensino Médio")
                print("2. Técnico")
                print("3. Graduação")
                print("4. Pós-graduação")
                print("5. Mestrado")
                print("6. Doutorado")
                nivel_op = input("Escolha (1-6): ").strip()
                niveis = {"1": "Ensino Médio", "2": "Técnico", "3": "Graduação", 
                          "4": "Pós-graduação", "5": "Mestrado", "6": "Doutorado"}
                novo_nivel = niveis.get(nivel_op)
                if novo_nivel:
                    self.service.atualizar(self.candidato_logado.id, "nivel_formacao", novo_nivel)
                    self.candidato_logado.nivel_formacao = novo_nivel
                    print("\n✅ Nível de formação atualizado!")
                else:
                    print("\n❌ Opção inválida")
            elif opcao == "5":
                return
        except Exception as e:
            print(f"\n❌ Erro ao atualizar: {e}")
        
        input("\nPressione ENTER para continuar...")

    def _excluir_conta(self) -> bool:
        """Exclui a conta do candidato"""
        self._limpar_tela()
        print("\n=== EXCLUIR CONTA ===\n")
        print("⚠️  ATENÇÃO: Esta ação é irreversível!")
        print("Todos os seus dados, candidaturas e inscrições serão removidos.\n")
        
        confirma = input("Digite 'CONFIRMAR' para excluir sua conta: ").strip()
        
        if confirma == "CONFIRMAR":
            try:
                self.service.deletar(self.candidato_logado.id)
                print("\n✅ Conta excluída com sucesso.")
                print("Você será redirecionado para a tela inicial.")
                input("\nPressione ENTER para continuar...")
                self.candidato_logado = None
                return True
            except Exception as e:
                print(f"\n❌ Erro ao excluir conta: {e}")
                input("\nPressione ENTER para voltar...")
        else:
            print("\n❌ Exclusão cancelada.")
            input("\nPressione ENTER para voltar...")
        
        return False

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
                if opcao_num == 8:
                    return False
                return True
            else:
                self._limpar_tela()
                print("\n❌ Opção inválida! Digite um número entre 1 e 8.")
                input("Pressione ENTER para continuar...")
                return True

        except ValueError:
            self._limpar_tela()
            print("\n❌ Entrada inválida! Digite um número entre 1 e 8.")
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