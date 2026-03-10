"""
Fluxo de Instituição de Ensino - Gerencia a navegação e ações da instituição na plataforma
"""

import os
from datetime import date
from typing import Optional
from src.dominio.instituicao_ensino import InstituicaoEnsino
from src.dominio.curso_competencia import TipoCursoCompetencia
from src.services.service_instituicao_ensino import ServiceInstituicaoEnsino
from src.services.service_curso_ead import CursoEADService
from src.services.service_curso_presencial import CursoPresencialService
from src.services.service_curso_competencia import CursoCompetenciaService
from src.services.service_inscricao_curso import InscricaoCursoService
from src.services.service_competencia import CompetenciaService
from src.services.service_area_ensino import AreaEnsinoService
from src.services.service_instituicao_area_ensino import InstituicaoAreaEnsinoService


class FluxoInstituicao:
    """Orquestra o fluxo completo de instituições de ensino na plataforma"""

    def __init__(
        self,
        service_instituicao: ServiceInstituicaoEnsino,
        service_curso_ead: Optional[CursoEADService] = None,
        service_curso_presencial: Optional[CursoPresencialService] = None,
        service_curso_competencia: Optional[CursoCompetenciaService] = None,
        service_inscricao_curso: Optional[InscricaoCursoService] = None,
        service_competencia: Optional[CompetenciaService] = None,
        service_area_ensino: Optional[AreaEnsinoService] = None,
        service_instituicao_area: Optional[InstituicaoAreaEnsinoService] = None,
    ):
        """
        Inicializa o fluxo de instituição
        
        Args:
            service_instituicao: Serviço de instituições de ensino
            service_curso_ead: Serviço de cursos EAD
            service_curso_presencial: Serviço de cursos presenciais
            service_curso_competencia: Serviço de competências de cursos
            service_inscricao_curso: Serviço de inscrições em cursos
            service_competencia: Serviço de competências
            service_area_ensino: Serviço de áreas de ensino
            service_instituicao_area: Serviço de relação instituição-área
        """
        self.service = service_instituicao
        self.service_curso_ead = service_curso_ead
        self.service_curso_presencial = service_curso_presencial
        self.service_curso_competencia = service_curso_competencia
        self.service_inscricao_curso = service_inscricao_curso
        self.service_competencia = service_competencia
        self.service_area_ensino = service_area_ensino
        self.service_instituicao_area = service_instituicao_area
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
            instituicao = self.service.buscar_por_id(id_instituicao)
            
            if instituicao:
                self.instituicao_logada = instituicao
                self._limpar_tela()
                print(f"\n✅ Login realizado com sucesso!")
                print(f"Bem-vindo, {instituicao.nome_fantasia}!\n")
                input("Pressione ENTER para continuar...")
            else:
                self._limpar_tela()
                print("\n❌ Instituição não encontrada!")
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
            nome = input("Nome (fantasia): ").strip()
            razao_social = input("Razão Social: ").strip()
            nome_fantasia = input("Nome Fantasia: ").strip()
            cnpj = input("CNPJ (14 dígitos): ").strip()
            registro_educacional = input("Registro Educacional: ").strip()
            tipo = input("Tipo (Pública/Privada): ").strip().capitalize()
            modalidades = input("Modalidades (separadas por vírgula, ex: Presencial,EAD): ").strip().split(",")
            modalidades = [mod.strip() for mod in modalidades]
            email = input("Email: ").strip()
            telefone = input("Telefone: ").strip()
            endereco = input("Endereço: ").strip()
            website = input("Website (opcional): ").strip()

            # Obter próximo ID
            todas = self.service.listar()
            novo_id = 1 if not todas else max(i.id for i in todas) + 1

            instituicao = InstituicaoEnsino(
                id=novo_id,
                nome=nome,
                razao_social=razao_social,
                nome_fantasia=nome_fantasia,
                _cnpj=cnpj,
                registro_educacional=registro_educacional,
                tipo=tipo,
                modalidades=modalidades,
                credenciada=True,
                email=email,
                telefone=telefone,
                endereco=endereco,
                website=website,
            )

            self.service.criar_conta(instituicao)
            self.instituicao_logada = instituicao

            self._limpar_tela()
            print(f"\n✅ Cadastro realizado com sucesso!")
            print(f"ID da instituição: {instituicao.id}")
            print(f"Bem-vindo, {instituicao.nome_fantasia}!\n")
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
            5: self._gerenciar_areas_ensino,
            6: self._ver_perfil,
            7: lambda: None  # Sair
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
        print("5. Gerenciar Áreas de Ensino")
        print("6. Perfil da Instituição")
        print("7. Sair")
        print("\n" + "-" * 60)

        opcao = input("Digite a opção desejada (1-7): ").strip()
        return opcao

    def _publicar_curso(self) -> None:
        """Menu para publicar novo curso"""
        self._limpar_tela()
        print("\n=== PUBLICAR NOVO CURSO ===\n")
        print("Selecione a modalidade:")
        print("  1. Curso EAD")
        print("  2. Curso Presencial")
        print("  3. Voltar")
        
        opcao = input("\nEscolha (1-3): ").strip()
        
        if opcao == "1":
            self._publicar_curso_ead()
        elif opcao == "2":
            self._publicar_curso_presencial()

    def _publicar_curso_ead(self) -> None:
        """Publica um novo curso EAD"""
        if not self.service_curso_ead:
            print("\n❌ Serviço de cursos EAD não disponível")
            input("Pressione ENTER...")
            return

        self._limpar_tela()
        print("\n=== PUBLICAR CURSO EAD ===\n")

        try:
            nome = input("Nome do curso: ").strip()
            area = input("Área (ex: Tecnologia, Saúde): ").strip()
            carga_horaria = int(input("Carga horária (horas): ").strip())
            capacidade = int(input("Capacidade máxima de alunos: ").strip())
            plataforma_url = input("URL da plataforma EAD: ").strip()
            
            prazo_str = input("Prazo de inscrição (AAAA-MM-DD) ou ENTER para sem prazo: ").strip()
            prazo = date.fromisoformat(prazo_str) if prazo_str else None

            curso = self.service_curso_ead.cadastrar(
                id_instituicao=self.instituicao_logada.id,
                nome=nome,
                area=area,
                carga_horaria=carga_horaria,
                capacidade=capacidade,
                plataforma_url=plataforma_url,
                prazo_inscricao=prazo,
            )

            self._limpar_tela()
            print(f"\n✅ Curso EAD publicado com sucesso!")
            print(f"ID do curso: {curso.id}")
            print(f"Nome: {curso.nome}")
            
            # Adicionar competências
            self._adicionar_competencias_curso(curso.id, TipoCursoCompetencia.EAD)

        except ValueError as e:
            print(f"\n❌ Erro de validação: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao publicar curso: {e}")
        input("\nPressione ENTER para voltar...")

    def _publicar_curso_presencial(self) -> None:
        """Publica um novo curso presencial"""
        if not self.service_curso_presencial:
            print("\n❌ Serviço de cursos presenciais não disponível")
            input("Pressione ENTER...")
            return

        self._limpar_tela()
        print("\n=== PUBLICAR CURSO PRESENCIAL ===\n")

        try:
            nome = input("Nome do curso: ").strip()
            area = input("Área (ex: Tecnologia, Saúde): ").strip()
            carga_horaria = int(input("Carga horária (horas): ").strip())
            capacidade = int(input("Capacidade máxima de alunos: ").strip())
            localidade = input("Localidade (cidade): ").strip()
            
            prazo_str = input("Prazo de inscrição (AAAA-MM-DD) ou ENTER para sem prazo: ").strip()
            prazo = date.fromisoformat(prazo_str) if prazo_str else None

            curso = self.service_curso_presencial.cadastrar(
                id_instituicao=self.instituicao_logada.id,
                nome=nome,
                area=area,
                carga_horaria=carga_horaria,
                capacidade=capacidade,
                localidade=localidade,
                prazo_inscricao=prazo,
            )

            self._limpar_tela()
            print(f"\n✅ Curso presencial publicado com sucesso!")
            print(f"ID do curso: {curso.id}")
            print(f"Nome: {curso.nome}")
            
            # Adicionar competências
            self._adicionar_competencias_curso(curso.id, TipoCursoCompetencia.PRESENCIAL)

        except ValueError as e:
            print(f"\n❌ Erro de validação: {e}")
        except Exception as e:
            print(f"\n❌ Erro ao publicar curso: {e}")
        input("\nPressione ENTER para voltar...")

    def _adicionar_competencias_curso(self, id_curso: int, tipo_curso: TipoCursoCompetencia) -> None:
        """Adiciona competências a um curso"""
        if not self.service_curso_competencia or not self.service_competencia:
            return
        
        add_comp = input("\nDeseja adicionar competências ao curso? (s/n): ").strip().lower()
        while add_comp == "s":
            try:
                competencias = self.service_competencia.listar_todos()
                if not competencias:
                    print("\n⚠️  Nenhuma competência cadastrada no sistema.")
                    break
                
                print("\n--- Competências disponíveis ---")
                for c in competencias:
                    print(f"  {c.id}. {c.nome}")
                
                id_comp = int(input("ID da competência: ").strip())
                print("\nNível conferido pelo curso:")
                print("  1. Iniciante")
                print("  2. Intermediário")
                print("  3. Avançado")
                opt_nivel = input("Escolha (1-3): ").strip()
                niveis = {"1": "iniciante", "2": "intermediario", "3": "avancado"}
                nivel = niveis.get(opt_nivel, "iniciante")
                
                self.service_curso_competencia.cadastrar(
                    id_curso=id_curso,
                    id_competencia=id_comp,
                    nivel_conferido=nivel,
                    tipo_curso=tipo_curso,
                )
                print("✅ Competência adicionada!")
            except Exception as e:
                print(f"❌ Erro: {e}")
            
            add_comp = input("\nAdicionar outra competência? (s/n): ").strip().lower()

    def _gerenciar_cursos(self) -> None:
        """Menu para gerenciar cursos publicados"""
        while True:
            self._limpar_tela()
            print("\n=== GERENCIAR CURSOS ===\n")
            print("1. Listar meus cursos EAD")
            print("2. Listar meus cursos presenciais")
            print("3. Ver detalhes de um curso EAD")
            print("4. Ver detalhes de um curso presencial")
            print("5. Adicionar competência a curso")
            print("6. Encerrar curso EAD")
            print("7. Encerrar curso presencial")
            print("8. Voltar")
            
            opcao = input("\nEscolha (1-8): ").strip()
            
            if opcao == "1":
                self._listar_cursos_ead()
            elif opcao == "2":
                self._listar_cursos_presenciais()
            elif opcao == "3":
                self._ver_detalhes_curso_ead()
            elif opcao == "4":
                self._ver_detalhes_curso_presencial()
            elif opcao == "5":
                self._adicionar_competencia_curso_existente()
            elif opcao == "6":
                self._encerrar_curso_ead()
            elif opcao == "7":
                self._encerrar_curso_presencial()
            elif opcao == "8":
                break

    def _listar_cursos_ead(self) -> None:
        """Lista cursos EAD da instituição"""
        if not self.service_curso_ead:
            print("\n❌ Serviço não disponível")
            input("Pressione ENTER...")
            return
        
        self._limpar_tela()
        print("\n=== MEUS CURSOS EAD ===\n")
        
        try:
            cursos = self.service_curso_ead.listar_por_instituicao(self.instituicao_logada.id)
            if not cursos:
                print("Nenhum curso EAD cadastrado.")
            else:
                for c in cursos:
                    status = "✅ Ativo" if c.ativo else "⏸️ Pausado"
                    print(f"  ID: {c.id} | {c.nome} | {c.carga_horaria}h | {status}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione ENTER para voltar...")

    def _listar_cursos_presenciais(self) -> None:
        """Lista cursos presenciais da instituição"""
        if not self.service_curso_presencial:
            print("\n❌ Serviço não disponível")
            input("Pressione ENTER...")
            return
        
        self._limpar_tela()
        print("\n=== MEUS CURSOS PRESENCIAIS ===\n")
        
        try:
            cursos = self.service_curso_presencial.listar_por_instituicao(self.instituicao_logada.id)
            if not cursos:
                print("Nenhum curso presencial cadastrado.")
            else:
                for c in cursos:
                    status = "✅ Ativo" if c.ativo else "⏸️ Pausado"
                    print(f"  ID: {c.id} | {c.nome} | {c.localidade} | {c.carga_horaria}h | {status}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione ENTER para voltar...")

    def _ver_detalhes_curso_ead(self) -> None:
        """Mostra detalhes de um curso EAD"""
        if not self.service_curso_ead:
            print("\n❌ Serviço não disponível")
            input("Pressione ENTER...")
            return
        
        try:
            id_curso = int(input("ID do curso EAD: ").strip())
            curso = self.service_curso_ead.buscar_por_id(id_curso)
            
            if not curso or curso.id_instituicao != self.instituicao_logada.id:
                print("\n❌ Curso não encontrado ou não pertence a esta instituição")
            else:
                self._limpar_tela()
                print("\n=== DETALHES DO CURSO EAD ===\n")
                print(f"ID: {curso.id}")
                print(f"Nome: {curso.nome}")
                print(f"Área: {curso.area}")
                print(f"Carga Horária: {curso.carga_horaria}h")
                print(f"Capacidade: {curso.capacidade} alunos")
                print(f"Plataforma: {curso.plataforma_url}")
                print(f"Prazo Inscrição: {curso.prazo_inscricao or 'Sem prazo'}")
                print(f"Status: {'Ativo' if curso.ativo else 'Pausado'}")
                
                # Listar competências do curso
                if self.service_curso_competencia:
                    comps = self.service_curso_competencia.listar_por_curso(id_curso)
                    if comps:
                        print("\nCompetências conferidas:")
                        for cc in comps:
                            print(f"  - ID Comp: {cc.id_competencia} | Nível: {cc.nivel_conferido}")
        except ValueError:
            print("\n❌ ID inválido")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        input("\nPressione ENTER para voltar...")

    def _ver_detalhes_curso_presencial(self) -> None:
        """Mostra detalhes de um curso presencial"""
        if not self.service_curso_presencial:
            print("\n❌ Serviço não disponível")
            input("Pressione ENTER...")
            return
        
        try:
            id_curso = int(input("ID do curso presencial: ").strip())
            curso = self.service_curso_presencial.buscar_por_id(id_curso)
            
            if not curso or curso.id_instituicao != self.instituicao_logada.id:
                print("\n❌ Curso não encontrado ou não pertence a esta instituição")
            else:
                self._limpar_tela()
                print("\n=== DETALHES DO CURSO PRESENCIAL ===\n")
                print(f"ID: {curso.id}")
                print(f"Nome: {curso.nome}")
                print(f"Área: {curso.area}")
                print(f"Carga Horária: {curso.carga_horaria}h")
                print(f"Capacidade: {curso.capacidade} alunos")
                print(f"Localidade: {curso.localidade}")
                print(f"Prazo Inscrição: {curso.prazo_inscricao or 'Sem prazo'}")
                print(f"Status: {'Ativo' if curso.ativo else 'Pausado'}")
                
                # Listar competências do curso
                if self.service_curso_competencia:
                    comps = self.service_curso_competencia.listar_por_curso(id_curso)
                    if comps:
                        print("\nCompetências conferidas:")
                        for cc in comps:
                            print(f"  - ID Comp: {cc.id_competencia} | Nível: {cc.nivel_conferido}")
        except ValueError:
            print("\n❌ ID inválido")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        input("\nPressione ENTER para voltar...")

    def _adicionar_competencia_curso_existente(self) -> None:
        """Adiciona competência a um curso existente"""
        if not self.service_curso_competencia or not self.service_competencia:
            print("\n❌ Serviços não disponíveis")
            input("Pressione ENTER...")
            return
        
        print("\nTipo do curso:")
        print("  1. EAD")
        print("  2. Presencial")
        tipo_opt = input("Escolha (1-2): ").strip()
        tipo_curso = TipoCursoCompetencia.EAD if tipo_opt == "1" else TipoCursoCompetencia.PRESENCIAL
        
        try:
            id_curso = int(input("ID do curso: ").strip())
            self._adicionar_competencias_curso(id_curso, tipo_curso)
        except ValueError:
            print("\n❌ ID inválido")
            input("Pressione ENTER...")

    def _encerrar_curso_ead(self) -> None:
        """Encerra um curso EAD, concluindo inscrições e atribuindo competências"""
        if not self.service_inscricao_curso or not self.service_curso_ead:
            print("\n❌ Serviços não disponíveis")
            input("Pressione ENTER...")
            return
        
        self._limpar_tela()
        print("\n=== ENCERRAR CURSO EAD ===\n")
        
        try:
            # Listar cursos EAD ativos da instituição
            cursos = self.service_curso_ead.listar_por_instituicao(self.instituicao_logada.id)
            cursos_ativos = [c for c in cursos if c.ativo]
            
            if not cursos_ativos:
                print("Nenhum curso EAD ativo para encerrar.")
                input("\nPressione ENTER para voltar...")
                return
            
            print("--- Cursos EAD Ativos ---")
            for c in cursos_ativos:
                print(f"  ID: {c.id} | {c.nome}")
            
            id_curso = int(input("\nID do curso a encerrar: ").strip())
            
            # Verificar se o curso pertence à instituição
            curso = next((c for c in cursos_ativos if c.id == id_curso), None)
            if not curso:
                print("\n❌ Curso não encontrado ou não está ativo.")
                input("Pressione ENTER para voltar...")
                return
            
            # Confirmar encerramento
            print(f"\n⚠️  ATENÇÃO: Você está prestes a encerrar o curso '{curso.nome}'.")
            print("Isso irá:")
            print("  - Concluir todas as inscrições deferidas")
            print("  - Atribuir as competências do curso a todos os alunos inscritos")
            print("  - Desativar o curso para novas inscrições")
            
            confirmacao = input("\nDigite 'ENCERRAR' para confirmar: ").strip()
            
            if confirmacao != "ENCERRAR":
                print("\n❌ Encerramento cancelado.")
                input("Pressione ENTER para voltar...")
                return
            
            # Encerrar curso
            from src.dominio.inscricao_curso import TipoCursoInscricao
            resultado = self.service_inscricao_curso.encerrar_curso(id_curso, TipoCursoInscricao.EAD)
            
            print(f"\n✅ Curso encerrado com sucesso!")
            print(f"   - Alunos inscritos: {resultado['total_inscritos']}")
            print(f"   - Alunos concluídos: {resultado['concluidos']}")
            print(f"   - Competências atribuídas: {resultado['competencias_atribuidas']}")
            
        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
        
        input("\nPressione ENTER para voltar...")

    def _encerrar_curso_presencial(self) -> None:
        """Encerra um curso presencial, concluindo inscrições e atribuindo competências"""
        if not self.service_inscricao_curso or not self.service_curso_presencial:
            print("\n❌ Serviços não disponíveis")
            input("Pressione ENTER...")
            return
        
        self._limpar_tela()
        print("\n=== ENCERRAR CURSO PRESENCIAL ===\n")
        
        try:
            # Listar cursos presenciais ativos da instituição
            cursos = self.service_curso_presencial.listar_por_instituicao(self.instituicao_logada.id)
            cursos_ativos = [c for c in cursos if c.ativo]
            
            if not cursos_ativos:
                print("Nenhum curso presencial ativo para encerrar.")
                input("\nPressione ENTER para voltar...")
                return
            
            print("--- Cursos Presenciais Ativos ---")
            for c in cursos_ativos:
                print(f"  ID: {c.id} | {c.nome} | {c.localidade}")
            
            id_curso = int(input("\nID do curso a encerrar: ").strip())
            
            # Verificar se o curso pertence à instituição
            curso = next((c for c in cursos_ativos if c.id == id_curso), None)
            if not curso:
                print("\n❌ Curso não encontrado ou não está ativo.")
                input("Pressione ENTER para voltar...")
                return
            
            # Confirmar encerramento
            print(f"\n⚠️  ATENÇÃO: Você está prestes a encerrar o curso '{curso.nome}'.")
            print("Isso irá:")
            print("  - Concluir todas as inscrições deferidas")
            print("  - Atribuir as competências do curso a todos os alunos inscritos")
            print("  - Desativar o curso para novas inscrições")
            
            confirmacao = input("\nDigite 'ENCERRAR' para confirmar: ").strip()
            
            if confirmacao != "ENCERRAR":
                print("\n❌ Encerramento cancelado.")
                input("Pressione ENTER para voltar...")
                return
            
            # Encerrar curso
            from src.dominio.inscricao_curso import TipoCursoInscricao
            resultado = self.service_inscricao_curso.encerrar_curso(id_curso, TipoCursoInscricao.PRESENCIAL)
            
            print(f"\n✅ Curso encerrado com sucesso!")
            print(f"   - Alunos inscritos: {resultado['total_inscritos']}")
            print(f"   - Alunos concluídos: {resultado['concluidos']}")
            print(f"   - Competências atribuídas: {resultado['competencias_atribuidas']}")
            
        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro inesperado: {e}")
        
        input("\nPressione ENTER para voltar...")

    def _ver_inscritos(self) -> None:
        """Menu para ver inscritos nos cursos"""
        while True:
            self._limpar_tela()
            print("\n=== VER INSCRITOS ===\n")
            print("1. Listar inscritos em curso EAD")
            print("2. Listar inscritos em curso presencial")
            print("3. Ver detalhes de uma inscrição")
            print("4. Voltar")
            
            opcao = input("\nEscolha (1-4): ").strip()
            
            if opcao == "1":
                self._listar_inscritos_ead()
            elif opcao == "2":
                self._listar_inscritos_presencial()
            elif opcao == "3":
                self._ver_detalhes_inscricao()
            elif opcao == "4":
                break

    def _listar_inscritos_ead(self) -> None:
        """Lista inscritos em um curso EAD"""
        if not self.service_inscricao_curso or not self.service_curso_ead:
            print("\n❌ Serviços não disponíveis")
            input("Pressione ENTER...")
            return
        
        try:
            # Primeiro listar cursos EAD da instituição
            cursos = self.service_curso_ead.listar_por_instituicao(self.instituicao_logada.id)
            if not cursos:
                print("\n⚠️ Nenhum curso EAD cadastrado.")
                input("Pressione ENTER...")
                return
            
            print("\n--- Meus Cursos EAD ---")
            for c in cursos:
                print(f"  ID: {c.id} | {c.nome}")
            
            id_curso = int(input("\nID do curso: ").strip())
            
            self._limpar_tela()
            print(f"\n=== INSCRITOS NO CURSO EAD ID {id_curso} ===\n")
            
            inscritos = self.service_inscricao_curso.listar_por_curso(id_curso)
            if not inscritos:
                print("Nenhum inscrito neste curso.")
            else:
                for i in inscritos:
                    print(f"  ID Inscrição: {i.id} | Aluno ID: {i.id_aluno} | Data: {i.data_inscricao} | Status: {i.status.value}")
        except ValueError:
            print("\n❌ ID inválido")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        input("\nPressione ENTER para voltar...")

    def _listar_inscritos_presencial(self) -> None:
        """Lista inscritos em um curso presencial"""
        if not self.service_inscricao_curso or not self.service_curso_presencial:
            print("\n❌ Serviços não disponíveis")
            input("Pressione ENTER...")
            return
        
        try:
            # Primeiro listar cursos presenciais da instituição
            cursos = self.service_curso_presencial.listar_por_instituicao(self.instituicao_logada.id)
            if not cursos:
                print("\n⚠️ Nenhum curso presencial cadastrado.")
                input("Pressione ENTER...")
                return
            
            print("\n--- Meus Cursos Presenciais ---")
            for c in cursos:
                print(f"  ID: {c.id} | {c.nome}")
            
            id_curso = int(input("\nID do curso: ").strip())
            
            self._limpar_tela()
            print(f"\n=== INSCRITOS NO CURSO PRESENCIAL ID {id_curso} ===\n")
            
            inscritos = self.service_inscricao_curso.listar_por_curso(id_curso)
            if not inscritos:
                print("Nenhum inscrito neste curso.")
            else:
                for i in inscritos:
                    print(f"  ID Inscrição: {i.id} | Aluno ID: {i.id_aluno} | Data: {i.data_inscricao} | Status: {i.status.value}")
        except ValueError:
            print("\n❌ ID inválido")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        input("\nPressione ENTER para voltar...")

    def _ver_detalhes_inscricao(self) -> None:
        """Mostra detalhes de uma inscrição"""
        if not self.service_inscricao_curso:
            print("\n❌ Serviço não disponível")
            input("Pressione ENTER...")
            return
        
        try:
            id_inscricao = int(input("ID da inscrição: ").strip())
            inscricao = self.service_inscricao_curso.buscar_por_id(id_inscricao)
            
            if not inscricao:
                print("\n❌ Inscrição não encontrada")
            else:
                self._limpar_tela()
                print("\n=== DETALHES DA INSCRIÇÃO ===\n")
                print(f"ID: {inscricao.id}")
                print(f"ID Aluno: {inscricao.id_aluno}")
                print(f"ID Curso: {inscricao.id_curso}")
                print(f"Data Inscrição: {inscricao.data_inscricao}")
                print(f"Status: {inscricao.status.value}")
        except ValueError:
            print("\n❌ ID inválido")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        input("\nPressione ENTER para voltar...")

    def _gerenciar_competencias(self) -> None:
        """Menu para gerenciar competências dos cursos"""
        while True:
            self._limpar_tela()
            print("\n=== GERENCIAR COMPETÊNCIAS ===\n")
            print("1. Listar todas as competências")
            print("2. Ver competências de um curso EAD")
            print("3. Ver competências de um curso presencial")
            print("4. Adicionar competência a curso")
            print("5. Voltar")
            
            opcao = input("\nEscolha (1-5): ").strip()
            
            if opcao == "1":
                self._listar_todas_competencias()
            elif opcao == "2":
                self._ver_competencias_curso_ead()
            elif opcao == "3":
                self._ver_competencias_curso_presencial()
            elif opcao == "4":
                self._adicionar_competencia_curso_existente()
            elif opcao == "5":
                break

    def _listar_todas_competencias(self) -> None:
        """Lista todas as competências cadastradas no sistema"""
        if not self.service_competencia:
            print("\n❌ Serviço não disponível")
            input("Pressione ENTER...")
            return
        
        self._limpar_tela()
        print("\n=== COMPETÊNCIAS DISPONÍVEIS ===\n")
        
        try:
            competencias = self.service_competencia.listar_todos()
            if not competencias:
                print("Nenhuma competência cadastrada no sistema.")
            else:
                for c in competencias:
                    print(f"  ID: {c.id} | {c.nome} | {c.descricao or 'Sem descrição'}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione ENTER para voltar...")

    def _ver_competencias_curso_ead(self) -> None:
        """Lista competências de um curso EAD"""
        if not self.service_curso_competencia or not self.service_curso_ead:
            print("\n❌ Serviços não disponíveis")
            input("Pressione ENTER...")
            return
        
        try:
            # Listar cursos EAD da instituição
            cursos = self.service_curso_ead.listar_por_instituicao(self.instituicao_logada.id)
            if not cursos:
                print("\n⚠️ Nenhum curso EAD cadastrado.")
                input("Pressione ENTER...")
                return
            
            print("\n--- Meus Cursos EAD ---")
            for c in cursos:
                print(f"  ID: {c.id} | {c.nome}")
            
            id_curso = int(input("\nID do curso: ").strip())
            
            self._limpar_tela()
            print(f"\n=== COMPETÊNCIAS DO CURSO EAD ID {id_curso} ===\n")
            
            comps = self.service_curso_competencia.listar_por_curso(id_curso)
            if not comps:
                print("Nenhuma competência associada a este curso.")
            else:
                for cc in comps:
                    print(f"  ID Competência: {cc.id_competencia} | Nível: {cc.nivel_conferido}")
        except ValueError:
            print("\n❌ ID inválido")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        input("\nPressione ENTER para voltar...")

    def _ver_competencias_curso_presencial(self) -> None:
        """Lista competências de um curso presencial"""
        if not self.service_curso_competencia or not self.service_curso_presencial:
            print("\n❌ Serviços não disponíveis")
            input("Pressione ENTER...")
            return
        
        try:
            # Listar cursos presenciais da instituição
            cursos = self.service_curso_presencial.listar_por_instituicao(self.instituicao_logada.id)
            if not cursos:
                print("\n⚠️ Nenhum curso presencial cadastrado.")
                input("Pressione ENTER...")
                return
            
            print("\n--- Meus Cursos Presenciais ---")
            for c in cursos:
                print(f"  ID: {c.id} | {c.nome}")
            
            id_curso = int(input("\nID do curso: ").strip())
            
            self._limpar_tela()
            print(f"\n=== COMPETÊNCIAS DO CURSO PRESENCIAL ID {id_curso} ===\n")
            
            comps = self.service_curso_competencia.listar_por_curso(id_curso)
            if not comps:
                print("Nenhuma competência associada a este curso.")
            else:
                for cc in comps:
                    print(f"  ID Competência: {cc.id_competencia} | Nível: {cc.nivel_conferido}")
        except ValueError:
            print("\n❌ ID inválido")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        input("\nPressione ENTER para voltar...")

    def _gerenciar_areas_ensino(self) -> None:
        """Menu para gerenciar áreas de ensino da instituição"""
        while True:
            self._limpar_tela()
            print("\n=== GERENCIAR ÁREAS DE ENSINO ===\n")
            print("1. Listar todas as áreas de ensino")
            print("2. Ver minhas áreas")
            print("3. Adicionar área à instituição")
            print("4. Voltar")
            
            opcao = input("\nEscolha (1-4): ").strip()
            
            if opcao == "1":
                self._listar_todas_areas()
            elif opcao == "2":
                self._listar_minhas_areas()
            elif opcao == "3":
                self._adicionar_area_instituicao()
            elif opcao == "4":
                break

    def _listar_todas_areas(self) -> None:
        """Lista todas as áreas de ensino disponíveis"""
        if not self.service_area_ensino:
            print("\n❌ Serviço não disponível")
            input("Pressione ENTER...")
            return
        
        self._limpar_tela()
        print("\n=== ÁREAS DE ENSINO DISPONÍVEIS ===\n")
        
        try:
            areas = self.service_area_ensino.listar_todas()
            if not areas:
                print("Nenhuma área de ensino cadastrada no sistema.")
            else:
                for a in areas:
                    print(f"  ID: {a.id_area} | {a.nome_area}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione ENTER para voltar...")

    def _listar_minhas_areas(self) -> None:
        """Lista áreas de ensino vinculadas à instituição"""
        if not self.service_instituicao_area or not self.service_area_ensino:
            print("\n❌ Serviços não disponíveis")
            input("Pressione ENTER...")
            return
        
        self._limpar_tela()
        print("\n=== MINHAS ÁREAS DE ENSINO ===\n")
        
        try:
            relacoes = self.service_instituicao_area.listar_por_instituicao(self.instituicao_logada.id)
            if not relacoes:
                print("A instituição não possui áreas de ensino cadastradas.")
            else:
                for rel in relacoes:
                    try:
                        area = self.service_area_ensino.buscar_por_id(rel.id_area)
                        print(f"  ID: {rel.id_instituicao_area} | Área: {area.nome_area}")
                    except:
                        print(f"  ID: {rel.id_instituicao_area} | Área ID: {rel.id_area}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        input("\nPressione ENTER para voltar...")

    def _adicionar_area_instituicao(self) -> None:
        """Adiciona uma área de ensino à instituição"""
        if not self.service_instituicao_area or not self.service_area_ensino:
            print("\n❌ Serviços não disponíveis")
            input("Pressione ENTER...")
            return
        
        self._limpar_tela()
        print("\n=== ADICIONAR ÁREA DE ENSINO ===\n")
        
        try:
            # Listar áreas disponíveis
            areas = self.service_area_ensino.listar_todas()
            if not areas:
                print("⚠️ Nenhuma área de ensino cadastrada no sistema.")
                input("Pressione ENTER...")
                return
            
            print("--- Áreas disponíveis ---")
            for a in areas:
                print(f"  {a.id_area}. {a.nome_area}")
            
            id_area = int(input("\nID da área a adicionar: ").strip())
            
            self.service_instituicao_area.cadastrar(
                id_instituicao=self.instituicao_logada.id,
                id_area=id_area
            )
            print("\n✅ Área adicionada com sucesso!")
        except ValueError as e:
            print(f"\n❌ Erro: {e}")
        except Exception as e:
            print(f"\n❌ Erro: {e}")
        input("Pressione ENTER para continuar...")

    def _ver_perfil(self) -> None:
        """Exibe o perfil da instituição com opções de edição e exclusão"""
        while True:
            self._limpar_tela()
            print("\n=== PERFIL DA INSTITUIÇÃO ===\n")
            
            if not self.instituicao_logada:
                print("⚠️  Instituição não autenticada")
                print("\nPerfil será exibido após login/cadastro.")
                input("\nPressione ENTER para voltar...")
                return
            
            print(f"ID: {self.instituicao_logada.id}")
            print(f"Nome: {self.instituicao_logada.nome}")
            print(f"CNPJ: {self.instituicao_logada.cnpj}")
            print(f"Email: {self.instituicao_logada.email or 'Não informado'}")
            print(f"Telefone: {self.instituicao_logada.telefone or 'Não informado'}")
            print(f"Endereço: {self.instituicao_logada.endereco or 'Não informado'}")
            print(f"Website: {self.instituicao_logada.website or 'Não informado'}")
            
            print("\n--- OPÇÕES ---")
            print("1. Editar perfil")
            print("2. Excluir conta")
            print("3. Voltar")
            
            opcao = input("\nEscolha uma opção: ").strip()
            
            if opcao == "1":
                self._editar_perfil()
            elif opcao == "2":
                if self._excluir_conta():
                    return  # Conta excluída, sair do menu
            elif opcao == "3":
                return
            else:
                print("\n❌ Opção inválida!")
                input("Pressione ENTER para continuar...")

    def _editar_perfil(self) -> None:
        """Permite editar os dados da instituição"""
        self._limpar_tela()
        print("\n=== EDITAR PERFIL ===\n")
        print("Deixe em branco para manter o valor atual.\n")
        
        # Nome
        print(f"Nome atual: {self.instituicao_logada.nome}")
        novo_nome = input("Novo nome: ").strip()
        if novo_nome:
            self.instituicao_logada.nome = novo_nome
        
        # Email
        print(f"\nEmail atual: {self.instituicao_logada.email or 'Não informado'}")
        novo_email = input("Novo email: ").strip()
        if novo_email:
            self.instituicao_logada.email = novo_email
        
        # Telefone
        print(f"\nTelefone atual: {self.instituicao_logada.telefone or 'Não informado'}")
        novo_telefone = input("Novo telefone: ").strip()
        if novo_telefone:
            self.instituicao_logada.telefone = novo_telefone
        
        # Endereço
        print(f"\nEndereço atual: {self.instituicao_logada.endereco or 'Não informado'}")
        novo_endereco = input("Novo endereço: ").strip()
        if novo_endereco:
            self.instituicao_logada.endereco = novo_endereco
        
        # Website
        print(f"\nWebsite atual: {self.instituicao_logada.website or 'Não informado'}")
        novo_website = input("Novo website: ").strip()
        if novo_website:
            self.instituicao_logada.website = novo_website
        
        try:
            self.service.atualizar(self.instituicao_logada)
            print("\n✅ Perfil atualizado com sucesso!")
        except Exception as e:
            print(f"\n❌ Erro ao atualizar perfil: {e}")
        
        input("Pressione ENTER para continuar...")

    def _excluir_conta(self) -> bool:
        """Exclui a conta da instituição. Retorna True se conta foi excluída."""
        self._limpar_tela()
        print("\n=== EXCLUIR CONTA ===\n")
        print("⚠️  ATENÇÃO: Esta ação é IRREVERSÍVEL!")
        print("Todos os seus dados serão permanentemente excluídos.")
        print("Isso inclui todos os cursos e áreas de ensino cadastradas.\n")
        
        confirmacao = input("Digite 'EXCLUIR' para confirmar a exclusão: ").strip()
        
        if confirmacao == "EXCLUIR":
            try:
                self.service.deletar(self.instituicao_logada.id)
                print("\n✅ Conta excluída com sucesso!")
                print("Obrigado por usar o SkillUp.")
                input("Pressione ENTER para sair...")
                self.instituicao_logada = None
                return True
            except Exception as e:
                print(f"\n❌ Erro ao excluir conta: {e}")
                input("Pressione ENTER para continuar...")
                return False
        else:
            print("\n❌ Exclusão cancelada.")
            input("Pressione ENTER para continuar...")
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