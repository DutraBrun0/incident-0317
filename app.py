import os

from dotenv import load_dotenv

from flask import (
    Flask,
    render_template,
    request,
    session,
    redirect,
    url_for,
)

from game import (
    obter_incidente_inicial,
    criar_estado_inicial,
    processar_acao,
    interpretar_comando,
    obter_comandos_disponiveis,
    sortear_incidente,
)


load_dotenv()


def obter_chave_secreta():
    chave = os.getenv("SECRET_KEY")

    if not chave:
        raise RuntimeError(
            "A variável SECRET_KEY não foi configurada. "
            "Crie o arquivo .env antes de executar o projeto."
        )

    return chave


def obter_modo_debug():
    valor = os.getenv(
        "FLASK_DEBUG",
        "false",
    )

    return valor.lower() in {
        "1",
        "true",
        "yes",
        "sim",
    }


app = Flask(__name__)

app.config["SECRET_KEY"] = obter_chave_secreta()


def formatar_tempo(segundos):
    minutos = segundos // 60
    segundos_restantes = segundos % 60

    return (
        f"{minutos:02d}:"
        f"{segundos_restantes:02d}"
    )


def criar_nova_partida(cenario_anterior=None):
    cenario_id = sortear_incidente(
        cenario_anterior
    )

    return criar_estado_inicial(
        cenario_id
    )


def obter_estado():
    estado = session.get("estado")

    if not isinstance(estado, dict):
        estado = criar_nova_partida()
        session["estado"] = estado

        return estado

    cenario_id = estado.get("cenario_id")

    estado_padrao = criar_estado_inicial(
        cenario_id
    )

    estado["cenario_id"] = (
        estado_padrao["cenario_id"]
    )

    for chave, valor in estado_padrao.items():
        estado.setdefault(chave, valor)

    session["estado"] = estado

    return estado


def gerar_relatorio_final(estado):
    resultado_final = (
        estado.get("resultado_final") or {}
    )

    sucesso = resultado_final.get(
        "sucesso",
        False,
    )

    pontuacao = estado["pontuacao"]

    usuarios_afetados = (
        estado["usuarios_afetados"]
    )

    estado_inicial = criar_estado_inicial(
        estado["cenario_id"]
    )

    usuarios_iniciais = (
        estado_inicial["usuarios_afetados"]
    )

    tempo_inicial = (
        estado_inicial["tempo_restante"]
    )

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

    impacto_relativo = (
        usuarios_afetados / usuarios_iniciais
        if usuarios_iniciais > 0
        else 0
    )

    if (
        sucesso
        and pontuacao >= 250
        and impacto_relativo <= 0.5
        and estado["tempo_restante"] > 0
    ):
        classificacao = "EXEMPLAR"

        avaliacao = (
            "O incidente foi investigado, contido e "
            "recuperado com excelente controle operacional."
        )

    elif (
        sucesso
        and impacto_relativo <= 1
        and estado["tempo_restante"] > 0
    ):
        classificacao = "CONTROLADO"

        avaliacao = (
            "O serviço foi recuperado com impacto "
            "controlado e sem deixar falhas ativas."
        )

    elif sucesso:
        classificacao = "ARRISCADO"

        avaliacao = (
            "O sistema foi recuperado, mas a resposta "
            "demorou e o impacto aumentou durante a operação."
        )

    else:
        classificacao = "CRÍTICO"

        avaliacao = (
            "A resposta não conseguiu controlar o "
            "incidente. A sequência das decisões deve "
            "ser revisada."
        )

    tempo_utilizado = max(
        0,
        tempo_inicial - estado["tempo_restante"],
    )

    sequencia_comandos = [
        item["comando"]
        for item in historico_acoes
    ]

    return {
        "classificacao": classificacao,
        "avaliacao": avaliacao,
        "pontuacao": pontuacao,
        "usuarios_afetados": usuarios_afetados,
        "tempo_utilizado": formatar_tempo(
            tempo_utilizado
        ),
        "tempo_restante": formatar_tempo(
            estado["tempo_restante"]
        ),
        "total_decisoes": len(historico_acoes),
        "decisoes_corretas": decisoes_corretas,
        "decisoes_prejudiciais": (
            decisoes_prejudiciais
        ),
        "decisoes_neutras": decisoes_neutras,
        "sequencia_comandos": sequencia_comandos,
        "sucesso": sucesso,
    }


@app.route("/")
def index():
    estado = obter_estado()

    incidente = obter_incidente_inicial(
        estado["cenario_id"]
    )

    return render_template(
        "index.html",
        incidente=incidente,
        estado=estado,
    )


@app.route("/comando", methods=["POST"])
def executar_comando():
    estado = obter_estado()

    incidente = obter_incidente_inicial(
        estado["cenario_id"]
    )

    comando = request.form.get(
        "comando",
        "",
    )

    acao_id = interpretar_comando(
        comando,
        estado,
    )

    if acao_id == "reiniciar_partida":
        cenario_anterior = estado.get(
            "cenario_id"
        )

        session.clear()

        session["estado"] = criar_nova_partida(
            cenario_anterior
        )

        return redirect(
            url_for("index")
        )

    acao_executada = False

    if estado["finalizado"]:
        resultado = {
            "titulo": "Simulação encerrada",
            "mensagem": (
                'Digite "reiniciar" para começar '
                "um novo incidente."
            ),
        }

    elif acao_id == "ajuda":
        comandos = [
            "ajuda",
            "status",
            "reiniciar",
        ]

        comandos.extend(
            obter_comandos_disponiveis(
                estado
            )
        )

        resultado = {
            "titulo": "Comandos disponíveis",
            "mensagem": ", ".join(comandos),
        }

    elif acao_id == "status":
        tempo = formatar_tempo(
            estado["tempo_restante"]
        )

        resultado = {
            "titulo": "Estado do incidente",
            "mensagem": (
                f"Pontuação: "
                f"{estado['pontuacao']} | "
                f"Usuários afetados: "
                f"{estado['usuarios_afetados']} | "
                f"Tempo restante: {tempo} | "
                f"Fase: {estado['fase']}"
            ),
        }

    elif acao_id is None:
        resultado = {
            "titulo": "Comando não reconhecido",
            "mensagem": (
                'Digite "ajuda" para visualizar '
                "os comandos disponíveis."
            ),
        }

    else:
        acoes_anteriores = set(
            estado["acoes_realizadas"]
        )

        resultado, estado = processar_acao(
            acao_id,
            estado,
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
            resultado.get(
                "usuarios_adicionados",
                0,
            )
            if acao_executada
            else 0
        ),
    }

    estado["historico"].append(registro)

    if estado["finalizado"]:
        estado["relatorio_final"] = (
            gerar_relatorio_final(estado)
        )

    session["estado"] = estado

    return render_template(
        "index.html",
        incidente=incidente,
        estado=estado,
    )


@app.route("/reiniciar", methods=["POST"])
def reiniciar():
    estado_anterior = session.get(
        "estado",
        {},
    )

    cenario_anterior = (
        estado_anterior.get("cenario_id")
        if isinstance(estado_anterior, dict)
        else None
    )

    session.clear()

    session["estado"] = criar_nova_partida(
        cenario_anterior
    )

    return redirect(
        url_for("index")
    )


if __name__ == "__main__":
    app.run(
        debug=obter_modo_debug()
    )