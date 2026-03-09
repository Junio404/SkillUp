"""
Fluxo de Administração de Candidatos (Back Office)
Gerencia candidatos e suas funcionalidades sem necessidade de login
"""

import os
from typing import Optional, List
from src.dominio.candidato import Candidato
from src.dominio.inscricao_curso import StatusInscricao
from src.services.service_candidato import CandidatoService
from src.services.service_candidatura import CandidaturaService
from src.services.service_inscricao_curso import InscricaoCursoService
from src.services.service_curso_ead import CursoEADService
from src.services.service_curso_presencial import CursoPresencialService
from src.services.service_competencia_candidato import CompetenciaCandidatoService
from src.services.service_competencia import CompetenciaService


class FluxoCandidatoAdmin:
    """Back Office para administração de candidatos"""

    def __init__(
        self,
        service_candidato: CandidatoService,
        service_candidatura: CandidaturaService,
        service_inscricao_curso: InscricaoCursoService,
        service_curso_ead: CursoEADService,
        service_curso_presencial: CursoPresencialService,
        service_competencia_candidato: Optional[CompetenciaCandidatoService] = None,
        service_competencia: Optional[CompetenciaService] = None,
    ):
        """Inicializa o back office com todos os serviços necessários"""
        self.service = service_candidato
        self.service_candidatura = service_candidatura
        self.service_inscricao_curso = service_inscricao_curso
        self.service_curso_ead = service_curso_ead
        self.service_curso_presencial = service_curso_presencial
        self.service_competencia_candidato = service_competencia_candidato
        self.service_competencia = service_competencia

        self.candidato_selecionado: Optional[Candidato] = None

    def _limpar_tela(self) -> None:
        """Limpa a tela do console"""
        os.system("clear" if os.name == "posix" else "cls")

    def _pausar(self, mensagem: str = "Pressione ENTER para continuar...") -> None:
        """Pausa a execução aguardando input do usuário"""
        input(mensagem)

    # ==========================
    # MENU PRINCIPAL
    # ==========================

    def _exibir_menu_principal(self) -> str:
        """Exibe o menu principal do back office"""
        self._limpar_tela()
        print("=" * 60)
        print("     SKILLUP - BACK OFFICE DE CANDIDATOS".center(60))
        print("=" * 60)
        print("\n1. Listar Todos os Candidatos")
        print("2. Cadastrar Novo Candidato")
        print("3. Buscar Candidato por ID")
        print("4. Buscar Candidato por CPF")
        print("5. Gerenciar Candidato (Selecionar)")
        print("6. Excluir Candidato")
        print("7. Sair")
        print("\n" + "-" * 60)

        opcao = input("Digite a opção desejada (1-7): ").strip()
        return opcao

    def _processar_opcao_principal(self, opcao: str) -> bool:
        """Processa opção do menu principal. Retorna False para sair."""
        acoes = {
            "1": self._listar_candidatos,
            "2": self._cadastrar_candidato,
            "3": self._buscar_por_id,
            "4": self._buscar_por_cpf,
            "5": self._selecionar_e_gerenciar,
            "6": self._excluir_candidato,
            "7": lambda: None,
        }

        acao = acoes.get(opcao)
        if acao:
            acao()
            return opcao != "7"
        else:
            print("\n❌ Opção inválida!")
            self._pausar()
            return True

    # ==========================
    # CRUD DE CANDIDATOS
    # ==========================

    def _listar_candidatos(self) -> None:
        """Lista todos os candidatos cadastrados"""
        self._limpar_tela()
        print("\n=== TODOS OS CANDIDATOS ===\n")

        try:
            candidatos = self.service.listar_todos()
            if not candidatos:
                print("Nenhum candidato cadastrado.")
            else:
                print(f"Total: {len(candidatos)} candidatos\n")
                for c in candidatos:
                    self._exibir_candidato_resumo(c)

        except Exception as e:
            print(f"Erro ao listar candidatos: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _exibir_candidato_resumo(self, c: Candidato) -> None:
        """Exibe resumo de um candidato"""
        print(f"ID: {c.id} | {c.nome}")
        print(f"   CPF: {c.cpf} | Email: {c.email}")
        print(f"   Localidade: {c.localidade} | Formação: {c.nivel_formacao}")
        print(f"   Áreas: {', '.join(c.areas_interesse)}")
        print("-" * 50)

    def _exibir_candidato_completo(self, c: Candidato) -> None:
        """Exibe dados completos de um candidato"""
        print(f"ID: {c.id}")
        print(f"Nome: {c.nome}")
        print(f"CPF: {c.cpf}")
        print(f"Email: {c.email}")
        print(f"Localidade: {c.localidade}")
        print(f"Nível de Formação: {c.nivel_formacao}")
        print(f"Áreas de Interesse: {', '.join(c.areas_interesse)}")

    def _cadastrar_candidato(self) -> None:
        """Cadastra um novo candidato"""
        self._limpar_tela()
        print("\n=== CADASTRAR NOVO CANDIDATO ===\n")

        try:
            nome = input("Nome completo: ").strip()
            cpf = input("CPF (11 dígitos): ").strip()
            email = input("Email: ").strip()
            areas = input("Áreas de interesse (separadas por vírgula): ").strip().split(",")
            areas = [a.strip() for a in areas if a.strip()]
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

            print(f"\n✅ Candidato cadastrado com sucesso!")
            print(f"ID atribuído: {candidato.id}")

        except ValueError as e:
            print(f"\n❌ Erro de validação: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao cadastrar: {e}")

        self._pausar()

    def _buscar_por_id(self) -> None:
        """Busca candidato por ID"""
        self._limpar_tela()
        print("\n=== BUSCAR CANDIDATO POR ID ===\n")

        try:
            id_candidato = int(input("Digite o ID do candidato: ").strip())
            candidato = self.service.buscar_por_id(id_candidato)

            print("\n" + "=" * 40)
            self._exibir_candidato_completo(candidato)
            print("=" * 40)

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Candidato não encontrado: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _buscar_por_cpf(self) -> None:
        """Busca candidato por CPF"""
        self._limpar_tela()
        print("\n=== BUSCAR CANDIDATO POR CPF ===\n")

        try:
            cpf = input("Digite o CPF (11 dígitos): ").strip()
            candidato = self.service.buscar_por_cpf(cpf)

            if candidato:
                print("\n" + "=" * 40)
                self._exibir_candidato_completo(candidato)
                print("=" * 40)
            else:
                print("\n❌ Candidato não encontrado.")

        except Exception as e:
            print(f"\n❌ Erro ao buscar: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _excluir_candidato(self) -> None:
        """Exclui um candidato"""
        self._limpar_tela()
        print("\n=== EXCLUIR CANDIDATO ===\n")

        try:
            id_candidato = int(input("Digite o ID do candidato a excluir: ").strip())
            candidato = self.service.buscar_por_id(id_candidato)

            print(f"\nCandidato encontrado: {candidato.nome}")
            print("⚠️  Esta ação é irreversível!")

            confirmacao = input("\nDigite 'CONFIRMAR' para excluir: ").strip()

            if confirmacao == "CONFIRMAR":
                self.service.deletar(id_candidato)
                print("\n✅ Candidato excluído com sucesso!")
            else:
                print("\n❌ Exclusão cancelada.")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao excluir: {e}")

        self._pausar()

    # ==========================
    # GERENCIAMENTO DE CANDIDATO
    # ==========================

    def _selecionar_e_gerenciar(self) -> None:
        """Seleciona um candidato e abre menu de gerenciamento"""
        self._limpar_tela()
        print("\n=== SELECIONAR CANDIDATO ===\n")

        try:
            id_candidato = int(input("Digite o ID do candidato: ").strip())
            candidato = self.service.buscar_por_id(id_candidato)
            self.candidato_selecionado = candidato

            print(f"\n✅ Candidato selecionado: {candidato.nome}")
            self._pausar()

            # Menu de gerenciamento
            self._menu_gerenciar_candidato()

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
            self._pausar()
        except Exception as e:
            print(f"\n❌ Candidato não encontrado: {e}")
            self._pausar()

    def _menu_gerenciar_candidato(self) -> None:
        """Menu de gerenciamento do candidato selecionado"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print(f"  GERENCIANDO: {self.candidato_selecionado.nome}".center(60))
            print(f"  (ID: {self.candidato_selecionado.id})".center(60))
            print("=" * 60)
            print("\n1. Ver Dados Completos")
            print("2. Editar Dados")
            print("3. Candidaturas")
            print("4. Inscrições em Cursos")
            print("5. Competências")
            print("6. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Digite a opção desejada (1-6): ").strip()

            if opcao == "1":
                self._ver_dados_candidato()
            elif opcao == "2":
                self._editar_dados_candidato()
            elif opcao == "3":
                self._menu_candidaturas()
            elif opcao == "4":
                self._menu_inscricoes()
            elif opcao == "5":
                self._menu_competencias()
            elif opcao == "6":
                self.candidato_selecionado = None
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _ver_dados_candidato(self) -> None:
        """Exibe dados completos do candidato selecionado"""
        self._limpar_tela()
        print("\n=== DADOS DO CANDIDATO ===\n")
        self._exibir_candidato_completo(self.candidato_selecionado)
        self._pausar("\nPressione ENTER para voltar...")

    def _editar_dados_candidato(self) -> None:
        """Menu para editar dados do candidato"""
        while True:
            self._limpar_tela()
            print("\n=== EDITAR DADOS DO CANDIDATO ===\n")
            print(f"Editando: {self.candidato_selecionado.nome}\n")
            print("1. Nome")
            print("2. Email")
            print("3. Localidade")
            print("4. Nível de Formação")
            print("5. Áreas de Interesse")
            print("6. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Qual campo deseja editar (1-6): ").strip()

            campos = {
                "1": ("nome", "Novo nome"),
                "2": ("email", "Novo email"),
                "3": ("localidade", "Nova localidade"),
                "4": ("nivel_formacao", "Novo nível de formação"),
            }

            if opcao in campos:
                campo, descricao = campos[opcao]
                self._atualizar_campo_candidato(campo, descricao)
            elif opcao == "5":
                self._atualizar_areas_interesse()
            elif opcao == "6":
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _atualizar_campo_candidato(self, campo: str, descricao: str) -> None:
        """Atualiza um campo específico do candidato"""
        try:
            valor_atual = getattr(self.candidato_selecionado, campo, "")
            print(f"\nValor atual: {valor_atual}")
            novo_valor = input(f"{descricao}: ").strip()

            if novo_valor:
                self.service.atualizar(self.candidato_selecionado.id, campo, novo_valor)
                self.candidato_selecionado = self.service.buscar_por_id(self.candidato_selecionado.id)
                print(f"\n✅ {campo.replace('_', ' ').title()} atualizado!")
            else:
                print("\n❌ Valor não pode ser vazio.")

        except ValueError as e:
            print(f"\n❌ Erro de validação: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao atualizar: {e}")

        self._pausar()

    def _atualizar_areas_interesse(self) -> None:
        """Atualiza as áreas de interesse"""
        try:
            print(f"\nÁreas atuais: {', '.join(self.candidato_selecionado.areas_interesse)}")
            novas_areas = input("Novas áreas (separadas por vírgula): ").strip()

            if novas_areas:
                areas = [a.strip() for a in novas_areas.split(",") if a.strip()]
                self.service.atualizar(self.candidato_selecionado.id, "areas_interesse", areas)
                self.candidato_selecionado = self.service.buscar_por_id(self.candidato_selecionado.id)
                print("\n✅ Áreas de interesse atualizadas!")
            else:
                print("\n❌ Valor não pode ser vazio.")

        except ValueError as e:
            print(f"\n❌ Erro de validação: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao atualizar: {e}")

        self._pausar()

    # ==========================
    # MENU DE CANDIDATURAS
    # ==========================

    def _menu_candidaturas(self) -> None:
        """Menu de candidaturas do candidato"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print(f"  CANDIDATURAS - {self.candidato_selecionado.nome}".center(60))
            print("=" * 60)
            print("\n1. Listar Candidaturas")
            print("2. Criar Nova Candidatura")
            print("3. Cancelar Candidatura")
            print("4. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Digite a opção desejada (1-4): ").strip()

            if opcao == "1":
                self._listar_candidaturas()
            elif opcao == "2":
                self._criar_candidatura()
            elif opcao == "3":
                self._cancelar_candidatura()
            elif opcao == "4":
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _listar_candidaturas(self) -> None:
        """Lista candidaturas do candidato"""
        self._limpar_tela()
        print(f"\n=== CANDIDATURAS DE {self.candidato_selecionado.nome} ===\n")

        try:
            candidaturas = self.service_candidatura.listar_por_candidato(self.candidato_selecionado.id)

            if not candidaturas:
                print("Nenhuma candidatura encontrada.")
            else:
                print(f"Total: {len(candidaturas)} candidaturas\n")
                for c in candidaturas:
                    status = c.status.name if hasattr(c.status, 'name') else c.status
                    print(f"ID: {c.id} | Vaga ID: {c.id_vaga}")
                    print(f"   Status: {status}")
                    if hasattr(c, 'data_candidatura') and c.data_candidatura:
                        print(f"   Data: {c.data_candidatura}")
                    print("-" * 40)

        except Exception as e:
            print(f"Erro ao listar: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _criar_candidatura(self) -> None:
        """Cria candidatura para o candidato"""
        self._limpar_tela()
        print("\n=== CRIAR CANDIDATURA ===\n")

        try:
            id_vaga = int(input("Digite o ID da vaga: ").strip())
            self.service_candidatura.cadastrar(id_vaga, self.candidato_selecionado.id)
            print("\n✅ Candidatura criada com sucesso!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao criar: {e}")

        self._pausar()

    def _cancelar_candidatura(self) -> None:
        """Cancela candidatura do candidato"""
        self._limpar_tela()
        print("\n=== CANCELAR CANDIDATURA ===\n")

        try:
            candidaturas = self.service_candidatura.listar_por_candidato(self.candidato_selecionado.id)

            if not candidaturas:
                print("Nenhuma candidatura para cancelar.")
                self._pausar()
                return

            for c in candidaturas:
                status = c.status.name if hasattr(c.status, 'name') else c.status
                print(f"ID: {c.id} | Vaga: {c.id_vaga} | Status: {status}")

            print()
            id_candidatura = int(input("Digite o ID da candidatura a cancelar: ").strip())

            if hasattr(self.service_candidatura, 'cancelar'):
                self.service_candidatura.cancelar(id_candidatura)
            elif hasattr(self.service_candidatura, 'remover'):
                self.service_candidatura.remover(id_candidatura)
            else:
                print("\n❌ Funcionalidade não disponível.")
                self._pausar()
                return

            print("\n✅ Candidatura cancelada!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao cancelar: {e}")

        self._pausar()

    # ==========================
    # MENU DE INSCRIÇÕES
    # ==========================

    def _menu_inscricoes(self) -> None:
        """Menu de inscrições em cursos"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print(f"  INSCRIÇÕES - {self.candidato_selecionado.nome}".center(60))
            print("=" * 60)
            print("\n1. Listar Inscrições")
            print("2. Criar Nova Inscrição")
            print("3. Concluir Curso (Atribuir Competências)")
            print("4. Cancelar Inscrição")
            print("5. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Digite a opção desejada (1-5): ").strip()

            if opcao == "1":
                self._listar_inscricoes()
            elif opcao == "2":
                self._criar_inscricao()
            elif opcao == "3":
                self._concluir_inscricao()
            elif opcao == "4":
                self._cancelar_inscricao()
            elif opcao == "5":
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _listar_inscricoes(self) -> None:
        """Lista inscrições do candidato"""
        self._limpar_tela()
        print(f"\n=== INSCRIÇÕES DE {self.candidato_selecionado.nome} ===\n")

        try:
            inscricoes = self.service_inscricao_curso.listar_por_candidato(self.candidato_selecionado.id)

            if not inscricoes:
                print("Nenhuma inscrição encontrada.")
            else:
                print(f"Total: {len(inscricoes)} inscrições\n")
                for i in inscricoes:
                    status = i.status.name if hasattr(i.status, 'name') else i.status
                    print(f"ID: {i.id} | Curso ID: {i.id_curso}")
                    print(f"   Status: {status}")
                    if hasattr(i, 'data_inscricao') and i.data_inscricao:
                        print(f"   Data: {i.data_inscricao}")
                    print("-" * 40)

        except Exception as e:
            print(f"Erro ao listar: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _criar_inscricao(self) -> None:
        """Cria inscrição em curso para o candidato"""
        self._limpar_tela()
        print("\n=== CRIAR INSCRIÇÃO EM CURSO ===\n")

        # Mostrar cursos disponíveis
        try:
            print("Cursos EAD disponíveis:")
            cursos_ead = self.service_curso_ead.listar_todos()
            for c in cursos_ead[:5]:  # Limita a 5
                print(f"  ID: {c.id} | {c.nome}")

            print("\nCursos Presenciais disponíveis:")
            cursos_pres = self.service_curso_presencial.listar_todos()
            for c in cursos_pres[:5]:
                print(f"  ID: {c.id} | {c.nome}")

        except Exception:
            pass

        try:
            print()
            id_curso = int(input("Digite o ID do curso: ").strip())
            self.service_inscricao_curso.inscrever(self.candidato_selecionado.id, id_curso)
            print("\n✅ Inscrição criada com sucesso!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao criar: {e}")

        self._pausar()

    def _concluir_inscricao(self) -> None:
        """Conclui inscrição e atribui competências"""
        self._limpar_tela()
        print("\n=== CONCLUIR CURSO ===\n")

        try:
            inscricoes = self.service_inscricao_curso.listar_por_candidato(self.candidato_selecionado.id)
            inscricoes_deferidas = [i for i in inscricoes if i.status == StatusInscricao.DEFERIDO]

            if not inscricoes_deferidas:
                print("Nenhuma inscrição deferida para concluir.")
                self._pausar()
                return

            print("Inscrições disponíveis para conclusão:\n")
            for i in inscricoes_deferidas:
                print(f"ID: {i.id} | Curso ID: {i.id_curso} | Status: {i.status.name}")

            print()
            id_inscricao = int(input("Digite o ID da inscrição a concluir: ").strip())

            # Verificar se pertence ao candidato
            inscricao = next((i for i in inscricoes_deferidas if i.id == id_inscricao), None)
            if not inscricao:
                print("\n❌ Inscrição não encontrada ou não disponível.")
                self._pausar()
                return

            competencias = self.service_inscricao_curso.concluir_inscricao(id_inscricao)

            print("\n✅ Curso concluído com sucesso!")

            if competencias:
                print(f"\n🎓 Competências atribuídas: {len(competencias)}")
                for comp in competencias:
                    if self.service_competencia:
                        try:
                            c = self.service_competencia.buscar_por_id(comp.id_competencia)
                            print(f"   • {c.nome} - Nível: {comp.nivel_atual}")
                        except Exception:
                            print(f"   • Competência ID {comp.id_competencia} - Nível: {comp.nivel_atual}")
                    else:
                        print(f"   • Competência ID {comp.id_competencia} - Nível: {comp.nivel_atual}")
            else:
                print("\nℹ️  Este curso não possui competências associadas.")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao concluir: {e}")

        self._pausar()

    def _cancelar_inscricao(self) -> None:
        """Cancela inscrição do candidato"""
        self._limpar_tela()
        print("\n=== CANCELAR INSCRIÇÃO ===\n")

        try:
            inscricoes = self.service_inscricao_curso.listar_por_candidato(self.candidato_selecionado.id)

            if not inscricoes:
                print("Nenhuma inscrição para cancelar.")
                self._pausar()
                return

            for i in inscricoes:
                status = i.status.name if hasattr(i.status, 'name') else i.status
                print(f"ID: {i.id} | Curso: {i.id_curso} | Status: {status}")

            print()
            id_inscricao = int(input("Digite o ID da inscrição a cancelar: ").strip())

            if hasattr(self.service_inscricao_curso, 'cancelar'):
                self.service_inscricao_curso.cancelar(id_inscricao)
            elif hasattr(self.service_inscricao_curso, 'remover'):
                self.service_inscricao_curso.remover(id_inscricao)
            else:
                print("\n❌ Funcionalidade não disponível.")
                self._pausar()
                return

            print("\n✅ Inscrição cancelada!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao cancelar: {e}")

        self._pausar()

    # ==========================
    # MENU DE COMPETÊNCIAS
    # ==========================

    def _menu_competencias(self) -> None:
        """Menu de competências do candidato"""
        if not self.service_competencia_candidato:
            self._limpar_tela()
            print("\n❌ Serviço de competências não disponível.")
            self._pausar()
            return

        while True:
            self._limpar_tela()
            print("=" * 60)
            print(f"  COMPETÊNCIAS - {self.candidato_selecionado.nome}".center(60))
            print("=" * 60)
            print("\n1. Listar Competências")
            print("2. Adicionar Competência")
            print("3. Atualizar Nível de Competência")
            print("4. Remover Competência")
            print("5. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Digite a opção desejada (1-5): ").strip()

            if opcao == "1":
                self._listar_competencias()
            elif opcao == "2":
                self._adicionar_competencia()
            elif opcao == "3":
                self._atualizar_nivel_competencia()
            elif opcao == "4":
                self._remover_competencia()
            elif opcao == "5":
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _listar_competencias(self) -> None:
        """Lista competências do candidato"""
        self._limpar_tela()
        print(f"\n=== COMPETÊNCIAS DE {self.candidato_selecionado.nome} ===\n")

        try:
            competencias = self.service_competencia_candidato.listar_por_candidato(
                self.candidato_selecionado.id
            )

            if not competencias:
                print("Nenhuma competência registrada.")
            else:
                print(f"Total: {len(competencias)} competências\n")
                for comp in competencias:
                    nome_comp = "Desconhecida"
                    if self.service_competencia:
                        try:
                            c = self.service_competencia.buscar_por_id(comp.id_competencia)
                            nome_comp = c.nome
                        except Exception:
                            pass

                    print(f"ID: {comp.id} | {nome_comp}")
                    print(f"   Competência ID: {comp.id_competencia}")
                    print(f"   Nível: {comp.nivel_atual}")
                    print("-" * 40)

        except Exception as e:
            print(f"Erro ao listar: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _adicionar_competencia(self) -> None:
        """Adiciona competência ao candidato"""
        self._limpar_tela()
        print("\n=== ADICIONAR COMPETÊNCIA ===\n")

        # Mostrar competências disponíveis
        if self.service_competencia:
            try:
                print("Competências disponíveis:")
                todas = self.service_competencia.listar_todas()
                for c in todas[:10]:
                    print(f"  ID: {c.id} | {c.nome}")
                print()
            except Exception:
                pass

        try:
            id_competencia = int(input("Digite o ID da competência: ").strip())
            nivel = input("Nível (iniciante/intermediario/avancado/especialista): ").strip()

            self.service_competencia_candidato.cadastrar(
                id_candidato=self.candidato_selecionado.id,
                id_competencia=id_competencia,
                nivel_atual=nivel
            )
            print("\n✅ Competência adicionada com sucesso!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao adicionar: {e}")

        self._pausar()

    def _atualizar_nivel_competencia(self) -> None:
        """Atualiza nível de competência"""
        self._limpar_tela()
        print("\n=== ATUALIZAR NÍVEL DE COMPETÊNCIA ===\n")

        try:
            competencias = self.service_competencia_candidato.listar_por_candidato(
                self.candidato_selecionado.id
            )

            if not competencias:
                print("Nenhuma competência para atualizar.")
                self._pausar()
                return

            for comp in competencias:
                print(f"ID: {comp.id} | Comp ID: {comp.id_competencia} | Nível: {comp.nivel_atual}")

            print()
            id_comp_candidato = int(input("Digite o ID da competência do candidato: ").strip())
            novo_nivel = input("Novo nível (iniciante/intermediario/avancado/especialista): ").strip()

            self.service_competencia_candidato.atualizar_nivel(id_comp_candidato, novo_nivel)
            print("\n✅ Nível atualizado com sucesso!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao atualizar: {e}")

        self._pausar()

    def _remover_competencia(self) -> None:
        """Remove competência do candidato"""
        self._limpar_tela()
        print("\n=== REMOVER COMPETÊNCIA ===\n")

        try:
            competencias = self.service_competencia_candidato.listar_por_candidato(
                self.candidato_selecionado.id
            )

            if not competencias:
                print("Nenhuma competência para remover.")
                self._pausar()
                return

            for comp in competencias:
                print(f"ID: {comp.id} | Comp ID: {comp.id_competencia} | Nível: {comp.nivel_atual}")

            print()
            id_comp_candidato = int(input("Digite o ID da competência a remover: ").strip())

            self.service_competencia_candidato.remover(id_comp_candidato)
            print("\n✅ Competência removida com sucesso!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao remover: {e}")

        self._pausar()

    # ==========================
    # EXECUÇÃO DO FLUXO
    # ==========================

    def executar(self) -> None:
        """Executa o fluxo do back office"""
        while True:
            opcao = self._exibir_menu_principal()
            if not self._processar_opcao_principal(opcao):
                break

        # Despedida
        self._limpar_tela()
        print("\n" + "=" * 60)
        print("BACK OFFICE ENCERRADO".center(60))
        print("=" * 60)
        print("\nAté logo!\n")