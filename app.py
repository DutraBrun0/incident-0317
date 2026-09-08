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
    criar_estado_inicial,
    processar_acao,
    interpretar_comando,
    obter_comandos_disponiveis
)

app = Flask(__name__)

app.config["SECRET_KEY"] = "chave-de-desenvolvimento-0317"


def obter_estado():
    estado_padrao = criar_estado_inicial()
    estado = session.get("estado", {})

    for chave, valor in estado_padrao.items():
        estado.setdefault(chave, valor)

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


@app.route("/comando", methods=["POST"])
def executar_comando():
    comando = request.form.get("comando", "")

    incidente = obter_incidente_inicial()
    estado = obter_estado()

    acao_id = interpretar_comando(comando)

    if acao_id == "reiniciar_partida":
        session.clear()

        return redirect(url_for("index"))

    if acao_id == "ajuda":
        comandos = [
        "ajuda",
        "status",
        "reiniciar"
    ]

        comandos.extend(
        obter_comandos_disponiveis(estado)
    )

        resultado = {
        "titulo": "Comandos disponíveis",
        "mensagem": ", ".join(comandos)
    }

    elif acao_id == "status":
        resultado = {
            "titulo": "Estado do incidente",
            "mensagem": (
                f"Pontuação: {estado['pontuacao']} | "
                f"Usuários afetados: "
                f"{estado['usuarios_afetados']} | "
                f"Fase: {estado['fase']}"
            )
        }

    elif acao_id is None:
        resultado = {
            "titulo": "Comando não reconhecido",
            "mensagem": (
                'Digite "ajuda" para visualizar os comandos.'
            )
        }

    else:
        resultado, estado = processar_acao(
            acao_id,
            estado
        )

    estado["historico"].append({
        "comando": comando,
        "titulo": resultado["titulo"],
        "resposta": resultado["mensagem"]
    })

    session["estado"] = estado

    return render_template(
        "index.html",
        incidente=incidente,
        estado=estado
    )

@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    session.clear()

    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)