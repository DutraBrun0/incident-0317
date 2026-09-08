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
        "03:17:15 - 1.248 usuários afetados",
    ],

    "acoes": [
        {
            "id": "verificar_logs",
            "titulo": "Verificar logs",
            "descricao": "Investigar os registros mais recentes.",
        },
        {
            "id": "reiniciar_servidor",
            "titulo": "Reiniciar servidor",
            "descricao": "Tentar restaurar o serviço imediatamente.",
        },
        {
            "id": "fazer_rollback",
            "titulo": "Fazer rollback",
            "descricao": "Voltar para a versão anterior do sistema.",
        },
        {
            "id": "analisar_banco",
            "titulo": "Analisar banco",
            "descricao": "Verificar conexões e consultas travadas.",
        },
    ],
}


RESULTADOS_ACOES = {
    "verificar_logs": {
        "comando": "logs",
        "titulo": "Logs analisados",
        "mensagem": (
            "Os erros começaram logo após a última atualização. "
            "O número de conexões aumentou rapidamente."
        ),
        "pontos": 15,
        "usuarios_adicionados": 40,
        "tempo_gasto": 30,
        "requisitos": [],
        "pista": "erro_apos_deploy",
        "pista_texto": (
            "Os erros começaram depois do último deploy."
        ),
    },

    "reiniciar_servidor": {
        "comando": "reiniciar servidor",
        "titulo": "Reinicialização malsucedida",
        "mensagem": (
            "O servidor voltou por alguns segundos, "
            "mas caiu novamente."
        ),
        "pontos": -25,
        "usuarios_adicionados": 420,
        "tempo_gasto": 60,
        "requisitos": [],
        "pista": None,
        "pista_texto": None,
    },

    "analisar_banco": {
        "comando": "analisar banco",
        "titulo": "Banco analisado",
        "mensagem": (
            "O pool de conexões está completamente esgotado."
        ),
        "pontos": 20,
        "usuarios_adicionados": 30,
        "tempo_gasto": 45,
        "requisitos": [
            "erro_apos_deploy",
        ],
        "pista": "pool_esgotado",
        "pista_texto": (
            "A aplicação não está encerrando as conexões."
        ),
    },

    "fazer_rollback": {
        "comando": "rollback",
        "titulo": "Rollback iniciado",
        "mensagem": (
            "A versão anterior está sendo restaurada."
        ),
        "pontos": 30,
        "usuarios_adicionados": 0,
        "tempo_gasto": 60,
        "requisitos": [],
        "pista": None,
        "pista_texto": None,
    },

    "analisar_metricas": {
        "comando": "metricas",
        "titulo": "Métricas analisadas",
        "mensagem": (
            "A quantidade de conexões cresceu junto com "
            "a taxa de erros da API."
        ),
        "pontos": 10,
        "usuarios_adicionados": 50,
        "tempo_gasto": 30,
        "requisitos": [],
        "pista": "pico_de_conexoes",
        "pista_texto": (
            "Existe um pico anormal de conexões."
        ),
    },

    "verificar_filas": {
        "comando": "verificar filas",
        "titulo": "Filas verificadas",
        "mensagem": (
            "As filas estão processando normalmente. "
            "Elas provavelmente não causaram o incidente."
        ),
        "pontos": 5,
        "usuarios_adicionados": 40,
        "tempo_gasto": 25,
        "requisitos": [],
        "pista": "filas_normais",
        "pista_texto": (
            "O sistema de filas está funcionando normalmente."
        ),
    },

    "verificar_servicos_externos": {
        "comando": "verificar externos",
        "titulo": "Serviços externos verificados",
        "mensagem": (
            "Os serviços externos estão operacionais. "
            "A falha parece estar dentro da própria aplicação."
        ),
        "pontos": 5,
        "usuarios_adicionados": 45,
        "tempo_gasto": 30,
        "requisitos": [],
        "pista": "externos_operacionais",
        "pista_texto": (
            "Nenhum serviço externo apresentou falhas."
        ),
    },

    "verificar_cache": {
        "comando": "verificar cache",
        "titulo": "Cache verificado",
        "mensagem": (
            "O cache está respondendo normalmente e não "
            "apresenta aumento significativo de memória."
        ),
        "pontos": 5,
        "usuarios_adicionados": 35,
        "tempo_gasto": 25,
        "requisitos": [],
        "pista": "cache_operacional",
        "pista_texto": (
            "O cache não é a origem do incidente."
        ),
    },

    "analisar_deploy": {
        "comando": "analisar deploy",
        "titulo": "Deploy analisado",
        "mensagem": (
            "Uma nova versão foi publicada sete minutos "
            "antes do início dos erros."
        ),
        "pontos": 15,
        "usuarios_adicionados": 30,
        "tempo_gasto": 40,
        "requisitos": [
            "erro_apos_deploy",
        ],
        "pista": "deploy_suspeito",
        "pista_texto": (
            "O último deploy provavelmente iniciou o incidente."
        ),
    },

    "comparar_versoes": {
        "comando": "comparar versoes",
        "titulo": "Versões comparadas",
        "mensagem": (
            "A nova versão alterou a função responsável "
            "por abrir conexões com o banco."
        ),
        "pontos": 20,
        "usuarios_adicionados": 25,
        "tempo_gasto": 45,
        "requisitos": [
            "deploy_suspeito",
        ],
        "pista": "mudanca_nas_conexoes",
        "pista_texto": (
            "A nova versão modificou o controle das conexões."
        ),
    },

    "rastrear_requisicao": {
        "comando": "rastrear requisicao",
        "titulo": "Requisição rastreada",
        "mensagem": (
            "As requisições ficam travadas esperando uma "
            "conexão disponível com o banco."
        ),
        "pontos": 10,
        "usuarios_adicionados": 30,
        "tempo_gasto": 40,
        "requisitos": [
            "pico_de_conexoes",
        ],
        "pista": "requisicoes_aguardando",
        "pista_texto": (
            "As requisições estão paradas aguardando o banco."
        ),
    },

    "procurar_consultas_lentas": {
        "comando": "consultas lentas",
        "titulo": "Consultas analisadas",
        "mensagem": (
            "Nenhuma consulta lenta foi encontrada. "
            "O problema está na quantidade de conexões abertas."
        ),
        "pontos": 10,
        "usuarios_adicionados": 35,
        "tempo_gasto": 35,
        "requisitos": [
            "pool_esgotado",
        ],
        "pista": "sem_consultas_lentas",
        "pista_texto": (
            "Consultas lentas não causaram o incidente."
        ),
    },

    "inspecionar_conexoes": {
        "comando": "inspecionar conexoes",
        "titulo": "Conexões inspecionadas",
        "mensagem": (
            "Diversas conexões permanecem abertas mesmo "
            "depois que as requisições terminam."
        ),
        "pontos": 25,
        "usuarios_adicionados": 20,
        "tempo_gasto": 45,
        "requisitos": [
            "pool_esgotado",
            "mudanca_nas_conexoes",
        ],
        "pista": "vazamento_confirmado",
        "pista_texto": (
            "Foi confirmado um vazamento de conexões."
        ),
    },

    "limitar_trafego": {
        "comando": "limitar trafego",
        "titulo": "Tráfego limitado",
        "mensagem": (
            "Novas requisições foram temporariamente limitadas. "
            "A pressão sobre a API diminuiu."
        ),
        "pontos": 10,
        "usuarios_adicionados": -250,
        "tempo_gasto": 30,
        "requisitos": [
            "pico_de_conexoes",
        ],
        "pista": "trafego_limitado",
        "pista_texto": (
            "A entrada de novas requisições foi controlada."
        ),
    },

    "ativar_manutencao": {
        "comando": "ativar manutencao",
        "titulo": "Modo de manutenção ativado",
        "mensagem": (
            "O acesso de novos usuários foi interrompido. "
            "A pressão sobre a API diminuiu."
        ),
        "pontos": 15,
        "usuarios_adicionados": -400,
        "tempo_gasto": 20,
        "requisitos": [
            "pico_de_conexoes",
        ],
        "pista": "modo_manutencao",
        "pista_texto": (
            "O sistema está isolado de novas requisições."
        ),
    },

    "desativar_feature": {
        "comando": "desativar feature",
        "titulo": "Funcionalidade desativada",
        "mensagem": (
            "A funcionalidade publicada no último deploy "
            "foi temporariamente desativada."
        ),
        "pontos": 10,
        "usuarios_adicionados": -120,
        "tempo_gasto": 30,
        "requisitos": [
            "deploy_suspeito",
        ],
        "pista": "feature_desativada",
        "pista_texto": (
            "A funcionalidade suspeita não recebe mais tráfego."
        ),
    },

    "encerrar_conexoes": {
        "comando": "encerrar conexoes",
        "titulo": "Conexões encerradas",
        "mensagem": (
            "As conexões presas foram encerradas. "
            "O banco voltou a responder temporariamente."
        ),
        "pontos": 15,
        "usuarios_adicionados": -300,
        "tempo_gasto": 35,
        "requisitos": [
            "pool_esgotado",
        ],
        "pista": "conexoes_encerradas",
        "pista_texto": (
            "O banco foi aliviado, mas a causa ainda existe."
        ),
    },

    "aumentar_instancias": {
        "comando": "aumentar instancias",
        "titulo": "Novas instâncias iniciadas",
        "mensagem": (
            "As novas instâncias também abriram conexões. "
            "A sobrecarga do banco ficou ainda pior."
        ),
        "pontos": -20,
        "usuarios_adicionados": 250,
        "tempo_gasto": 40,
        "requisitos": [
            "pico_de_conexoes",
        ],
        "pista": None,
        "pista_texto": None,
    },

    "bloquear_endpoint": {
        "comando": "bloquear endpoint",
        "titulo": "Endpoint bloqueado",
        "mensagem": (
            "A rota com maior quantidade de requisições "
            "foi temporariamente bloqueada."
        ),
        "pontos": 10,
        "usuarios_adicionados": -180,
        "tempo_gasto": 30,
        "requisitos": [
            "requisicoes_aguardando",
        ],
        "pista": "endpoint_isolado",
        "pista_texto": (
            "A rota problemática não recebe novas requisições."
        ),
    },

    "pausar_filas": {
        "comando": "pausar filas",
        "titulo": "Filas pausadas",
        "mensagem": (
            "As filas não eram a causa do incidente. "
            "Agora diversas tarefas deixaram de ser processadas."
        ),
        "pontos": -15,
        "usuarios_adicionados": 150,
        "tempo_gasto": 35,
        "requisitos": [],
        "pista": None,
        "pista_texto": None,
    },

    "reiniciar_banco": {
        "comando": "reiniciar banco",
        "titulo": "Falha crítica durante a reinicialização",
        "mensagem": (
            "O banco foi reiniciado enquanto existiam operações "
            "ativas. O sistema perdeu acesso aos dados e o "
            "incidente saiu de controle."
        ),
        "pontos": -50,
        "usuarios_adicionados": 800,
        "tempo_gasto": 90,
        "requisitos": [
            "pool_esgotado",
        ],
        "pista": None,
        "pista_texto": None,
        "finalizado": True,
        "sucesso": False,
    },

    "acionar_dba": {
        "comando": "acionar dba",
        "titulo": "DBA acionado",
        "mensagem": (
            "O especialista em banco entrou no incidente e começou "
            "a avaliar a réplica e as conexões ativas."
        ),
        "pontos": 10,
        "usuarios_adicionados": 40,
        "tempo_gasto": 60,
        "requisitos": [
            "pool_esgotado",
        ],
        "pista": "dba_acionado",
        "pista_texto": (
            "O DBA confirmou que o banco principal está saudável, "
            "mas sobrecarregado pelas conexões da aplicação."
        ),
    },

    "verificar_replica": {
        "comando": "verificar replica",
        "titulo": "Réplica verificada",
        "mensagem": (
            "A réplica está sincronizada e pronta para receber tráfego."
        ),
        "pontos": 15,
        "usuarios_adicionados": 30,
        "tempo_gasto": 45,
        "requisitos": [
            "dba_acionado",
        ],
        "pista": "replica_saudavel",
        "pista_texto": (
            "Existe uma réplica saudável disponível para failover."
        ),
    },

    "failover_banco": {
        "comando": "failover banco",
        "titulo": "Alívio temporário",
        "mensagem": (
            "O tráfego foi enviado para a réplica, mas a aplicação "
            "continuou abrindo conexões sem encerrá-las. O incidente "
            "voltará a acontecer porque a causa não foi corrigida."
        ),
        "pontos": 5,
        "usuarios_adicionados": -350,
        "tempo_gasto": 60,
        "requisitos": [
            "replica_saudavel",
        ],
        "pista": None,
        "pista_texto": None,
        "finalizado": True,
        "sucesso": False,
    },

    "restaurar_backup": {
        "comando": "restaurar backup",
        "titulo": "Restauração desnecessária",
        "mensagem": (
            "O banco não estava corrompido. A restauração substituiu "
            "dados recentes e ampliou o impacto do incidente."
        ),
        "pontos": -40,
        "usuarios_adicionados": 700,
        "tempo_gasto": 120,
        "requisitos": [
            "pool_esgotado",
        ],
        "pista": None,
        "pista_texto": None,
        "finalizado": True,
        "sucesso": False,
    },

    "preparar_hotfix": {
        "comando": "preparar hotfix",
        "titulo": "Hotfix preparado",
        "mensagem": (
            "A função foi alterada para sempre encerrar a conexão "
            "depois de cada requisição."
        ),
        "pontos": 20,
        "usuarios_adicionados": 80,
        "tempo_gasto": 90,
        "requisitos": [
            "vazamento_confirmado",
        ],
        "pista": "hotfix_preparado",
        "pista_texto": (
            "Existe uma correção pronta para ser testada."
        ),
    },

    "testar_hotfix": {
        "comando": "testar hotfix",
        "titulo": "Hotfix validado",
        "mensagem": (
            "Os testes confirmaram que as conexões agora são "
            "encerradas corretamente."
        ),
        "pontos": 20,
        "usuarios_adicionados": 30,
        "tempo_gasto": 60,
        "requisitos": [
            "hotfix_preparado",
        ],
        "pista": "hotfix_validado",
        "pista_texto": (
            "A correção passou nos testes de conexão."
        ),
    },

    "aplicar_hotfix": {
        "comando": "aplicar hotfix",
        "titulo": "Hotfix aplicado",
        "mensagem": (
            "A versão corrigida foi publicada. Novas requisições "
            "não deixam conexões abertas."
        ),
        "pontos": 30,
        "usuarios_adicionados": -400,
        "tempo_gasto": 60,
        "requisitos": [
            "hotfix_validado",
        ],
        "pista": "correcao_aplicada",
        "pista_texto": (
            "A causa do vazamento foi corrigida em produção."
        ),
    },

    "reiniciar_api_controlado": {
        "comando": "reiniciar api controlado",
        "titulo": "API reiniciada com segurança",
        "mensagem": (
            "As instâncias antigas foram substituídas gradualmente "
            "sem interromper todas as requisições."
        ),
        "pontos": 20,
        "usuarios_adicionados": -500,
        "tempo_gasto": 45,
        "requisitos": [
            "correcao_aplicada",
            "conexoes_encerradas",
        ],
        "pista": "api_estavel",
        "pista_texto": (
            "A API voltou a responder sem criar novas conexões presas."
        ),
    },

    "restaurar_feature": {
        "comando": "restaurar feature",
        "titulo": "Funcionalidade restaurada",
        "mensagem": (
            "A funcionalidade foi reativada utilizando a versão corrigida."
        ),
        "pontos": 10,
        "usuarios_adicionados": 20,
        "tempo_gasto": 20,
        "requisitos": [
            "api_estavel",
            "feature_desativada",
        ],
        "pista": "feature_restaurada",
        "pista_texto": (
            "A funcionalidade voltou a operar normalmente."
        ),
    },

    "reabrir_trafego": {
        "comando": "reabrir trafego",
        "titulo": "Tráfego restaurado",
        "mensagem": (
            "O tráfego normal foi restaurado gradualmente. "
            "A API continua estável."
        ),
        "pontos": 10,
        "usuarios_adicionados": 50,
        "tempo_gasto": 30,
        "requisitos": [
            "api_estavel",
        ],
        "pista": "trafego_reaberto",
        "pista_texto": (
            "Os usuários voltaram a acessar o sistema normalmente."
        ),
    },

    "validar_recuperacao": {
        "comando": "validar recuperacao",
        "titulo": "Recuperação validada",
        "mensagem": (
            "O estado final do sistema está sendo avaliado."
        ),
        "pontos": 0,
        "usuarios_adicionados": 0,
        "tempo_gasto": 15,
        "requisitos": [
            "trafego_reaberto",
        ],
        "pista": None,
        "pista_texto": None,
    },
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
    "sucesso": True,
}


