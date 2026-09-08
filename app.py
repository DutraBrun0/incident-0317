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

    estado.setdefault("relatorio_final", None)

    session["estado"] = estado

    return estado


def formatar_tempo(segundos):
    minutos = segundos // 60
    segundos_restantes = segundos % 60

    return f"{minutos:02d}:{segundos_restantes:02d}"


def gerar_relatorio_final(estado):
    resultado_final = estado.get("resultado_final") or {}
    sucesso = resultado_final.get("sucesso", False)

    pontuacao = estado["pontuacao"]
    usuarios_afetados = estado["usuarios_afetados"]

    historico_acoes = [
        item
        for item in estado["historico"]
        if item.get("executada", False)
    ]

    decisoes_corretas = sum(
        1
        for item in historico_acoes
        if item.get("pontos", 0) > 0
    )

    decisoes_prejudiciais = sum(
        1
        for item in historico_acoes
        if item.get("pontos", 0) < 0
    )

    decisoes_neutras = sum(
        1
        for item in historico_acoes
        if item.get("pontos", 0) == 0
    )

    if (
        sucesso
        and pontuacao >= 250
        and usuarios_afetados <= 500
    ):
        classificacao = "EXEMPLAR"
        avaliacao = (
            "O incidente foi investigado, contido e recuperado "
            "com excelente controle operacional."
        )

    elif sucesso and usuarios_afetados <= 1200:
        classificacao = "CONTROLADO"
        avaliacao = (
            "O serviço foi recuperado com um impacto aceitável, "
            "apesar de algumas decisões terem consumido recursos."
        )

    elif sucesso:
        classificacao = "ARRISCADO"
        avaliacao = (
            "O sistema foi recuperado, mas a resposta demorou "
            "e muitos usuários foram afetados."
        )

    else:
        classificacao = "CRÍTICO"
        avaliacao = (
            "A resposta não conseguiu controlar o incidente. "
            "A sequência das decisões deve ser revisada."
        )

    tempo_inicial = criar_estado_inicial()["tempo_restante"]
    tempo_utilizado = tempo_inicial - estado["tempo_restante"]

    sequencia_comandos = [
        item["comando"]
        for item in historico_acoes
    ]

    return {
        "classificacao": classificacao,
        "avaliacao": avaliacao,
        "pontuacao": pontuacao,
        "usuarios_afetados": usuarios_afetados,
        "tempo_utilizado": formatar_tempo(tempo_utilizado),
        "tempo_restante": formatar_tempo(
            estado["tempo_restante"]
        ),
        "total_decisoes": len(historico_acoes),
        "decisoes_corretas": decisoes_corretas,
        "decisoes_prejudiciais": decisoes_prejudiciais,
        "decisoes_neutras": decisoes_neutras,
        "sequencia_comandos": sequencia_comandos,
        "sucesso": sucesso
    }


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

    acao_executada = False

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
        tempo = formatar_tempo(
            estado["tempo_restante"]
        )

        resultado = {
            "titulo": "Estado do incidente",
            "mensagem": (
                f"Pontuação: {estado['pontuacao']} | "
                f"Usuários afetados: "
                f"{estado['usuarios_afetados']} | "
                f"Tempo restante: {tempo} | "
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
        acoes_anteriores = set(
            estado["acoes_realizadas"]
        )

        resultado, estado = processar_acao(
            acao_id,
            estado
        )

        acao_executada = (
            acao_id in estado["acoes_realizadas"]
            and acao_id not in acoes_anteriores
        )

    registro = {
        "comando": comando,
        "titulo": resultado["titulo"],
        "resposta": resultado["mensagem"],
        "acao_id": acao_id,
        "executada": acao_executada,
        "pontos": (
            resultado.get("pontos", 0)
            if acao_executada
            else 0
        ),
        "impacto_usuarios": (
            resultado.get("usuarios_adicionados", 0)
            if acao_executada
            else 0
        )
    }

    estado["historico"].append(registro)

    if estado["finalizado"]:
        estado["relatorio_final"] = gerar_relatorio_final(
            estado
        )

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