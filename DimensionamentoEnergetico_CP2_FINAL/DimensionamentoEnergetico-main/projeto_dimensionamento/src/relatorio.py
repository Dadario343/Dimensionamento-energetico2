"""
Geração do resumo energético do imóvel e de um gráfico simples em modo texto.
Atende PB11 (resumo) e PB12 (visualização gráfica do histórico).
"""

from src.consumo import calcular_resumo_energetico, obter_historico
from src.equipamentos import calcular_consumo_total_estimado
from src.imoveis import buscar_imovel


def exibir_resumo_energetico(email_usuario, id_imovel):
    """Mostra um resumo com o consumo estimado, maior consumo, média e mês de pico."""
    imovel = buscar_imovel(email_usuario, id_imovel)
    if imovel is None:
        print("Erro: imóvel não encontrado.")
        return

    resumo = calcular_resumo_energetico(email_usuario, id_imovel)
    consumo_estimado = calcular_consumo_total_estimado(email_usuario, id_imovel)

    print(f"\n===== Resumo Energético - {imovel['nome']} =====")
    print(f"Consumo estimado atual (equipamentos cadastrados): {consumo_estimado:.2f} kWh/mês")

    if resumo is None:
        print("Nenhum histórico de consumo mensal registrado ainda.")
    else:
        print(
            f"Maior consumo registrado: {resumo['maior_consumo']:.2f} kWh "
            f"(mês: {resumo['mes_maior_consumo']})"
        )
        print(f"Consumo médio mensal: {resumo['consumo_medio']:.2f} kWh")
        print(f"Total de meses registrados: {resumo['quantidade_meses']}")

    print("=" * 45)


def exibir_grafico_consumo(email_usuario, id_imovel):
    """Gera um gráfico simples de barras (em texto) com o histórico de consumo."""
    historico = obter_historico(email_usuario, id_imovel)
    if not historico:
        print("\nNenhum dado de consumo para exibir no gráfico.")
        return

    print("\n--- Gráfico de Consumo (kWh) ---")
    maior_valor = max(r["consumo_kwh"] for r in historico)
    escala = 40 / maior_valor if maior_valor > 0 else 0

    for registro in historico:
        tamanho_barra = int(registro["consumo_kwh"] * escala)
        barra = "#" * tamanho_barra
        print(f"{registro['mes']:<15} | {barra} {registro['consumo_kwh']:.1f} kWh")