RESULTADO_DERROTA = {
    "titulo": "O incidente saiu de controle",
    "mensagem": (
        "O rollback foi realizado sem informações suficientes. "
        "A operação falhou e o banco de dados ficou ainda mais "
        "sobrecarregado."
    ),
    "pontos": -30,
    "usuarios_adicionados": 600,
    "finalizado": True,
    "sucesso": False,
}


def obter_incidente_inicial():
    return INCIDENTE_INICIAL


def executar_acao(acao_id):
    return RESULTADOS_ACOES.get(
        acao_id,
        {
            "titulo": "Ação inválida",
            "mensagem": (
                "O sistema não reconheceu essa decisão."
            ),
            "pontos": 0,
            "usuarios_adicionados": 0,
        },
    )


def obter_comandos_disponiveis(estado):
    if estado["finalizado"]:
        return []

    comandos_disponiveis = []

    pistas_encontradas = set(
        estado["pistas_encontradas"]
    )

    for id_acao, acao in RESULTADOS_ACOES.items():
        if id_acao in estado["acoes_realizadas"]:
            continue

        requisitos = set(
            acao.get("requisitos", [])
        )

        if requisitos.issubset(pistas_encontradas):
            comandos_disponiveis.append(
                acao["comando"]
            )

    return comandos_disponiveis


