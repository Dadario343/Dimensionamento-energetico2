"""
Funções simples de validação, usadas em vários módulos do sistema.
Atendem ao PB13 (alertar o usuário sobre dados inválidos ou incompletos).
"""

import re

PADRAO_EMAIL = r"^[\w\.-]+@[\w\.-]+\.\w+$"


def email_valido(email):
    """Verifica se o e-mail tem um formato válido (ex: nome@dominio.com)."""
    return isinstance(email, str) and re.match(PADRAO_EMAIL, email) is not None


def texto_valido(texto):
    """Verifica se o texto não é vazio nem só espaços."""
    return isinstance(texto, str) and texto.strip() != ""


def numero_positivo(valor):
    """Verifica se o valor pode ser convertido para float e é maior que zero."""
    try:
        return float(valor) > 0
    except (ValueError, TypeError):
        return False
