import json
import os
from src.dominio.candidato import Candidato
from src.interfaces.interface_candidato import ICandidatoRepositorio

'''Implementação de repositório de candidatos usando arquivos JSON para persistência.
Cada candidato é armazenado como um dicionário em uma lista dentro do arquivo JSON.'''
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CAMINHO_ARQUIVO = os.path.normpath(
    os.path.join(BASE_DIR, "..", "data", "candidato.json")
)


class RepositorioCandidatoJSON(ICandidatoRepositorio):
    '''
    Repositório de candidatos que utiliza um arquivo JSON para armazenar os dados.
    Implementa os métodos definidos na interface ICandidatoRepositorio.
    '''
    
    def _carregar_dados(self):
        ''' Carrega os dados do arquivo JSON. Retorna uma lista de dicionários representando os candidatos.'''
        if not os.path.exists(CAMINHO_ARQUIVO):
            return []

        try:
            with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def _salvar_dados(self, lista):
        ''' Salva a lista de candidatos no arquivo JSON. Cada candidato é convertido para um dicionário antes de ser salvo.'''
        os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
        with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as f:
            json.dump(lista, f, indent=4, ensure_ascii=False)

    def salvar(self, candidato: Candidato):
        '''Salva um candidato no arquivo JSON.'''
        dados = self._carregar_dados()
        dados.append(candidato.to_dict())
        self._salvar_dados(dados)

    def listar(self):
        '''Lista todos os candidatos armazenados no arquivo JSON. Retorna uma lista de objetos Candidato.'''
        dados = self._carregar_dados()
        return [Candidato.from_dict(d) for d in dados]

    def buscar_por_id(self, id_candidato: int):
        '''
        Busca um candidato pelo ID. Retorna um objeto Candidato se encontrado, ou None caso contrário.
        '''
        for candidato in self.listar():
            if candidato.id == id_candidato:
                return candidato
        return None

    def buscar_por_filtros(self, **filtros):
        '''Busca candidatos que correspondam aos filtros fornecidos. Os filtros são passados como argumentos nomeados e podem incluir qualquer atributo do candidato (ex: nome, cpf, áreas de interesse). Retorna uma lista de candidatos que correspondem aos critérios.
        '''
        candidatos = self.listar()
        resultado = []

        for candidato in candidatos:
            corresponde = True

            for campo, valor in filtros.items():
                if not hasattr(candidato, campo):
                    raise AttributeError(f"O campo '{campo}' não existe no candidato")

                atributo = getattr(candidato, campo)

                if isinstance(atributo, list):
                    if valor not in atributo:
                        corresponde = False
                        break
                else:
                    if atributo != valor:
                        corresponde = False
                        break

            if corresponde:
                resultado.append(candidato)

        return resultado

    def atualizar(self, candidato: Candidato):
        '''
    Atualiza um candidato existente no arquivo JSON. O candidato é identificado pelo ID. Se o candidato não for encontrado, uma exceção é levantada.
        '''
        dados = self._carregar_dados()

        for i, c in enumerate(dados):
            if c["id"] == candidato.id:
                dados[i] = candidato.to_dict()
                self._salvar_dados(dados)
                return

        raise ValueError("Candidato não encontrado")

    def deletar(self, id_candidato: int):
        ''' Deleta um candidato do arquivo JSON pelo ID. Se o candidato não for encontrado, uma exceção é levantada.'''
        dados = self._carregar_dados()

        if not any(c["id"] == id_candidato for c in dados):
            raise ValueError("Candidato não encontrado")

        dados = [c for c in dados if c["id"] != id_candidato]
        self._salvar_dados(dados)
