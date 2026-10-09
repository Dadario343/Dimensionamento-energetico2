"""
Sistema de Dimensionamento Energético — versão web (Flask)
------------------------------------------------------------
Reaproveita a persistência, validações e regras de negócio já
existentes em src/, através da camada de serviço em src/servicos.py.

O sistema de console (main.py) continua funcionando normalmente e
compartilha os mesmos dados: ambos leem/gravam em src/dados/dados.json.

Para executar:
    pip install -r requirements.txt
    python app.py

Depois acesse http://127.0.0.1:5000 no navegador.
"""

from functools import wraps

from flask import Flask, flash, redirect, render_template, request, session, url_for

from src import servicos

app = Flask(__name__)
app.secret_key = "troque-esta-chave-antes-de-colocar-em-producao"


def login_obrigatorio(view):
    """Bloqueia o acesso a uma rota se o usuário não estiver logado."""

    @wraps(view)
    def wrapper(*args, **kwargs):
        if "email_usuario" not in session:
            flash("Faça login para continuar.", "erro")
            return redirect(url_for("login"))
        return view(*args, **kwargs)

    return wrapper


# =========================================================
# Autenticação
# =========================================================

@app.route("/")
def index():
    if "email_usuario" in session:
        return redirect(url_for("listar_imoveis"))
    return redirect(url_for("login"))


