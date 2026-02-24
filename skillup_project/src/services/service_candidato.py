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



from src.repositorios.repositorio_candidato import RepositorioCandidatoJSON


def ok(mensagem):
    print(f"✔ {mensagem}")


def limpar_base(service):
    """
    Apenas para teste.
    Apaga todos os candidatos antes de começar.
    """
    candidatos = service.listar()
    for c in candidatos:
        service.deletar(c.id)


def testar_crud_completo():
    print("\n===== INICIANDO TESTES =====")

    repo = RepositorioCandidatoJSON()
    service = CandidatoService(repo)

    limpar_base(service)

    # -------------------------
    # TESTE 1 - Cadastro
    # -------------------------
    print("\n1) Testando cadastro...")

    c1 = service.cadastrar(
        "João Silva",
        "11111111111",
        "joao@email.com",
        ["TI"],
        "Superior"
    )

    c2 = service.cadastrar(
        "Maria Souza",
        "22222222222",
        "maria@email.com",
        ["RH"],
        "Médio"
    )

    assert c1.id == 1
    assert c2.id == 2
    ok("Cadastro funcionando corretamente.")

    # -------------------------
    # TESTE 2 - Listagem objeto
    # -------------------------
    print("\n2) Testando listagem (objetos)...")

    candidatos = service.listar()
    assert len(candidatos) == 2

    print("Lista retornada:")
    for c in candidatos:
        print(f"- ID: {c.id} | Nome: {c.nome} | Áreas: {c.areas_interesse}")

    ok("Listagem de objetos funcionando corretamente.")

    # -------------------------
    # TESTE 3 - Listagem formatada
    # -------------------------
    print("\n3) Testando listagem formatada...")

    candidatos_formatados = service.listar_formatado()
    assert isinstance(candidatos_formatados[0], str)

    print("Lista formatada:")
    for c in candidatos_formatados:
        print(c)
        print("-" * 30)

    ok("Listagem formatada funcionando corretamente.")

    # -------------------------
    # TESTE 4 - Buscar por ID objeto
    # -------------------------
    print("\n4) Testando busca por ID (objeto)...")

    candidato = service.buscar_por_id(c1.id)
    assert candidato.nome == "João Silva"

    print("Resultado da busca:")
    print(f"ID: {candidato.id} | Nome: {candidato.nome} | Áreas: {candidato.areas_interesse}")

    ok("Busca por ID funcionando corretamente.")

    # -------------------------
    # TESTE 5 - Buscar por ID formatado
    # -------------------------
    print("\n5) Testando busca por ID formatado...")

    candidato_str = service.buscar_por_id_formatado(c1.id)
    assert isinstance(candidato_str, str)

    print("Resultado formatado:")
    print(candidato_str)

    ok("Busca por ID formatada funcionando corretamente.")

    # -------------------------
    # TESTE 6 - Buscar por filtro objeto
    # -------------------------
    print("\n6) Testando filtro por área (objeto)...")

    resultado = service.buscar_por_filtros(areas_interesse="TI")
    assert len(resultado) == 1

    print("Resultado do filtro:")
    for c in resultado:
        print(f"- ID: {c.id} | Nome: {c.nome} | Áreas: {c.areas_interesse}")

    ok("Filtro por área funcionando corretamente.")

    # -------------------------
    # TESTE 7 - Buscar por filtro formatado
    # -------------------------
    print("\n7) Testando filtro formatado...")

    resultado_str = service.buscar_por_filtros_formatado(areas_interesse="TI")
    assert isinstance(resultado_str[0], str)

    print("Resultado formatado do filtro:")
    for c in resultado_str:
        print(c)
        print("-" * 30)

    ok("Filtro formatado funcionando corretamente.")

    # -------------------------
    # TESTE 8 - Atualização
    # -------------------------
    print("\n8) Testando atualização...")

    service.atualizar(c1.id, "nome", "João Atualizado")
    atualizado = service.buscar_por_id(c1.id)

    print(f"Nome atualizado: {atualizado.nome}")

    assert atualizado.nome == "João Atualizado"
    ok("Atualização funcionando corretamente.")

    # -------------------------
    # TESTE 9 - Exclusão
    # -------------------------
    print("\n9) Testando exclusão...")

    service.deletar(c2.id)
    candidatos = service.listar()

    print("Lista após exclusão:")
    for c in candidatos:
        print(f"- ID: {c.id} | Nome: {c.nome}")

    assert len(candidatos) == 1
    ok("Exclusão funcionando corretamente.")

    # -------------------------
    # TESTE 10 - Adicionar área
    # -------------------------
    print("\n10) Testando adicionar área de interesse...")

    candidato = service.buscar_por_id(c1.id)
    candidato.adicionar_area("Cloud")
    service.repo.atualizar(candidato)

    atualizado = service.buscar_por_id(c1.id)

    print(f"Áreas atuais: {atualizado.areas_interesse}")

    assert "Cloud" in atualizado.areas_interesse
    ok("Adição de área funcionando corretamente.")

    # -------------------------
    # TESTE 11 - Duplicidade
    # -------------------------
    print("\n11) Testando duplicidade de área...")

    try:
        candidato.adicionar_area("Cloud")
        assert False, "Era esperado ValueError"
    except ValueError:
        ok("Bloqueio de duplicidade funcionando corretamente.")

    # -------------------------
    # TESTE 12 - Remover área
    # -------------------------
    print("\n12) Testando remoção de área...")

    candidato.remover_area("Cloud")
    service.repo.atualizar(candidato)

    atualizado = service.buscar_por_id(c1.id)

    print(f"Áreas após remoção: {atualizado.areas_interesse}")

    assert "Cloud" not in atualizado.areas_interesse
    ok("Remoção de área funcionando corretamente.")

    # -------------------------
    # TESTE 13 - Erro ao remover inexistente
    # -------------------------
    print("\n13) Testando erro ao remover área inexistente...")

    try:
        candidato.remover_area("Inexistente")
        assert False, "Era esperado ValueError"
    except ValueError:
        ok("Erro ao remover área inexistente funcionando corretamente.")

    # -------------------------
    # TESTE 14 - Buscar ID inexistente
    # -------------------------
    print("\n14) Testando erro esperado...")

    try:
        service.buscar_por_id(999)
        assert False, "Era esperado ValueError"
    except ValueError:
        ok("Erro ao buscar candidato inexistente funcionando corretamente.")

    print("\n===== TODOS OS TESTES PASSARAM COM SUCESSO =====")


if __name__ == "__main__":
    testar_crud_completo()
