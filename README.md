# Central do Assessor

Abrir no navegador (Chrome ou Edge): https://central-assessor.github.io/

Arquivo único (`index.html`). Na abertura, o assessor arrasta o PDF do laudo recebido (a Central confere, marca no Registro de OS e abre a análise; daí também salva o modelo e inclui a OS no Registro) ou o PDF do QL (abre a preparação dos arquivos da OS já preenchida), ou prepara os arquivos da OS. O formulário vigente vem dentro da Central e vai com os arquivos da OS; `versao.json` diz qual é a versão vigente da Central (cópias antigas ficam bloqueadas para preparar OS). Os PDFs dos laudos são lidos no computador de quem usa; nada é enviado. As análises em andamento e o Registro de OS ficam guardados no navegador, separados por endereço.

Conexões: a página só se conecta aos servidores do mapa das amostras (OpenFreeMap e Esri). A biblioteca do mapa é carregada com a versão travada e o conteúdo conferido; qualquer outro envio é bloqueado pelo navegador.

Atualizar o formulário: `ferramentas/atualizar_formulario.py` (instruções no início do arquivo).

## Controle de Laudos

Abrir no navegador: https://central-assessor.github.io/controle/

Arquivo único (`controle/index.html`), sem conexões externas. Os dados ficam no `controle_laudos.json` da pasta escolhida pelo assessor (e uma cópia no navegador); nada é enviado. Como está no mesmo endereço da Central, os dois conversam pela ponte (`ponte-controle-central`): a Central avisa laudo recebido, devolvido e homologado, e o Controle manda a OS para o preparo do pacote. A Central só grava avisos no navegador onde o Controle já foi aberto.
