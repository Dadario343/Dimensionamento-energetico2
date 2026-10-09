"""
Registro do histórico de consumo mensal de um imóvel e cálculo do resumo
energético (maior consumo, mês de pico e consumo médio).
Atende PB06, PB07, PB08, PB09 e PB10.
"""

from src.persistencia import carregar_dados, salvar_dados
from src.validacoes import texto_valido, numero_positivo
from src.equipamentos import calcular_consumo_total_estimado


def registrar_consumo_mensal(email_usuario, id_imovel):
    """Registra o consumo (kWh) de um mês específico no histórico do imóvel."""
    print("\n--- Registrar Consumo Mensal ---")
    mes = input("Mês/Ano de referência (ex: Marco/2025): ").strip()

    consumo_estimado = calcular_consumo_total_estimado(email_usuario, id_imovel)
    print(f"Consumo estimado com base nos equipamentos cadastrados: {consumo_estimado:.2f} kWh")
    usar_estimado = input("Usar esse valor estimado como consumo do mês? (s/n): ").strip().lower()

    if usar_estimado == "s":
        consumo_kwh = consumo_estimado
    else:
        valor = input("Informe o consumo real do mês (kWh): ").strip()
        if not numero_positivo(valor):
            print("Erro: valor de consumo inválido.")
            return
        consumo_kwh = float(valor)

    if not texto_valido(mes):
        print("Erro: mês inválido.")
        return

    dados = carregar_dados()
    for imovel in dados["usuarios"][email_usuario]["imoveis"]:
        if imovel["id"] == id_imovel:
            imovel["historico_consumo"].append({
                "mes": mes,
                "consumo_kwh": round(consumo_kwh, 2),
            })
            salvar_dados(dados)
            print("Consumo registrado com sucesso!")
            return

    print("Erro: imóvel não encontrado.")


def obter_historico(email_usuario, id_imovel):
    """Retorna a lista de registros de consumo mensal de um imóvel."""
    dados = carregar_dados()
    for imovel in dados["usuarios"][email_usuario]["imoveis"]:
        if imovel["id"] == id_imovel:
            return imovel["historico_consumo"]
    return []


def exibir_historico(email_usuario, id_imovel):
    """Imprime no console o histórico de consumo de um imóvel."""
    historico = obter_historico(email_usuario, id_imovel)
    if not historico:
        print("\nNenhum consumo registrado ainda.")
        return

    print("\n--- Histórico de Consumo ---")
    for registro in historico:
        print(f"{registro['mes']}: {registro['consumo_kwh']:.2f} kWh")


def calcular_resumo_energetico(email_usuario, id_imovel):
    """
    Calcula o maior consumo, o mês em que ele ocorreu e a média mensal.
    Retorna None se não houver histórico registrado.
    """
    historico = obter_historico(email_usuario, id_imovel)
    if not historico:
        return None

    registro_maior = max(historico, key=lambda r: r["consumo_kwh"])
    media = sum(r["consumo_kwh"] for r in historico) / len(historico)

    return {
        "maior_consumo": registro_maior["consumo_kwh"],
        "mes_maior_consumo": registro_maior["mes"],
        "consumo_medio": media,
        "quantidade_meses": len(historico),
    }
