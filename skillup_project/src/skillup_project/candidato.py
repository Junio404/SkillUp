class Candidato:
    def __init__(self, nome, cpf, email, senha, area_interesse, nivel_formacao):
        self.nome = nome
        self.cpf = cpf
        self.email = email
        self.senha = senha
        self.area_interesse = area_interesse
        self.nivel_formacao = nivel_formacao
        
    
    # =========================
    # Métodos de perfil
    # =========================
    def atualizar_area_interesse(self, nova_area):
        self.area_interesse = nova_area

    def atualizar_nivel_formacao(self, novo_nivel):
        self.nivel_formacao = novo_nivel

    def atualizar_email(self, novo_email):
        self.email = novo_email

    def alterar_senha(self, senha_atual, nova_senha):
        if self.senha != senha_atual:
            raise ValueError("Senha atual incorreta.")
        self.senha = nova_senha

    # =========================
    # Métodos de interação
    # =========================
    def candidatar_se(self, vaga):
        """
        Cria uma candidatura para uma vaga.
        A validação de estado da vaga NÃO é responsabilidade do candidato.
        """
        return vaga.receber_candidatura(self)

    def inscrever_em_curso(self, curso):
        """
        Solicita inscrição em um curso.
        As validações de pré-requisito são responsabilidade do curso/inscrição.
        """
        return curso.receber_inscricao(self)

    # =========================
    # Métodos utilitários
    # =========================
    def _str_(self):
        return f"Candidato: {self.nome} ({self.email})"