def criar_resultado_rollback(estado):
    pistas = set(
        estado["pistas_encontradas"]
    )

    if "vazamento_confirmado" not in pistas:
        return RESULTADO_DERROTA.copy()

    houve_contencao = bool(
        {
            "modo_manutencao",
            "trafego_limitado",
            "endpoint_isolado",
        }
        & pistas
    )

    if (
        houve_contencao
        and "conexoes_encerradas" in pistas
    ):
        return {
            "titulo": "Rollback controlado",
            "mensagem": (
                "O tráfego foi contido, as conexões antigas "
                "foram encerradas e a versão estável foi "
                "restaurada. O incidente terminou com "
                "impacto reduzido."
            ),
            "pontos": 40,
            "usuarios_adicionados": -300,
            "finalizado": True,
            "sucesso": True,
        }

    if houve_contencao:
        return {
            "titulo": "Incidente resolvido com contenção",
            "mensagem": (
                "A versão anterior foi restaurada e a "
                "contenção evitou um impacto maior. Algumas "
                "conexões precisaram expirar naturalmente."
            ),
            "pontos": 30,
            "usuarios_adicionados": -150,
            "finalizado": True,
            "sucesso": True,
        }

    return RESULTADO_VITORIA.copy()


def criar_resultado_validacao(estado):
    pontuacao = estado["pontuacao"]
    usuarios = estado["usuarios_afetados"]
    tempo = estado["tempo_restante"]

    if (
        pontuacao >= 250
        and usuarios <= 500
        and tempo >= 45
    ):
        return {
            "titulo": "Recuperação exemplar",
            "mensagem": (
                "O hotfix eliminou o vazamento, a API foi "
                "reiniciada gradualmente e o tráfego voltou "
                "sem novos erros. A equipe encerrou o "
                "incidente com impacto mínimo."
            ),
            "pontos": 50,
            "usuarios_adicionados": 0,
            "finalizado": True,
            "sucesso": True,
        }

    if usuarios <= 1200 and tempo > 0:
        return {
            "titulo": "Sistema estabilizado",
            "mensagem": (
                "A causa foi corrigida e o serviço voltou ao "
                "normal. O incidente teve impacto moderado, "
                "mas não deixou problemas ativos."
            ),
            "pontos": 30,
            "usuarios_adicionados": 0,
            "finalizado": True,
            "sucesso": True,
        }

    return {
        "titulo": "Recuperação tardia",
        "mensagem": (
            "O sistema foi recuperado, mas a demora e as "
            "decisões anteriores ampliaram bastante o "
            "número de usuários afetados."
        ),
        "pontos": 10,
        "usuarios_adicionados": 0,
        "finalizado": True,
        "sucesso": True,
    }


