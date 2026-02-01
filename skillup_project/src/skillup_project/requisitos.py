class CursoCompetencia:
    def __init__(self, curso, competencia, nivel_conferido):
        self.curso = curso
        self.competencia = competencia
        self.nivel_conferido = nivel_conferido # Ex: 1-Básico, 2-Intermediário

class CompetenciaCandidato:
    def __init__(self, candidato, competencia, nivel_atual):
        self.candidato = candidato
        self.competencia = competencia
        self.nivel_atual = nivel_atual

class RequisitoVaga:
    def __init__(self, vaga, competencia, nivel_minimo, obrigatorio=True):
        self.vaga = vaga
        self.competencia = competencia
        self.nivel_minimo = nivel_minimo
        self.obrigatorio = obrigatorio