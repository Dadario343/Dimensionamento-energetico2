"""Pré-dimensionamento fotovoltaico acadêmico, com seleção por compatibilidade básica."""
from __future__ import annotations
import csv
import math
from pathlib import Path

DATASETS_DIR = Path(__file__).resolve().parent / "dados" / "fotovoltaico"
FATOR_DESEMPENHO_PADRAO = 0.80
EFICIENCIA_BATERIA_PADRAO = 0.90
DIAS_MES = 30


def carregar_dataset(nome):
    caminho = DATASETS_DIR / nome
    with caminho.open("r", encoding="utf-8-sig", newline="") as arquivo:
        return list(csv.DictReader(arquivo))


def numero(item, campo, padrao=None):
    try:
        valor = float(str(item.get(campo, "")).strip().replace(",", "."))
        return valor if math.isfinite(valor) else padrao
    except (ValueError, TypeError, AttributeError):
        return padrao


def _texto(item, campo):
    return str(item.get(campo, "") or "").strip().casefold()


def _validar_modulos(modulos):
    return [m for m in modulos
            if numero(m, "potencia_wp", 0) > 0
            and numero(m, "preco_brl", 0) > 0
            and all(numero(m, c) is not None and numero(m, c) > 0
                    for c in ("voc_v", "isc_a", "vmp_v", "imp_a"))]


def _configurar_strings(modulo, inversor, quantidade):
    """Procura uma divisão simples em strings iguais, sem exceder limites declarados.

    É uma verificação de triagem: não modela variação de Voc por temperatura,
    orientação/sombreamento, corrente de curto-circuito corrigida nem projeto executivo.
    """
    voc = numero(modulo, "voc_v")
    vmp = numero(modulo, "vmp_v")
    isc = numero(modulo, "isc_a")
    v_max = numero(inversor, "tensao_max_entrada_v")
    mppt_min = numero(inversor, "faixa_mppt_min_v")
    mppt_max = numero(inversor, "faixa_mppt_max_v")
    corrente = numero(inversor, "corrente_max_entrada_a")
    mppts = int(numero(inversor, "numero_mppt", 0) or 0)
    if not all(x is not None and x > 0 for x in (voc, vmp, isc, v_max, mppt_min, mppt_max, corrente)) or mppts < 1:
        return None
    if voc >= v_max or isc > corrente:
        return None
    max_serie = min(math.floor((v_max - 1e-9) / voc), math.floor(mppt_max / vmp))
    min_serie = max(1, math.ceil(mppt_min / vmp))
    for serie in range(max_serie, min_serie - 1, -1):
        if quantidade % serie != 0:
            continue
        strings = quantidade // serie
        if strings > mppts:
            continue
        # Uma string por MPPT nesta configuração simplificada.
        if serie * vmp < mppt_min or serie * vmp > mppt_max or serie * voc >= v_max:
            continue
        return {"modulos_por_string": serie, "numero_strings": strings,
                "tensao_operacao_string_v": round(serie * vmp, 2),
                "tensao_circuito_aberto_string_v": round(serie * voc, 2)}
    return None


