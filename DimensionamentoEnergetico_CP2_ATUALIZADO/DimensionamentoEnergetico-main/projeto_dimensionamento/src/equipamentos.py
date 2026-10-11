"""
Cadastro de equipamentos elétricos e cálculo do consumo estimado.
Atende PB05 (potência, quantidade, tempo de uso) e parte do PB08/PB09.
"""

from src.persistencia import carregar_dados, salvar_dados
from src.validacoes import texto_valido, numero_positivo
from src.imoveis import buscar_imovel

DIAS_NO_MES = 30


def cadastrar_equipamento(email_usuario, id_imovel):
    """Cadastra um equipamento elétrico dentro de um imóvel específico."""
    print("\n--- Cadastro de Equipamento ---")
    nome = input("Nome do equipamento (ex: Geladeira, Chuveiro): ").strip()
    potencia = input("Potência (em Watts): ").strip()
    quantidade = input("Quantidade de equipamentos iguais: ").strip()
    horas_dia = input("Tempo médio de uso por dia (em horas): ").strip()

    if not texto_valido(nome):
        print("Erro: nome do equipamento inválido.")
        return
    if not numero_positivo(potencia):
        print("Erro: potência inválida.")
        return
    if not quantidade.isdigit() or int(quantidade) <= 0:
        print("Erro: quantidade inválida.")
        return
    if not numero_positivo(horas_dia) or float(horas_dia) > 24:
        print("Erro: tempo de uso inválido (deve ser entre 0 e 24 horas).")
        return

    dados = carregar_dados()
    for imovel in dados["usuarios"][email_usuario]["imoveis"]:
        if imovel["id"] == id_imovel:
            imovel["equipamentos"].append({
                "nome": nome,
                "potencia_w": float(potencia),
                "quantidade": int(quantidade),
                "horas_dia": float(horas_dia),
            })
            salvar_dados(dados)
            print("Equipamento cadastrado com sucesso!")
            return

    print("Erro: imóvel não encontrado.")


def calcular_consumo_equipamento(equipamento):
    """
    Calcula o consumo mensal estimado (em kWh) de um equipamento.
    Fórmula: potência (kW) x quantidade x horas por dia x 30 dias.
    """
    potencia_kw = equipamento["potencia_w"] / 1000
    consumo_diario = potencia_kw * equipamento["quantidade"] * equipamento["horas_dia"]
    return consumo_diario * DIAS_NO_MES


def listar_equipamentos(email_usuario, id_imovel):
    """Lista os equipamentos de um imóvel, já mostrando o consumo estimado de cada um."""
    imovel = buscar_imovel(email_usuario, id_imovel)
    if imovel is None or not imovel["equipamentos"]:
        print("\nNenhum equipamento cadastrado neste imóvel.")
        return []

    print(f"\n--- Equipamentos de {imovel['nome']} ---")
    for indice, equipamento in enumerate(imovel["equipamentos"], start=1):
        consumo = calcular_consumo_equipamento(equipamento)
        print(
            f"[{indice}] {equipamento['nome']} - {equipamento['potencia_w']}W "
            f"x{equipamento['quantidade']} - {equipamento['horas_dia']}h/dia "
            f"=> {consumo:.2f} kWh/mês"
        )

    return imovel["equipamentos"]


def remover_equipamento(email_usuario, id_imovel):
    """Remove um equipamento de um imóvel, a partir da posição mostrada na listagem."""
    equipamentos = listar_equipamentos(email_usuario, id_imovel)
    if not equipamentos:
        return

    try:
        indice = int(input("Digite o número do equipamento a remover: ")) - 1
    except ValueError:
        print("Erro: valor inválido.")
        return

    if indice < 0 or indice >= len(equipamentos):
        print("Erro: equipamento não encontrado.")
        return

    dados = carregar_dados()
    for imovel in dados["usuarios"][email_usuario]["imoveis"]:
        if imovel["id"] == id_imovel:
            removido = imovel["equipamentos"].pop(indice)
            salvar_dados(dados)
            print(f"Equipamento '{removido['nome']}' removido com sucesso!")
            return


def calcular_consumo_total_estimado(email_usuario, id_imovel):
    """Soma o consumo mensal estimado (kWh) de todos os equipamentos do imóvel."""
    imovel = buscar_imovel(email_usuario, id_imovel)
    if imovel is None:
        return 0
    return sum(calcular_consumo_equipamento(eq) for eq in imovel["equipamentos"])