@app.route("/cadastro", methods=["GET", "POST"])
def cadastro():
    if request.method == "POST":
        nome = request.form.get("nome", "")
        email = request.form.get("email", "")
        senha = request.form.get("senha", "")
        confirmar_senha = request.form.get("confirmar_senha", "")

        if senha != confirmar_senha:
            flash("As senhas não coincidem.", "erro")
            return render_template("cadastro.html")

        sucesso, resultado = servicos.cadastrar_usuario_srv(nome, email, senha)
        if not sucesso:
            flash(resultado, "erro")
            return render_template("cadastro.html")

        flash("Conta criada com sucesso! Faça login para continuar.", "sucesso")
        return redirect(url_for("login"))

    return render_template("cadastro.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "")
        senha = request.form.get("senha", "")

        sucesso, nome_ou_erro, email_confirmado = servicos.autenticar_usuario_srv(email, senha)
        if not sucesso:
            flash(nome_ou_erro, "erro")
            return render_template("login.html")

        session["email_usuario"] = email_confirmado
        session["nome_usuario"] = nome_ou_erro
        flash(f"Bem-vindo(a), {nome_ou_erro}!", "sucesso")
        return redirect(url_for("listar_imoveis"))

    return render_template("login.html")


@app.route("/logout")
def logout():
    session.clear()
    flash("Logout realizado.", "sucesso")
    return redirect(url_for("login"))


# =========================================================
# Imóveis
# =========================================================

@app.route("/imoveis")
@login_obrigatorio
def listar_imoveis():
    imoveis = servicos.listar_imoveis_srv(session["email_usuario"])
    return render_template("imoveis.html", imoveis=imoveis)


@app.route("/imoveis/novo", methods=["GET", "POST"])
@login_obrigatorio
def novo_imovel():
    if request.method == "POST":
        nome = request.form.get("nome", "")
        endereco = request.form.get("endereco", "")

        sucesso, resultado = servicos.cadastrar_imovel_srv(session["email_usuario"], nome, endereco)
        if not sucesso:
            flash(resultado, "erro")
            return render_template("imovel_form.html", modo="novo")

        flash("Imóvel cadastrado com sucesso!", "sucesso")
        return redirect(url_for("listar_imoveis"))

    return render_template("imovel_form.html", modo="novo")


@app.route("/imoveis/<int:id_imovel>/editar", methods=["GET", "POST"])
@login_obrigatorio
def editar_imovel(id_imovel):
    imovel = servicos.buscar_imovel_srv(session["email_usuario"], id_imovel)
    if imovel is None:
        flash("Imóvel não encontrado.", "erro")
        return redirect(url_for("listar_imoveis"))

    if request.method == "POST":
        nome = request.form.get("nome", "")
        endereco = request.form.get("endereco", "")
        sucesso, mensagem = servicos.editar_imovel_srv(session["email_usuario"], id_imovel, nome, endereco)
        flash(mensagem, "sucesso" if sucesso else "erro")
        return redirect(url_for("listar_imoveis"))

    return render_template("imovel_form.html", modo="editar", imovel=imovel)


@app.route("/imoveis/<int:id_imovel>/excluir", methods=["POST"])
@login_obrigatorio
def excluir_imovel(id_imovel):
    sucesso, mensagem = servicos.excluir_imovel_srv(session["email_usuario"], id_imovel)
    flash(mensagem, "sucesso" if sucesso else "erro")
    return redirect(url_for("listar_imoveis"))


@app.route("/imoveis/<int:id_imovel>")
@login_obrigatorio
def detalhe_imovel(id_imovel):
    imovel = servicos.buscar_imovel_srv(session["email_usuario"], id_imovel)
    if imovel is None:
        flash("Imóvel não encontrado.", "erro")
        return redirect(url_for("listar_imoveis"))

    consumo_estimado = servicos.calcular_consumo_total_estimado_srv(session["email_usuario"], id_imovel)
    resumo = servicos.calcular_resumo_energetico_srv(session["email_usuario"], id_imovel)
    historico = servicos.obter_historico_srv(session["email_usuario"], id_imovel)
    maior_valor = max((registro["consumo_kwh"] for registro in historico), default=0)

    return render_template(
        "imovel_detalhe.html",
        imovel=imovel,
        consumo_estimado=consumo_estimado,
        resumo=resumo,
        historico=historico,
        maior_valor=maior_valor,
    )


# =========================================================
# Equipamentos
# =========================================================

@app.route("/imoveis/<int:id_imovel>/equipamentos/novo", methods=["GET", "POST"])
@login_obrigatorio
def novo_equipamento(id_imovel):
    imovel = servicos.buscar_imovel_srv(session["email_usuario"], id_imovel)
    if imovel is None:
        flash("Imóvel não encontrado.", "erro")
        return redirect(url_for("listar_imoveis"))

    if request.method == "POST":
        nome = request.form.get("nome", "")
        potencia = request.form.get("potencia", "")
        quantidade = request.form.get("quantidade", "")
        horas_dia = request.form.get("horas_dia", "")

        sucesso, mensagem = servicos.cadastrar_equipamento_srv(
            session["email_usuario"], id_imovel, nome, potencia, quantidade, horas_dia
        )
        if sucesso:
            flash(mensagem, "sucesso")
            return redirect(url_for("detalhe_imovel", id_imovel=id_imovel))

        flash(mensagem, "erro")
        return render_template("equipamento_form.html", imovel=imovel)

    return render_template("equipamento_form.html", imovel=imovel)


@app.route("/imoveis/<int:id_imovel>/equipamentos/<int:indice>/remover", methods=["POST"])
@login_obrigatorio
def remover_equipamento(id_imovel, indice):
    sucesso, mensagem = servicos.remover_equipamento_srv(session["email_usuario"], id_imovel, indice)
    flash(mensagem, "sucesso" if sucesso else "erro")
    return redirect(url_for("detalhe_imovel", id_imovel=id_imovel))


# =========================================================
# Consumo
# =========================================================

@app.route("/imoveis/<int:id_imovel>/consumo/novo", methods=["GET", "POST"])
@login_obrigatorio
def novo_consumo(id_imovel):
    imovel = servicos.buscar_imovel_srv(session["email_usuario"], id_imovel)
    if imovel is None:
        flash("Imóvel não encontrado.", "erro")
        return redirect(url_for("listar_imoveis"))

    consumo_estimado = servicos.calcular_consumo_total_estimado_srv(session["email_usuario"], id_imovel)

    if request.method == "POST":
        mes = request.form.get("mes", "")
        usar_estimado = request.form.get("usar_estimado")
        consumo_kwh = consumo_estimado if usar_estimado == "sim" else request.form.get("consumo_kwh", "")

        sucesso, mensagem = servicos.registrar_consumo_srv(session["email_usuario"], id_imovel, mes, consumo_kwh)
        flash(mensagem, "sucesso" if sucesso else "erro")
        if sucesso:
            return redirect(url_for("detalhe_imovel", id_imovel=id_imovel))

    return render_template("consumo_form.html", imovel=imovel, consumo_estimado=consumo_estimado)


# =========================================================
# Dimensionamento fotovoltaico (CP2)
# =========================================================
from src.fotovoltaico import carregar_dataset, dimensionar

@app.route("/imoveis/<int:id_imovel>/fotovoltaico", methods=["GET", "POST"])
@login_obrigatorio
def dimensionar_fotovoltaico(id_imovel):
    imovel = servicos.buscar_imovel_srv(session["email_usuario"], id_imovel)
    if imovel is None:
        flash("Imóvel não encontrado.", "erro")
        return redirect(url_for("listar_imoveis"))

    historico = imovel.get("historico_consumo", [])
    consumo_medio = (sum(float(r.get("consumo_kwh", 0)) for r in historico) / len(historico)) if historico else servicos.calcular_consumo_total_estimado_srv(session["email_usuario"], id_imovel)
    modulos = carregar_dataset("modulos.csv")
    inversores = carregar_dataset("inversores.csv")
    baterias = carregar_dataset("baterias.csv")
    resultado = None
    if request.method == "POST":
        try:
            consumo = float(request.form.get("consumo_kwh", consumo_medio))
            hsp = float(request.form.get("hsp", "4.5"))
            percentual = float(request.form.get("percentual", "100"))
            usar_bateria = request.form.get("baterias") == "sim"
            autonomia = float(request.form.get("autonomia", "0")) if usar_bateria else 0
            localizacao = request.form.get("localizacao", "").strip() or imovel.get("endereco", "Não informada")
            fonte_hsp = request.form.get("fonte_hsp", "").strip() or "Valor de HSP informado manualmente; validar com fonte solar local"
            resultado = dimensionar(consumo, hsp, percentual, modulos, inversores, baterias, usar_bateria, autonomia,
                                    localizacao=localizacao, fonte_hsp=fonte_hsp)
        except (ValueError, TypeError) as erro:
            flash(str(erro) or "Confira os valores informados.", "erro")
    return render_template("fotovoltaico.html", imovel=imovel, consumo_medio=consumo_medio,
        modulos=modulos, inversores=inversores, baterias=baterias, resultado=resultado,
        modulos_com_preco=sum(1 for m in modulos if float(str(m.get("preco_brl", "0") or "0").replace(",", ".")) > 0),
        inversores_com_preco=sum(1 for i in inversores if float(str(i.get("preco_brl", "0") or "0").replace(",", ".")) > 0),
        baterias_com_preco=sum(1 for b in baterias if float(str(b.get("preco_brl", "0") or "0").replace(",", ".")) > 0))


if __name__ == "__main__":
    app.run(debug=True)
