"""
Fluxo de Empresa - Gerencia a navegação e ações da empresa na plataforma
"""

import os
from datetime import date
from typing import Optional
from src.dominio.empresa import Empresa
from src.dominio.vaga import Modalidade, TipoVaga
from src.dominio.requisitos_vaga import TipoVagaRequisito
from src.services.services_empresa import EmpresaService
from src.services.service_vaga_clt import VagaCLTService
from src.services.service_vaga_estagio import VagaEstagioService
from src.services.service_requisito_vaga import RequisitoVagaService
from src.services.service_candidatura import CandidaturaService
from src.services.service_competencia import CompetenciaService


class FluxoEmpresa:
    """Orquestra o fluxo completo de empresas na plataforma"""

    def __init__(
        self,
        service_empresa: EmpresaService,
        service_vaga_clt: Optional[VagaCLTService] = None,
        service_vaga_estagio: Optional[VagaEstagioService] = None,
        service_requisito_vaga: Optional[RequisitoVagaService] = None,
        service_candidatura: Optional[CandidaturaService] = None,
        service_competencia: Optional[CompetenciaService] = None,
    ):
        """
        Inicializa o fluxo de empresa
        
        Args:
            service_empresa: Serviço de empresas
            service_vaga_clt: Serviço de vagas CLT
            service_vaga_estagio: Serviço de vagas de estágio
            service_requisito_vaga: Serviço de requisitos de vagas
            service_candidatura: Serviço de candidaturas
            service_competencia: Serviço de competências
        """
        self.service = service_empresa
        self.service_vaga_clt = service_vaga_clt
        self.service_vaga_estagio = service_vaga_estagio
        self.service_requisito_vaga = service_requisito_vaga
        self.service_candidatura = service_candidatura
        self.service_competencia = service_competencia
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
        """Menu para publicar nova vaga CLT"""
        if not self.service_vaga_clt:
            self._limpar_tela()
            print("\n❌ Serviço de vagas não disponível")
            input("Pressione ENTER para voltar...")
            return

        self._limpar_tela()
        print("\n=== PUBLICAR VAGA DE EMPREGO ===\n")

        try:
            titulo = input("Título da vaga: ").strip()
            descricao = input("Descrição: ").strip()
            area = input("Área (ex: TI, RH, Financeiro): ").strip()
            
            print("\nModalidade:")
            print("  1. Presencial")
            print("  2. Remoto")
            print("  3. Híbrido")
            opt_mod = input("Escolha (1-3): ").strip()
            modalidades = {"1": Modalidade.PRESENCIAL, "2": Modalidade.REMOTO, "3": Modalidade.HIBRIDO}
            modalidade = modalidades.get(opt_mod, Modalidade.PRESENCIAL)
            
            print("\nTipo da vaga:")
            print("  1. Emprego")
            print("  2. Estágio")
            print("  3. Trainee")
            opt_tipo = input("Escolha (1-3): ").strip()
            tipos = {"1": TipoVaga.EMPREGO, "2": TipoVaga.ESTAGIO, "3": TipoVaga.TRAINEE}
            tipo = tipos.get(opt_tipo, TipoVaga.EMPREGO)
            
            salario = float(input("Salário base: R$ ").strip())
            localidade = input("Localidade (cidade): ").strip()
            
            prazo_str = input("Prazo de inscrição (AAAA-MM-DD) ou ENTER para sem prazo: ").strip()
            prazo = date.fromisoformat(prazo_str) if prazo_str else None

            vaga = self.service_vaga_clt.cadastrar(
                id_empresa=self.empresa_logada.id,
                titulo=titulo,
                descricao=descricao,
                area=area,
                modalidade=modalidade,
                tipo=tipo,
                salario_base=salario,
                localidade=localidade,
                prazo_inscricao=prazo,
            )

            self._limpar_tela()
            print(f"\n✅ Vaga publicada com sucesso!")
            print(f"ID da vaga: {vaga.id}")
            print(f"Título: {vaga.titulo}")
            
            # Adicionar requisitos
            add_req = input("\nDeseja adicionar requisitos? (s/n): ").strip().lower()
            while add_req == "s" and self.service_requisito_vaga and self.service_competencia:
                self._adicionar_requisito_vaga(vaga.id, TipoVagaRequisito.CLT)
                add_req = input("\nAdicionar outro requisito? (s/n): ").strip().lower()
            
            input("\nPressione ENTER para voltar ao menu...")

        except ValueError as e:
            self._limpar_tela()
            print(f"\n❌ Erro de validação: {e}")
            input("Pressione ENTER para voltar...")
        except Exception as e:
            self._limpar_tela()
            print(f"\n❌ Erro ao publicar vaga: {e}")
            input("Pressione ENTER para voltar...")

    def _adicionar_requisito_vaga(self, id_vaga: int, tipo_vaga: TipoVagaRequisito) -> None:
        """Adiciona requisito de competência a uma vaga"""
        try:
            competencias = self.service_competencia.listar_todos()
            if not competencias:
                print("\n⚠️  Nenhuma competência cadastrada no sistema.")
                return
            
            print("\n--- Competências disponíveis ---")
            for c in competencias:
                print(f"  {c.id}. {c.nome}")
            
            id_comp = int(input("ID da competência: ").strip())
            print("\nNível mínimo:")
            print("  1. Iniciante")
            print("  2. Intermediário")
            print("  3. Avançado")
            opt_nivel = input("Escolha (1-3): ").strip()
            niveis = {"1": "iniciante", "2": "intermediario", "3": "avancado"}
            nivel = niveis.get(opt_nivel, "iniciante")
            
            obrigatorio = input("Requisito obrigatório? (s/n): ").strip().lower() == "s"
            
            self.service_requisito_vaga.cadastrar(
                id_vaga=id_vaga,
                id_competencia=id_comp,
                nivel_minimo=nivel,
                tipo_vaga=tipo_vaga,
                obrigatorio=obrigatorio,
            )
            print("✅ Requisito adicionado!")
        except Exception as e:
            print(f"❌ Erro ao adicionar requisito: {e}")

    def _publicar_curso(self) -> None:
        """Informa que empresas não publicam cursos diretamente"""
        self._limpar_tela()
        print("\n=== PUBLICAR CURSO ===\n")
        print("ℹ️  Empresas podem oferecer vagas vinculadas a cursos,")
        print("   mas a publicação de cursos é feita por Instituições de Ensino.")
        print("\n   Para requisitar cursos em vagas, use 'Gerenciar Vagas'.")
        input("\nPressione ENTER para voltar...")

    def _gerenciar_vagas(self) -> None:
        """Menu para gerenciar vagas publicadas"""
        if not self.service_vaga_clt:
            self._limpar_tela()
            print("\n❌ Serviço de vagas não disponível")
            input("Pressione ENTER para voltar...")
            return

        while True:
            self._limpar_tela()
            print("\n=== GERENCIAR VAGAS ===\n")
            print("1. Listar minhas vagas")
            print("2. Ver detalhes de uma vaga")
            print("3. Pausar/Ativar vaga")
            print("4. Adicionar requisito")
            print("5. Voltar")
            
            opcao = input("\nEscolha uma opção (1-5): ").strip()
            
            if opcao == "1":
                self._listar_vagas_empresa()
            elif opcao == "2":
                self._ver_detalhes_vaga()
            elif opcao == "3":
                self._pausar_ativar_vaga()
            elif opcao == "4":
                self._adicionar_requisito_existente()
            elif opcao == "5":
                break
            else:
                print("❌ Opção inválida!")
                input("Pressione ENTER...")

    def _listar_vagas_empresa(self) -> None:
        """Lista todas as vagas da empresa logada"""
        vagas = self.service_vaga_clt.listar_por_empresa(self.empresa_logada.id)
        
        if not vagas:
            print("\n📋 Nenhuma vaga publicada ainda.")
        else:
            print(f"\n📋 Suas vagas ({len(vagas)}):\n")
            for v in vagas:
                status = "🟢 Ativa" if v.ativa else "🔴 Pausada"
                print(f"  [{v.id}] {v.titulo} - {v.area} | {status}")
        input("\nPressione ENTER para continuar...")

    def _ver_detalhes_vaga(self) -> None:
        """Exibe detalhes de uma vaga específica"""
        try:
            id_vaga = int(input("\nID da vaga: ").strip())
            vaga = self.service_vaga_clt.buscar_por_id(id_vaga)
            
            if vaga.id_empresa != self.empresa_logada.id:
                print("❌ Esta vaga não pertence à sua empresa.")
            else:
                print(f"\n{'='*50}")
                print(f"Título: {vaga.titulo}")
                print(f"Descrição: {vaga.descricao}")
                print(f"Área: {vaga.area}")
                print(f"Modalidade: {vaga.modalidade.value}")
                print(f"Tipo: {vaga.tipo.value}")
                print(f"Salário: R$ {vaga.salario_base:.2f}")
                print(f"Localidade: {vaga.localidade}")
                print(f"Status: {'Ativa' if vaga.ativa else 'Pausada'}")
                
                if self.service_requisito_vaga:
                    requisitos = self.service_requisito_vaga.listar_por_vaga(id_vaga)
                    if requisitos:
                        print(f"\nRequisitos ({len(requisitos)}):")
                        for r in requisitos:
                            obr = "Obrigatório" if r.obrigatorio else "Desejável"
                            print(f"  • Competência {r.id_competencia} - {r.nivel_minimo} ({obr})")
        except ValueError as e:
            print(f"❌ Erro: {e}")
        input("\nPressione ENTER para continuar...")

    def _pausar_ativar_vaga(self) -> None:
        """Pausa ou ativa uma vaga"""
        try:
            id_vaga = int(input("\nID da vaga: ").strip())
            vaga = self.service_vaga_clt.buscar_por_id(id_vaga)
            
            if vaga.id_empresa != self.empresa_logada.id:
                print("❌ Esta vaga não pertence à sua empresa.")
            else:
                if vaga.ativa:
                    self.service_vaga_clt.pausar(id_vaga)
                    print("✅ Vaga pausada com sucesso!")
                else:
                    self.service_vaga_clt.publicar(id_vaga)
                    print("✅ Vaga ativada com sucesso!")
        except ValueError as e:
            print(f"❌ Erro: {e}")
        input("\nPressione ENTER para continuar...")

    def _adicionar_requisito_existente(self) -> None:
        """Adiciona requisito a uma vaga existente"""
        if not self.service_requisito_vaga or not self.service_competencia:
            print("❌ Serviços de requisitos/competências não disponíveis")
            input("Pressione ENTER...")
            return
        
        try:
            id_vaga = int(input("\nID da vaga: ").strip())
            vaga = self.service_vaga_clt.buscar_por_id(id_vaga)
            
            if vaga.id_empresa != self.empresa_logada.id:
                print("❌ Esta vaga não pertence à sua empresa.")
            else:
                self._adicionar_requisito_vaga(id_vaga, TipoVagaRequisito.CLT)
        except ValueError as e:
            print(f"❌ Erro: {e}")
        input("\nPressione ENTER para continuar...")

    def _gerenciar_cursos(self) -> None:
        """Informa sobre gerenciamento de cursos"""
        self._limpar_tela()
        print("\n=== GERENCIAR CURSOS ===\n")
        print("ℹ️  A publicação e gestão de cursos é feita por Instituições de Ensino.")
        print("\n   Para vincular cursos como requisitos de vagas:")
        print("   1. Acesse 'Gerenciar Vagas'")
        print("   2. Adicione requisitos de competências")
        print("   3. Candidatos podem buscar cursos que desenvolvam essas competências")
        input("\nPressione ENTER para voltar...")

    def _ver_candidaturas(self) -> None:
        """Menu para ver candidaturas recebidas"""
        if not self.service_candidatura or not self.service_vaga_clt:
            self._limpar_tela()
            print("\n❌ Serviço de candidaturas não disponível")
            input("Pressione ENTER para voltar...")
            return

        while True:
            self._limpar_tela()
            print("\n=== CANDIDATURAS RECEBIDAS ===\n")
            print("1. Listar candidaturas por vaga")
            print("2. Ver detalhes de candidatura")
            print("3. Aprovar candidatura")
            print("4. Reprovar candidatura")
            print("5. Voltar")
            
            opcao = input("\nEscolha uma opção (1-5): ").strip()
            
            if opcao == "1":
                self._listar_candidaturas_por_vaga()
            elif opcao == "2":
                self._ver_detalhes_candidatura()
            elif opcao == "3":
                self._aprovar_candidatura()
            elif opcao == "4":
                self._reprovar_candidatura()
            elif opcao == "5":
                break
            else:
                print("❌ Opção inválida!")
                input("Pressione ENTER...")

    def _listar_candidaturas_por_vaga(self) -> None:
        """Lista candidaturas de uma vaga específica"""
        try:
            # Primeiro mostra as vagas da empresa
            vagas = self.service_vaga_clt.listar_por_empresa(self.empresa_logada.id)
            if not vagas:
                print("\n📋 Nenhuma vaga publicada.")
                input("\nPressione ENTER...")
                return
            
            print("\n📋 Suas vagas:")
            for v in vagas:
                print(f"  [{v.id}] {v.titulo}")
            
            id_vaga = int(input("\nID da vaga: ").strip())
            vaga = self.service_vaga_clt.buscar_por_id(id_vaga)
            
            if vaga.id_empresa != self.empresa_logada.id:
                print("❌ Esta vaga não pertence à sua empresa.")
            else:
                candidaturas = self.service_candidatura.listar_por_vaga(id_vaga)
                if not candidaturas:
                    print(f"\n📋 Nenhuma candidatura para '{vaga.titulo}'")
                else:
                    print(f"\n📋 Candidaturas para '{vaga.titulo}' ({len(candidaturas)}):\n")
                    for c in candidaturas:
                        print(f"  [{c.id}] Candidato {c.id_candidato} | Status: {c.status.value}")
        except ValueError as e:
            print(f"❌ Erro: {e}")
        input("\nPressione ENTER para continuar...")

    def _ver_detalhes_candidatura(self) -> None:
        """Exibe detalhes de uma candidatura"""
        try:
            id_cand = int(input("\nID da candidatura: ").strip())
            candidatura = self.service_candidatura.buscar_por_id(id_cand)
            
            print(f"\n{'='*50}")
            print(f"ID Candidatura: {candidatura.id}")
            print(f"ID Vaga: {candidatura.id_vaga}")
            print(f"ID Candidato: {candidatura.id_candidato}")
            print(f"Tipo Vaga: {candidatura.tipo_vaga.value}")
            print(f"Status: {candidatura.status.value}")
            print(f"Data: {candidatura.data_candidatura}")
        except ValueError as e:
            print(f"❌ Erro: {e}")
        input("\nPressione ENTER para continuar...")

    def _aprovar_candidatura(self) -> None:
        """Aprova uma candidatura"""
        try:
            id_cand = int(input("\nID da candidatura a aprovar: ").strip())
            self.service_candidatura.aprovar(id_cand)
            print("✅ Candidatura aprovada com sucesso!")
        except ValueError as e:
            print(f"❌ Erro: {e}")
        input("\nPressione ENTER para continuar...")

    def _reprovar_candidatura(self) -> None:
        """Reprova uma candidatura"""
        try:
            id_cand = int(input("\nID da candidatura a reprovar: ").strip())
            self.service_candidatura.reprovar(id_cand)
            print("✅ Candidatura reprovada.")
        except ValueError as e:
            print(f"❌ Erro: {e}")
        input("\nPressione ENTER para continuar...")

    def _ver_perfil(self) -> None:
        """Menu de gerenciamento do perfil da empresa"""
        while True:
            self._limpar_tela()
            print("\n=== PERFIL DA EMPRESA ===\n")
            print(f"ID: {self.empresa_logada.id}")
            print(f"Nome: {self.empresa_logada.nome}")
            print(f"CNPJ: {self.empresa_logada.cnpj}")
            print(f"Porte: {self.empresa_logada.porte}")
            print(f"Limite de publicações: {self.empresa_logada.obter_limites_publicacao()}")
            print("\n" + "-" * 40)
            print("\n1. Editar perfil")
            print("2. Excluir conta")
            print("3. Voltar")
            
            opcao = input("\nEscolha (1-3): ").strip()
            
            if opcao == "1":
                self._editar_perfil()
            elif opcao == "2":
                if self._excluir_conta():
                    return
            elif opcao == "3":
                break

    def _editar_perfil(self) -> None:
        """Edita dados do perfil da empresa"""
        self._limpar_tela()
        print("\n=== EDITAR PERFIL ===\n")
        print("Qual campo deseja editar?")
        print("1. Nome")
        print("2. Porte")
        print("3. Voltar")
        
        opcao = input("\nEscolha (1-3): ").strip()
        
        try:
            if opcao == "1":
                novo_nome = input("Novo nome: ").strip()
                self.service.atualizar(self.empresa_logada.id, "nome", novo_nome)
                self.empresa_logada.nome = novo_nome
                print("\n✅ Nome atualizado!")
            elif opcao == "2":
                print("\nPortes disponíveis:")
                print("1. Pequeno")
                print("2. Médio")
                print("3. Grande")
                porte_op = input("Escolha (1-3): ").strip()
                portes = {"1": "pequeno", "2": "medio", "3": "grande"}
                novo_porte = portes.get(porte_op)
                if novo_porte:
                    self.service.atualizar(self.empresa_logada.id, "porte", novo_porte)
                    self.empresa_logada.porte = novo_porte
                    print("\n✅ Porte atualizado!")
                else:
                    print("\n❌ Opção inválida")
            elif opcao == "3":
                return
        except Exception as e:
            print(f"\n❌ Erro ao atualizar: {e}")
        
        input("\nPressione ENTER para continuar...")

    def _excluir_conta(self) -> bool:
        """Exclui a conta da empresa"""
        self._limpar_tela()
        print("\n=== EXCLUIR CONTA ===\n")
        print("⚠️  ATENÇÃO: Esta ação é irreversível!")
        print("Todos os seus dados e vagas publicadas serão removidos.\n")
        
        confirma = input("Digite 'CONFIRMAR' para excluir sua conta: ").strip()
        
        if confirma == "CONFIRMAR":
            try:
                self.service.deletar(self.empresa_logada.id)
                print("\n✅ Conta excluída com sucesso.")
                print("Você será redirecionado para a tela inicial.")
                input("\nPressione ENTER para continuar...")
                self.empresa_logada = None
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