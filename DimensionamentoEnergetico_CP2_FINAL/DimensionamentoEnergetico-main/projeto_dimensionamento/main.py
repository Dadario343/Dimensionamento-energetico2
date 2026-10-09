"""
Sistema de Dimensionamento Energético
--------------------------------------
Arquivo principal: contém os menus do sistema e conecta todos os módulos.

Para executar:
    python main.py
"""

from src.usuarios import cadastrar_usuario, autenticar_usuario
from src.imoveis import cadastrar_imovel, listar_imoveis, editar_imovel, excluir_imovel
from src.equipamentos import cadastrar_equipamento, listar_equipamentos, remover_equipamento
from src.consumo import registrar_consumo_mensal, exibir_historico
from src.relatorio import exibir_resumo_energetico, exibir_grafico_consumo


def menu_imovel(email_usuario, id_imovel, nome_imovel):
    """Menu com as ações disponíveis dentro de um imóvel selecionado."""
    while True:
        print(f"\n=== Imóvel: {nome_imovel} ===")
        print("1 - Cadastrar equipamento")
        print("2 - Listar equipamentos")
        print("3 - Remover equipamento")
        print("4 - Registrar consumo mensal")
        print("5 - Ver histórico de consumo")
        print("6 - Ver gráfico de consumo")
        print("7 - Gerar resumo energético")
        print("0 - Voltar")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_equipamento(email_usuario, id_imovel)
        elif opcao == "2":
            listar_equipamentos(email_usuario, id_imovel)
        elif opcao == "3":
            remover_equipamento(email_usuario, id_imovel)
        elif opcao == "4":
            registrar_consumo_mensal(email_usuario, id_imovel)
        elif opcao == "5":
            exibir_historico(email_usuario, id_imovel)
        elif opcao == "6":
            exibir_grafico_consumo(email_usuario, id_imovel)
        elif opcao == "7":
            exibir_resumo_energetico(email_usuario, id_imovel)
        elif opcao == "0":
            break
        else:
            print("Opção inválida.")


def menu_usuario(email_usuario):
    """Menu principal do usuário logado (gerenciamento de imóveis)."""
    while True:
        print("\n=== Menu Principal ===")
        print("1 - Cadastrar imóvel")
        print("2 - Listar imóveis")
        print("3 - Editar imóvel")
        print("4 - Excluir imóvel")
        print("5 - Selecionar imóvel")
        print("0 - Logout")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_imovel(email_usuario)
        elif opcao == "2":
            listar_imoveis(email_usuario)
        elif opcao == "3":
            editar_imovel(email_usuario)
        elif opcao == "4":
            excluir_imovel(email_usuario)
        elif opcao == "5":
            imoveis = listar_imoveis(email_usuario)
            if imoveis:
                try:
                    id_imovel = int(input("Digite o ID do imóvel: "))
                except ValueError:
                    print("Erro: ID inválido.")
                    continue

                escolhido = next((i for i in imoveis if i["id"] == id_imovel), None)
                if escolhido:
                    menu_imovel(email_usuario, id_imovel, escolhido["nome"])
                else:
                    print("Erro: imóvel não encontrado.")
        elif opcao == "0":
            print("Logout realizado.")
            break
        else:
            print("Opção inválida.")


def menu_principal():
    """Menu inicial do sistema (cadastro, login e saída)."""
    while True:
        print("\n########################################")
        print("   Sistema de Dimensionamento Energético")
        print("########################################")
        print("1 - Cadastrar usuário")
        print("2 - Login")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_usuario()
        elif opcao == "2":
            email_usuario = autenticar_usuario()
            if email_usuario:
                menu_usuario(email_usuario)
        elif opcao == "0":
            print("Encerrando o sistema. Até logo!")
            break
        else:
            print("Opção inválida.")


if __name__ == "__main__":
    menu_principal()
