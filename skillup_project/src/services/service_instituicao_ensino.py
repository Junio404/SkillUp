from src.dominio.instituicao_ensino import InstituicaoEnsino
from src.interfaces.interface_instituicao_ensino import IInstituicaoEnsino
from src.repositorios.repositorio_curso import RepositorioCurso

class ServiceInstituicaoEnsino:
    def _init_(self, repositorio_instituicao: IInstituicaoEnsino, repositorio_curso: RepositorioCurso):
        self.repositorio_instituicao = repositorio_instituicao
        self.repositorio_curso = repositorio_curso

    def criar_conta(self, instituicao: InstituicaoEnsino):
        """
        Cadastra uma nova instituição no sistema.
        """
        # Aqui entram validações de negócio extras antes de salvar
        self.repositorio_instituicao.salvar(instituicao)

    def fazer_login(self, cnpj: str, senha_fornecida: str) -> InstituicaoEnsino:
        """
        Autentica a instituição no sistema.
        """
        instituicao = self.repositorio_instituicao.buscar_por_cnpj(cnpj)
        if instituicao and instituicao.senha == senha_fornecida:
            return instituicao
        return None

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