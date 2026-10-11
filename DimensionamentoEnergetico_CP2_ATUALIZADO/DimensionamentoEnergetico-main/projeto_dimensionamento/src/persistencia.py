"""
Módulo responsável por salvar e carregar os dados do sistema.
Usamos um arquivo JSON simples como "banco de dados" (PB14 - Persistência).
"""

import json
import os

CAMINHO_ARQUIVO = os.path.join(os.path.dirname(__file__), "dados", "dados.json")


def carregar_dados():
    """Lê o arquivo JSON e retorna os dados como um dicionário Python."""
    if not os.path.exists(CAMINHO_ARQUIVO):
        return {"usuarios": {}}

    with open(CAMINHO_ARQUIVO, "r", encoding="utf-8") as arquivo:
        try:
            return json.load(arquivo)
        except json.JSONDecodeError:
            # Se o arquivo estiver vazio ou corrompido, começamos do zero
            return {"usuarios": {}}


def salvar_dados(dados):
    """Escreve o dicionário de dados no arquivo JSON, criando a pasta se necessário."""
    os.makedirs(os.path.dirname(CAMINHO_ARQUIVO), exist_ok=True)
    with open(CAMINHO_ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, indent=4, ensure_ascii=False)