def aplicar_consequencias_da_ordem(
    acao_id,
    estado,
    resultado
):
    resultado_ajustado = resultado.copy()

    acoes_realizadas = estado["acoes_realizadas"]
    conjunto_acoes = set(acoes_realizadas)

    ultima_acao = (
        acoes_realizadas[-1]
        if acoes_realizadas
        else None
    )

    houve_contencao = bool(
        {
            "limitar_trafego",
            "ativar_manutencao",
            "bloquear_endpoint",
        }
        & conjunto_acoes
    )

    if acao_id == "reiniciar_servidor":
        if "verificar_logs" not in conjunto_acoes:
            resultado_ajustado.update({
                "titulo": "Reinicialização às cegas",
                "mensagem": (
                    "O servidor foi reiniciado sem que os "
                    "logs fossem analisados. A API voltou "
                    "recebendo o mesmo volume de requisições "
                    "e caiu novamente."
                ),
                "pontos": -40,
                "usuarios_adicionados": 600,
                "tempo_extra": 30,
            })

        elif not houve_contencao:
            resultado_ajustado.update({
                "titulo": "Reinicialização sem contenção",
                "mensagem": (
                    "O servidor voltou a receber todo o "
                    "tráfego imediatamente. A reinicialização "
                    "não resolveu a origem do incidente."
                ),
                "pontos": -25,
                "usuarios_adicionados": 350,
                "tempo_extra": 15,
            })

        else:
            resultado_ajustado.update({
                "titulo": "Reinicialização controlada",
                "mensagem": (
                    "Como o tráfego estava contido, a "
                    "reinicialização reduziu temporariamente "
                    "os erros. A causa ainda precisa ser "
                    "corrigida."
                ),
                "pontos": 5,
                "usuarios_adicionados": -120,
                "tempo_extra": 0,
            })

    elif (
        acao_id == "encerrar_conexoes"
        and "inspecionar_conexoes" not in conjunto_acoes
    ):
        resultado_ajustado.update({
            "titulo": "Conexões encerradas sem confirmação",
            "mensagem": (
                "As conexões foram encerradas antes de serem "
                "inspecionadas. Algumas requisições ativas "
                "foram interrompidas e usuários perderam "
                "operações em andamento."
            ),
            "pontos": -10,
            "usuarios_adicionados": 180,
            "tempo_extra": 20,
        })

    elif (
        acao_id == "aumentar_instancias"
        and "analisar_banco" not in conjunto_acoes
    ):
        resultado_ajustado.update({
            "titulo": "Escalonamento precipitado",
            "mensagem": (
                "Novas instâncias foram criadas antes que o "
                "banco fosse analisado. Cada instância abriu "
                "mais conexões e acelerou a sobrecarga."
            ),
            "pontos": -35,
            "usuarios_adicionados": 420,
            "tempo_extra": 20,
        })

    elif (
        acao_id == "pausar_filas"
        and "verificar_filas" not in conjunto_acoes
    ):
        resultado_ajustado.update({
            "titulo": "Filas pausadas sem investigação",
            "mensagem": (
                "As filas foram pausadas sem qualquer "
                "evidência de falha. Tarefas importantes "
                "deixaram de ser processadas."
            ),
            "pontos": -30,
            "usuarios_adicionados": 300,
            "tempo_extra": 20,
        })

    elif (
        acao_id == "analisar_deploy"
        and ultima_acao == "verificar_logs"
    ):
        resultado_ajustado["pontos"] += 5

        resultado_ajustado["mensagem"] += (
            " A sequência de investigação foi eficiente."
        )

    elif (
        acao_id == "comparar_versoes"
        and ultima_acao == "analisar_deploy"
    ):
        resultado_ajustado["pontos"] += 5

        resultado_ajustado["mensagem"] += (
            " A comparação foi realizada no momento correto."
        )

    elif (
        acao_id == "inspecionar_conexoes"
        and ultima_acao in {
            "analisar_banco",
            "comparar_versoes",
        }
    ):
        resultado_ajustado["pontos"] += 10

        resultado_ajustado["mensagem"] += (
            " O diagnóstico seguiu uma sequência precisa."
        )

    return resultado_ajustado


