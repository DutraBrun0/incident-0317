def criar_acao(
    comando,
    titulo,
    mensagem,
    pontos,
    usuarios_adicionados,
    tempo_gasto,
    requisitos=(),
    pista=None,
    pista_texto=None,
    apelidos=(),
    finalizado=False,
    sucesso=None,
):
    acao = {
        "comando": comando,
        "apelidos": list(apelidos),
        "titulo": titulo,
        "mensagem": mensagem,
        "pontos": pontos,
        "usuarios_adicionados": usuarios_adicionados,
        "tempo_gasto": tempo_gasto,
        "requisitos": list(requisitos),
        "pista": pista,
        "pista_texto": pista_texto,
    }

    if finalizado:
        acao["finalizado"] = True
        acao["sucesso"] = sucesso

    return acao


ACOES_API_0317 = {
    "verificar_logs": criar_acao(
        comando="logs",
        apelidos=("verificar logs",),
        titulo="Logs analisados",
        mensagem=(
            "Os erros começaram logo após a última atualização. "
            "O número de conexões aumentou rapidamente."
        ),
        pontos=15,
        usuarios_adicionados=40,
        tempo_gasto=30,
        pista="erro_apos_deploy",
        pista_texto=(
            "Os erros começaram depois do último deploy."
        ),
    ),

    "reiniciar_servidor": criar_acao(
        comando="reiniciar servidor",
        apelidos=("reiniciar api",),
        titulo="Reinicialização malsucedida",
        mensagem=(
            "O servidor voltou por alguns segundos, "
            "mas caiu novamente."
        ),
        pontos=-25,
        usuarios_adicionados=420,
        tempo_gasto=60,
    ),

    "analisar_banco": criar_acao(
        comando="analisar banco",
        apelidos=("banco",),
        titulo="Banco analisado",
        mensagem=(
            "O pool de conexões está completamente esgotado."
        ),
        pontos=20,
        usuarios_adicionados=30,
        tempo_gasto=45,
        requisitos=("erro_apos_deploy",),
        pista="pool_esgotado",
        pista_texto=(
            "A aplicação não está encerrando as conexões."
        ),
    ),

    "fazer_rollback": criar_acao(
        comando="rollback",
        apelidos=("fazer rollback",),
        titulo="Rollback iniciado",
        mensagem=(
            "A versão anterior está sendo restaurada."
        ),
        pontos=30,
        usuarios_adicionados=0,
        tempo_gasto=60,
    ),

    "analisar_metricas": criar_acao(
        comando="metricas",
        apelidos=(
            "métricas",
            "analisar metricas",
            "analisar métricas",
        ),
        titulo="Métricas analisadas",
        mensagem=(
            "A quantidade de conexões cresceu junto com "
            "a taxa de erros da API."
        ),
        pontos=10,
        usuarios_adicionados=50,
        tempo_gasto=30,
        pista="pico_de_conexoes",
        pista_texto=(
            "Existe um pico anormal de conexões."
        ),
    ),

    "verificar_filas": criar_acao(
        comando="verificar filas",
        apelidos=("filas",),
        titulo="Filas verificadas",
        mensagem=(
            "As filas estão processando normalmente. "
            "Elas provavelmente não causaram o incidente."
        ),
        pontos=5,
        usuarios_adicionados=40,
        tempo_gasto=25,
        pista="filas_normais",
        pista_texto=(
            "O sistema de filas está funcionando normalmente."
        ),
    ),

    "verificar_servicos_externos": criar_acao(
        comando="verificar externos",
        apelidos=(
            "externos",
            "verificar servicos externos",
            "verificar serviços externos",
        ),
        titulo="Serviços externos verificados",
        mensagem=(
            "Os serviços externos estão operacionais. "
            "A falha parece estar dentro da própria aplicação."
        ),
        pontos=5,
        usuarios_adicionados=45,
        tempo_gasto=30,
        pista="externos_operacionais",
        pista_texto=(
            "Nenhum serviço externo apresentou falhas."
        ),
    ),

    "verificar_cache": criar_acao(
        comando="verificar cache",
        apelidos=("cache",),
        titulo="Cache verificado",
        mensagem=(
            "O cache está respondendo normalmente e não "
            "apresenta aumento significativo de memória."
        ),
        pontos=5,
        usuarios_adicionados=35,
        tempo_gasto=25,
        pista="cache_operacional",
        pista_texto=(
            "O cache não é a origem do incidente."
        ),
    ),

    "analisar_deploy": criar_acao(
        comando="analisar deploy",
        apelidos=("deploy",),
        titulo="Deploy analisado",
        mensagem=(
            "Uma nova versão foi publicada sete minutos "
            "antes do início dos erros."
        ),
        pontos=15,
        usuarios_adicionados=30,
        tempo_gasto=40,
        requisitos=("erro_apos_deploy",),
        pista="deploy_suspeito",
        pista_texto=(
            "O último deploy provavelmente iniciou o incidente."
        ),
    ),

    "comparar_versoes": criar_acao(
        comando="comparar versoes",
        apelidos=("comparar versões",),
        titulo="Versões comparadas",
        mensagem=(
            "A nova versão alterou a função responsável "
            "por abrir conexões com o banco."
        ),
        pontos=20,
        usuarios_adicionados=25,
        tempo_gasto=45,
        requisitos=("deploy_suspeito",),
        pista="mudanca_nas_conexoes",
        pista_texto=(
            "A nova versão modificou o controle das conexões."
        ),
    ),

    "rastrear_requisicao": criar_acao(
        comando="rastrear requisicao",
        apelidos=("rastrear requisição",),
        titulo="Requisição rastreada",
        mensagem=(
            "As requisições ficam travadas esperando uma "
            "conexão disponível com o banco."
        ),
        pontos=10,
        usuarios_adicionados=30,
        tempo_gasto=40,
        requisitos=("pico_de_conexoes",),
        pista="requisicoes_aguardando",
        pista_texto=(
            "As requisições estão paradas aguardando o banco."
        ),
    ),

    "procurar_consultas_lentas": criar_acao(
        comando="consultas lentas",
        apelidos=("procurar consultas lentas",),
        titulo="Consultas analisadas",
        mensagem=(
            "Nenhuma consulta lenta foi encontrada. "
            "O problema está na quantidade de conexões abertas."
        ),
        pontos=10,
        usuarios_adicionados=35,
        tempo_gasto=35,
        requisitos=("pool_esgotado",),
        pista="sem_consultas_lentas",
        pista_texto=(
            "Consultas lentas não causaram o incidente."
        ),
    ),

    "inspecionar_conexoes": criar_acao(
        comando="inspecionar conexoes",
        apelidos=("inspecionar conexões",),
        titulo="Conexões inspecionadas",
        mensagem=(
            "Diversas conexões permanecem abertas mesmo "
            "depois que as requisições terminam."
        ),
        pontos=25,
        usuarios_adicionados=20,
        tempo_gasto=45,
        requisitos=(
            "pool_esgotado",
            "mudanca_nas_conexoes",
        ),
        pista="vazamento_confirmado",
        pista_texto=(
            "Foi confirmado um vazamento de conexões."
        ),
    ),

    "limitar_trafego": criar_acao(
        comando="limitar trafego",
        apelidos=("limitar tráfego",),
        titulo="Tráfego limitado",
        mensagem=(
            "Novas requisições foram temporariamente limitadas. "
            "A pressão sobre a API diminuiu."
        ),
        pontos=10,
        usuarios_adicionados=-250,
        tempo_gasto=30,
        requisitos=("pico_de_conexoes",),
        pista="trafego_limitado",
        pista_texto=(
            "A entrada de novas requisições foi controlada."
        ),
    ),

    "ativar_manutencao": criar_acao(
        comando="ativar manutencao",
        apelidos=(
            "ativar manutenção",
            "modo manutencao",
            "modo manutenção",
        ),
        titulo="Modo de manutenção ativado",
        mensagem=(
            "O acesso de novos usuários foi interrompido. "
            "A pressão sobre a API diminuiu."
        ),
        pontos=15,
        usuarios_adicionados=-400,
        tempo_gasto=20,
        requisitos=("pico_de_conexoes",),
        pista="modo_manutencao",
        pista_texto=(
            "O sistema está isolado de novas requisições."
        ),
    ),

    "desativar_feature": criar_acao(
        comando="desativar feature",
        apelidos=("desativar funcionalidade",),
        titulo="Funcionalidade desativada",
        mensagem=(
            "A funcionalidade publicada no último deploy "
            "foi temporariamente desativada."
        ),
        pontos=10,
        usuarios_adicionados=-120,
        tempo_gasto=30,
        requisitos=("deploy_suspeito",),
        pista="feature_desativada",
        pista_texto=(
            "A funcionalidade suspeita não recebe mais tráfego."
        ),
    ),

    "encerrar_conexoes": criar_acao(
        comando="encerrar conexoes",
        apelidos=("encerrar conexões",),
        titulo="Conexões encerradas",
        mensagem=(
            "As conexões presas foram encerradas. "
            "O banco voltou a responder temporariamente."
        ),
        pontos=15,
        usuarios_adicionados=-300,
        tempo_gasto=35,
        requisitos=("pool_esgotado",),
        pista="conexoes_encerradas",
        pista_texto=(
            "O banco foi aliviado, mas a causa ainda existe."
        ),
    ),

    "aumentar_instancias": criar_acao(
        comando="aumentar instancias",
        apelidos=("aumentar instâncias",),
        titulo="Novas instâncias iniciadas",
        mensagem=(
            "As novas instâncias também abriram conexões. "
            "A sobrecarga do banco ficou ainda pior."
        ),
        pontos=-20,
        usuarios_adicionados=250,
        tempo_gasto=40,
        requisitos=("pico_de_conexoes",),
    ),

    "bloquear_endpoint": criar_acao(
        comando="bloquear endpoint",
        titulo="Endpoint bloqueado",
        mensagem=(
            "A rota com maior quantidade de requisições "
            "foi temporariamente bloqueada."
        ),
        pontos=10,
        usuarios_adicionados=-180,
        tempo_gasto=30,
        requisitos=("requisicoes_aguardando",),
        pista="endpoint_isolado",
        pista_texto=(
            "A rota problemática não recebe novas requisições."
        ),
    ),

    "pausar_filas": criar_acao(
        comando="pausar filas",
        titulo="Filas pausadas",
        mensagem=(
            "As filas não eram a causa do incidente. "
            "Agora diversas tarefas deixaram de ser processadas."
        ),
        pontos=-15,
        usuarios_adicionados=150,
        tempo_gasto=35,
    ),

    "reiniciar_banco": criar_acao(
        comando="reiniciar banco",
        titulo="Falha crítica durante a reinicialização",
        mensagem=(
            "O banco foi reiniciado enquanto existiam operações "
            "ativas. O sistema perdeu acesso aos dados e o "
            "incidente saiu de controle."
        ),
        pontos=-50,
        usuarios_adicionados=800,
        tempo_gasto=90,
        requisitos=("pool_esgotado",),
        finalizado=True,
        sucesso=False,
    ),

    "acionar_dba": criar_acao(
        comando="acionar dba",
        apelidos=("chamar dba",),
        titulo="DBA acionado",
        mensagem=(
            "O especialista em banco entrou no incidente e começou "
            "a avaliar a réplica e as conexões ativas."
        ),
        pontos=10,
        usuarios_adicionados=40,
        tempo_gasto=60,
        requisitos=("pool_esgotado",),
        pista="dba_acionado",
        pista_texto=(
            "O DBA confirmou que o banco principal está saudável, "
            "mas sobrecarregado pelas conexões da aplicação."
        ),
    ),

    "verificar_replica": criar_acao(
        comando="verificar replica",
        apelidos=("verificar réplica",),
        titulo="Réplica verificada",
        mensagem=(
            "A réplica está sincronizada e pronta para receber tráfego."
        ),
        pontos=15,
        usuarios_adicionados=30,
        tempo_gasto=45,
        requisitos=("dba_acionado",),
        pista="replica_saudavel",
        pista_texto=(
            "Existe uma réplica saudável disponível para failover."
        ),
    ),

    "failover_banco": criar_acao(
        comando="failover banco",
        apelidos=("failover",),
        titulo="Alívio temporário",
        mensagem=(
            "O tráfego foi enviado para a réplica, mas a aplicação "
            "continuou abrindo conexões sem encerrá-las. O incidente "
            "voltará a acontecer porque a causa não foi corrigida."
        ),
        pontos=5,
        usuarios_adicionados=-350,
        tempo_gasto=60,
        requisitos=("replica_saudavel",),
        finalizado=True,
        sucesso=False,
    ),

    "restaurar_backup": criar_acao(
        comando="restaurar backup",
        apelidos=("backup",),
        titulo="Restauração desnecessária",
        mensagem=(
            "O banco não estava corrompido. A restauração substituiu "
            "dados recentes e ampliou o impacto do incidente."
        ),
        pontos=-40,
        usuarios_adicionados=700,
        tempo_gasto=120,
        requisitos=("pool_esgotado",),
        finalizado=True,
        sucesso=False,
    ),

    "preparar_hotfix": criar_acao(
        comando="preparar hotfix",
        titulo="Hotfix preparado",
        mensagem=(
            "A função foi alterada para sempre encerrar a conexão "
            "depois de cada requisição."
        ),
        pontos=20,
        usuarios_adicionados=80,
        tempo_gasto=90,
        requisitos=("vazamento_confirmado",),
        pista="hotfix_preparado",
        pista_texto=(
            "Existe uma correção pronta para ser testada."
        ),
    ),

    "testar_hotfix": criar_acao(
        comando="testar hotfix",
        titulo="Hotfix validado",
        mensagem=(
            "Os testes confirmaram que as conexões agora são "
            "encerradas corretamente."
        ),
        pontos=20,
        usuarios_adicionados=30,
        tempo_gasto=60,
        requisitos=("hotfix_preparado",),
        pista="hotfix_validado",
        pista_texto=(
            "A correção passou nos testes de conexão."
        ),
    ),

    "aplicar_hotfix": criar_acao(
        comando="aplicar hotfix",
        titulo="Hotfix aplicado",
        mensagem=(
            "A versão corrigida foi publicada. Novas requisições "
            "não deixam conexões abertas."
        ),
        pontos=30,
        usuarios_adicionados=-400,
        tempo_gasto=60,
        requisitos=("hotfix_validado",),
        pista="correcao_aplicada",
        pista_texto=(
            "A causa do vazamento foi corrigida em produção."
        ),
    ),

    "reiniciar_api_controlado": criar_acao(
        comando="reiniciar api controlado",
        apelidos=("reiniciar api de forma controlada",),
        titulo="API reiniciada com segurança",
        mensagem=(
            "As instâncias antigas foram substituídas gradualmente "
            "sem interromper todas as requisições."
        ),
        pontos=20,
        usuarios_adicionados=-500,
        tempo_gasto=45,
        requisitos=(
            "correcao_aplicada",
            "conexoes_encerradas",
        ),
        pista="api_estavel",
        pista_texto=(
            "A API voltou a responder sem criar novas conexões presas."
        ),
    ),

    "restaurar_feature": criar_acao(
        comando="restaurar feature",
        apelidos=("restaurar funcionalidade",),
        titulo="Funcionalidade restaurada",
        mensagem=(
            "A funcionalidade foi reativada utilizando a versão corrigida."
        ),
        pontos=10,
        usuarios_adicionados=20,
        tempo_gasto=20,
        requisitos=(
            "api_estavel",
            "feature_desativada",
        ),
        pista="feature_restaurada",
        pista_texto=(
            "A funcionalidade voltou a operar normalmente."
        ),
    ),

    "reabrir_trafego": criar_acao(
        comando="reabrir trafego",
        apelidos=("reabrir tráfego",),
        titulo="Tráfego restaurado",
        mensagem=(
            "O tráfego normal foi restaurado gradualmente. "
            "A API continua estável."
        ),
        pontos=10,
        usuarios_adicionados=50,
        tempo_gasto=30,
        requisitos=("api_estavel",),
        pista="trafego_reaberto",
        pista_texto=(
            "Os usuários voltaram a acessar o sistema normalmente."
        ),
    ),

    "validar_recuperacao": criar_acao(
        comando="validar recuperacao",
        apelidos=(
            "validar recuperação",
            "validar sistema",
        ),
        titulo="Recuperação validada",
        mensagem=(
            "O estado final do sistema está sendo avaliado."
        ),
        pontos=0,
        usuarios_adicionados=0,
        tempo_gasto=15,
        requisitos=("trafego_reaberto",),
    ),
}


