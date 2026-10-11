"""
Camada de serviço da aplicação.
-------------------------------
As funções aqui NÃO usam input()/print(): recebem parâmetros e devolvem
resultados (sucesso/erro + dados), para poderem ser chamadas tanto pela
interface web (app.py) quanto por qualquer outra interface no futuro.

Reaproveita a mesma persistência (src/persistencia.py), as mesmas
validações (src/validacoes.py) e o mesmo cálculo de consumo
(src/equipamentos.py) usados pela versão de console (main.py), então
os dois modos de uso compartilham os mesmos dados e as mesmas regras.
"""

from src.persistencia import carregar_dados, salvar_dados
from src.validacoes import email_valido, texto_valido, numero_positivo
from src.usuarios import gerar_hash_senha
from src.equipamentos import calcular_consumo_equipamento


# =========================================================
# Usuários
# =========================================================

def cadastrar_usuario_srv(nome, email, senha):
    """Cadastra um usuário. Retorna (sucesso: bool, mensagem_ou_email: str)."""
    dados = carregar_dados()

    nome = (nome or "").strip()
    email = (email or "").strip().lower()
    senha = senha or ""

    if not texto_valido(nome):
        return False, "Nome inválido."
    if not email_valido(email):
        return False, "E-mail inválido."
    if email in dados["usuarios"]:
        return False, "Já existe um usuário cadastrado com esse e-mail."
    if not texto_valido(senha) or len(senha) < 4:
        return False, "A senha deve ter pelo menos 4 caracteres."

    dados["usuarios"][email] = {
        "nome": nome,
        "senha_hash": gerar_hash_senha(senha),
        "imoveis": [],
    }
    salvar_dados(dados)
    return True, email


def autenticar_usuario_srv(email, senha):
    """Autentica um usuário. Retorna (sucesso: bool, nome_ou_erro: str, email: str|None)."""
    dados = carregar_dados()

    email = (email or "").strip().lower()
    senha = senha or ""

    usuario = dados["usuarios"].get(email)
    if usuario is None:
        return False, "Usuário não encontrado.", None
    if usuario["senha_hash"] != gerar_hash_senha(senha):
        return False, "Senha incorreta.", None

    return True, usuario["nome"], email


# =========================================================
# Imóveis
# =========================================================

def listar_imoveis_srv(email_usuario):
    dados = carregar_dados()
    return dados["usuarios"][email_usuario]["imoveis"]


def buscar_imovel_srv(email_usuario, id_imovel):
    for imovel in listar_imoveis_srv(email_usuario):
        if imovel["id"] == id_imovel:
            return imovel
    return None


def cadastrar_imovel_srv(email_usuario, nome, endereco):
    nome = (nome or "").strip()
    endereco = (endereco or "").strip()

    if not texto_valido(nome):
        return False, "Nome do imóvel inválido."

    dados = carregar_dados()
    usuario = dados["usuarios"][email_usuario]
    novo_id = len(usuario["imoveis"]) + 1

    usuario["imoveis"].append({
        "id": novo_id,
        "nome": nome,
        "endereco": endereco,
        "equipamentos": [],
        "historico_consumo": [],
    })
    salvar_dados(dados)
    return True, novo_id


def editar_imovel_srv(email_usuario, id_imovel, novo_nome, novo_endereco):
    dados = carregar_dados()
    for imovel in dados["usuarios"][email_usuario]["imoveis"]:
        if imovel["id"] == id_imovel:
            if texto_valido(novo_nome):
                imovel["nome"] = novo_nome.strip()
            if texto_valido(novo_endereco):
                imovel["endereco"] = novo_endereco.strip()
            salvar_dados(dados)
            return True, "Imóvel atualizado com sucesso!"
    return False, "Imóvel não encontrado."


def excluir_imovel_srv(email_usuario, id_imovel):
    dados = carregar_dados()
    usuario = dados["usuarios"][email_usuario]
    quantidade_antes = len(usuario["imoveis"])

    usuario["imoveis"] = [i for i in usuario["imoveis"] if i["id"] != id_imovel]

    if len(usuario["imoveis"]) < quantidade_antes:
        salvar_dados(dados)
        return True, "Imóvel excluído com sucesso!"
    return False, "Imóvel não encontrado."


# =========================================================
# Equipamentos
# =========================================================

def cadastrar_equipamento_srv(email_usuario, id_imovel, nome, potencia, quantidade, horas_dia):
    nome = (nome or "").strip()

    if not texto_valido(nome):
        return False, "Nome do equipamento inválido."
    if not numero_positivo(potencia):
        return False, "Potência inválida."
    if not str(quantidade).isdigit() or int(quantidade) <= 0:
        return False, "Quantidade inválida."
    if not numero_positivo(horas_dia) or float(horas_dia) > 24:
        return False, "Tempo de uso inválido (deve ser entre 0 e 24 horas)."

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
            return True, "Equipamento cadastrado com sucesso!"
    return False, "Imóvel não encontrado."


def remover_equipamento_srv(email_usuario, id_imovel, indice):
    dados = carregar_dados()
    for imovel in dados["usuarios"][email_usuario]["imoveis"]:
        if imovel["id"] == id_imovel:
            if 0 <= indice < len(imovel["equipamentos"]):
                removido = imovel["equipamentos"].pop(indice)
                salvar_dados(dados)
                return True, f"Equipamento '{removido['nome']}' removido com sucesso!"
            return False, "Equipamento não encontrado."
    return False, "Imóvel não encontrado."


def calcular_consumo_total_estimado_srv(email_usuario, id_imovel):
    imovel = buscar_imovel_srv(email_usuario, id_imovel)
    if imovel is None:
        return 0
    return sum(calcular_consumo_equipamento(eq) for eq in imovel["equipamentos"])


# =========================================================
# Consumo
# =========================================================

def registrar_consumo_srv(email_usuario, id_imovel, mes, consumo_kwh):
    mes = (mes or "").strip()

    if not texto_valido(mes):
        return False, "Mês inválido."
    if not numero_positivo(consumo_kwh):
        return False, "Valor de consumo inválido."

    dados = carregar_dados()
    for imovel in dados["usuarios"][email_usuario]["imoveis"]:
        if imovel["id"] == id_imovel:
            imovel["historico_consumo"].append({
                "mes": mes,
                "consumo_kwh": round(float(consumo_kwh), 2),
            })
            salvar_dados(dados)
            return True, "Consumo registrado com sucesso!"
    return False, "Imóvel não encontrado."


def obter_historico_srv(email_usuario, id_imovel):
    imovel = buscar_imovel_srv(email_usuario, id_imovel)
    return imovel["historico_consumo"] if imovel else []


def calcular_resumo_energetico_srv(email_usuario, id_imovel):
    historico = obter_historico_srv(email_usuario, id_imovel)
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