def processar_acao(acao_id, estado):
    if estado["finalizado"]:
        return estado["resultado_final"], estado

    if acao_id not in RESULTADOS_ACOES:
        resultado = {
            "titulo": "Comando inválido",
            "mensagem": "Essa ação não existe.",
        }

        return resultado, estado

    if acao_id in estado["acoes_realizadas"]:
        resultado = {
            "titulo": "Ação já realizada",
            "mensagem": (
                "Você precisa escolher outra estratégia."
            ),
        }

        return resultado, estado

    acao = RESULTADOS_ACOES[acao_id]

    pistas_encontradas = set(
        estado["pistas_encontradas"]
    )

    requisitos = set(
        acao.get("requisitos", [])
    )

    if not requisitos.issubset(pistas_encontradas):
        resultado = {
            "titulo": "Comando bloqueado",
            "mensagem": (
                "Você ainda não encontrou as pistas "
                "necessárias para executar essa ação."
            ),
        }

        return resultado, estado

    comandos_anteriores = set(
        obter_comandos_disponiveis(estado)
    )

    if acao_id == "fazer_rollback":
        resultado = criar_resultado_rollback(estado)

    elif acao_id == "validar_recuperacao":
        resultado = criar_resultado_validacao(estado)

    else:
        resultado = acao.copy()

    resultado = aplicar_consequencias_da_ordem(
        acao_id,
        estado,
        resultado
    )

    estado["pontuacao"] = max(
        0,
        estado["pontuacao"]
        + resultado["pontos"]
    )

    estado["usuarios_afetados"] = max(
        0,
        estado["usuarios_afetados"]
        + resultado["usuarios_adicionados"]
    )

    tempo_total = (
        acao.get("tempo_gasto", 0)
        + resultado.get("tempo_extra", 0)
    )

    estado["tempo_restante"] = max(
        0,
        estado["tempo_restante"]
        - tempo_total
    )

    if (
        estado["tempo_restante"] == 0
        and not resultado.get("finalizado", False)
    ):
        resultado["titulo"] = "Tempo esgotado"

        resultado["mensagem"] += (
            " O tempo de resposta terminou antes que "
            "o sistema fosse recuperado."
        )

        resultado["finalizado"] = True
        resultado["sucesso"] = False

    estado["acoes_realizadas"].append(
        acao_id
    )

    pista = acao.get("pista")

    if (
        pista
        and pista not in estado["pistas_encontradas"]
    ):
        estado["pistas_encontradas"].append(
            pista
        )

        resultado["mensagem"] += (
            f" Pista encontrada: {acao['pista_texto']}"
        )

    pistas_atualizadas = set(
        estado["pistas_encontradas"]
    )

    if "vazamento_confirmado" in pistas_atualizadas:
        estado["fase"] = "recuperacao"

    elif {
        "pool_esgotado",
        "pico_de_conexoes",
    } & pistas_atualizadas:
        estado["fase"] = "contencao"

    if resultado.get("finalizado", False):
        estado["finalizado"] = True
        estado["fase"] = "encerrado"

        estado["resultado_final"] = {
            "titulo": resultado["titulo"],
            "mensagem": resultado["mensagem"],
            "sucesso": resultado["sucesso"],
        }

    comandos_atuais = set(
        obter_comandos_disponiveis(estado)
    )

    novos_comandos = (
        comandos_atuais
        - comandos_anteriores
    )

    if novos_comandos:
        resultado["mensagem"] += (
            " Novo comando desbloqueado: "
            + ", ".join(
                sorted(novos_comandos)
            )
            + "."
        )

    return resultado, estado


