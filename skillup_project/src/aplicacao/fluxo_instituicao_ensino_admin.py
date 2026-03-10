"""
Fluxo de Administração de Instituições de Ensino (Back Office)
Gerencia instituições, áreas de ensino, cursos, competências e inscrições
"""

import os
from typing import Optional
from src.dominio.instituicao_ensino import InstituicaoEnsino
from src.services.service_area_ensino import AreaEnsinoService
from src.services.service_instituicao_area_ensino import InstituicaoAreaEnsinoService
from src.services.service_curso_ead import CursoEADService
from src.services.service_curso_presencial import CursoPresencialService
from src.services.service_curso_competencia import CursoCompetenciaService
from src.services.service_inscricao_curso import InscricaoCursoService
from src.services.service_competencia import CompetenciaService


class FluxoInstituicaoAdmin:
    """Back Office para administração de Instituições de Ensino"""

    def __init__(
        self,
        service_area_ensino: AreaEnsinoService,
        service_instituicao_area: InstituicaoAreaEnsinoService,
        service_curso_ead: CursoEADService,
        service_curso_presencial: CursoPresencialService,
        service_curso_competencia: CursoCompetenciaService,
        service_inscricao_curso: InscricaoCursoService,
        service_competencia: Optional[CompetenciaService] = None,
    ):
        """Inicializa o back office com todos os serviços necessários"""
        self.service_area_ensino = service_area_ensino
        self.service_instituicao_area = service_instituicao_area
        self.service_curso_ead = service_curso_ead
        self.service_curso_presencial = service_curso_presencial
        self.service_curso_competencia = service_curso_competencia
        self.service_inscricao_curso = service_inscricao_curso
        self.service_competencia = service_competencia

        # Armazenamento em memória para instituições (já que não existe repositório completo)
        self._instituicoes: dict = {}
        self._proximo_id_instituicao = 1

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
        print("  SKILLUP - BACK OFFICE DE INSTITUIÇÕES DE ENSINO".center(60))
        print("=" * 60)
        print("\n1. Gerenciar Áreas de Ensino")
        print("2. Gerenciar Instituições")
        print("3. Gerenciar Cursos EAD")
        print("4. Gerenciar Cursos Presenciais")
        print("5. Gerenciar Competências de Cursos")
        print("6. Gerenciar Inscrições em Cursos")
        print("7. Sair")
        print("\n" + "-" * 60)

        opcao = input("Digite a opção desejada (1-7): ").strip()
        return opcao

    def _processar_opcao_principal(self, opcao: str) -> bool:
        """Processa opção do menu principal. Retorna False para sair."""
        acoes = {
            "1": self._menu_areas_ensino,
            "2": self._menu_instituicoes,
            "3": self._menu_cursos_ead,
            "4": self._menu_cursos_presenciais,
            "5": self._menu_curso_competencias,
            "6": self._menu_inscricoes,
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
    # MENU DE ÁREAS DE ENSINO
    # ==========================

    def _menu_areas_ensino(self) -> None:
        """Menu de áreas de ensino"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print("         ÁREAS DE ENSINO".center(60))
            print("=" * 60)
            print("\n1. Listar Todas as Áreas")
            print("2. Cadastrar Nova Área")
            print("3. Buscar Área por ID")
            print("4. Buscar Área por Nome")
            print("5. Atualizar Nome de Área")
            print("6. Remover Área")
            print("7. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Digite a opção desejada (1-7): ").strip()

            if opcao == "1":
                self._listar_areas()
            elif opcao == "2":
                self._cadastrar_area()
            elif opcao == "3":
                self._buscar_area_por_id()
            elif opcao == "4":
                self._buscar_area_por_nome()
            elif opcao == "5":
                self._atualizar_area()
            elif opcao == "6":
                self._remover_area()
            elif opcao == "7":
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _listar_areas(self) -> None:
        """Lista todas as áreas de ensino"""
        self._limpar_tela()
        print("\n=== ÁREAS DE ENSINO ===\n")

        try:
            areas = self.service_area_ensino.listar_todas()
            if not areas:
                print("Nenhuma área de ensino cadastrada.")
            else:
                print(f"Total: {len(areas)} áreas\n")
                for a in areas:
                    print(f"ID: {a.id_area} | {a.nome_area}")
                    print("-" * 40)

        except Exception as e:
            print(f"Erro ao listar: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _cadastrar_area(self) -> None:
        """Cadastra nova área de ensino"""
        self._limpar_tela()
        print("\n=== CADASTRAR ÁREA DE ENSINO ===\n")

        try:
            nome = input("Nome da área: ").strip()
            area = self.service_area_ensino.cadastrar(nome)

            print(f"\n✅ Área cadastrada com sucesso!")
            print(f"ID: {area.id_area}")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao cadastrar: {e}")

        self._pausar()

    def _buscar_area_por_id(self) -> None:
        """Busca área por ID"""
        self._limpar_tela()
        print("\n=== BUSCAR ÁREA POR ID ===\n")

        try:
            id_area = int(input("ID da área: ").strip())
            area = self.service_area_ensino.buscar_por_id(id_area)
            print(f"\n✅ Encontrada: {area.nome_area} (ID: {area.id_area})")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Área não encontrada: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _buscar_area_por_nome(self) -> None:
        """Busca área por nome"""
        self._limpar_tela()
        print("\n=== BUSCAR ÁREA POR NOME ===\n")

        try:
            nome = input("Nome da área: ").strip()
            area = self.service_area_ensino.buscar_por_nome(nome)
            print(f"\n✅ Encontrada: {area.nome_area} (ID: {area.id_area})")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Área não encontrada: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _atualizar_area(self) -> None:
        """Atualiza nome de área"""
        self._limpar_tela()
        print("\n=== ATUALIZAR ÁREA ===\n")

        try:
            id_area = int(input("ID da área: ").strip())
            area = self.service_area_ensino.buscar_por_id(id_area)
            print(f"\nNome atual: {area.nome_area}")

            novo_nome = input("Novo nome: ").strip()
            if novo_nome:
                self.service_area_ensino.atualizar(id_area, novo_nome)
                print("\n✅ Área atualizada!")
            else:
                print("\n❌ Nome não pode ser vazio.")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao atualizar: {e}")

        self._pausar()

    def _remover_area(self) -> None:
        """Remove área de ensino"""
        self._limpar_tela()
        print("\n=== REMOVER ÁREA ===\n")

        try:
            id_area = int(input("ID da área a remover: ").strip())
            area = self.service_area_ensino.buscar_por_id(id_area)

            print(f"\nÁrea: {area.nome_area}")
            confirmacao = input("Confirmar remoção? (s/n): ").strip().lower()

            if confirmacao == "s":
                self.service_area_ensino.remover(id_area)
                print("\n✅ Área removida!")
            else:
                print("\n❌ Remoção cancelada.")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    # ==========================
    # MENU DE INSTITUIÇÕES
    # ==========================

    def _menu_instituicoes(self) -> None:
        """Menu de instituições de ensino"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print("         INSTITUIÇÕES DE ENSINO".center(60))
            print("=" * 60)
            print("\n1. Listar Instituições")
            print("2. Cadastrar Instituição (com Área de Ensino)")
            print("3. Adicionar Área a uma Instituição")
            print("4. Listar Áreas de uma Instituição")
            print("5. Remover Área de uma Instituição")
            print("6. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Digite a opção desejada (1-6): ").strip()

            if opcao == "1":
                self._listar_instituicoes()
            elif opcao == "2":
                self._cadastrar_instituicao_com_area()
            elif opcao == "3":
                self._adicionar_area_instituicao()
            elif opcao == "4":
                self._listar_areas_instituicao()
            elif opcao == "5":
                self._remover_area_instituicao()
            elif opcao == "6":
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _listar_instituicoes(self) -> None:
        """Lista todas as instituições"""
        self._limpar_tela()
        print("\n=== INSTITUIÇÕES DE ENSINO ===\n")

        if not self._instituicoes:
            print("Nenhuma instituição cadastrada.")
        else:
            print(f"Total: {len(self._instituicoes)} instituições\n")
            for id_inst, inst in self._instituicoes.items():
                print(f"ID: {id_inst} | {inst['nome']}")
                print(f"   CNPJ: {inst['cnpj']}")
                # Verificar áreas associadas
                areas_inst = self.service_instituicao_area.listar_por_instituicao(id_inst)
                if areas_inst:
                    nomes_areas = []
                    for ai in areas_inst:
                        try:
                            area = self.service_area_ensino.buscar_por_id(ai.id_area)
                            nomes_areas.append(area.nome_area)
                        except:
                            nomes_areas.append(f"ID {ai.id_area}")
                    print(f"   Áreas: {', '.join(nomes_areas)}")
                print("-" * 50)

        self._pausar("\nPressione ENTER para voltar...")

    def _cadastrar_instituicao_com_area(self) -> None:
        """Cadastra instituição criando também área de ensino e vinculação"""
        self._limpar_tela()
        print("\n=== CADASTRAR INSTITUIÇÃO COM ÁREA ===\n")
        print("Este cadastro criará automaticamente:")
        print("  1. A Instituição de Ensino")
        print("  2. A Área de Ensino (se não existir)")
        print("  3. A vinculação Instituição-Área")
        print("\n" + "-" * 40 + "\n")

        try:
            # Dados da instituição
            nome_inst = input("Nome da instituição: ").strip()
            cnpj = input("CNPJ (14 dígitos): ").strip()

            # Verificar se já existe
            for inst in self._instituicoes.values():
                if inst['cnpj'] == cnpj:
                    raise ValueError("Já existe instituição com este CNPJ")

            # Dados da área
            print("\n--- Área de Ensino ---")
            print("(Digite o nome da área ou deixe vazio para pular)")
            nome_area = input("Nome da área de ensino: ").strip()

            # Criar instituição
            id_instituicao = self._proximo_id_instituicao
            self._instituicoes[id_instituicao] = {
                'nome': nome_inst,
                'cnpj': cnpj,
            }
            self._proximo_id_instituicao += 1

            print(f"\n✅ Instituição cadastrada! ID: {id_instituicao}")

            # Criar área se fornecida
            if nome_area:
                try:
                    # Verificar se área já existe
                    area = self.service_area_ensino.buscar_por_nome(nome_area)
                    print(f"   Área '{nome_area}' já existe (ID: {area.id_area})")
                except:
                    # Criar nova área
                    area = self.service_area_ensino.cadastrar(nome_area)
                    print(f"✅ Área '{nome_area}' criada! ID: {area.id_area}")

                # Vincular instituição-área
                try:
                    vinculo = self.service_instituicao_area.cadastrar(
                        id_instituicao=id_instituicao,
                        id_area=area.id_area
                    )
                    print(f"✅ Vinculação Instituição-Área criada! ID: {vinculo.id_instituicao_area}")
                except ValueError as ve:
                    print(f"   Vinculação já existe: {ve}")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao cadastrar: {e}")

        self._pausar()

    def _adicionar_area_instituicao(self) -> None:
        """Adiciona área a uma instituição"""
        self._limpar_tela()
        print("\n=== ADICIONAR ÁREA A INSTITUIÇÃO ===\n")

        # Listar instituições
        if not self._instituicoes:
            print("Nenhuma instituição cadastrada.")
            self._pausar()
            return

        print("Instituições disponíveis:")
        for id_inst, inst in self._instituicoes.items():
            print(f"  ID: {id_inst} | {inst['nome']}")

        # Listar áreas
        print("\nÁreas disponíveis:")
        try:
            areas = self.service_area_ensino.listar_todas()
            for a in areas:
                print(f"  ID: {a.id_area} | {a.nome_area}")
        except:
            print("  (Nenhuma área cadastrada)")

        try:
            print()
            id_instituicao = int(input("ID da instituição: ").strip())
            id_area = int(input("ID da área: ").strip())

            vinculo = self.service_instituicao_area.cadastrar(
                id_instituicao=id_instituicao,
                id_area=id_area
            )

            print(f"\n✅ Área vinculada à instituição! ID: {vinculo.id_instituicao_area}")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    def _listar_areas_instituicao(self) -> None:
        """Lista áreas de uma instituição"""
        self._limpar_tela()
        print("\n=== ÁREAS DA INSTITUIÇÃO ===\n")

        try:
            id_instituicao = int(input("ID da instituição: ").strip())

            if id_instituicao not in self._instituicoes:
                print("\n❌ Instituição não encontrada.")
                self._pausar()
                return

            inst = self._instituicoes[id_instituicao]
            print(f"\nInstituição: {inst['nome']}\n")

            areas_inst = self.service_instituicao_area.listar_por_instituicao(id_instituicao)

            if not areas_inst:
                print("Nenhuma área vinculada.")
            else:
                print(f"Áreas vinculadas: {len(areas_inst)}\n")
                for ai in areas_inst:
                    try:
                        area = self.service_area_ensino.buscar_por_id(ai.id_area)
                        print(f"  ID Vínculo: {ai.id_instituicao_area} | {area.nome_area}")
                    except:
                        print(f"  ID Vínculo: {ai.id_instituicao_area} | Área ID {ai.id_area}")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _remover_area_instituicao(self) -> None:
        """Remove área de uma instituição"""
        self._limpar_tela()
        print("\n=== REMOVER ÁREA DE INSTITUIÇÃO ===\n")

        try:
            id_vinculo = int(input("ID do vínculo instituição-área: ").strip())
            self.service_instituicao_area.remover(id_vinculo)
            print("\n✅ Vínculo removido!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    # ==========================
    # MENU DE CURSOS EAD
    # ==========================

    def _menu_cursos_ead(self) -> None:
        """Menu de cursos EAD"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print("         CURSOS EAD".center(60))
            print("=" * 60)
            print("\n1. Listar Todos os Cursos EAD")
            print("2. Cadastrar Novo Curso EAD")
            print("3. Buscar Curso por ID")
            print("4. Atualizar Curso")
            print("5. Publicar/Pausar Curso")
            print("6. Remover Curso")
            print("7. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Digite a opção desejada (1-7): ").strip()

            if opcao == "1":
                self._listar_cursos_ead()
            elif opcao == "2":
                self._cadastrar_curso_ead()
            elif opcao == "3":
                self._buscar_curso_ead()
            elif opcao == "4":
                self._atualizar_curso_ead()
            elif opcao == "5":
                self._publicar_pausar_curso_ead()
            elif opcao == "6":
                self._remover_curso_ead()
            elif opcao == "7":
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _listar_cursos_ead(self) -> None:
        """Lista cursos EAD"""
        self._limpar_tela()
        print("\n=== CURSOS EAD ===\n")

        try:
            cursos = self.service_curso_ead.listar_todos()
            if not cursos:
                print("Nenhum curso EAD cadastrado.")
            else:
                print(f"Total: {len(cursos)} cursos\n")
                for c in cursos:
                    status = "Ativo" if c.ativo else "Inativo"
                    print(f"ID: {c.id} | {c.nome}")
                    print(f"   Área: {c.area} | Carga: {c.carga_horaria}h")
                    print(f"   Capacidade: {c.capacidade} | Status: {status}")
                    print(f"   URL: {c.plataforma_url}")
                    print("-" * 50)

        except Exception as e:
            print(f"Erro: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _cadastrar_curso_ead(self) -> None:
        """Cadastra curso EAD"""
        self._limpar_tela()
        print("\n=== CADASTRAR CURSO EAD ===\n")

        try:
            nome = input("Nome do curso: ").strip()
            area = input("Área: ").strip()
            carga = int(input("Carga horária (horas): ").strip())
            capacidade = int(input("Capacidade (vagas): ").strip())
            url = input("URL da plataforma: ").strip()

            curso = self.service_curso_ead.cadastrar(
                id_instituicao=self.instituicao_selecionada.id,
                nome=nome,
                area=area,
                carga_horaria=carga,
                capacidade=capacidade,
                plataforma_url=url,
            )

            print(f"\n✅ Curso EAD cadastrado! ID: {curso.id}")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao cadastrar: {e}")

        self._pausar()

    def _buscar_curso_ead(self) -> None:
        """Busca curso EAD por ID"""
        self._limpar_tela()
        print("\n=== BUSCAR CURSO EAD ===\n")

        try:
            id_curso = int(input("ID do curso: ").strip())
            curso = self.service_curso_ead.buscar_por_id(id_curso)

            print(f"\n{curso.nome}")
            print(f"  Área: {curso.area}")
            print(f"  Carga Horária: {curso.carga_horaria}h")
            print(f"  Capacidade: {curso.capacidade}")
            print(f"  Status: {'Ativo' if curso.ativo else 'Inativo'}")
            print(f"  URL: {curso.plataforma_url}")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Curso não encontrado: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _atualizar_curso_ead(self) -> None:
        """Atualiza curso EAD"""
        self._limpar_tela()
        print("\n=== ATUALIZAR CURSO EAD ===\n")

        try:
            id_curso = int(input("ID do curso: ").strip())
            curso = self.service_curso_ead.buscar_por_id(id_curso)

            print(f"\nCurso: {curso.nome}")
            print("\nCampos: nome, area, carga_horaria, capacidade, plataforma_url")
            campo = input("Campo a atualizar: ").strip()
            novo_valor = input("Novo valor: ").strip()

            # Converter se necessário
            if campo in ['carga_horaria', 'capacidade']:
                novo_valor = int(novo_valor)

            self.service_curso_ead.atualizar(id_curso, campo, novo_valor)
            print("\n✅ Curso atualizado!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    def _publicar_pausar_curso_ead(self) -> None:
        """Publica ou pausa curso EAD"""
        self._limpar_tela()
        print("\n=== PUBLICAR/PAUSAR CURSO EAD ===\n")

        try:
            id_curso = int(input("ID do curso: ").strip())
            curso = self.service_curso_ead.buscar_por_id(id_curso)

            print(f"\nCurso: {curso.nome}")
            print(f"Status atual: {'Ativo' if curso.ativo else 'Inativo'}")

            if curso.ativo:
                self.service_curso_ead.pausar(id_curso)
                print("\n✅ Curso pausado!")
            else:
                self.service_curso_ead.publicar(id_curso)
                print("\n✅ Curso publicado!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    def _remover_curso_ead(self) -> None:
        """Remove curso EAD"""
        self._limpar_tela()
        print("\n=== REMOVER CURSO EAD ===\n")

        try:
            id_curso = int(input("ID do curso a remover: ").strip())
            self.service_curso_ead.remover(id_curso)
            print("\n✅ Curso removido!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    # ==========================
    # MENU DE CURSOS PRESENCIAIS
    # ==========================

    def _menu_cursos_presenciais(self) -> None:
        """Menu de cursos presenciais"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print("         CURSOS PRESENCIAIS".center(60))
            print("=" * 60)
            print("\n1. Listar Todos os Cursos Presenciais")
            print("2. Cadastrar Novo Curso Presencial")
            print("3. Buscar Curso por ID")
            print("4. Atualizar Curso")
            print("5. Publicar/Pausar Curso")
            print("6. Remover Curso")
            print("7. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Digite a opção desejada (1-7): ").strip()

            if opcao == "1":
                self._listar_cursos_presenciais()
            elif opcao == "2":
                self._cadastrar_curso_presencial()
            elif opcao == "3":
                self._buscar_curso_presencial()
            elif opcao == "4":
                self._atualizar_curso_presencial()
            elif opcao == "5":
                self._publicar_pausar_curso_presencial()
            elif opcao == "6":
                self._remover_curso_presencial()
            elif opcao == "7":
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _listar_cursos_presenciais(self) -> None:
        """Lista cursos presenciais"""
        self._limpar_tela()
        print("\n=== CURSOS PRESENCIAIS ===\n")

        try:
            cursos = self.service_curso_presencial.listar_todos()
            if not cursos:
                print("Nenhum curso presencial cadastrado.")
            else:
                print(f"Total: {len(cursos)} cursos\n")
                for c in cursos:
                    status = "Ativo" if c.ativo else "Inativo"
                    print(f"ID: {c.id} | {c.nome}")
                    print(f"   Área: {c.area} | Carga: {c.carga_horaria}h")
                    print(f"   Capacidade: {c.capacidade} | Status: {status}")
                    print(f"   Localidade: {c.localidade}")
                    print("-" * 50)

        except Exception as e:
            print(f"Erro: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _cadastrar_curso_presencial(self) -> None:
        """Cadastra curso presencial"""
        self._limpar_tela()
        print("\n=== CADASTRAR CURSO PRESENCIAL ===\n")

        try:
            nome = input("Nome do curso: ").strip()
            area = input("Área: ").strip()
            carga = int(input("Carga horária (horas): ").strip())
            capacidade = int(input("Capacidade (vagas): ").strip())
            localidade = input("Localidade: ").strip()

            curso = self.service_curso_presencial.cadastrar(
                id_instituicao=self.instituicao_selecionada.id,
                nome=nome,
                area=area,
                carga_horaria=carga,
                capacidade=capacidade,
                localidade=localidade,
            )

            print(f"\n✅ Curso presencial cadastrado! ID: {curso.id}")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao cadastrar: {e}")

        self._pausar()

    def _buscar_curso_presencial(self) -> None:
        """Busca curso presencial por ID"""
        self._limpar_tela()
        print("\n=== BUSCAR CURSO PRESENCIAL ===\n")

        try:
            id_curso = int(input("ID do curso: ").strip())
            curso = self.service_curso_presencial.buscar_por_id(id_curso)

            print(f"\n{curso.nome}")
            print(f"  Área: {curso.area}")
            print(f"  Carga Horária: {curso.carga_horaria}h")
            print(f"  Capacidade: {curso.capacidade}")
            print(f"  Status: {'Ativo' if curso.ativo else 'Inativo'}")
            print(f"  Localidade: {curso.localidade}")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Curso não encontrado: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _atualizar_curso_presencial(self) -> None:
        """Atualiza curso presencial"""
        self._limpar_tela()
        print("\n=== ATUALIZAR CURSO PRESENCIAL ===\n")

        try:
            id_curso = int(input("ID do curso: ").strip())
            curso = self.service_curso_presencial.buscar_por_id(id_curso)

            print(f"\nCurso: {curso.nome}")
            print("\nCampos: nome, area, carga_horaria, capacidade, localidade")
            campo = input("Campo a atualizar: ").strip()
            novo_valor = input("Novo valor: ").strip()

            if campo in ['carga_horaria', 'capacidade']:
                novo_valor = int(novo_valor)

            self.service_curso_presencial.atualizar(id_curso, campo, novo_valor)
            print("\n✅ Curso atualizado!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    def _publicar_pausar_curso_presencial(self) -> None:
        """Publica ou pausa curso presencial"""
        self._limpar_tela()
        print("\n=== PUBLICAR/PAUSAR CURSO PRESENCIAL ===\n")

        try:
            id_curso = int(input("ID do curso: ").strip())
            curso = self.service_curso_presencial.buscar_por_id(id_curso)

            print(f"\nCurso: {curso.nome}")
            print(f"Status atual: {'Ativo' if curso.ativo else 'Inativo'}")

            if curso.ativo:
                self.service_curso_presencial.pausar(id_curso)
                print("\n✅ Curso pausado!")
            else:
                self.service_curso_presencial.publicar(id_curso)
                print("\n✅ Curso publicado!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    def _remover_curso_presencial(self) -> None:
        """Remove curso presencial"""
        self._limpar_tela()
        print("\n=== REMOVER CURSO PRESENCIAL ===\n")

        try:
            id_curso = int(input("ID do curso a remover: ").strip())
            self.service_curso_presencial.remover(id_curso)
            print("\n✅ Curso removido!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    # ==========================
    # MENU DE COMPETÊNCIAS DE CURSOS
    # ==========================

    def _menu_curso_competencias(self) -> None:
        """Menu de competências de cursos"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print("         COMPETÊNCIAS DE CURSOS".center(60))
            print("=" * 60)
            print("\n1. Listar Competências de um Curso")
            print("2. Adicionar Competência a um Curso")
            print("3. Atualizar Nível de Competência")
            print("4. Remover Competência de Curso")
            print("5. Listar Cursos que Oferecem uma Competência")
            print("6. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Digite a opção desejada (1-6): ").strip()

            if opcao == "1":
                self._listar_competencias_curso()
            elif opcao == "2":
                self._adicionar_competencia_curso()
            elif opcao == "3":
                self._atualizar_nivel_competencia_curso()
            elif opcao == "4":
                self._remover_competencia_curso()
            elif opcao == "5":
                self._listar_cursos_por_competencia()
            elif opcao == "6":
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _listar_competencias_curso(self) -> None:
        """Lista competências de um curso"""
        self._limpar_tela()
        print("\n=== COMPETÊNCIAS DO CURSO ===\n")

        try:
            id_curso = int(input("ID do curso: ").strip())
            competencias = self.service_curso_competencia.listar_por_curso(id_curso)

            if not competencias:
                print("\nNenhuma competência vinculada a este curso.")
            else:
                print(f"\nCompetências do curso {id_curso}:\n")
                for cc in competencias:
                    nome_comp = self._obter_nome_competencia(cc.id_competencia)
                    print(f"ID: {cc.id} | {nome_comp}")
                    print(f"   Nível Conferido: {cc.nivel_conferido}")
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

    def _adicionar_competencia_curso(self) -> None:
        """Adiciona competência a um curso"""
        self._limpar_tela()
        print("\n=== ADICIONAR COMPETÊNCIA AO CURSO ===\n")

        # Mostrar competências disponíveis
        if self.service_competencia:
            try:
                print("Competências disponíveis:")
                competencias = self.service_competencia.listar_todos()
                for c in competencias[:15]:
                    print(f"  ID: {c.id} | {c.nome}")
                print()
            except:
                pass

        try:
            id_curso = int(input("ID do curso: ").strip())
            id_competencia = int(input("ID da competência: ").strip())
            nivel = input("Nível conferido (iniciante/intermediario/avancado/especialista): ").strip()

            curso_comp = self.service_curso_competencia.cadastrar(
                id_curso=id_curso,
                id_competencia=id_competencia,
                nivel_conferido=nivel,
            )

            print(f"\n✅ Competência adicionada ao curso! ID: {curso_comp.id}")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    def _atualizar_nivel_competencia_curso(self) -> None:
        """Atualiza nível de competência"""
        self._limpar_tela()
        print("\n=== ATUALIZAR NÍVEL DE COMPETÊNCIA ===\n")

        try:
            id_curso_competencia = int(input("ID da competência do curso: ").strip())
            novo_nivel = input("Novo nível (iniciante/intermediario/avancado/especialista): ").strip()

            self.service_curso_competencia.atualizar_nivel(id_curso_competencia, novo_nivel)
            print("\n✅ Nível atualizado!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    def _remover_competencia_curso(self) -> None:
        """Remove competência de curso"""
        self._limpar_tela()
        print("\n=== REMOVER COMPETÊNCIA DO CURSO ===\n")

        try:
            id_curso_competencia = int(input("ID da competência de curso a remover: ").strip())
            self.service_curso_competencia.remover(id_curso_competencia)
            print("\n✅ Competência removida!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    def _listar_cursos_por_competencia(self) -> None:
        """Lista cursos que oferecem uma competência"""
        self._limpar_tela()
        print("\n=== CURSOS QUE OFERECEM COMPETÊNCIA ===\n")

        try:
            id_competencia = int(input("ID da competência: ").strip())
            cursos_comp = self.service_curso_competencia.listar_por_competencia(id_competencia)

            nome_comp = self._obter_nome_competencia(id_competencia)

            if not cursos_comp:
                print(f"\nNenhum curso oferece a competência '{nome_comp}'.")
            else:
                print(f"\nCursos que oferecem '{nome_comp}':\n")
                for cc in cursos_comp:
                    print(f"  Curso ID: {cc.id_curso} | Nível: {cc.nivel_conferido}")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    # ==========================
    # MENU DE INSCRIÇÕES
    # ==========================

    def _menu_inscricoes(self) -> None:
        """Menu de inscrições em cursos"""
        while True:
            self._limpar_tela()
            print("=" * 60)
            print("         INSCRIÇÕES EM CURSOS".center(60))
            print("=" * 60)
            print("\n1. Listar Inscrições de um Curso")
            print("2. Listar Inscrições de um Candidato")
            print("3. Deferir Inscrição")
            print("4. Indeferir Inscrição")
            print("5. Concluir Inscrição (Atribuir Competências)")
            print("6. Voltar")
            print("\n" + "-" * 60)

            opcao = input("Digite a opção desejada (1-6): ").strip()

            if opcao == "1":
                self._listar_inscricoes_por_curso()
            elif opcao == "2":
                self._listar_inscricoes_por_candidato()
            elif opcao == "3":
                self._deferir_inscricao()
            elif opcao == "4":
                self._indeferir_inscricao()
            elif opcao == "5":
                self._concluir_inscricao()
            elif opcao == "6":
                break
            else:
                print("\n❌ Opção inválida!")
                self._pausar()

    def _listar_inscricoes_por_curso(self) -> None:
        """Lista inscrições de um curso"""
        self._limpar_tela()
        print("\n=== INSCRIÇÕES DO CURSO ===\n")

        try:
            id_curso = int(input("ID do curso: ").strip())
            inscricoes = self.service_inscricao_curso.listar_por_curso(id_curso)

            if not inscricoes:
                print("\nNenhuma inscrição neste curso.")
            else:
                print(f"\nInscrições do curso {id_curso}:\n")
                for i in inscricoes:
                    status = i.status.name if hasattr(i.status, 'name') else i.status
                    print(f"ID: {i.id} | Candidato: {i.id_aluno} | Status: {status}")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _listar_inscricoes_por_candidato(self) -> None:
        """Lista inscrições de um candidato"""
        self._limpar_tela()
        print("\n=== INSCRIÇÕES DO CANDIDATO ===\n")

        try:
            id_candidato = int(input("ID do candidato: ").strip())
            inscricoes = self.service_inscricao_curso.listar_por_candidato(id_candidato)

            if not inscricoes:
                print("\nNenhuma inscrição deste candidato.")
            else:
                print(f"\nInscrições do candidato {id_candidato}:\n")
                for i in inscricoes:
                    status = i.status.name if hasattr(i.status, 'name') else i.status
                    print(f"ID: {i.id} | Curso: {i.id_curso} | Status: {status}")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar("\nPressione ENTER para voltar...")

    def _deferir_inscricao(self) -> None:
        """Defere uma inscrição"""
        self._limpar_tela()
        print("\n=== DEFERIR INSCRIÇÃO ===\n")

        try:
            id_inscricao = int(input("ID da inscrição: ").strip())

            if hasattr(self.service_inscricao_curso, 'deferir'):
                self.service_inscricao_curso.deferir(id_inscricao)
            else:
                # Fallback: atualizar status manualmente
                inscricao = self.service_inscricao_curso.buscar_por_id(id_inscricao)
                inscricao.deferir()
                # Salvar

            print("\n✅ Inscrição deferida!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    def _indeferir_inscricao(self) -> None:
        """Indefere uma inscrição"""
        self._limpar_tela()
        print("\n=== INDEFERIR INSCRIÇÃO ===\n")

        try:
            id_inscricao = int(input("ID da inscrição: ").strip())

            if hasattr(self.service_inscricao_curso, 'indeferir'):
                self.service_inscricao_curso.indeferir(id_inscricao)
            else:
                inscricao = self.service_inscricao_curso.buscar_por_id(id_inscricao)
                inscricao.indeferir()

            print("\n✅ Inscrição indeferida!")

        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")

        self._pausar()

    def _concluir_inscricao(self) -> None:
        """Conclui inscrição e atribui competências"""
        self._limpar_tela()
        print("\n=== CONCLUIR INSCRIÇÃO ===\n")

        try:
            id_inscricao = int(input("ID da inscrição: ").strip())
            competencias = self.service_inscricao_curso.concluir_inscricao(id_inscricao)

            print("\n✅ Inscrição concluída!")

            if competencias:
                print(f"\n🎓 Competências atribuídas: {len(competencias)}")
                for comp in competencias:
                    nome = self._obter_nome_competencia(comp.id_competencia)
                    print(f"   • {nome} - Nível: {comp.nivel_atual}")
            else:
                print("\nℹ️  Nenhuma competência atribuída (curso sem competências).")

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
        print("BACK OFFICE DE INSTITUIÇÕES ENCERRADO".center(60))
        print("=" * 60)
        print("\nAté logo!\n")