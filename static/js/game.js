document.addEventListener("DOMContentLoaded", function () {
    const terminalSaida =
        document.getElementById("terminalSaida");

    const campoComando =
        document.getElementById("comando");

    const formulario =
        document.querySelector(".terminal-formulario");

    const terminal =
        document.getElementById("terminal");

    const tempoRestante =
        document.getElementById("tempoRestante");

    const horarioGlitch =
        document.querySelector(".horario-glitch");

    const textoDecodificar =
        document.querySelector("[data-decode]");

    const codigoIncidente =
        document.body.dataset.incidente || "0317";

    const chaveHistorico =
        "incident-" +
        codigoIncidente +
        "-historico-comandos";

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
            console.log(
                "Não foi possível carregar o histórico."
            );
        }

        return [];
    }

    function salvarHistorico() {
        try {
            sessionStorage.setItem(
                chaveHistorico,
                JSON.stringify(historicoComandos)
            );
        } catch (erro) {
            console.log(
                "Não foi possível salvar o histórico."
            );
        }
    }

    function rolarTerminalParaFinal() {
        if (!terminalSaida) {
            return;
        }

        terminalSaida.scrollTop =
            terminalSaida.scrollHeight;
    }

    function focarCampo() {
        if (campoComando) {
            campoComando.focus();
        }
    }

    function levarCursorParaFinal() {
        if (!campoComando) {
            return;
        }

        const tamanho =
            campoComando.value.length;

        campoComando.setSelectionRange(
            tamanho,
            tamanho
        );
    }

    function mostrarHistorico() {
        if (!campoComando) {
            return;
        }

        if (
            posicaoHistorico ===
            historicoComandos.length
        ) {
            campoComando.value =
                comandoAtual;
        } else {
            campoComando.value =
                historicoComandos[
                    posicaoHistorico
                ];
        }

        levarCursorParaFinal();
    }

    function formatarTempo(totalSegundos) {
        const minutos =
            Math.floor(totalSegundos / 60);

        const segundos =
            totalSegundos % 60;

        return (
            String(minutos).padStart(2, "0") +
            ":" +
            String(segundos).padStart(2, "0")
        );
    }

    function iniciarContador() {
        if (!tempoRestante) {
            return;
        }

        const segundosIniciais =
            Number(
                tempoRestante.dataset.segundos
            );

        const finalizado =
            tempoRestante.dataset.finalizado ===
            "true";

        if (
            !Number.isFinite(segundosIniciais)
        ) {
            return;
        }

        tempoRestante.textContent =
            formatarTempo(segundosIniciais);

        if (finalizado) {
            return;
        }

        const inicio = Date.now();

        function atualizar() {
            const segundosPassados =
                Math.floor(
                    (Date.now() - inicio) / 1000
                );

            const segundosAtuais =
                Math.max(
                    0,
                    segundosIniciais -
                    segundosPassados
                );

            tempoRestante.textContent =
                formatarTempo(segundosAtuais);

            if (segundosAtuais <= 60) {
                tempoRestante.classList.add(
                    "tempo-critico"
                );
            }

            return segundosAtuais;
        }

        atualizar();

        const intervalo = setInterval(
            function () {
                if (atualizar() === 0) {
                    clearInterval(intervalo);
                }
            },
            1000
        );
    }

    function decodificarTexto() {
        if (!textoDecodificar) {
            return;
        }

        const textoFinal =
            textoDecodificar.dataset.decode;

        if (!textoFinal) {
            return;
        }

        const caracteres =
            "01#$%&*@<>/[]";

        let progresso = 0;

        const intervalo = setInterval(
            function () {
                textoDecodificar.textContent =
                    textoFinal
                        .split("")
                        .map(
                            function (
                                caractere,
                                indice
                            ) {
                                if (
                                    caractere === " "
                                ) {
                                    return " ";
                                }

                                if (
                                    indice < progresso
                                ) {
                                    return caractere;
                                }

                                const posicao =
                                    Math.floor(
                                        Math.random() *
                                        caracteres.length
                                    );

                                return caracteres[
                                    posicao
                                ];
                            }
                        )
                        .join("");

                progresso += 0.55;

                if (
                    progresso >=
                    textoFinal.length
                ) {
                    clearInterval(intervalo);

                    textoDecodificar.textContent =
                        textoFinal;
                }
            },
            35
        );
    }

    function executarGlitch() {
        if (!horarioGlitch) {
            return;
        }

        horarioGlitch.classList.add(
            "glitch-ativo"
        );

        setTimeout(
            function () {
                horarioGlitch.classList.remove(
                    "glitch-ativo"
                );
            },
            180
        );
    }

    function iniciarGlitch() {
        if (!horarioGlitch) {
            return;
        }

        setTimeout(
            executarGlitch,
            650
        );

        setInterval(
            executarGlitch,
            4200
        );
    }

    if (campoComando) {
        campoComando.addEventListener(
            "keydown",
            function (evento) {
                if (evento.key === "ArrowUp") {
                    evento.preventDefault();

                    if (
                        historicoComandos.length === 0
                    ) {
                        return;
                    }

                    if (
                        posicaoHistorico ===
                        historicoComandos.length
                    ) {
                        comandoAtual =
                            campoComando.value;
                    }

                    if (
                        posicaoHistorico > 0
                    ) {
                        posicaoHistorico -= 1;
                    }

                    mostrarHistorico();
                }

                if (
                    evento.key === "ArrowDown"
                ) {
                    evento.preventDefault();

                    if (
                        posicaoHistorico <
                        historicoComandos.length
                    ) {
                        posicaoHistorico += 1;
                    }

                    mostrarHistorico();
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

                const ultimoComando =
                    historicoComandos[
                        historicoComandos.length - 1
                    ];

                if (
                    ultimoComando !== comando
                ) {
                    historicoComandos.push(
                        comando
                    );
                }

                historicoComandos =
                    historicoComandos.slice(-50);

                salvarHistorico();

                if (terminal) {
                    terminal.classList.add(
                        "enviando"
                    );
                }
            }
        );
    }

    if (terminal && campoComando) {
        terminal.addEventListener(
            "click",
            function () {
                const textoSelecionado =
                    window
                        .getSelection()
                        .toString();

                if (!textoSelecionado) {
                    focarCampo();
                }
            }
        );
    }

    window.addEventListener(
        "pageshow",
        function () {
            rolarTerminalParaFinal();
            focarCampo();
        }
    );

    rolarTerminalParaFinal();
    focarCampo();
    iniciarContador();
    decodificarTexto();
    iniciarGlitch();
});