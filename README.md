# Central do Assessor

Abrir no navegador (Chrome ou Edge): https://central-assessor.github.io/

Arquivo único (`index.html`). A abertura leva a preparar os arquivos da OS, analisar um laudo ou extrair o modelo. O formulário vigente vem dentro da Central e vai com os arquivos da OS; `versao.json` diz qual é a versão vigente da Central (cópias antigas ficam bloqueadas para preparar OS). Os PDFs dos laudos são lidos no computador de quem usa; nada é enviado. As análises em andamento e o Registro de OS ficam guardados no navegador, separados por endereço.

Conexões: a página só se conecta aos servidores do mapa das amostras (OpenFreeMap e Esri). A biblioteca do mapa é carregada com a versão travada e o conteúdo conferido; qualquer outro envio é bloqueado pelo navegador.

Atualizar o formulário: `ferramentas/atualizar_formulario.py` (instruções no início do arquivo).
