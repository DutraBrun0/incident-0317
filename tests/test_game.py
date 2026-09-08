from game import (
    criar_estado_inicial,
    interpretar_comando,
    obter_comandos_disponiveis,
    obter_incidente_inicial,
    obter_incidentes_disponiveis,
    processar_acao,
    sortear_incidente,
)


def executar_sequencia(estado, acoes):
    ultimo_resultado = None

    for acao_id in acoes:
        ultimo_resultado, estado = processar_acao(
            acao_id,
            estado,
        )

    return ultimo_resultado, estado


def test_lista_os_dois_incidentes():
    incidentes = obter_incidentes_disponiveis()

    ids = {
        incidente["id"]
        for incidente in incidentes
    }

    assert "api_0317" in ids
    assert "ddos_0241" in ids
    assert len(incidentes) == 2


def test_obtem_dados_do_incidente_api():
    incidente = obter_incidente_inicial(
        "api_0317"
    )

    assert incidente["codigo"] == "0317"
    assert incidente["horario"] == "03:17"
    assert incidente["nivel"] == "CRÍTICO"
    assert incidente["titulo"] == (
        "Falha crítica na API"
    )


def test_obtem_dados_do_incidente_ddos():
    incidente = obter_incidente_inicial(
        "ddos_0241"
    )

    assert incidente["codigo"] == "0241"
    assert incidente["horario"] == "02:41"
    assert incidente["nivel"] == "SEVERO"
    assert incidente["titulo"] == (
    "Ataque distribuído à autenticação"
)


def test_cria_estado_inicial_da_api():
    estado = criar_estado_inicial(
        "api_0317"
    )

    assert estado["cenario_id"] == "api_0317"
    assert estado["pontuacao"] == 100
    assert estado["usuarios_afetados"] == 1248
    assert estado["tempo_restante"] == 600
    assert estado["fase"] == "investigacao"
    assert estado["finalizado"] is False


def test_cria_estado_inicial_do_ddos():
    estado = criar_estado_inicial(
        "ddos_0241"
    )

    assert estado["cenario_id"] == "ddos_0241"
    assert estado["pontuacao"] == 100
    assert estado["usuarios_afetados"] == 3180
    assert estado["tempo_restante"] == 480
    assert estado["fase"] == "investigacao"
    assert estado["finalizado"] is False


def test_interpreta_comando_da_api():
    estado = criar_estado_inicial(
        "api_0317"
    )

    assert interpretar_comando(
        "logs",
        estado,
    ) == "verificar_logs"

    assert interpretar_comando(
        "MÉTRICAS",
        estado,
    ) == "analisar_metricas"

    assert interpretar_comando(
        "analisar banco",
        estado,
    ) == "analisar_banco"


def test_interpreta_comando_do_ddos():
    estado = criar_estado_inicial(
        "ddos_0241"
    )

    assert interpretar_comando(
        "analisar tráfego",
        estado,
    ) == "analisar_trafego"

    assert interpretar_comando(
        "WAF",
        estado,
    ) == "verificar_waf"

    assert interpretar_comando(
        "logs de acesso",
        estado,
    ) == "analisar_logs_acesso"


def test_comando_de_outro_cenario_nao_funciona():
    estado_ddos = criar_estado_inicial(
        "ddos_0241"
    )

    assert interpretar_comando(
        "analisar banco",
        estado_ddos,
    ) is None


def test_comandos_gerais_funcionam_em_todos_cenarios():
    estado_api = criar_estado_inicial(
        "api_0317"
    )

    estado_ddos = criar_estado_inicial(
        "ddos_0241"
    )

    for estado in (estado_api, estado_ddos):
        assert interpretar_comando(
            "ajuda",
            estado,
        ) == "ajuda"

        assert interpretar_comando(
            "status",
            estado,
        ) == "status"

        assert interpretar_comando(
            "reiniciar",
            estado,
        ) == "reiniciar_partida"


def test_acao_bloqueada_nao_altera_estado():
    estado = criar_estado_inicial(
        "api_0317"
    )

    pontuacao_inicial = estado["pontuacao"]
    usuarios_iniciais = estado["usuarios_afetados"]
    tempo_inicial = estado["tempo_restante"]

    resultado, estado = processar_acao(
        "analisar_banco",
        estado,
    )

    assert resultado["titulo"] == "Comando bloqueado"
    assert estado["pontuacao"] == pontuacao_inicial
    assert estado["usuarios_afetados"] == usuarios_iniciais
    assert estado["tempo_restante"] == tempo_inicial
    assert estado["acoes_realizadas"] == []


def test_pista_desbloqueia_novos_comandos():
    estado = criar_estado_inicial(
        "api_0317"
    )

    comandos_iniciais = obter_comandos_disponiveis(
        estado
    )

    assert "analisar banco" not in comandos_iniciais
    assert "analisar deploy" not in comandos_iniciais

    _, estado = processar_acao(
        "verificar_logs",
        estado,
    )

    comandos_atualizados = obter_comandos_disponiveis(
        estado
    )

    assert "analisar banco" in comandos_atualizados
    assert "analisar deploy" in comandos_atualizados


