"""
Cadastro e autenticação de usuários.
Atende PB01 (cadastro) e PB02 (login).
"""

import hashlib

from src.persistencia import carregar_dados, salvar_dados
from src.validacoes import email_valido, texto_valido


def gerar_hash_senha(senha):
    """
    Transforma a senha em um hash (não guardamos a senha em texto puro).
    Isso é importante para a privacidade dos dados (PB15).
    """
    return hashlib.sha256(senha.encode("utf-8")).hexdigest()


def cadastrar_usuario():
    """Cadastra um novo usuário. Retorna o e-mail cadastrado ou None em caso de erro."""
    dados = carregar_dados()

    print("\n--- Cadastro de Usuário ---")
    nome = input("Nome: ").strip()
    email = input("E-mail: ").strip().lower()
    senha = input("Senha: ").strip()

    if not texto_valido(nome):
        print("Erro: nome inválido.")
        return None

    if not email_valido(email):
        print("Erro: e-mail inválido.")
        return None

    if email in dados["usuarios"]:
        print("Erro: já existe um usuário cadastrado com esse e-mail.")
        return None

    if not texto_valido(senha) or len(senha) < 4:
        print("Erro: a senha deve ter pelo menos 4 caracteres.")
        return None

    dados["usuarios"][email] = {
        "nome": nome,
        "senha_hash": gerar_hash_senha(senha),
        "imoveis": [],
    }
    salvar_dados(dados)

    print(f"Usuário '{nome}' cadastrado com sucesso!")
    return email


def autenticar_usuario():
    """Realiza o login. Retorna o e-mail do usuário autenticado ou None."""
    dados = carregar_dados()

    print("\n--- Login ---")
    email = input("E-mail: ").strip().lower()
    senha = input("Senha: ").strip()

    usuario = dados["usuarios"].get(email)

    if usuario is None:
        print("Erro: usuário não encontrado.")
        return None

    if usuario["senha_hash"] != gerar_hash_senha(senha):
        print("Erro: senha incorreta.")
        return None

    print(f"Bem-vindo(a), {usuario['nome']}!")
    return email