def criar_estado_inicial():
    return {
        "pontuacao": 100,
        "usuarios_afetados": (
            INCIDENTE_INICIAL["usuarios_afetados"]
        ),
        "tempo_restante": 600,
        "fase": "investigacao",
        "pistas_encontradas": [],
        "acoes_realizadas": [],
        "historico": [],
        "finalizado": False,
        "resultado_final": None,
    }


def interpretar_comando(comando):
    if not comando:
        return None

    comando_normalizado = " ".join(
        comando.lower().strip().split()
    )

    comandos = {
        # Comandos gerais
        "ajuda": "ajuda",
        "help": "ajuda",
        "?": "ajuda",
        "status": "status",

        "reiniciar": "reiniciar_partida",
        "reiniciar partida": "reiniciar_partida",

        # Investigação inicial
        "logs": "verificar_logs",
        "verificar logs": "verificar_logs",

        "metricas": "analisar_metricas",
        "métricas": "analisar_metricas",
        "analisar metricas": "analisar_metricas",
        "analisar métricas": "analisar_metricas",

        "filas": "verificar_filas",
        "verificar filas": "verificar_filas",

        "externos": "verificar_servicos_externos",
        "verificar externos": (
            "verificar_servicos_externos"
        ),
        "verificar servicos externos": (
            "verificar_servicos_externos"
        ),
        "verificar serviços externos": (
            "verificar_servicos_externos"
        ),

        "cache": "verificar_cache",
        "verificar cache": "verificar_cache",

        # Investigação desbloqueada
        "banco": "analisar_banco",
        "analisar banco": "analisar_banco",

        "deploy": "analisar_deploy",
        "analisar deploy": "analisar_deploy",

        "comparar versoes": "comparar_versoes",
        "comparar versões": "comparar_versoes",

        "rastrear requisicao": "rastrear_requisicao",
        "rastrear requisição": "rastrear_requisicao",

        "consultas lentas": (
            "procurar_consultas_lentas"
        ),

        "inspecionar conexoes": "inspecionar_conexoes",
        "inspecionar conexões": "inspecionar_conexoes",

        # Contenção
        "limitar trafego": "limitar_trafego",
        "limitar tráfego": "limitar_trafego",

        "ativar manutencao": "ativar_manutencao",
        "ativar manutenção": "ativar_manutencao",

        "desativar feature": "desativar_feature",

        "encerrar conexoes": "encerrar_conexoes",
        "encerrar conexões": "encerrar_conexoes",

        "aumentar instancias": "aumentar_instancias",
        "aumentar instâncias": "aumentar_instancias",

        "bloquear endpoint": "bloquear_endpoint",
        "pausar filas": "pausar_filas",

        # Banco de dados
        "reiniciar servidor": "reiniciar_servidor",
        "reiniciar banco": "reiniciar_banco",
        "acionar dba": "acionar_dba",

        "verificar replica": "verificar_replica",
        "verificar réplica": "verificar_replica",

        "failover banco": "failover_banco",
        "restaurar backup": "restaurar_backup",

        # Correção
        "preparar hotfix": "preparar_hotfix",
        "testar hotfix": "testar_hotfix",
        "aplicar hotfix": "aplicar_hotfix",

        "reiniciar api controlado": (
            "reiniciar_api_controlado"
        ),

        "restaurar feature": "restaurar_feature",

        "reabrir trafego": "reabrir_trafego",
        "reabrir tráfego": "reabrir_trafego",

        "validar recuperacao": "validar_recuperacao",
        "validar recuperação": "validar_recuperacao",
        "validar sistema": "validar_recuperacao",

        # Finalização alternativa
        "rollback": "fazer_rollback",
        "fazer rollback": "fazer_rollback",
    }

    return comandos.get(
        comando_normalizado
    )