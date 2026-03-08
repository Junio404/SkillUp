"""
Configuração compartilhada de testes do SkillUp.
Fixtures disponíveis para todos os módulos de teste.
"""
import sys
import os
from datetime import date

import pytest

# Garante que o diretório raiz do projeto está no sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


@pytest.fixture
def future_date():
    """Data futura para uso em testes de prazo."""
    return date(2027, 12, 31)


@pytest.fixture
def past_date():
    """Data passada para uso em testes de prazo."""
    return date(2020, 1, 1)
