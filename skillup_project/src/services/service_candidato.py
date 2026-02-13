from src.dominio.candidato import Candidato
from src.interfaces.interface_candidato import ICandidatoRepositorio


class CandidatoService:
    ''' Serviço de domínio para gerenciamento de candidatos. Contém a lógica de negócio e validações relacionadas aos candidatos.
    Recebe um repositório que implementa a interface ICandidatoRepositorio para realizar operações de persistência.'''
    def __init__(self, repositorio: ICandidatoRepositorio):
        ''' Inicializa o serviço com um repositório específico.'''
        self.repo = repositorio

    def cadastrar(self, nome, cpf, email, areas_interesse, nivel_formacao):
        ''' Cadastra um novo candidato. Realiza validações de negócio, como verificar se já existe um candidato com o mesmo CPF.'''
        candidatos = self.repo.listar()

        if any(c.cpf == cpf for c in candidatos):
            raise ValueError("Já existe candidato com este CPF")

        novo_id = 1 if not candidatos else max(c.id for c in candidatos) + 1

        candidato = Candidato(
            novo_id,
            nome,
            cpf,
            email,
            areas_interesse,
            nivel_formacao
        )

        self.repo.salvar(candidato)
        return candidato

    def listar(self):
        ''' Lista todos os candidatos utilizando o repositório. Retorna uma lista de objetos Candidato.'''
        return self.repo.listar()

    def buscar_por_id(self, id_candidato: int):
        ''' Busca um candidato pelo ID utilizando o repositório. Se o candidato não for encontrado, uma exceção é levantada.'''
        candidato = self.repo.buscar_por_id(id_candidato)

        if not candidato:
            raise ValueError("Candidato não encontrado")

        return candidato

    def buscar_por_filtros(self, **filtros):
        '''Busca candidatos que correspondam aos filtros fornecidos. Os filtros são passados como argumentos nomeados e podem incluir qualquer atributo do candidato (ex: nome, cpf, áreas de interesse). Retorna uma lista de candidatos que correspondem aos critérios.'''
        return self.repo.buscar_por_filtros(**filtros)

    def listar_formatado(self):
        '''Retorna uma lista de strings representando os candidatos formatados. Cada string contém as informações do candidato de forma legível.'''
        return [str(c) for c in self.listar()]

    def buscar_por_id_formatado(self, id_candidato: int):
        '''Retorna uma string formatada representando o candidato encontrado pelo ID. Se o candidato não for encontrado, uma exceção é levantada.'''
        return str(self.buscar_por_id(id_candidato))

    def buscar_por_filtros_formatado(self, **filtros):
        '''Retorna uma lista de strings representando os candidatos que correspondem aos filtros fornecidos. Cada string contém as informações do candidato de forma legível.'''
        return [str(c) for c in self.buscar_por_filtros(**filtros)]

    def atualizar(self, id_candidato: int, campo: str, novo_valor):
        '''Atualiza um campo específico de um candidato identificado pelo ID. O campo a ser atualizado é passado como string (ex: "nome", "cpf"). Se o candidato ou o campo não for encontrado, uma exceção é levantada.'''
        candidato = self.buscar_por_id(id_candidato)
        candidato.atualizar_dado(campo, novo_valor)
        self.repo.atualizar(candidato)
        return candidato

    def deletar(self, id_candidato: int):
        ''' Deleta um candidato identificado pelo ID. Se o candidato não for encontrado, uma exceção é levantada.'''
        self.buscar_por_id(id_candidato)
        self.repo.deletar(id_candidato)

