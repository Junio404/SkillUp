from typing import List, Optional
from src.dominio.instituicao_ensino import InstituicaoEnsino
from src.interfaces.interface_instituicao_ensino import IInstituicaoEnsino
from src.repositorios.repositorio_curso_ead import RepositorioCursoEADJSON


class ServiceInstituicaoEnsino:
    def __init__(self, repositorio_instituicao: IInstituicaoEnsino, repositorio_curso: RepositorioCursoEADJSON):
        self.repositorio_instituicao = repositorio_instituicao
        self.repositorio_curso = repositorio_curso

    def criar_conta(self, instituicao: InstituicaoEnsino) -> InstituicaoEnsino:
        """
        Cadastra uma nova instituição no sistema.
        """
        # Verificar duplicidade de CNPJ
        existente = self.repositorio_instituicao.buscar_por_cnpj(instituicao.cnpj)
        if existente:
            raise ValueError("Já existe uma instituição com este CNPJ")
        
        self.repositorio_instituicao.salvar(instituicao)
        return instituicao

    def buscar_por_id(self, id_instituicao: int) -> Optional[InstituicaoEnsino]:
        """Busca instituição por ID."""
        return self.repositorio_instituicao.buscar_por_id(id_instituicao)

    def buscar_por_cnpj(self, cnpj: str) -> Optional[InstituicaoEnsino]:
        """Busca instituição por CNPJ."""
        return self.repositorio_instituicao.buscar_por_cnpj(cnpj)

    def listar(self) -> List[InstituicaoEnsino]:
        """Lista todas as instituições."""
        return self.repositorio_instituicao.listar()

    def fazer_login(self, id_instituicao: int) -> Optional[InstituicaoEnsino]:
        """
        Autentica a instituição no sistema pelo ID.
        """
        instituicao = self.repositorio_instituicao.buscar_por_id(id_instituicao)
        return instituicao

    def cadastrar_curso(self, instituicao: InstituicaoEnsino, curso):
        """
        Publica um novo curso no sistema, validando se a instituição pode publicar.
        """
        try:
            instituicao.validar_publicacao()
            self.repositorio_curso.salvar(curso)
            return True
        except PermissionError as e:
            print(f"Erro ao cadastrar curso: {e}")
            return False

    def listar_cursos(self, instituicao_id: int):
        """
        Recupera a lista de cursos da instituição.
        """
        return self.repositorio_curso.listar_por_instituicao(instituicao_id)