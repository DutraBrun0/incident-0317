from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for
)

from game import (
    obter_incidente_inicial,
    executar_acao,
    criar_estado_inicial,
    processar_acao
)

app = Flask(__name__)

app.config["SECRET_KEY"] = "chave-de-desenvolvimento-0317"


def obter_estado():
    if "estado" not in session:
        session["estado"] = criar_estado_inicial()

    estado = session["estado"]

    estado.setdefault("finalizado", False)
    estado.setdefault("resultado_final", None)

    session["estado"] = estado

    return estado


@app.route("/")
def index():
    incidente = obter_incidente_inicial()
    estado = obter_estado()

    return render_template(
        "index.html",
        incidente=incidente,
        estado=estado
    )


@app.route("/acao", methods=["POST"])
def escolher_acao():
    acao_id = request.form.get("acao")

    incidente = obter_incidente_inicial()
    estado = obter_estado()

    resultado, estado = processar_acao(
        acao_id,
        estado
    )

    session["estado"] = estado

    return render_template(
        "index.html",
        incidente=incidente,
        estado=estado,
        resultado=resultado
    )

@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    session.clear()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)