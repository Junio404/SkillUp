"""
Fluxo de Administração de Empresas (Back Office)
Gerencia empresas, vagas, requisitos e candidaturas
"""

import os
from typing import Optional
from src.dominio.empresa import Empresa
from src.dominio.vaga import Modalidade, TipoVaga
from src.services.services_empresa import EmpresaService
from src.services.service_vaga_clt import VagaCLTService
from src.services.service_vaga_estagio import VagaEstagioService
from src.services.service_requisito_vaga import RequisitoVagaService
from src.services.service_candidatura import CandidaturaService
from src.services.service_competencia import CompetenciaService


class FluxoEmpresaAdmin:
    """Back Office para administração de empresas"""

    def __init__(
        self,
        service_empresa: EmpresaService,
        service_vaga_clt: VagaCLTService,
        service_vaga_estagio: VagaEstagioService,
        service_requisito_vaga: RequisitoVagaService,
        service_candidatura: CandidaturaService,
        service_competencia: Optional[CompetenciaService] = None,
    ):
        """Inicializa o back office com todos os serviços necessários"""
        self.service_empresa = service_empresa
        self.service_vaga_clt = service_vaga_clt
        self.service_vaga_estagio = service_vaga_estagio
        self.service_requisito_vaga = service_requisito_vaga
        self.service_candidatura = service_candidatura
        self.service_competencia = service_competencia

        self.empresa_selecionada: Optional[Empresa] = None

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
        print("     SKILLUP - BACK OFFICE DE EMPRESAS".center(60))
        print("=" * 60)
        print("\n1. Listar Todas as Empresas")
        print("2. Cadastrar Nova Empresa")
        print("3. Buscar Empresa por ID")
        print("4. Gerenciar Empresa (Selecionar)")
        print("5. Excluir Empresa")
        print("6. Gerenciar Vagas (Sem Empresa)")
        print("7. Gerenciar Candidaturas")
        print("8. Sair")
        print("\n" + "-" * 60)

        opcao = input("Digite a opção desejada (1-8): ").strip()
        return opcao

    def _processar_opcao_principal(self, opcao: str) -> bool:
        """Processa opção do menu principal. Retorna False para sair."""
        acoes = {
            "1": self._listar_empresas,
            "2": self._cadastrar_empresa,
            "3": self._buscar_por_id,
            "4": self._selecionar_e_gerenciar,
            "5": self._excluir_empresa,
            "6": self._menu_vagas_geral,
            "7": self._menu_candidaturas_geral,
            "8": lambda: None,
        }

        acao = acoes.get(opcao)
        if acao:
            acao()
            return opcao != "8"
        else:
            print("\n❌ Opção inválida!")
            self._pausar()
            return True

    # ==========================
    # CRUD DE EMPRESAS
    # ==========================

    def _listar_empresas(self) -> None:
        """Lista todas as empresas cadastradas"""
        self._limpar_tela()
        print("\n=== TODAS AS EMPRESAS ===\n")

        try:
            empresas = self.service_empresa.listar()
            if not empresas:
                print("Nenhuma empresa cadastrada.")
            else:
                print(f"Total: {len(empresas)} empresas\n")
                for e in empresas:
                    self._exibir_empresa_resumo(e)

        except Exception as e:
            print(f"Erro ao listar empresas: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _exibir_empresa_resumo(self, e: Empresa) -> None:
        """Exibe resumo de uma empresa"""
        print(f"ID: {e.id} | {e.nome}")
        print(f"   CNPJ: {e.cnpj} | Porte: {e.porte}")
        print("-" * 50)

    def _exibir_empresa_completa(self, e: Empresa) -> None:
        """Exibe dados completos de uma empresa"""
        print(f"ID: {e.id}")
        print(f"Nome: {e.nome}")
        print(f"CNPJ: {e.cnpj}")
        print(f"Porte: {e.porte}")

    def _cadastrar_empresa(self) -> None:
        """Cadastra uma nova empresa"""
        self._limpar_tela()
        print("\n=== CADASTRAR NOVA EMPRESA ===\n")

        try:
            nome = input("Nome da empresa: ").strip()
            cnpj = input("CNPJ (14 dígitos): ").strip()
            porte = input("Porte (pequeno/medio/grande): ").strip()

            empresa = self.service_empresa.cadastrar(
                nome=nome,
                cnpj=cnpj,
                porte=porte
            )

            print(f"\n✅ Empresa cadastrada com sucesso!")
            print(f"ID atribuído: {empresa.id}")

        except ValueError as e:
            print(f"\n❌ Erro de validação: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao cadastrar: {e}")

        self._pausar()

    def _buscar_por_id(self) -> None:
        """Busca empresa por ID"""
        self._limpar_tela()
        print("\n=== BUSCAR EMPRESA POR ID ===\n")

        try:
            id_empresa = int(input("Digite o ID da empresa: ").strip())
            empresa = self.service_empresa.buscar_por_id(id_empresa)

            print("\n" + "=" * 40)
            self._exibir_empresa_completa(empresa)
            print("=" * 40)

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Empresa não encontrada: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _excluir_empresa(self) -> None:
        """Exclui uma empresa"""
        self._limpar_tela()
        print("\n=== EXCLUIR EMPRESA ===\n")

        try:
            id_empresa = int(input("Digite o ID da empresa a excluir: ").strip())
            empresa = self.service_empresa.buscar_por_id(id_empresa)

            print(f"\nEmpresa encontrada: {empresa.nome}")
            print("⚠️  Esta ação é irreversível!")

            confirmacao = input("\nDigite 'CONFIRMAR' para excluir: ").strip()

            if confirmacao == "CONFIRMAR":
                self.service_empresa.deletar(id_empresa)
                print("\n✅ Empresa excluída com sucesso!")
            else:
                print("\n❌ Exclusão cancelada.")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao excluir: {e}")

        self._pausar()

    # ==========================
    # GERENCIAMENTO DE EMPRESA
    # ==========================

    def _selecionar_e_gerenciar(self) -> None:
        """Seleciona uma empresa e abre menu de gerenciamento"""
        self._limpar_tela()
        print("\n=== SELECIONAR EMPRESA ===\n")

        try:
            id_empresa = int(input("Digite o ID da empresa: ").strip())
            empresa = self.service_empresa.buscar_por_id(id_empresa)
            self.empresa_selecionada = empresa

            print(f"\n✅ Empresa selecionada: {empresa.nome}")
            self._pausar()

            self._menu_gerenciar_empresa()

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
            self._pausar()
        except Exception as e:
            print(f"\n❌ Empresa não encontrada: {e}")
            self._pausar()

    def _menu_gerenciar_empresa(self) -> None:
        """Menu de gerenciamento da empresa selecionada"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print(f"  GERENCIANDO: {self.empresa_selecionada.nome}".center(60))
            print(f"  (ID: {self.empresa_selecionada.id})".center(60))
            print("=" * 60)
            print("\n1. Ver Dados Completos")
            print("2. Editar Dados")
            print("3. Gerenciar Vagas CLT")
            print("4. Gerenciar Vagas de Estágio")
            print("5. Ver Candidaturas às Vagas")
            print("6. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Digite a opção desejada (1-6): ").strip()

            if opcao == "1":
                self._ver_dados_empresa()
            elif opcao == "2":
                self._editar_dados_empresa()
            elif opcao == "3":
                self._menu_vagas_clt()
            elif opcao == "4":
                self._menu_vagas_estagio()
            elif opcao == "5":
                self._ver_candidaturas_empresa()
            elif opcao == "6":
                self.empresa_selecionada = None
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _ver_dados_empresa(self) -> None:
        """Exibe dados completos da empresa selecionada"""
        self._limpar_tela()
        print("\n=== DADOS DA EMPRESA ===\n")
        self._exibir_empresa_completa(self.empresa_selecionada)
        self._pausar("\nPressione ENTER para voltar...")

    def _editar_dados_empresa(self) -> None:
        """Menu para editar dados da empresa"""
        while True:
            self._limpar_tela()
            print("\n=== EDITAR DADOS DA EMPRESA ===\n")
            print(f"Editando: {self.empresa_selecionada.nome}\n")
            print("1. Nome")
            print("2. Porte")
            print("3. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Qual campo deseja editar (1-3): ").strip()

            campos = {
                "1": ("nome", "Novo nome"),
                "2": ("porte", "Novo porte"),
            }

            if opcao in campos:
                campo, descricao = campos[opcao]
                self._atualizar_campo_empresa(campo, descricao)
            elif opcao == "3":
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _atualizar_campo_empresa(self, campo: str, descricao: str) -> None:
        """Atualiza um campo específico da empresa"""
        try:
            valor_atual = getattr(self.empresa_selecionada, campo, "")
            print(f"\nValor atual: {valor_atual}")
            novo_valor = input(f"{descricao}: ").strip()

            if novo_valor:
                self.service_empresa.atualizar(self.empresa_selecionada.id, campo, novo_valor)
                self.empresa_selecionada = self.service_empresa.buscar_por_id(self.empresa_selecionada.id)
                print(f"\n✅ {campo.replace('_', ' ').title()} atualizado!")
            else:
                print("\n❌ Valor não pode ser vazio.")

        except ValueError as e:
            print(f"\n❌ Erro de validação: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao atualizar: {e}")

        self._pausar()

    # ==========================
    # MENU DE VAGAS CLT
    # ==========================

    def _menu_vagas_clt(self) -> None:
        """Menu de vagas CLT da empresa"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print(f"  VAGAS CLT - {self.empresa_selecionada.nome}".center(60))
            print("=" * 60)
            print("\n1. Listar Vagas CLT")
            print("2. Cadastrar Nova Vaga CLT")
            print("3. Gerenciar Requisitos de Vaga")
            print("4. Ativar/Desativar Vaga")
            print("5. Excluir Vaga")
            print("6. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Digite a opção desejada (1-6): ").strip()

            if opcao == "1":
                self._listar_vagas_clt()
            elif opcao == "2":
                self._cadastrar_vaga_clt()
            elif opcao == "3":
                self._menu_requisitos_vaga()
            elif opcao == "4":
                self._ativar_desativar_vaga_clt()
            elif opcao == "5":
                self._excluir_vaga_clt()
            elif opcao == "6":
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _listar_vagas_clt(self) -> None:
        """Lista vagas CLT"""
        self._limpar_tela()
        print(f"\n=== VAGAS CLT ===\n")

        try:
            vagas = self.service_vaga_clt.listar_todas()

            if not vagas:
                print("Nenhuma vaga CLT cadastrada.")
            else:
                print(f"Total: {len(vagas)} vagas\n")
                for v in vagas:
                    status = "Ativa" if getattr(v, 'ativa', True) else "Inativa"
                    print(f"ID: {v.id} | {v.titulo}")
                    print(f"   Área: {v.area} | Modalidade: {v.modalidade.value}")
                    print(f"   Salário: R$ {v.salario_base:.2f} | Status: {status}")
                    print(f"   Localidade: {v.localidade}")
                    print("-" * 40)

        except Exception as e:
            print(f"Erro ao listar: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _cadastrar_vaga_clt(self) -> None:
        """Cadastra nova vaga CLT"""
        self._limpar_tela()
        print("\n=== CADASTRAR VAGA CLT ===\n")

        try:
            titulo = input("Título da vaga: ").strip()
            descricao = input("Descrição: ").strip()
            area = input("Área: ").strip()

            print("\nModalidades: PRESENCIAL, REMOTO, HIBRIDO")
            modalidade_str = input("Modalidade: ").strip().upper()
            modalidade = Modalidade(modalidade_str)

            print("\nTipos: CLT, ESTAGIO, FREELANCER")
            tipo_str = input("Tipo (CLT): ").strip().upper() or "CLT"
            tipo = TipoVaga(tipo_str)

            salario = float(input("Salário base: R$ ").strip())
            localidade = input("Localidade: ").strip()

            vaga = self.service_vaga_clt.cadastrar(
                titulo=titulo,
                descricao=descricao,
                area=area,
                modalidade=modalidade,
                tipo=tipo,
                salario_base=salario,
                localidade=localidade,
            )

            print(f"\n✅ Vaga CLT cadastrada com sucesso!")
            print(f"ID: {vaga.id}")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao cadastrar: {e}")

        self._pausar()

    def _ativar_desativar_vaga_clt(self) -> None:
        """Ativa ou desativa uma vaga CLT"""
        self._limpar_tela()
        print("\n=== ATIVAR/DESATIVAR VAGA CLT ===\n")

        try:
            vagas = self.service_vaga_clt.listar_todas()
            for v in vagas:
                status = "Ativa" if getattr(v, 'ativa', True) else "Inativa"
                print(f"ID: {v.id} | {v.titulo} | Status: {status}")

            print()
            id_vaga = int(input("Digite o ID da vaga: ").strip())
            vaga = self.service_vaga_clt.buscar_por_id(id_vaga)

            if getattr(vaga, 'ativa', True):
                vaga.ativa = False
                print("\n✅ Vaga desativada!")
            else:
                vaga.ativa = True
                print("\n✅ Vaga ativada!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    def _excluir_vaga_clt(self) -> None:
        """Exclui uma vaga CLT"""
        self._limpar_tela()
        print("\n=== EXCLUIR VAGA CLT ===\n")

        try:
            vagas = self.service_vaga_clt.listar_todas()
            for v in vagas:
                print(f"ID: {v.id} | {v.titulo}")

            print()
            id_vaga = int(input("Digite o ID da vaga a excluir: ").strip())
            self.service_vaga_clt.excluir(id_vaga)
            print("\n✅ Vaga excluída!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    # ==========================
    # MENU DE VAGAS ESTÁGIO
    # ==========================

    def _menu_vagas_estagio(self) -> None:
        """Menu de vagas de estágio"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print(f"  VAGAS ESTÁGIO - {self.empresa_selecionada.nome}".center(60))
            print("=" * 60)
            print("\n1. Listar Vagas de Estágio")
            print("2. Cadastrar Nova Vaga de Estágio")
            print("3. Gerenciar Requisitos de Vaga")
            print("4. Excluir Vaga")
            print("5. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Digite a opção desejada (1-5): ").strip()

            if opcao == "1":
                self._listar_vagas_estagio()
            elif opcao == "2":
                self._cadastrar_vaga_estagio()
            elif opcao == "3":
                self._menu_requisitos_vaga()
            elif opcao == "4":
                self._excluir_vaga_estagio()
            elif opcao == "5":
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _listar_vagas_estagio(self) -> None:
        """Lista vagas de estágio"""
        self._limpar_tela()
        print(f"\n=== VAGAS DE ESTÁGIO ===\n")

        try:
            vagas = self.service_vaga_estagio.listar_todas()

            if not vagas:
                print("Nenhuma vaga de estágio cadastrada.")
            else:
                print(f"Total: {len(vagas)} vagas\n")
                for v in vagas:
                    print(f"ID: {v.id} | {v.titulo}")
                    print(f"   Área: {v.area} | Modalidade: {v.modalidade.value}")
                    print(f"   Bolsa: R$ {v.bolsa_auxilio:.2f}")
                    print(f"   Instituição Conveniada: {v.instituicao_conveniada}")
                    print(f"   Localidade: {v.localidade}")
                    print("-" * 40)

        except Exception as e:
            print(f"Erro ao listar: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _cadastrar_vaga_estagio(self) -> None:
        """Cadastra nova vaga de estágio"""
        self._limpar_tela()
        print("\n=== CADASTRAR VAGA DE ESTÁGIO ===\n")

        try:
            titulo = input("Título da vaga: ").strip()
            descricao = input("Descrição: ").strip()
            area = input("Área: ").strip()

            print("\nModalidades: PRESENCIAL, REMOTO, HIBRIDO")
            modalidade_str = input("Modalidade: ").strip().upper()
            modalidade = Modalidade(modalidade_str)

            bolsa = float(input("Bolsa auxílio: R$ ").strip())
            instituicao = input("Instituição conveniada: ").strip()
            localidade = input("Localidade: ").strip()

            vaga = self.service_vaga_estagio.cadastrar(
                titulo=titulo,
                descricao=descricao,
                area=area,
                modalidade=modalidade,
                tipo=TipoVaga.ESTAGIO,
                bolsa_auxilio=bolsa,
                instituicao_conveniada=instituicao,
                localidade=localidade,
            )

            print(f"\n✅ Vaga de estágio cadastrada!")
            print(f"ID: {vaga.id}")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao cadastrar: {e}")

        self._pausar()

    def _excluir_vaga_estagio(self) -> None:
        """Exclui uma vaga de estágio"""
        self._limpar_tela()
        print("\n=== EXCLUIR VAGA DE ESTÁGIO ===\n")

        try:
            vagas = self.service_vaga_estagio.listar_todas()
            for v in vagas:
                print(f"ID: {v.id} | {v.titulo}")

            print()
            id_vaga = int(input("Digite o ID da vaga a excluir: ").strip())
            self.service_vaga_estagio.excluir(id_vaga)
            print("\n✅ Vaga excluída!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    # ==========================
    # MENU DE REQUISITOS DE VAGA
    # ==========================

    def _menu_requisitos_vaga(self) -> None:
        """Menu de requisitos de vaga"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print("         REQUISITOS DE VAGA".center(60))
            print("=" * 60)
            print("\n1. Listar Requisitos de uma Vaga")
            print("2. Adicionar Requisito a uma Vaga")
            print("3. Atualizar Nível de Requisito")
            print("4. Tornar Obrigatório/Opcional")
            print("5. Remover Requisito")
            print("6. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Digite a opção desejada (1-6): ").strip()

            if opcao == "1":
                self._listar_requisitos_vaga()
            elif opcao == "2":
                self._adicionar_requisito()
            elif opcao == "3":
                self._atualizar_nivel_requisito()
            elif opcao == "4":
                self._alternar_obrigatoriedade()
            elif opcao == "5":
                self._remover_requisito()
            elif opcao == "6":
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _listar_requisitos_vaga(self) -> None:
        """Lista requisitos de uma vaga"""
        self._limpar_tela()
        print("\n=== LISTAR REQUISITOS DE VAGA ===\n")

        try:
            id_vaga = int(input("Digite o ID da vaga: ").strip())
            requisitos = self.service_requisito_vaga.listar_por_vaga(id_vaga)

            if not requisitos:
                print("\nNenhum requisito cadastrado para esta vaga.")
            else:
                print(f"\nRequisitos da vaga {id_vaga}:\n")
                for r in requisitos:
                    obrig = "Obrigatório" if r.obrigatorio else "Opcional"
                    nome_comp = self._obter_nome_competencia(r.id_competencia)
                    print(f"ID: {r.id} | Competência: {nome_comp}")
                    print(f"   Nível Mínimo: {r.nivel_minimo} | {obrig}")
                    print("-" * 40)

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _obter_nome_competencia(self, id_competencia: int) -> str:
        """Obtém nome de competência pelo ID"""
        if self.service_competencia:
            try:
                comp = self.service_competencia.buscar_por_id(id_competencia)
                return comp.nome if comp else f"ID {id_competencia}"
            except:
                pass
        return f"ID {id_competencia}"

    def _adicionar_requisito(self) -> None:
        """Adiciona requisito a uma vaga"""
        self._limpar_tela()
        print("\n=== ADICIONAR REQUISITO ===\n")

        # Mostrar competências disponíveis
        if self.service_competencia:
            try:
                print("Competências disponíveis:")
                competencias = self.service_competencia.listar_todas()
                for c in competencias[:10]:
                    print(f"  ID: {c.id} | {c.nome}")
                print()
            except:
                pass

        try:
            id_vaga = int(input("ID da vaga: ").strip())
            id_competencia = int(input("ID da competência: ").strip())
            nivel = input("Nível mínimo (iniciante/intermediario/avancado/especialista): ").strip()
            obrigatorio = input("Obrigatório? (s/n): ").strip().lower() == "s"

            requisito = self.service_requisito_vaga.cadastrar(
                id_vaga=id_vaga,
                id_competencia=id_competencia,
                nivel_minimo=nivel,
                obrigatorio=obrigatorio,
            )

            print(f"\n✅ Requisito adicionado! ID: {requisito.id}")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    def _atualizar_nivel_requisito(self) -> None:
        """Atualiza nível de um requisito"""
        self._limpar_tela()
        print("\n=== ATUALIZAR NÍVEL DE REQUISITO ===\n")

        try:
            id_requisito = int(input("ID do requisito: ").strip())
            novo_nivel = input("Novo nível (iniciante/intermediario/avancado/especialista): ").strip()

            self.service_requisito_vaga.atualizar_nivel(id_requisito, novo_nivel)
            print("\n✅ Nível atualizado!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    def _alternar_obrigatoriedade(self) -> None:
        """Alterna obrigatoriedade de um requisito"""
        self._limpar_tela()
        print("\n=== ALTERAR OBRIGATORIEDADE ===\n")

        try:
            id_requisito = int(input("ID do requisito: ").strip())
            requisito = self.service_requisito_vaga.buscar_por_id(id_requisito)

            if requisito.obrigatorio:
                self.service_requisito_vaga.tornar_opcional(id_requisito)
                print("\n✅ Requisito agora é opcional!")
            else:
                self.service_requisito_vaga.tornar_obrigatorio(id_requisito)
                print("\n✅ Requisito agora é obrigatório!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    def _remover_requisito(self) -> None:
        """Remove um requisito"""
        self._limpar_tela()
        print("\n=== REMOVER REQUISITO ===\n")

        try:
            id_requisito = int(input("ID do requisito a remover: ").strip())
            self.service_requisito_vaga.remover(id_requisito)
            print("\n✅ Requisito removido!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    # ==========================
    # CANDIDATURAS
    # ==========================

    def _ver_candidaturas_empresa(self) -> None:
        """Ver candidaturas às vagas da empresa"""
        self._limpar_tela()
        print(f"\n=== CANDIDATURAS - {self.empresa_selecionada.nome} ===\n")

        try:
            # Listar vagas CLT e estágio
            vagas_clt = self.service_vaga_clt.listar_todas()
            vagas_estagio = self.service_vaga_estagio.listar_todas()

            for v in vagas_clt + vagas_estagio:
                candidaturas = self.service_candidatura.listar_por_vaga(v.id)
                if candidaturas:
                    print(f"\nVaga: {v.titulo} (ID: {v.id})")
                    print("-" * 40)
                    for c in candidaturas:
                        status = c.status.value if hasattr(c.status, 'value') else c.status
                        print(f"  Candidatura ID: {c.id} | Candidato: {c.id_candidato}")
                        print(f"     Status: {status}")

            print("\n" + "=" * 40)

        except Exception as e:
            print(f"Erro: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _menu_vagas_geral(self) -> None:
        """Menu geral de vagas sem empresa específica"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print("         GERENCIAR VAGAS (GERAL)".center(60))
            print("=" * 60)
            print("\n1. Listar Todas as Vagas CLT")
            print("2. Listar Todas as Vagas de Estágio")
            print("3. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Digite a opção desejada (1-3): ").strip()

            if opcao == "1":
                self._listar_vagas_clt()
            elif opcao == "2":
                self._listar_vagas_estagio()
            elif opcao == "3":
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _menu_candidaturas_geral(self) -> None:
        """Menu geral de candidaturas"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print("         GERENCIAR CANDIDATURAS".center(60))
            print("=" * 60)
            print("\n1. Listar Todas as Candidaturas")
            print("2. Listar por Vaga")
            print("3. Aprovar Candidatura")
            print("4. Reprovar Candidatura")
            print("5. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Digite a opção desejada (1-5): ").strip()

            if opcao == "1":
                self._listar_todas_candidaturas()
            elif opcao == "2":
                self._listar_candidaturas_por_vaga()
            elif opcao == "3":
                self._aprovar_candidatura()
            elif opcao == "4":
                self._reprovar_candidatura()
            elif opcao == "5":
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _listar_todas_candidaturas(self) -> None:
        """Lista todas as candidaturas"""
        self._limpar_tela()
        print("\n=== TODAS AS CANDIDATURAS ===\n")

        try:
            candidaturas = self.service_candidatura.listar_todas()

            if not candidaturas:
                print("Nenhuma candidatura encontrada.")
            else:
                print(f"Total: {len(candidaturas)}\n")
                for c in candidaturas:
                    status = c.status.value if hasattr(c.status, 'value') else c.status
                    print(f"ID: {c.id} | Vaga: {c.id_vaga} | Candidato: {c.id_candidato}")
                    print(f"   Status: {status}")
                    print("-" * 40)

        except Exception as e:
            print(f"Erro: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _listar_candidaturas_por_vaga(self) -> None:
        """Lista candidaturas de uma vaga"""
        self._limpar_tela()
        print("\n=== CANDIDATURAS POR VAGA ===\n")

        try:
            id_vaga = int(input("ID da vaga: ").strip())
            candidaturas = self.service_candidatura.listar_por_vaga(id_vaga)

            if not candidaturas:
                print("\nNenhuma candidatura para esta vaga.")
            else:
                print(f"\nCandidaturas para vaga {id_vaga}:\n")
                for c in candidaturas:
                    status = c.status.value if hasattr(c.status, 'value') else c.status
                    print(f"ID: {c.id} | Candidato: {c.id_candidato} | Status: {status}")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _aprovar_candidatura(self) -> None:
        """Aprova uma candidatura"""
        self._limpar_tela()
        print("\n=== APROVAR CANDIDATURA ===\n")

        try:
            id_candidatura = int(input("ID da candidatura: ").strip())
            self.service_candidatura.aprovar(id_candidatura)
            print("\n✅ Candidatura aprovada!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    def _reprovar_candidatura(self) -> None:
        """Reprova uma candidatura"""
        self._limpar_tela()
        print("\n=== REPROVAR CANDIDATURA ===\n")

        try:
            id_candidatura = int(input("ID da candidatura: ").strip())
            self.service_candidatura.reprovar(id_candidatura)
            print("\n✅ Candidatura reprovada!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

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
        print("BACK OFFICE DE EMPRESAS ENCERRADO".center(60))
        print("=" * 60)
        print("\nAté logo!\n")