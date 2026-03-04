from abc import ABC, abstractmethod
from typing import List, Optional
from src.dominio.requisitos_vaga import RequisitoVaga

'''Interface para repositório de RequisitoVaga. Define os métodos que qualquer implementação deve seguir.'''
class IRequisitoVagaRepositorio(ABC):
    """
    Interface que define o contrato para repositórios de RequisitoVaga.
    Classes concretas devem implementar a persistência de requisitos de vagas.
    """

    @abstractmethod
    def salvar(self, requisito: RequisitoVaga) -> None:
        """
        Salva ou atualiza um requisito de vaga no armazenamento.
        param requisito: Objeto RequisitoVaga a ser persistido.
        """
        pass

    @abstractmethod
    def buscar_por_id(self, id_requisito: int) -> Optional[RequisitoVaga]:
        """
        Busca um requisito de vaga pelo ID.
        param id_requisito: Identificador do requisito.
        return: Objeto RequisitoVaga encontrado ou None.
        """
        pass

    @abstractmethod
    def listar_todos(self) -> List[RequisitoVaga]:
        """
        Retorna todos os requisitos de vagas cadastrados.
        return: Lista de objetos RequisitoVaga.
        """
        pass

    @abstractmethod
    def listar_por_vaga(self, id_vaga: int) -> List[RequisitoVaga]:
        """
        Retorna todos os requisitos de uma vaga específica.
        param id_vaga: ID da vaga.
        return: Lista de requisitos da vaga.
        """
        pass

    @abstractmethod
    def listar_por_competencia(self, id_competencia: int) -> List[RequisitoVaga]:
        """
        Retorna todas as vagas que exigem uma competência específica.
        param id_competencia: ID da competência.
        return: Lista de requisitos que usam esta competência.
        """
        pass

    @abstractmethod
    def listar_obrigatorios_por_vaga(self, id_vaga: int) -> List[RequisitoVaga]:
        """
        Retorna todos os requisitos obrigatórios de uma vaga.
        param id_vaga: ID da vaga.
        return: Lista de requisitos obrigatórios.
        """
        pass

    @abstractmethod
    def listar_por_nivel_minimo(self, nivel: str) -> List[RequisitoVaga]:
        """
        Retorna todos os requisitos que exigem um nível mínimo específico.
        param nivel: Nível mínimo (iniciante, intermediario, avancado).
        return: Lista de requisitos com este nível mínimo.
        """
        pass

    @abstractmethod
    def buscar_por_vaga_e_competencia(self, id_vaga: int, id_competencia: int) -> Optional[RequisitoVaga]:
        """
        Busca um requisito específico de uma vaga para uma competência.
        param id_vaga: ID da vaga.
        param id_competencia: ID da competência.
        return: Objeto RequisitoVaga encontrado ou None.
        """
        pass

    @abstractmethod
    def atualizar(self, requisito: RequisitoVaga) -> None:
        """
        Atualiza os dados de um requisito de vaga.
        param requisito: Objeto RequisitoVaga com dados atualizados.
        """
        pass

    @abstractmethod
    def remover_por_id(self, id_requisito: int) -> bool:
        """
        Remove um requisito de vaga pelo ID.
        param id_requisito: Identificador do requisito.
        return: True se removeu com sucesso, False caso contrário.
        """
        pass

    @abstractmethod
    def remover_por_vaga(self, id_vaga: int) -> bool:
        """
        Remove todos os requisitos de uma vaga (ao deletar vaga).
        param id_vaga: ID da vaga.
        return: True se removeu com sucesso, False caso contrário.
        """
        pass

    @abstractmethod
    def contar_requisitos_vaga(self, id_vaga: int) -> int:
        """
        Retorna o total de requisitos de uma vaga.
        param id_vaga: ID da vaga.
        return: Quantidade de requisitos.
        """
        pass

    @abstractmethod
    def contar_requisitos_obrigatorios(self, id_vaga: int) -> int:
        """
        Retorna o total de requisitos obrigatórios de uma vaga.
        param id_vaga: ID da vaga.
        return: Quantidade de requisitos obrigatórios.
        """
        pass