RESULTADO_VITORIA_API = {
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


RESULTADO_DERROTA_API = {
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


CENARIO_API_0317 = {
    "id": "api_0317",
    "codigo": "0317",
    "horario": "03:17",
    "titulo": "Falha crítica na API",
    "descricao": (
        "A API parou de responder após uma nova atualização."
    ),
    "nivel": "CRÍTICO",
    "usuarios_afetados": 1248,
    "pontuacao_inicial": 100,
    "tempo_inicial": 600,

    "logs": [
        "03:16:43 - Taxa de erros acima de 80%",
        "03:16:52 - Banco de dados sem resposta",
        "03:17:05 - Timeouts detectados na API",
        "03:17:15 - 1.248 usuários afetados",
    ],

    "acoes": ACOES_API_0317,

    "regras_fase": [
        {
            "fase": "recuperacao",
            "pistas": ["vazamento_confirmado"],
        },
        {
            "fase": "contencao",
            "pistas": [
                "pool_esgotado",
                "pico_de_conexoes",
            ],
        },
    ],

    "resultado_vitoria": RESULTADO_VITORIA_API,
    "resultado_derrota": RESULTADO_DERROTA_API,
}


ACOES_DDOS_0241 = {
    "analisar_trafego": criar_acao(
        comando="analisar trafego",
        apelidos=(
            "trafego",
            "tráfego",
            "analisar tráfego",
        ),
        titulo="Tráfego analisado",
        mensagem=(
            "A API está recebendo milhares de requisições "
            "por segundo vindas de origens diferentes."
        ),
        pontos=15,
        usuarios_adicionados=120,
        tempo_gasto=30,
        pista="ataque_distribuido",
        pista_texto=(
            "O volume indica um ataque distribuído."
        ),
    ),

    "analisar_logs_acesso": criar_acao(
        comando="logs acesso",
        apelidos=(
            "analisar logs acesso",
            "logs de acesso",
        ),
        titulo="Logs de acesso analisados",
        mensagem=(
            "Milhares de requisições repetem o mesmo padrão "
            "e tentam acessar a rota de autenticação."
        ),
        pontos=15,
        usuarios_adicionados=110,
        tempo_gasto=30,
        pista="padrao_automatizado",
        pista_texto=(
            "As requisições apresentam comportamento automatizado."
        ),
    ),

    "verificar_waf": criar_acao(
        comando="verificar waf",
        apelidos=("waf",),
        titulo="WAF verificado",
        mensagem=(
            "O firewall está ativo, mas não possui uma regra "
            "capaz de identificar o padrão atual."
        ),
        pontos=10,
        usuarios_adicionados=100,
        tempo_gasto=25,
        pista="waf_sem_regra",
        pista_texto=(
            "Será necessário criar uma regra específica."
        ),
    ),

    "verificar_infra": criar_acao(
        comando="verificar infraestrutura",
        apelidos=(
            "infra",
            "infraestrutura",
            "verificar infra",
        ),
        titulo="Infraestrutura verificada",
        mensagem=(
            "Os servidores estão saudáveis. O problema é o "
            "volume anormal de tráfego recebido."
        ),
        pontos=10,
        usuarios_adicionados=80,
        tempo_gasto=25,
        pista="infra_saudavel",
        pista_texto=(
            "Não existe falha física ou interna nos servidores."
        ),
    ),

    "verificar_dns": criar_acao(
        comando="verificar dns",
        apelidos=("dns",),
        titulo="DNS verificado",
        mensagem=(
            "Os registros DNS estão corretos e não sofreram alterações."
        ),
        pontos=5,
        usuarios_adicionados=70,
        tempo_gasto=20,
        pista="dns_normal",
        pista_texto=(
            "O DNS não é a origem do incidente."
        ),
    ),

    "comunicar_incidente": criar_acao(
        comando="comunicar incidente",
        apelidos=("comunicar equipe",),
        titulo="Equipe comunicada",
        mensagem=(
            "As equipes de segurança e atendimento foram avisadas "
            "sobre a indisponibilidade."
        ),
        pontos=5,
        usuarios_adicionados=30,
        tempo_gasto=15,
        pista="equipes_comunicadas",
        pista_texto=(
            "As equipes responsáveis estão acompanhando a resposta."
        ),
    ),

    "reiniciar_gateway": criar_acao(
        comando="reiniciar gateway",
        titulo="Gateway reiniciado",
        mensagem=(
            "O gateway voltou a operar por poucos segundos, "
            "mas foi sobrecarregado novamente pelo mesmo tráfego."
        ),
        pontos=-25,
        usuarios_adicionados=500,
        tempo_gasto=45,
    ),

    "aumentar_cache": criar_acao(
        comando="aumentar cache",
        titulo="Cache ampliado sem efeito",
        mensagem=(
            "Aumentar o cache não reduziu as requisições maliciosas "
            "e consumiu recursos desnecessariamente."
        ),
        pontos=-10,
        usuarios_adicionados=180,
        tempo_gasto=30,
    ),

    "bloquear_todo_trafego": criar_acao(
        comando="bloquear tudo",
        apelidos=("bloquear todo trafego", "bloquear todo tráfego"),
        titulo="Todo o tráfego foi bloqueado",
        mensagem=(
            "Usuários legítimos e atacantes foram bloqueados. "
            "O serviço ficou completamente indisponível."
        ),
        pontos=-50,
        usuarios_adicionados=900,
        tempo_gasto=20,
        finalizado=True,
        sucesso=False,
    ),

    "desligar_api": criar_acao(
        comando="desligar api",
        titulo="API desligada",
        mensagem=(
            "A API foi desligada para interromper o ataque, "
            "mas todos os usuários perderam acesso ao sistema."
        ),
        pontos=-60,
        usuarios_adicionados=1200,
        tempo_gasto=15,
        finalizado=True,
        sucesso=False,
    ),

    "listar_origens": criar_acao(
        comando="listar origens",
        apelidos=("listar ips", "analisar ips"),
        titulo="Origens identificadas",
        mensagem=(
            "O tráfego vem de milhares de endereços distribuídos "
            "por diferentes regiões."
        ),
        pontos=15,
        usuarios_adicionados=100,
        tempo_gasto=35,
        requisitos=("ataque_distribuido",),
        pista="origens_distribuidas",
        pista_texto=(
            "Bloquear somente alguns endereços IP não será suficiente."
        ),
    ),

    "analisar_user_agents": criar_acao(
        comando="analisar user agents",
        apelidos=("user agents",),
        titulo="Assinatura dos bots encontrada",
        mensagem=(
            "Os clientes maliciosos compartilham cabeçalhos "
            "e intervalos de requisição semelhantes."
        ),
        pontos=20,
        usuarios_adicionados=80,
        tempo_gasto=35,
        requisitos=("padrao_automatizado",),
        pista="assinatura_bot",
        pista_texto=(
            "Existe uma assinatura capaz de identificar os bots."
        ),
    ),

    "identificar_endpoint": criar_acao(
        comando="identificar endpoint",
        apelidos=("endpoint",),
        titulo="Endpoint principal identificado",
        mensagem=(
            "A maior parte do tráfego está concentrada na rota /login."
        ),
        pontos=20,
        usuarios_adicionados=90,
        tempo_gasto=40,
        requisitos=(
            "ataque_distribuido",
            "padrao_automatizado",
        ),
        pista="endpoint_login",
        pista_texto=(
            "A rota de autenticação é o principal alvo do ataque."
        ),
    ),

    "verificar_credenciais": criar_acao(
        comando="verificar credenciais",
        titulo="Credenciais verificadas",
        mensagem=(
            "Não existem sinais de vazamento de senhas. "
            "O objetivo é indisponibilizar o serviço."
        ),
        pontos=10,
        usuarios_adicionados=60,
        tempo_gasto=35,
        requisitos=("endpoint_login",),
        pista="sem_vazamento_credenciais",
        pista_texto=(
            "O ataque não apresentou comprometimento de contas."
        ),
    ),

    "acionar_provedor": criar_acao(
        comando="acionar provedor",
        apelidos=("chamar provedor",),
        titulo="Provedor acionado",
        mensagem=(
            "O provedor disponibilizou sua infraestrutura "
            "especializada em filtragem de tráfego."
        ),
        pontos=15,
        usuarios_adicionados=70,
        tempo_gasto=40,
        requisitos=("origens_distribuidas",),
        pista="provedor_acionado",
        pista_texto=(
            "O tráfego pode ser enviado para um serviço de mitigação."
        ),
    ),

    "ativar_rate_limit": criar_acao(
        comando="ativar rate limit",
        apelidos=("rate limit", "limitar requisicoes"),
        titulo="Rate limit ativado",
        mensagem=(
            "A quantidade de requisições permitida por cliente "
            "foi reduzida na rota de autenticação."
        ),
        pontos=20,
        usuarios_adicionados=-450,
        tempo_gasto=30,
        requisitos=("endpoint_login",),
        pista="rate_limit_ativo",
        pista_texto=(
            "O endpoint agora limita requisições excessivas."
        ),
    ),

    "criar_regra_waf": criar_acao(
        comando="criar regra waf",
        titulo="Regra de WAF criada",
        mensagem=(
            "Uma nova regra foi preparada usando a assinatura "
            "encontrada nos clientes automatizados."
        ),
        pontos=25,
        usuarios_adicionados=50,
        tempo_gasto=45,
        requisitos=(
            "assinatura_bot",
            "waf_sem_regra",
        ),
        pista="regra_waf_pronta",
        pista_texto=(
            "A regra está pronta para ser aplicada."
        ),
    ),

    "aplicar_regra_waf": criar_acao(
        comando="aplicar regra waf",
        titulo="Regra de WAF aplicada",
        mensagem=(
            "O firewall começou a bloquear as requisições "
            "que apresentam a assinatura dos bots."
        ),
        pontos=30,
        usuarios_adicionados=-700,
        tempo_gasto=30,
        requisitos=("regra_waf_pronta",),
        pista="bots_bloqueados",
        pista_texto=(
            "Grande parte do tráfego malicioso foi interrompida."
        ),
    ),

    "ativar_scrubbing": criar_acao(
        comando="ativar scrubbing",
        apelidos=("filtrar trafego", "filtrar tráfego"),
        titulo="Filtragem externa ativada",
        mensagem=(
            "O tráfego está passando pela infraestrutura do provedor "
            "antes de chegar à aplicação."
        ),
        pontos=25,
        usuarios_adicionados=-600,
        tempo_gasto=50,
        requisitos=(
            "provedor_acionado",
            "origens_distribuidas",
        ),
        pista="scrubbing_ativo",
        pista_texto=(
            "Pacotes maliciosos estão sendo removidos externamente."
        ),
    ),

    "bloquear_paises": criar_acao(
        comando="bloquear paises",
        apelidos=("bloquear países",),
        titulo="Regiões inteiras bloqueadas",
        mensagem=(
            "O bloqueio reduziu parte do ataque, mas também impediu "
            "o acesso de muitos usuários legítimos."
        ),
        pontos=-20,
        usuarios_adicionados=350,
        tempo_gasto=30,
        requisitos=("origens_distribuidas",),
    ),

    "aumentar_instancias_ddos": criar_acao(
        comando="aumentar instancias",
        apelidos=("aumentar instâncias",),
        titulo="Capacidade temporariamente ampliada",
        mensagem=(
            "As novas instâncias reduziram a pressão por alguns "
            "instantes, mas não removeram o tráfego malicioso."
        ),
        pontos=5,
        usuarios_adicionados=-100,
        tempo_gasto=40,
        requisitos=("infra_saudavel",),
        pista="capacidade_ampliada",
        pista_texto=(
            "A aplicação ganhou tempo, mas o ataque continua ativo."
        ),
    ),

    "failover_regiao": criar_acao(
        comando="failover regiao",
        apelidos=("failover região",),
        titulo="Ataque transferido para outra região",
        mensagem=(
            "O failover apenas mudou o destino do tráfego. "
            "A segunda região também começou a ficar sobrecarregada."
        ),
        pontos=-25,
        usuarios_adicionados=450,
        tempo_gasto=50,
        requisitos=("infra_saudavel",),
    ),

    "validar_taxa_erros": criar_acao(
        comando="validar taxa erros",
        apelidos=("validar erros",),
        titulo="Taxa de erros normalizada",
        mensagem=(
            "A combinação do rate limit com a regra de WAF "
            "reduziu os erros para níveis normais."
        ),
        pontos=20,
        usuarios_adicionados=-300,
        tempo_gasto=30,
        requisitos=(
            "rate_limit_ativo",
            "bots_bloqueados",
        ),
        pista="taxa_normalizada",
        pista_texto=(
            "A API voltou a responder dentro dos níveis esperados."
        ),
    ),

    "validar_login": criar_acao(
        comando="validar login",
        titulo="Autenticação validada",
        mensagem=(
            "Usuários legítimos conseguem autenticar novamente "
            "sem lentidão ou bloqueios indevidos."
        ),
        pontos=20,
        usuarios_adicionados=-250,
        tempo_gasto=30,
        requisitos=("taxa_normalizada",),
        pista="login_estavel",
        pista_texto=(
            "O fluxo de autenticação está estável."
        ),
    ),

    "normalizar_limites": criar_acao(
        comando="normalizar limites",
        apelidos=("restaurar limites",),
        titulo="Limites normalizados",
        mensagem=(
            "Os limites foram ajustados gradualmente para não "
            "prejudicar os usuários legítimos."
        ),
        pontos=10,
        usuarios_adicionados=-100,
        tempo_gasto=20,
        requisitos=("login_estavel",),
        pista="limites_normalizados",
        pista_texto=(
            "A proteção permanece ativa sem bloquear o uso normal."
        ),
    ),

    "encerrar_incidente_ddos": criar_acao(
        comando="encerrar incidente",
        apelidos=("finalizar incidente",),
        titulo="Ataque mitigado",
        mensagem=(
            "O tráfego malicioso foi filtrado, o login voltou "
            "ao normal e as proteções permaneceram ativas."
        ),
        pontos=40,
        usuarios_adicionados=-350,
        tempo_gasto=15,
        requisitos=(
            "login_estavel",
            "limites_normalizados",
        ),
        finalizado=True,
        sucesso=True,
    ),
}


CENARIO_DDOS_0241 = {
    "id": "ddos_0241",
    "codigo": "0241",
    "horario": "02:41",
    "titulo": "Ataque distribuído à autenticação",
    "descricao": (
        "A rota de login está sendo sobrecarregada por milhares "
        "de requisições automatizadas."
    ),
    "nivel": "SEVERO",
    "usuarios_afetados": 3180,
    "pontuacao_inicial": 100,
    "tempo_inicial": 480,

    "logs": [
        "02:40:21 - Volume acima de 12.000 requisições por segundo",
        "02:40:36 - Latência da autenticação ultrapassou 9 segundos",
        "02:40:48 - Requisições originadas de milhares de endereços",
        "02:41:02 - 3.180 usuários sem acesso ao sistema",
    ],

    "acoes": ACOES_DDOS_0241,

    "regras_fase": [
        {
            "fase": "recuperacao",
            "pistas": [
                "taxa_normalizada",
                "login_estavel",
            ],
        },
        {
            "fase": "contencao",
            "pistas": [
                "ataque_distribuido",
                "endpoint_login",
                "bots_bloqueados",
                "scrubbing_ativo",
            ],
        },
    ],

    "resultado_vitoria": {
        "titulo": "Ataque mitigado",
        "mensagem": (
            "O tráfego malicioso foi filtrado e os usuários "
            "legítimos recuperaram o acesso ao sistema."
        ),
        "pontos": 40,
        "usuarios_adicionados": -350,
        "finalizado": True,
        "sucesso": True,
    },

    "resultado_derrota": {
        "titulo": "Serviço indisponível",
        "mensagem": (
            "A resposta ao ataque bloqueou usuários legítimos "
            "e não conseguiu manter o serviço disponível."
        ),
        "pontos": -50,
        "usuarios_adicionados": 900,
        "finalizado": True,
        "sucesso": False,
    },
}


CENARIOS = {
    CENARIO_API_0317["id"]: CENARIO_API_0317,
    CENARIO_DDOS_0241["id"]: CENARIO_DDOS_0241,
}


CENARIO_PADRAO = "api_0317"


def obter_cenario(cenario_id):
    return CENARIOS.get(
        cenario_id,
        CENARIOS[CENARIO_PADRAO],
    )


def listar_cenarios():
    return list(CENARIOS.values())