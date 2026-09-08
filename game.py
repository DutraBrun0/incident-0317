import random
import unicodedata

from incidentes import (
    CENARIOS,
    CENARIO_PADRAO,
    obter_cenario,
    listar_cenarios,
)


def normalizar_texto(texto):
    texto_sem_acentos = "".join(
        caractere
        for caractere in unicodedata.normalize(
            "NFD",
            texto
        )
        if unicodedata.category(caractere) != "Mn"
    )

    return " ".join(
        texto_sem_acentos.lower().strip().split()
    )


def obter_id_cenario(estado=None, cenario_id=None):
    if cenario_id in CENARIOS:
        return cenario_id

    if estado:
        id_estado = estado.get("cenario_id")

        if id_estado in CENARIOS:
            return id_estado

    return CENARIO_PADRAO


def obter_cenario_do_estado(estado):
    cenario_id = obter_id_cenario(estado=estado)

    return obter_cenario(cenario_id)


def obter_incidente_inicial(cenario_id=None):
    cenario_id = obter_id_cenario(
        cenario_id=cenario_id
    )

    cenario = obter_cenario(cenario_id)

    acoes_resumidas = []

    for acao_id, acao in cenario["acoes"].items():
        acoes_resumidas.append({
            "id": acao_id,
            "titulo": acao["titulo"],
            "descricao": acao["mensagem"],
        })

    return {
        "id": cenario["id"],
        "codigo": cenario["codigo"],
        "horario": cenario["horario"],
        "titulo": cenario["titulo"],
        "descricao": cenario["descricao"],
        "nivel": cenario["nivel"],
        "usuarios_afetados": (
            cenario["usuarios_afetados"]
        ),
        "logs": list(cenario["logs"]),
        "acoes": acoes_resumidas,
    }


def obter_incidentes_disponiveis():
    incidentes = []

    for cenario in listar_cenarios():
        incidentes.append({
            "id": cenario["id"],
            "codigo": cenario["codigo"],
            "horario": cenario["horario"],
            "titulo": cenario["titulo"],
            "descricao": cenario["descricao"],
            "nivel": cenario["nivel"],
        })

    return incidentes


def sortear_incidente(cenario_anterior=None):
    ids_cenarios = list(CENARIOS.keys())

    if (
        cenario_anterior in ids_cenarios
        and len(ids_cenarios) > 1
    ):
        ids_cenarios.remove(cenario_anterior)

    return random.choice(ids_cenarios)


def obter_acoes_do_estado(estado):
    cenario = obter_cenario_do_estado(estado)

    return cenario["acoes"]