def test_acao_repetida_nao_altera_estado():
    estado = criar_estado_inicial(
        "api_0317"
    )

    _, estado = processar_acao(
        "verificar_logs",
        estado,
    )

    pontuacao = estado["pontuacao"]
    usuarios = estado["usuarios_afetados"]
    tempo = estado["tempo_restante"]

    resultado, estado = processar_acao(
        "verificar_logs",
        estado,
    )

    assert resultado["titulo"] == "Ação já realizada"
    assert estado["pontuacao"] == pontuacao
    assert estado["usuarios_afetados"] == usuarios
    assert estado["tempo_restante"] == tempo
    assert estado["acoes_realizadas"].count(
        "verificar_logs"
    ) == 1


def test_rollback_precoce_causa_derrota():
    estado = criar_estado_inicial(
        "api_0317"
    )

    resultado, estado = processar_acao(
        "fazer_rollback",
        estado,
    )

    assert resultado["finalizado"] is True
    assert resultado["sucesso"] is False
    assert estado["finalizado"] is True
    assert estado["fase"] == "encerrado"
    assert estado["resultado_final"]["sucesso"] is False


def test_reiniciar_servidor_sem_logs_aplica_penalidade():
    estado = criar_estado_inicial(
        "api_0317"
    )

    resultado, estado = processar_acao(
        "reiniciar_servidor",
        estado,
    )

    assert resultado["titulo"] == (
        "Reinicialização às cegas"
    )

    assert resultado["pontos"] == -40
    assert resultado["usuarios_adicionados"] == 600
    assert estado["pontuacao"] == 60
    assert estado["usuarios_afetados"] == 1848
    assert estado["tempo_restante"] == 510


def test_ordem_correta_encontra_vazamento():
    estado = criar_estado_inicial(
        "api_0317"
    )

    sequencia = [
        "verificar_logs",
        "analisar_deploy",
        "comparar_versoes",
        "analisar_banco",
        "inspecionar_conexoes",
    ]

    _, estado = executar_sequencia(
        estado,
        sequencia,
    )

    assert "vazamento_confirmado" in (
        estado["pistas_encontradas"]
    )

    assert estado["fase"] == "recuperacao"
    assert estado["pontuacao"] == 215
    assert estado["finalizado"] is False


def test_rollback_depois_da_investigacao_vence():
    estado = criar_estado_inicial(
        "api_0317"
    )

    sequencia = [
        "verificar_logs",
        "analisar_deploy",
        "comparar_versoes",
        "analisar_banco",
        "inspecionar_conexoes",
        "fazer_rollback",
    ]

    resultado, estado = executar_sequencia(
        estado,
        sequencia,
    )

    assert resultado["finalizado"] is True
    assert resultado["sucesso"] is True
    assert estado["finalizado"] is True
    assert estado["fase"] == "encerrado"
    assert estado["resultado_final"]["sucesso"] is True


def test_bloquear_tudo_no_ddos_causa_derrota():
    estado = criar_estado_inicial(
        "ddos_0241"
    )

    resultado, estado = processar_acao(
        "bloquear_todo_trafego",
        estado,
    )

    assert resultado["finalizado"] is True
    assert resultado["sucesso"] is False
    assert estado["finalizado"] is True
    assert estado["resultado_final"]["sucesso"] is False


def test_caminho_correto_resolve_ddos():
    estado = criar_estado_inicial(
        "ddos_0241"
    )

    sequencia = [
        "analisar_trafego",
        "analisar_logs_acesso",
        "analisar_user_agents",
        "identificar_endpoint",
        "ativar_rate_limit",
        "verificar_waf",
        "criar_regra_waf",
        "aplicar_regra_waf",
        "validar_taxa_erros",
        "validar_login",
        "normalizar_limites",
        "encerrar_incidente_ddos",
    ]

    resultado, estado = executar_sequencia(
        estado,
        sequencia,
    )

    assert resultado["finalizado"] is True
    assert resultado["sucesso"] is True
    assert estado["finalizado"] is True
    assert estado["fase"] == "encerrado"
    assert estado["resultado_final"]["sucesso"] is True
    assert estado["pontuacao"] >= 250
    assert estado["tempo_restante"] > 0


def test_tempo_esgotado_encerra_partida():
    estado = criar_estado_inicial(
        "api_0317"
    )

    estado["tempo_restante"] = 10

    resultado, estado = processar_acao(
        "verificar_logs",
        estado,
    )

    assert resultado["titulo"] == "Tempo esgotado"
    assert resultado["finalizado"] is True
    assert resultado["sucesso"] is False
    assert estado["tempo_restante"] == 0
    assert estado["finalizado"] is True
    assert estado["fase"] == "encerrado"


def test_partida_encerrada_nao_aceita_nova_acao():
    estado = criar_estado_inicial(
        "api_0317"
    )

    _, estado = processar_acao(
        "fazer_rollback",
        estado,
    )

    quantidade_acoes = len(
        estado["acoes_realizadas"]
    )

    resultado, estado = processar_acao(
        "verificar_logs",
        estado,
    )

    assert resultado == estado["resultado_final"]

    assert len(
        estado["acoes_realizadas"]
    ) == quantidade_acoes


def test_sorteio_nao_repete_incidente_anterior():
    assert sortear_incidente(
        "api_0317"
    ) == "ddos_0241"

    assert sortear_incidente(
        "ddos_0241"
    ) == "api_0317"
