"""
Gerenciamento de imóveis pertencentes a um usuário.
Atende PB03 (cadastrar) e PB04 (editar/excluir).
"""

from src.persistencia import carregar_dados, salvar_dados
from src.validacoes import texto_valido


def cadastrar_imovel(email_usuario):
    """Cadastra um novo imóvel para o usuário logado."""
    dados = carregar_dados()
    usuario = dados["usuarios"][email_usuario]

    print("\n--- Cadastro de Imóvel ---")
    nome = input("Nome do imóvel (ex: Casa, Apartamento): ").strip()
    endereco = input("Endereço: ").strip()

    if not texto_valido(nome):
        print("Erro: nome do imóvel inválido.")
        return

    novo_id = len(usuario["imoveis"]) + 1
    imovel = {
        "id": novo_id,
        "nome": nome,
        "endereco": endereco,
        "equipamentos": [],
        "historico_consumo": [],
    }

    usuario["imoveis"].append(imovel)
    salvar_dados(dados)
    print("Imóvel cadastrado com sucesso!")


def listar_imoveis(email_usuario):
    """Lista todos os imóveis do usuário e também os retorna."""
    dados = carregar_dados()
    imoveis = dados["usuarios"][email_usuario]["imoveis"]

    if not imoveis:
        print("\nNenhum imóvel cadastrado ainda.")
        return []

    print("\n--- Seus Imóveis ---")
    for imovel in imoveis:
        print(f"[{imovel['id']}] {imovel['nome']} - {imovel['endereco']}")

    return imoveis


def buscar_imovel(email_usuario, id_imovel):
    """Retorna o dicionário do imóvel com o id informado, ou None se não existir."""
    dados = carregar_dados()
    for imovel in dados["usuarios"][email_usuario]["imoveis"]:
        if imovel["id"] == id_imovel:
            return imovel
    return None


def editar_imovel(email_usuario):
    """Permite editar o nome e o endereço de um imóvel existente."""
    imoveis = listar_imoveis(email_usuario)
    if not imoveis:
        return

    try:
        id_imovel = int(input("Digite o ID do imóvel que deseja editar: "))
    except ValueError:
        print("Erro: ID inválido.")
        return

    dados = carregar_dados()
    for imovel in dados["usuarios"][email_usuario]["imoveis"]:
        if imovel["id"] == id_imovel:
            novo_nome = input(f"Novo nome ({imovel['nome']}), deixe vazio para manter: ").strip()
            novo_endereco = input(f"Novo endereço ({imovel['endereco']}), deixe vazio para manter: ").strip()

            if texto_valido(novo_nome):
                imovel["nome"] = novo_nome
            if texto_valido(novo_endereco):
                imovel["endereco"] = novo_endereco

            salvar_dados(dados)
            print("Imóvel atualizado com sucesso!")
            return

    print("Erro: imóvel não encontrado.")


def excluir_imovel(email_usuario):
    """Remove um imóvel do usuário, dado o seu ID."""
    imoveis = listar_imoveis(email_usuario)
    if not imoveis:
        return

    try:
        id_imovel = int(input("Digite o ID do imóvel que deseja excluir: "))
    except ValueError:
        print("Erro: ID inválido.")
        return

    dados = carregar_dados()
    usuario = dados["usuarios"][email_usuario]
    quantidade_antes = len(usuario["imoveis"])

    usuario["imoveis"] = [i for i in usuario["imoveis"] if i["id"] != id_imovel]

    if len(usuario["imoveis"]) < quantidade_antes:
        salvar_dados(dados)
        print("Imóvel excluído com sucesso!")
    else:
        print("Erro: imóvel não encontrado.")
