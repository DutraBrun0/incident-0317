document.addEventListener("DOMContentLoaded", function () {
    const terminalSaida =
        document.getElementById("terminalSaida");

    const campoComando =
        document.getElementById("comando");

    const formulario =
        document.querySelector(".terminal-formulario");

    const areaTerminal =
        document.querySelector(".area-terminal");

    const tempoRestante =
        document.getElementById("tempoRestante");

    const estadoSimulacao =
        document.querySelector(".estado-simulacao");

    const chaveHistorico =
        "incident-0317-historico-comandos";

    const simulacaoFinalizada =
        tempoRestante?.dataset.finalizado === "true";

    let historicoComandos = carregarHistorico();
    let posicaoHistorico = historicoComandos.length;
    let comandoAtual = "";


    function carregarHistorico() {
        try {
            const historicoSalvo =
                sessionStorage.getItem(chaveHistorico);

            const historico =
                JSON.parse(historicoSalvo);

            if (Array.isArray(historico)) {
                return historico;
            }
        } catch (erro) {
            console.log("Histórico não encontrado.");
        }

        return [];
    }


    function salvarHistorico() {
        sessionStorage.setItem(
            chaveHistorico,
            JSON.stringify(historicoComandos)
        );
    }


    function normalizarComando(comando) {
        return comando
            .toLowerCase()
            .trim()
            .replace(/\s+/g, " ");
    }


    function comandoReiniciaPartida(comando) {
        const comandoNormalizado =
            normalizarComando(comando);

        return (
            comandoNormalizado === "reiniciar"
            || comandoNormalizado === "reiniciar partida"
        );
    }


    function rolarTerminalParaFinal() {
        if (terminalSaida) {
            terminalSaida.scrollTop =
                terminalSaida.scrollHeight;
        }
    }


    function levarCursorParaFinal() {
        if (!campoComando) {
            return;
        }

        const tamanho = campoComando.value.length;

        campoComando.setSelectionRange(
            tamanho,
            tamanho
        );
    }


    function mostrarComandoDoHistorico() {
        if (!campoComando) {
            return;
        }

        if (
            posicaoHistorico
            === historicoComandos.length
        ) {
            campoComando.value = comandoAtual;
        } else {
            campoComando.value =
                historicoComandos[posicaoHistorico];
        }

        levarCursorParaFinal();
    }


    function formatarTempo(totalSegundos) {
        const minutos =
            Math.floor(totalSegundos / 60);

        const segundos =
            totalSegundos % 60;

        return (
            String(minutos).padStart(2, "0")
            + ":"
            + String(segundos).padStart(2, "0")
        );
    }


    function iniciarContador() {
        if (!tempoRestante) {
            return;
        }

        const segundosIniciais =
            Number(tempoRestante.dataset.segundos);

        if (!Number.isFinite(segundosIniciais)) {
            return;
        }

        tempoRestante.textContent =
            formatarTempo(segundosIniciais);

        if (simulacaoFinalizada) {
            return;
        }

        const inicio = Date.now();

        function atualizarContador() {
            const segundosPassados = Math.floor(
                (Date.now() - inicio) / 1000
            );

            const segundosAtuais = Math.max(
                0,
                segundosIniciais - segundosPassados
            );

            tempoRestante.textContent =
                formatarTempo(segundosAtuais);

            return segundosAtuais;
        }

        const intervalo = setInterval(function () {
            if (atualizarContador() === 0) {
                clearInterval(intervalo);
            }
        }, 1000);
    }


    function prepararPartidaFinalizada() {
        if (!simulacaoFinalizada) {
            return;
        }

        if (estadoSimulacao) {
            estadoSimulacao.classList.add(
                "simulacao-finalizada"
            );
        }

        if (campoComando) {
            campoComando.value = "";

            campoComando.placeholder =
                'Digite "reiniciar"';

            campoComando.setAttribute(
                "aria-label",
                'Simulação encerrada. Digite "reiniciar".'
            );
        }
    }


    if (campoComando) {
        campoComando.focus();

        campoComando.addEventListener(
            "input",
            function () {
                campoComando.setCustomValidity("");
            }
        );

        campoComando.addEventListener(
            "keydown",
            function (evento) {
                if (simulacaoFinalizada) {
                    return;
                }

                if (evento.key === "ArrowUp") {
                    evento.preventDefault();

                    if (historicoComandos.length === 0) {
                        return;
                    }

                    if (
                        posicaoHistorico
                        === historicoComandos.length
                    ) {
                        comandoAtual =
                            campoComando.value;
                    }

                    if (posicaoHistorico > 0) {
                        posicaoHistorico -= 1;
                    }

                    mostrarComandoDoHistorico();
                }

                if (evento.key === "ArrowDown") {
                    evento.preventDefault();

                    if (
                        posicaoHistorico
                        < historicoComandos.length
                    ) {
                        posicaoHistorico += 1;
                    }

                    mostrarComandoDoHistorico();
                }
            }
        );
    }


    if (formulario && campoComando) {
        formulario.addEventListener(
            "submit",
            function (evento) {
                const comando =
                    campoComando.value.trim();

                if (!comando) {
                    evento.preventDefault();
                    return;
                }

                if (
                    simulacaoFinalizada
                    && !comandoReiniciaPartida(comando)
                ) {
                    evento.preventDefault();

                    campoComando.setCustomValidity(
                        'A simulação terminou. Digite "reiniciar".'
                    );

                    campoComando.reportValidity();
                    campoComando.focus();

                    return;
                }

                if (comandoReiniciaPartida(comando)) {
                    sessionStorage.removeItem(
                        chaveHistorico
                    );

                    return;
                }

                const ultimoComando =
                    historicoComandos[
                        historicoComandos.length - 1
                    ];

                if (ultimoComando !== comando) {
                    historicoComandos.push(comando);
                }

                historicoComandos =
                    historicoComandos.slice(-50);

                salvarHistorico();
            }
        );
    }


    if (areaTerminal && campoComando) {
        areaTerminal.addEventListener(
            "click",
            function () {
                const selecao =
                    window.getSelection();

                const textoSelecionado =
                    selecao ? selecao.toString() : "";

                if (!textoSelecionado) {
                    campoComando.focus();
                }
            }
        );
    }


    prepararPartidaFinalizada();
    rolarTerminalParaFinal();
    iniciarContador();
});