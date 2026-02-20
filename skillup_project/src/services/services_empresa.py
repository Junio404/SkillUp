from src.dominio.empresa import Empresa
from src.interfaces.interface_empresa import IEmpresaRepositorio


class EmpresaService:
    """
    Serviço de domínio para gerenciamento de empresas.
    Contém a lógica de negócio e validações relacionadas às empresas.

    Recebe um repositório que implementa a interface IEmpresaRepositorio
    para realizar operações de persistência.
    """

    def __init__(self, repositorio: IEmpresaRepositorio):
        """Inicializa o serviço com um repositório específico."""
        self.repo = repositorio

    def cadastrar(self, nome, cnpj, porte):
        """
        Cadastra uma nova empresa.
        Validação: não permitir CNPJ duplicado.
        """
        empresas = self.repo.listar()

        if any(e.cnpj == cnpj for e in empresas):
            raise ValueError("Já existe empresa com este CNPJ")

        novo_id = 1 if not empresas else max(e.id for e in empresas) + 1

        empresa = Empresa(
            novo_id,
            nome,
            cnpj,
            porte
        )

        self.repo.salvar(empresa)
        return empresa

    def listar(self):
        """Lista todas as empresas utilizando o repositório."""
        return self.repo.listar()

    def buscar_por_id(self, id_empresa: int):
        """Busca uma empresa pelo ID. Se não encontrar, lança exceção."""
        empresa = self.repo.buscar_por_id(id_empresa)

        if not empresa:
            raise ValueError("Empresa não encontrada")

        return empresa

    def buscar_por_filtros(self, **filtros):
        """Busca empresas que correspondam aos filtros fornecidos."""
        return self.repo.buscar_por_filtros(**filtros)

    def listar_formatado(self):
        """Retorna uma lista de strings com empresas formatadas."""
        return [str(e) for e in self.listar()]

    def buscar_por_id_formatado(self, id_empresa: int):
        """Retorna a empresa (por ID) em formato de string."""
        return str(self.buscar_por_id(id_empresa))

    def buscar_por_filtros_formatado(self, **filtros):
        """Retorna lista formatada das empresas filtradas."""
        return [str(e) for e in self.buscar_por_filtros(**filtros)]

    def atualizar(self, id_empresa: int, campo: str, novo_valor):
        """
        Atualiza um campo específico de uma empresa identificada pelo ID.
        Ex: campo="nome" ou campo="porte".

        Observação: se 'cnpj' for imutável na entidade, a própria Empresa deve bloquear.
        """
        empresa = self.buscar_por_id(id_empresa)
        empresa.atualizar_dado(campo, novo_valor)
        self.repo.atualizar(empresa)
        return empresa

    def deletar(self, id_empresa: int):
        """Deleta uma empresa pelo ID. Se não existir, lança exceção."""
        self.buscar_por_id(id_empresa)
        self.repo.deletar(id_empresa)