🤖 Bot-de-Trading-em-Tempo-Real-com-Dashboard-Web 💹

🚀 Sobre o Projeto

Este projeto é a combinação de um cérebro analítico de trading com uma interface web vibrante e interativa. Ele opera em tempo real, conectando-se diretamente à exchange de criptomoedas Binance para negociar o par BTC/USDT.

O sistema é dividido em duas potências:

🧠 Servidor Python (Backend): O coração da operação. Usando Flask e Socket.IO, este servidor executa toda a lógica do bot. Ele se conecta à API da Binance para buscar preços de mercado ao vivo e para executar ordens de compra e venda com precisão cirúrgica. A cada ciclo, a estratégia é analisada e os dados são enviados para o dashboard.

🖥️ Dashboard Web (Frontend): A janela para a alma do bot. Criado com HTML, CSS e JavaScript, este painel se conecta ao servidor para exibir um show de dados em tempo real: preço atual, sinais da estratégia, status do bot e um log detalhado de cada movimento. O destaque é um gráfico dinâmico que dá vida aos dados, plotando o preço e as médias móveis para uma visualização clara da estratégia em ação.

O objetivo é claro: criar uma plataforma visual e poderosa para automatizar e monitorar estratégias de trading, colocando o controle total nas suas mãos através de uma interface web intuitiva.

✨ Funcionalidades
🔗 Conexão Real com a Binance: Integração total com a API oficial da Binance para dados de mercado e execução de ordens.

📈 Estratégia de Médias Móveis: Gera sinais de COMPRA (BUY), VENDA (SELL) ou MANTER (HOLD) com base no cruzamento de uma média móvel curta (5 períodos) e uma longa (12 períodos).

💻 Dashboard Interativo: Uma interface web moderna para monitorar o bot, visualizar preços, sinais e um log detalhado de todas as operações em tempo real.

🎮 Controle Remoto: Botões de "Iniciar" e "Parar" no dashboard para você ter o controle total da execução do bot no servidor.

📊 Visualização Gráfica: Um gráfico dinâmico que exibe o histórico de preços e as duas médias móveis, tornando a estratégia fácil de acompanhar visualmente.

📡 Comunicação em Tempo Real: Uso de WebSockets (Socket.IO) para uma comunicação instantânea e eficiente entre o servidor e o seu dashboard.

🛠️ Tecnologias Utilizadas
⚙️ Backend:

Python

Flask

Flask-SocketIO

python-binance

🎨 Frontend:

HTML5

CSS3

JavaScript

Socket.IO Client

Chart.js

✅ Pré-requisitos
Antes de mergulhar, garanta que você tenha:

Python 3.x instalado.

pip (gerenciador de pacotes do Python) pronto para usar.

🔑 Chaves de API da Binance. (IMPORTANTE: Comece com as chaves da Testnet para não arriscar dinheiro real!).

🚀 Como Executar
📂 Clone o repositório:

Bash

git clone <url-do-repositorio>
cd <nome-do-repositorio>
📦 Instale as dependências:

Bash

pip install Flask Flask-SocketIO Flask-Cors python-binance pandas
🔧 Configure suas chaves de API:

Abra o arquivo trade_bot_server.py.

Encontre estas linhas e preencha com suas chaves:

Python

API_KEY = ""
SECRET_KEY = ""
Para usar a conta de testes (Paper Trading), descomente a linha da testnet e comente a linha da conta real:

Python

# Para usar a conta de testes (Paper Trading), descomente la linha abaixo:
client = Client(API_KEY, SECRET_KEY, base_url='https://testnet.binance.vision')
# Para usar a conta real, use a linha abaixo:
# client = Client(API_KEY, SECRET_KEY)
🚀 Inicie o servidor:

Bash

python trade_bot_server.py
O servidor estará no ar em http://127.0.0.1:5000.

🌐 Abra o Dashboard:

Abra o arquivo trade_bot_dashboard_html_v2.html no seu navegador favorito.

▶️ Opere o Bot:

Clique em Iniciar no dashboard para ligar os motores.

Acompanhe toda a ação em tempo real.

Clique em Parar para pausar as operações.

🗄️ Estrutura dos Arquivos
trade_bot_server.py 🐍: O cérebro do projeto. Contém o servidor Flask, a lógica de trading, a conexão com a API da Binance e a comunicação via WebSocket.

trade_bot_dashboard_html_v2.html 📄: A face do projeto. Um arquivo único com a estrutura (HTML), o estilo (CSS) e a interatividade (JavaScript) do dashboard.

📊 Funcionalidades do Dashboard
🕹️ Controles: Botões intuitivos para Iniciar e Parar o bot.

💲 Preço Atual (BTCUSD): O valor do Bitcoin em relação ao USDT, atualizado a cada ciclo.

🚦 Sinal da Estratégia: Indicação visual e colorida do sinal atual: BUY (verde), SELL (vermelho) ou HOLD (amarelo).

💡 Status: Saiba se o bot está Rodando ou Parado a qualquer momento.

📈 Gráfico de Preços: Um gráfico de linha dinâmico que plota o preço do BTC e as médias móveis curta e longa.

📜 Log de Eventos: Um console em tempo real que mostra cada passo do bot: preços, sinais, ordens executadas e possíveis erros.

🔄 Lógica do Servidor
O servidor opera em um ciclo contínuo (dentro de uma thread) que se repete a cada 5 segundos após ser iniciado. Cada ciclo segue estes passos:

📥 Coleta de Dados: Busca o preço de mercado mais recente do par BTCUSDT na Binance.

🧠 Análise de Estratégia: Usa o Pandas para calcular as médias móveis (curta de 5 períodos, longa de 12) com base no histórico de preços.

📊 Geração de Sinal: Compara as médias móveis para identificar cruzamentos e gerar um sinal: BUY, SELL ou HOLD.

💸 Execução de Ordem: Se o sinal for BUY ou SELL, uma ordem a mercado é enviada para a Binance com uma quantidade pré-definida.

📤 Transmissão de Status: Todas as informações relevantes (preço, sinal, status, MAs) são transmitidas via Socket.IO para todos os dashboards conectados.

⚠️ Disclaimer
Este projeto é uma ferramenta para fins educacionais e de demonstração. O trading de criptomoedas é uma atividade de alto risco. Os autores não se responsabilizam por quaisquer perdas financeiras. Sempre utilize a conta de testes (Testnet) para validar sua estratégia antes de pensar em operar com dinheiro real. Negocie com responsabilidade!