def executar_acao(acao_id, estado=None):
    if estado is None:
        cenario = obter_cenario(CENARIO_PADRAO)
    else:
        cenario = obter_cenario_do_estado(estado)

    return cenario["acoes"].get(
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
    acoes = obter_acoes_do_estado(estado)

    pistas_encontradas = set(
        estado["pistas_encontradas"]
    )

    for acao_id, acao in acoes.items():
        if acao_id in estado["acoes_realizadas"]:
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
    cenario = obter_cenario_do_estado(estado)

    pistas = set(
        estado["pistas_encontradas"]
    )

    if "vazamento_confirmado" not in pistas:
        return cenario["resultado_derrota"].copy()

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
            "titulo": (
                "Incidente resolvido com contenção"
            ),
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

    return cenario["resultado_vitoria"].copy()


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


def aplicar_consequencias_api(
    acao_id,
    estado,
    resultado,
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
                "titulo": (
                    "Reinicialização sem contenção"
                ),
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
                "titulo": (
                    "Reinicialização controlada"
                ),
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
        and "inspecionar_conexoes"
        not in conjunto_acoes
    ):
        resultado_ajustado.update({
            "titulo": (
                "Conexões encerradas sem confirmação"
            ),
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
        and "analisar_banco"
        not in conjunto_acoes
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
        and "verificar_filas"
        not in conjunto_acoes
    ):
        resultado_ajustado.update({
            "titulo": (
                "Filas pausadas sem investigação"
            ),
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


def aplicar_consequencias_ddos(
    acao_id,
    estado,
    resultado,
):
    resultado_ajustado = resultado.copy()

    acoes_realizadas = estado["acoes_realizadas"]
    conjunto_acoes = set(acoes_realizadas)

    ultima_acao = (
        acoes_realizadas[-1]
        if acoes_realizadas
        else None
    )

    houve_mitigacao = bool(
        {
            "ativar_rate_limit",
            "aplicar_regra_waf",
            "ativar_scrubbing",
        }
        & conjunto_acoes
    )

    if acao_id == "reiniciar_gateway":
        if "analisar_trafego" not in conjunto_acoes:
            resultado_ajustado.update({
                "titulo": (
                    "Gateway reiniciado às cegas"
                ),
                "mensagem": (
                    "O gateway foi reiniciado antes que o "
                    "tráfego fosse analisado. O ataque "
                    "continuou e a nova instância ficou "
                    "sobrecarregada imediatamente."
                ),
                "pontos": -40,
                "usuarios_adicionados": 700,
                "tempo_extra": 30,
            })

        elif not houve_mitigacao:
            resultado_ajustado.update({
                "titulo": (
                    "Reinicialização sem mitigação"
                ),
                "mensagem": (
                    "O gateway voltou a operar sem qualquer "
                    "filtro de tráfego. Os bots retomaram "
                    "a sobrecarga em poucos segundos."
                ),
                "pontos": -25,
                "usuarios_adicionados": 450,
                "tempo_extra": 15,
            })

        else:
            resultado_ajustado.update({
                "titulo": (
                    "Gateway reiniciado com proteção"
                ),
                "mensagem": (
                    "As proteções reduziram o tráfego durante "
                    "a reinicialização. O gateway voltou sem "
                    "receber toda a carga maliciosa."
                ),
                "pontos": 10,
                "usuarios_adicionados": -150,
                "tempo_extra": 0,
            })

    elif (
        acao_id == "bloquear_paises"
        and "assinatura_bot"
        not in estado["pistas_encontradas"]
    ):
        resultado_ajustado.update({
            "titulo": "Bloqueio geográfico impreciso",
            "mensagem": (
                "Regiões foram bloqueadas sem que a assinatura "
                "dos bots fosse analisada. Muitos usuários "
                "legítimos perderam acesso ao serviço."
            ),
            "pontos": -35,
            "usuarios_adicionados": 550,
            "tempo_extra": 15,
        })

    elif acao_id == "aumentar_instancias_ddos":
        if not houve_mitigacao:
            resultado_ajustado.update({
                "titulo": (
                    "Escalonamento sem proteção"
                ),
                "mensagem": (
                    "As novas instâncias receberam o mesmo "
                    "tráfego malicioso. A capacidade extra "
                    "apenas atrasou a sobrecarga."
                ),
                "pontos": -10,
                "usuarios_adicionados": 250,
                "tempo_extra": 10,
            })

    elif (
        acao_id == "analisar_logs_acesso"
        and ultima_acao == "analisar_trafego"
    ):
        resultado_ajustado["pontos"] += 5

        resultado_ajustado["mensagem"] += (
            " A investigação seguiu uma sequência eficiente."
        )

    elif (
        acao_id == "analisar_user_agents"
        and ultima_acao == "analisar_logs_acesso"
    ):
        resultado_ajustado["pontos"] += 5

        resultado_ajustado["mensagem"] += (
            " A assinatura foi localizada rapidamente."
        )

    elif (
        acao_id == "identificar_endpoint"
        and ultima_acao in {
            "analisar_logs_acesso",
            "analisar_user_agents",
        }
    ):
        resultado_ajustado["pontos"] += 10

        resultado_ajustado["mensagem"] += (
            " O alvo foi identificado no momento correto."
        )

    elif (
        acao_id == "ativar_rate_limit"
        and ultima_acao == "identificar_endpoint"
    ):
        resultado_ajustado["pontos"] += 5

        resultado_ajustado["mensagem"] += (
            " A contenção foi aplicada diretamente no alvo."
        )

    elif (
        acao_id == "aplicar_regra_waf"
        and ultima_acao == "criar_regra_waf"
    ):
        resultado_ajustado["pontos"] += 5

        resultado_ajustado["mensagem"] += (
            " A regra foi aplicada sem demora."
        )

    elif (
        acao_id == "acionar_provedor"
        and ultima_acao == "listar_origens"
    ):
        resultado_ajustado["pontos"] += 5

        resultado_ajustado["mensagem"] += (
            " O provedor recebeu as evidências necessárias."
        )

    elif (
        acao_id == "validar_taxa_erros"
        and ultima_acao in {
            "aplicar_regra_waf",
            "ativar_rate_limit",
        }
    ):
        resultado_ajustado["pontos"] += 10

        resultado_ajustado["mensagem"] += (
            " A validação foi realizada logo após a mitigação."
        )

    return resultado_ajustado


def aplicar_consequencias_da_ordem(
    acao_id,
    estado,
    resultado,
):
    cenario_id = obter_id_cenario(
        estado=estado
    )

    if cenario_id == "api_0317":
        return aplicar_consequencias_api(
            acao_id,
            estado,
            resultado,
        )

    if cenario_id == "ddos_0241":
        return aplicar_consequencias_ddos(
            acao_id,
            estado,
            resultado,
        )

    return resultado.copy()


def atualizar_fase(estado):
    if estado["finalizado"]:
        estado["fase"] = "encerrado"
        return

    cenario = obter_cenario_do_estado(estado)

    pistas_encontradas = set(
        estado["pistas_encontradas"]
    )

    estado["fase"] = "investigacao"

    for regra in cenario.get("regras_fase", []):
        pistas_da_regra = set(
            regra.get("pistas", [])
        )

        if pistas_da_regra & pistas_encontradas:
            estado["fase"] = regra["fase"]
            return


def processar_acao(acao_id, estado):
    if estado["finalizado"]:
        return estado["resultado_final"], estado

    acoes = obter_acoes_do_estado(estado)

    if acao_id not in acoes:
        resultado = {
            "titulo": "Comando inválido",
            "mensagem": (
                "Essa ação não existe neste incidente."
            ),
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

    acao = acoes[acao_id]

    pistas_encontradas = set(
        estado["pistas_encontradas"]
    )

    requisitos = set(
        acao.get("requisitos", [])
    )

    if not requisitos.issubset(pistas_encontradas):
        pistas_faltando = sorted(
            requisitos - pistas_encontradas
        )

        resultado = {
            "titulo": "Comando bloqueado",
            "mensagem": (
                "Você ainda não encontrou as pistas "
                "necessárias para executar essa ação. "
                "Pistas pendentes: "
                + ", ".join(pistas_faltando)
                + "."
            ),
        }

        return resultado, estado

    comandos_anteriores = set(
        obter_comandos_disponiveis(estado)
    )

    cenario_id = obter_id_cenario(
        estado=estado
    )

    if (
        cenario_id == "api_0317"
        and acao_id == "fazer_rollback"
    ):
        resultado = criar_resultado_rollback(
            estado
        )

    elif (
        cenario_id == "api_0317"
        and acao_id == "validar_recuperacao"
    ):
        resultado = criar_resultado_validacao(
            estado
        )

    else:
        resultado = acao.copy()

    resultado = aplicar_consequencias_da_ordem(
        acao_id,
        estado,
        resultado,
    )

    estado["pontuacao"] = max(
        0,
        estado["pontuacao"]
        + resultado.get("pontos", 0),
    )

    estado["usuarios_afetados"] = max(
        0,
        estado["usuarios_afetados"]
        + resultado.get(
            "usuarios_adicionados",
            0,
        ),
    )

    tempo_total = (
        acao.get("tempo_gasto", 0)
        + resultado.get("tempo_extra", 0)
    )

    estado["tempo_restante"] = max(
        0,
        estado["tempo_restante"]
        - tempo_total,
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
    pista_texto = acao.get("pista_texto")

    if (
        pista
        and pista not in estado["pistas_encontradas"]
    ):
        estado["pistas_encontradas"].append(
            pista
        )

        if pista_texto:
            resultado["mensagem"] += (
                f" Pista encontrada: {pista_texto}"
            )

    if resultado.get("finalizado", False):
        estado["finalizado"] = True

        estado["resultado_final"] = {
            "titulo": resultado["titulo"],
            "mensagem": resultado["mensagem"],
            "sucesso": resultado.get(
                "sucesso",
                False,
            ),
        }

    atualizar_fase(estado)

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


def criar_estado_inicial(cenario_id=None):
    cenario_id = obter_id_cenario(
        cenario_id=cenario_id
    )

    cenario = obter_cenario(cenario_id)

    return {
        "cenario_id": cenario_id,
        "pontuacao": cenario["pontuacao_inicial"],
        "usuarios_afetados": (
            cenario["usuarios_afetados"]
        ),
        "tempo_restante": cenario["tempo_inicial"],
        "fase": "investigacao",
        "pistas_encontradas": [],
        "acoes_realizadas": [],
        "historico": [],
        "finalizado": False,
        "resultado_final": None,
        "relatorio_final": None,
    }


def interpretar_comando(comando, estado=None):
    if not comando:
        return None

    comando_normalizado = normalizar_texto(
        comando
    )

    comandos_gerais = {
        "ajuda": "ajuda",
        "help": "ajuda",
        "?": "ajuda",
        "status": "status",
        "reiniciar": "reiniciar_partida",
        "reiniciar partida": "reiniciar_partida",
    }

    if comando_normalizado in comandos_gerais:
        return comandos_gerais[
            comando_normalizado
        ]

    if estado is None:
        cenario = obter_cenario(
            CENARIO_PADRAO
        )
    else:
        cenario = obter_cenario_do_estado(
            estado
        )

    for acao_id, acao in cenario["acoes"].items():
        nomes_comando = [
            acao["comando"],
            *acao.get("apelidos", []),
        ]

        for nome in nomes_comando:
            if (
                normalizar_texto(nome)
                == comando_normalizado
            ):
                return acao_id

    return None