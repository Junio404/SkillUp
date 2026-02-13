from src.dominio.entidade_publicadora import EntidadePublicadora

import json
import os
from src.dominio.entidade_publicadora import EntidadePublicadora

CAMINHO_ARQUIVO = os.path.join("data", "instituicao_ensino.json")


class InstituicaoEnsino(EntidadePublicadora):
    def __init__(self, id_instituicao: int, nome: str, cnpj: str,
                 registro_educacional: str, tipo: str, credenciada: bool = True):
        super().__init__(id_instituicao, nome, cnpj)
        self.registro_educacional = registro_educacional
        self.tipo = tipo
        self.credenciada = credenciada

    # ===== PROPERTIES =====
    @property
    def registro_educacional(self):
        return self._registro_educacional

    @registro_educacional.setter
    def registro_educacional(self, valor):
        if not valor:
            raise ValueError("Registro educacional é obrigatório")
        self._registro_educacional = valor

    @property
    def tipo(self):
        return self._tipo

    @tipo.setter
    def tipo(self, valor):
        self._tipo = valor

    @property
    def credenciada(self):
        return self._credenciada

    @credenciada.setter
    def credenciada(self, valor):
        if not isinstance(valor, bool):
            raise ValueError("Credenciada deve ser booleano")
        self._credenciada = valor

    # ===== MÉTODOS DO DIAGRAMA =====

    def criar_conta(self, repositorio):
        """DIP: depende de abstração"""
        repositorio.salvar(self)

    def cadastrar_curso(self, curso, repositorio_curso):
        self.validar_publicacao()
        repositorio_curso.salvar(curso)

    def gerenciar_cursos(self, repositorio_curso):
        """Ex: listar, editar, pausar"""
        return repositorio_curso.listar_por_instituicao(self.id)

    # ===== CONTRATO ABSTRATO =====
    def validar_publicacao(self):
        if not self.credenciada:
            raise PermissionError("Instituição não credenciada não pode publicar cursos")

    # ===== JSON =====
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "cnpj": self.cnpj,
            "registro_educacional": self.registro_educacional,
            "tipo": self.tipo,
            "credenciada": self.credenciada
        }

    @staticmethod
    def from_dict(d):
        return InstituicaoEnsino(
            id_instituicao=d["id"],
            nome=d["nome"],
            cnpj=d["cnpj"],
            registro_educacional=d["registro_educacional"],
            tipo=d["tipo"],
            credenciada=d.get("credenciada", True)
        )

class AreaEnsino:
    def __init__(self, id_area, nome_area):
        self.id_area = id_area
        self.nome_area = nome_area
        

class InstituicaoAreaEnsino:
    def __init__(self, id_instituicao_area, id_instituicao, id_area):
        self.id_instituicao_area = id_instituicao_area
        self.id_instituicao = id_instituicao
        self.id_area = id_area