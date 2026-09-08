INCIDENTE_INICIAL = {
    "horario": "03:17",
    "titulo": "Falha crítica na API",
    "descricao": "A API parou de responder após uma nova atualização.",
    "nivel": "CRÍTICO",
    "usuarios_afetados": 1248,

    "logs": [
        "03:16:43 - Taxa de erros acima de 80%",
        "03:16:52 - Banco de dados sem resposta",
        "03:17:05 - Timeouts detectados na API",
        "03:17:15 - 1.248 usuários afetados"
    ],

    "acoes": [
        {
            "id": "verificar_logs",
            "titulo": "Verificar logs",
            "descricao": "Investigar os registros mais recentes."
        },
        {
            "id": "reiniciar_servidor",
            "titulo": "Reiniciar servidor",
            "descricao": "Tentar restaurar o serviço imediatamente."
        },
        {
            "id": "fazer_rollback",
            "titulo": "Fazer rollback",
            "descricao": "Voltar para a versão anterior do sistema."
        },
        {
            "id": "analisar_banco",
            "titulo": "Analisar banco",
            "descricao": "Verificar conexões e consultas travadas."
        }
    ]
}


RESULTADOS_ACOES = {
    "verificar_logs": {
        "titulo": "Logs analisados",
        "mensagem": (
            "Os erros começaram logo após a última atualização. "
            "O número de conexões com o banco está aumentando rapidamente."
        ),
        "pontos": 15,
        "usuarios_adicionados": 40
    },

    "reiniciar_servidor": {
        "titulo": "Reinicialização malsucedida",
        "mensagem": (
            "O servidor voltou por alguns segundos, mas caiu novamente. "
            "Mais usuários foram afetados."
        ),
        "pontos": -25,
        "usuarios_adicionados": 420
    },

    "fazer_rollback": {
        "titulo": "Rollback iniciado",
        "mensagem": (
            "A versão anterior foi restaurada, mas o banco de dados "
            "continua sobrecarregado."
        ),
        "pontos": 5,
        "usuarios_adicionados": 110
    },

    "analisar_banco": {
        "titulo": "Banco analisado",
        "mensagem": (
            "O limite de conexões foi atingido. A versão atual parece "
            "estar criando conexões sem encerrá-las."
        ),
        "pontos": 20,
        "usuarios_adicionados": 30
    }
}

RESULTADO_VITORIA = {
    "titulo": "Incidente resolvido",
    "mensagem": (
        "As pistas confirmaram que a nova versão estava mantendo "
        "conexões abertas com o banco. O rollback restaurou o sistema."
    ),
    "pontos": 30,
    "usuarios_adicionados": 0,
    "finalizado": True,
    "sucesso": True
}


RESULTADO_DERROTA = {
    "titulo": "O incidente saiu de controle",
    "mensagem": (
        "O rollback foi realizado sem informações suficientes. "
        "A operação falhou e o banco de dados ficou ainda mais sobrecarregado."
    ),
    "pontos": -30,
    "usuarios_adicionados": 600,
    "finalizado": True,
    "sucesso": False
}

def obter_incidente_inicial():
    return INCIDENTE_INICIAL

def executar_acao(acao_id):
    return RESULTADOS_ACOES.get(
        acao_id,
        {
            "titulo": "Ação inválida",
            "mensagem": "O sistema não reconheceu essa decisão.",
            "pontos": 0,
            "usuarios_adicionados": 0
        }
    )

def processar_acao(acao_id, estado):
    if estado["finalizado"]:
        return estado["resultado_final"], estado

    if acao_id in estado["acoes_realizadas"]:
        resultado = {
            "titulo": "Ação já realizada",
            "mensagem": "Você precisa escolher outra estratégia."
        }

        return resultado, estado

    if acao_id == "fazer_rollback":
        pistas_necessarias = {
            "verificar_logs",
            "analisar_banco"
        }

        pistas_encontradas = set(
            estado["acoes_realizadas"]
        )

        if pistas_necessarias.issubset(pistas_encontradas):
            resultado = RESULTADO_VITORIA
        else:
            resultado = RESULTADO_DERROTA

    else:
        resultado = executar_acao(acao_id)

    estado["pontuacao"] = max(
        0,
        estado["pontuacao"] + resultado["pontos"]
    )

    estado["usuarios_afetados"] += resultado[
        "usuarios_adicionados"
    ]

    estado["acoes_realizadas"].append(acao_id)

    if resultado.get("finalizado", False):
        estado["finalizado"] = True

        estado["resultado_final"] = {
            "titulo": resultado["titulo"],
            "mensagem": resultado["mensagem"],
            "sucesso": resultado["sucesso"]
        }

    return resultado, estado

def criar_estado_inicial():
    return {
        "pontuacao": 100,
        "usuarios_afetados": 1248,
        "acoes_realizadas": [],
        "finalizado": False,
        "resultado_final": None
    }