def dimensionar(consumo_kwh, hsp, percentual, modulos=None, inversores=None,
                baterias=None, usar_bateria=False, autonomia_h=0,
                fator_desempenho=FATOR_DESEMPENHO_PADRAO,
                localizacao="Não informada", fonte_hsp="Informada pelo usuário"):
    """Calcula potência, seleciona equipamentos com preço e dados essenciais e estima orçamento."""
    try:
        consumo_kwh, hsp, percentual = float(consumo_kwh), float(hsp), float(percentual)
        fator_desempenho = float(fator_desempenho)
    except (TypeError, ValueError):
        raise ValueError("Informe números válidos para consumo, HSP, atendimento e fator de desempenho.")
    if not all(math.isfinite(v) for v in (consumo_kwh, hsp, percentual, fator_desempenho)):
        raise ValueError("Os valores informados precisam ser números finitos.")
    if consumo_kwh <= 0 or hsp <= 0 or not 0 < percentual <= 100:
        raise ValueError("Consumo e HSP devem ser positivos; atendimento deve estar entre 1 e 100%.")
    if not 0 < fator_desempenho <= 1:
        raise ValueError("O fator de desempenho deve estar entre 0 e 1.")
    if modulos is None: modulos = carregar_dataset("modulos.csv")
    if inversores is None: inversores = carregar_dataset("inversores.csv")
    if baterias is None: baterias = carregar_dataset("baterias.csv")

    energia = consumo_kwh * percentual / 100
    potencia_kwp = energia / (hsp * DIAS_MES * fator_desempenho)
    opcoes_modulo = _validar_modulos(modulos)
    if not opcoes_modulo:
        raise ValueError("Não há módulos com preço e especificações elétricas completas. Consulte FONTES_E_METODOLOGIA.md.")

    propostas = []
    for modulo in opcoes_modulo:
        qtd = math.ceil(potencia_kwp * 1000 / numero(modulo, "potencia_wp"))
        instalada = qtd * numero(modulo, "potencia_wp") / 1000
        for inversor in inversores:
            nominal = numero(inversor, "potencia_nominal_w")
            max_fv = numero(inversor, "potencia_max_fv_w")
            preco_inv = numero(inversor, "preco_brl")
            if not all(v is not None and v > 0 for v in (nominal, max_fv, preco_inv)):
                continue
            if _texto(inversor, "tipo") not in ("híbrido", "hibrido", "on-grid", "ongrid"):
                continue
            if nominal < potencia_kwp * 1000 * 0.7 or max_fv < instalada * 1000:
                continue
            if usar_bateria and (_texto(inversor, "tipo") not in ("híbrido", "hibrido") or _texto(inversor, "compativel_bateria") not in ("sim", "yes", "true", "1")):
                continue
            strings = _configurar_strings(modulo, inversor, qtd)
            if strings is None:
                continue
            custo_modulos = qtd * numero(modulo, "preco_brl")
            propostas.append((custo_modulos + preco_inv, modulo, inversor, qtd, instalada, strings))
    if not propostas:
        if usar_bateria:
            raise ValueError("Não há combinação com preço e compatibilidade básica para uma solução híbrida. Verifique preços e dados elétricos nos CSVs.")
        raise ValueError("Não há combinação de módulo e inversor com preço e compatibilidade básica. Verifique os CSVs e as fontes.")
    _, modulo, inversor, qtd_modulos, instalada, strings = min(propostas, key=lambda p: p[0])

    capacidade_necessaria = qtd_baterias = capacidade_instalada = custo_baterias = 0.0
    bateria_escolhida = None
    capacidade_util_bateria = 0.0
    if usar_bateria:
        try: autonomia_h = float(autonomia_h)
        except (TypeError, ValueError): raise ValueError("Informe a autonomia desejada em horas.")
        if not math.isfinite(autonomia_h) or not 0 < autonomia_h <= 24:
            raise ValueError("A autonomia deve ser maior que 0 e no máximo 24 horas.")
        energia_autonomia = (consumo_kwh / DIAS_MES) * (autonomia_h / 24)
        capacidade_necessaria = energia_autonomia / (0.90 * EFICIENCIA_BATERIA_PADRAO)
        opcoes_bateria = []
        for bateria in baterias:
            capacidade = numero(bateria, "capacidade_kwh")
            dod = numero(bateria, "dod_pct")
            preco = numero(bateria, "preco_brl")
            tensao = numero(bateria, "tensao_nominal_v")
            marca_compativel = _texto(bateria, "fabricante") == _texto(inversor, "fabricante")
            if (capacidade and dod and preco and tensao and capacidade > 0 and 0 < dod <= 100 and preco > 0
                    and 40 <= tensao <= 60 and marca_compativel):
                capacidade_util = capacidade * dod / 100
                opcoes_bateria.append((preco / capacidade_util, bateria, capacidade_util))
        if not opcoes_bateria:
            raise ValueError("Não há bateria com preço e tensão compatíveis e da mesma marca do inversor híbrido selecionado. A compatibilidade precisa ser confirmada pelo fabricante.")
        _, bateria_escolhida, capacidade_util_bateria = min(opcoes_bateria, key=lambda x: x[0])
        qtd_baterias = math.ceil(capacidade_necessaria / capacidade_util_bateria)
        capacidade_instalada = qtd_baterias * numero(bateria_escolhida, "capacidade_kwh")
        custo_baterias = qtd_baterias * numero(bateria_escolhida, "preco_brl")

    custo_modulos = qtd_modulos * numero(modulo, "preco_brl")
    custo_inversor = numero(inversor, "preco_brl")
    geracao_estimada = instalada * hsp * DIAS_MES * fator_desempenho
    return {
        "consumo": consumo_kwh, "percentual": percentual, "energia": energia,
        "hsp": hsp, "fator": fator_desempenho, "potencia": potencia_kwp,
        "geracao_estimada": geracao_estimada, "instalada": instalada,
        "localizacao": str(localizacao or "Não informada"), "fonte_hsp": str(fonte_hsp or "Não informada"),
        "modulo": modulo, "qtd_modulos": qtd_modulos, "inversor": inversor,
        "strings": strings, "usar_bateria": bool(usar_bateria), "autonomia": autonomia_h,
        "bateria": bateria_escolhida, "qtd_baterias": qtd_baterias,
        "capacidade_necessaria": capacidade_necessaria, "capacidade_util_bateria": capacidade_util_bateria,
        "capacidade_instalada": capacidade_instalada, "custo_modulos": custo_modulos,
        "custo_inversor": custo_inversor, "custo_baterias": custo_baterias,
        "custo_total": custo_modulos + custo_inversor + custo_baterias,
        "custos_inclusos": "módulos, inversor e baterias quando solicitadas",
        "custos_excluidos": "instalação, estrutura, cabos, conectores, proteções, frete e adequações elétricas",
    }
