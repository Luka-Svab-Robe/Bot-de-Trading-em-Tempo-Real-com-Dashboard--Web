<h1>
🤖 <strong>Real-Time Trading Bot & Dashboard | Análise Técnica</strong>
</h1>

Este repositório contém uma prova de conceito (PoC) de um bot de trading para a Binance, implementado com um backend Python (Flask/Socket.IO) e um dashboard de monitoramento single-page em HTML/JS. O sistema utiliza uma estratégia de cruzamento de médias móveis para executar ordens de mercado no par BTC/USDT.

🖼️ Dashboard Preview
A interface é projetada para fornecer uma visão consolidada e em tempo real das operações do bot.

(Imagem de referência ilustrando um dashboard de trading moderno)

A UI é segmentada nos seguintes componentes principais:

+---------------------------------------------------------------------------------+
|                                                                                 |
|                      DASHBOARD DO BOT DE TRADE (CLIENTE-SERVIDOR)                 |
|                                                                                 |
+--------------------------------------------------+------------------------------+
| [CONTROLES]                                      | [PREÇO ATUAL (BTCUSD)]       |
|  > Iniciar      > Parar                          |  $68,123.45                  |
+--------------------------------------------------+------------------------------+
| [SINAL DA ESTRATÉGIA]                            | [STATUS]                     |
|  BUY (verde) / SELL (vermelho) / HOLD (amarelo)  |  Rodando / Parado            |
+--------------------------------------------------+------------------------------+
|                                                                                 |
| [ GRÁFICO DE PREÇO E MÉDIAS MÓVEIS - Chart.js ]                                  |
|                                                                                 |
|  /``````\      /``````\       Preço ------                                       |
| /        \..../        \      Média Curta ......                                 |
|/                       /`\    Média Longa -- -- --                               |
|                                                                                 |
+---------------------------------------------------------------------------------+
|                                                                                 |
| [ LOG DE OPERAÇÕES EM TEMPO REAL ]                                              |
|  [15:30:01] Preço coletado: $68123.45                                            |
|  [15:30:01] Sinal da estratégia: HOLD                                           |
|  [15:30:06] Preço coletado: $68125.99                                            |
|  [15:30:06] Sinal da estratégia: HOLD                                           |
|                                                                                 |
+---------------------------------------------------------------------------------+
🏗️ Arquitetura do Sistema
O projeto segue um modelo cliente-servidor desacoplado com comunicação em tempo real via WebSockets.

Backend (trade_bot_server.py):

Servidor de Aplicação: Flask gerencia os endpoints de controle (/start, /stop).

Comunicação Real-Time: Flask-SocketIO estabelece uma conexão persistente com o cliente, emitindo eventos (status_update, log) a cada ciclo do bot. Isso é preferível a polling HTTP por sua baixa latência e menor overhead.

Concorrência: O ciclo principal do bot (run_bot_cycle) é executado em uma Thread separada para não bloquear o servidor Flask, permitindo que a aplicação permaneça responsiva aos comandos da UI. Um Event (stop_event) é usado para sinalizar a interrupção da thread de forma segura.

Lógica de Negócio:

RealAPIBroker: Uma classe que abstrai a interação com a API da Binance, encapsulando a busca de preços e a execução de ordens.

Strategy: Implementa a lógica de análise de dados (cálculo de MAs e cruzamentos) usando pandas, desacoplando a estratégia do ciclo principal do bot.

Frontend (trade_bot_dashboard_html_v2.html):

Interface: Um único arquivo HTML com CSS embarcado para simplicidade.

Comunicação: O cliente socket.io.min.js conecta-se ao backend e escuta os eventos. A UI é reativa, atualizando o DOM dinamicamente com base nos dados recebidos, sem a necessidade de page reloads.

Visualização: Chart.js é utilizado para renderizar o gráfico de preços e as médias móveis, atualizado a cada evento status_update.

🛠️ Setup do Ambiente de Desenvolvimento
Pré-requisitos: Python 3.7+, pip, venv.

Clonar e configurar o ambiente:

Bash

git clone <url-do-repositorio>
cd <diretorio-do-repositorio>
python -m venv venv
source venv/bin/activate # ou .\venv\Scripts\activate no Windows
Instalar dependências:

Bash

pip install -r requirements.txt # Assumindo a criação de um requirements.txt
# ou manualmente:
pip install Flask Flask-SocketIO Flask-Cors pandas python-binance
Configurar Variáveis:

Edite trade_bot_server.py e insira suas chaves de API da Binance.

[IMPORTANTE] Aponte para a base_url da Testnet para desenvolvimento e validação.

Execução:

Backend: python trade_bot_server.py

Frontend: Abra o arquivo trade_bot_dashboard_html_v2.html em um navegador.

🔬 Análise de Design e Pontos de Melhoria
Embora funcional como PoC, diversas melhorias são recomendadas para um ambiente de produção.

Gestão de Configuração:

Problema: Chaves de API e parâmetros da estratégia (janelas das MAs, quantidade a negociar) estão hardcoded.

Solução: Externalizar configurações para variáveis de ambiente (usando python-dotenv) ou um arquivo de configuração (e.g., config.yaml). Isso melhora a segurança e a flexibilidade.

Gestão de Estado:

Problema: O estado do bot (dados de mercado, status) é mantido em memória e perdido ao reiniciar o servidor. Uma desconexão do cliente também o faz perder o histórico do gráfico.

Solução: Persistir os dados de mercado e os logs de operações em um banco de dados (e.g., SQLite para simplicidade, ou uma time-series DB como InfluxDB para performance). O servidor poderia enviar um snapshot histórico ao cliente no momento da conexão.

Estratégia e Backtesting:

Problema: A estratégia é monolítica. Testar novas lógicas requer alterar o código principal. Não há framework para backtesting.

Solução: Implementar um "Strategy Pattern", onde diferentes estratégias possam ser carregadas dinamicamente. Desenvolver um simulador que possa rodar a mesma lógica do bot contra dados históricos para validar a eficácia da estratégia antes do deploy.

Robustez e Error Handling:

Problema: O tratamento de erros da API da Binance é básico. Falhas de rede ou limites de taxa podem interromper a operação de forma não graceful.

Solução: Implementar lógicas de retentativa com exponential backoff para chamadas de API. Adicionar um tratamento mais detalhado para os diferentes códigos de erro da Binance.

Arquitetura Frontend:

Problema: O código JS está misturado ao HTML, dificultando a manutenção.

Solução: Separar JS e CSS em arquivos distintos. Para uma aplicação mais complexa, migrar para um framework como React, Vue ou Svelte para componentização e gerenciamento de estado mais eficiente.

Deployment:

Solução: Containerizar a aplicação com Docker e Docker Compose para garantir um ambiente de execução consistente e simplificar o deploy.

:warning: ADVERTÊNCIA DE SEGURANÇA
NÃO FAÇA COMMIT DE CHAVES DE API NO REPOSITÓRIO. O arquivo trade_bot_server.py como está não é seguro para ser versionado em um repositório público se preenchido com chaves reais. Utilize variáveis de ambiente ou um sistema de secrets management (como HashiCorp Vault ou AWS Secrets Manager) para gerenciar credenciais em produção.
