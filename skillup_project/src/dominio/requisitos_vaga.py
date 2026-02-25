class RequisitoVaga:
    def __init__(self, vaga, competencia, nivel_minimo, obrigatorio=True):
        self.vaga = vaga
        self.competencia = competencia
        self.nivel_minimo = nivel_minimo
        self.obrigatorio = obrigatorio