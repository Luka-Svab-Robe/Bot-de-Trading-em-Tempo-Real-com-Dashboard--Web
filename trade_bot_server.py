import time
import random
import pandas as pd
from datetime import datetime
from threading import Thread, Event

# --- NOVO: Importe a biblioteca da corretora ---
from binance.spot import Spot as Client
from binance.error import ClientError

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

# --- Configuração do Servidor Flask e SocketIO ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
CORS(app, resources={r"/*": {"origins": "*"}}) 
socketio = SocketIO(app, cors_allowed_origins="*")

# --- NOVO: Insira suas chaves de API da Binance aqui ---
# IMPORTANTE: Comece com chaves da Testnet (Paper Trading) para não arriscar dinheiro real.
API_KEY = ""
SECRET_KEY = ""

# --- NOVO: Inicialize o cliente da corretora ---
# Para usar a conta de testes (Paper Trading), descomente a linha abaixo:
# client = Client(API_KEY, SECRET_KEY, base_url='https://testnet.binance.vision')
# Para usar a conta real, use a linha abaixo:
client = Client(API_KEY, SECRET_KEY)


# --- Variáveis de Estado Globais ---
bot_thread = None
stop_event = Event()
market_data = []

# --- Módulos do Bot (Lógica Principal) ---

# --- REMOVIDO: A classe MockAPIBroker foi substituída ---
# class MockAPIBroker: ...

# --- NOVO: Classe para interagir com a API real da Binance ---
class RealAPIBroker:
    def __init__(self, symbol="BTCUSDT"):
        self.symbol = symbol
        print(f"RealAPIBroker iniciado para o símbolo {self.symbol}.")

    def get_market_price(self):
        """Busca o preço de mercado real da Binance."""
        try:
            ticker_info = client.ticker_price(self.symbol)
            return float(ticker_info['price'])
        except ClientError as e:
            # Emite um log de erro para o dashboard
            socketio.emit('log', {'type': 'error', 'message': f"Erro na API da Binance: {e.error_message}"})
            print(f"Erro ao buscar preço da Binance: {e}")
            return None

    def execute_order(self, side, quantity):
        """Envia uma ordem de compra ou venda real para a Binance."""
        try:
            # CUIDADO: Esta linha executa uma ordem real se conectada à conta principal!
            print(f"Enviando ordem {side} de {quantity} {self.symbol}...")
            order = client.new_order(
                symbol=self.symbol,
                side=side,  # 'BUY' ou 'SELL'
                type='MARKET', # Ordem a mercado (executa no melhor preço atual)
                quantity=quantity
            )
            print("Ordem executada com sucesso:", order)
            return order
        except ClientError as e:
            socketio.emit('log', {'type': 'error', 'message': f"ERRO AO EXECUTAR ORDEM: {e.error_message}"})
            print(f"ERRO AO EXECUTAR ORDEM: {e}")
            return None

class Strategy:
    def __init__(self, short_window=5, long_window=12):
        self.short_window = short_window
        self.long_window = long_window

    def analyze(self, data_df):
        if len(data_df) < self.long_window:
            return {'signal': 'HOLD', 'short_ma': None, 'long_ma': None}

        prices = data_df['price']
        short_ma = prices.rolling(window=self.short_window).mean()
        long_ma = prices.rolling(window=self.long_window).mean()

        last_short_ma = short_ma.iloc[-1]
        prev_short_ma = short_ma.iloc[-2]
        last_long_ma = long_ma.iloc[-1]
        prev_long_ma = long_ma.iloc[-2]

        signal = 'HOLD'
        if pd.notna(prev_short_ma) and pd.notna(prev_long_ma):
            if prev_short_ma <= prev_long_ma and last_short_ma > last_long_ma:
                signal = 'BUY'
            elif prev_short_ma >= prev_long_ma and last_short_ma < last_long_ma:
                signal = 'SELL'
        
        return {'signal': signal, 'short_ma': last_short_ma, 'long_ma': last_long_ma}

# --- Loop de Execução do Bot (MODIFICADO) ---

def run_bot_cycle():
    """O ciclo principal do bot que roda em segundo plano."""
    global market_data
    # MODIFICADO: Usa o broker real em vez do simulador
    api_broker = RealAPIBroker(symbol="BTCUSDT")
    strategy = Strategy()
    
    socketio.emit('log', {'type': 'system', 'message': 'Thread do bot iniciada. Conectado à Binance.'})

    while not stop_event.is_set():
        # 1. Coleta de dados reais
        price = api_broker.get_market_price()
        if price is None: # Se houver erro na API, aguarda e tenta novamente
            socketio.sleep(5)
            continue
            
        timestamp = datetime.now()
        market_data.append({'timestamp': timestamp, 'price': price})
        socketio.emit('log', {'type': 'info', 'message': f'Preço coletado: ${price:.2f}'})

        if len(market_data) > 100:
            market_data.pop(0)

        # 2. Análise e decisão
        df = pd.DataFrame(market_data)
        analysis_result = strategy.analyze(df)
        signal = analysis_result['signal']
        
        socketio.emit('log', {'type': 'strategy', 'message': f'Sinal da estratégia: {signal}'})

        # 3. Execução REAL
        if signal == 'BUY':
            # DEFINA A QUANTIDADE A SER COMPRADA AQUI! Ex: 0.001 BTC
            quantity_to_trade = 0.001
            api_broker.execute_order(side='BUY', quantity=quantity_to_trade)
            socketio.emit('log', {'type': 'execution-buy', 'message': f'EXECUÇÃO: Ordem de COMPRA de {quantity_to_trade} enviada.'})
        elif signal == 'SELL':
            # DEFINA A QUANTIDADE A SER VENDIDA AQUI! Ex: 0.001 BTC
            quantity_to_trade = 0.001
            api_broker.execute_order(side='SELL', quantity=quantity_to_trade)
            socketio.emit('log', {'type': 'execution-sell', 'message': f'EXECUÇÃO: Ordem de VENDA de {quantity_to_trade} enviada.'})

        # 4. Emite o status para todos os clientes conectados
        socketio.emit('status_update', {
            'price': price,
            'signal': signal,
            'status': 'Rodando',
            'timestamp': timestamp.strftime('%H:%M:%S'),
            'short_ma': analysis_result['short_ma'],
            'long_ma': analysis_result['long_ma']
        })
        
        # Intervalo entre as checagens. Cuidado com os limites da API.
        socketio.sleep(5) 

    socketio.emit('log', {'type': 'system', 'message': 'Thread do bot parada.'})
    socketio.emit('status_update', {'status': 'Parado', 'price': 0, 'signal': 'N/A'})


# --- Endpoints da API para Controle (sem alterações) ---

@app.route('/start', methods=['POST'])
def start_bot():
    global bot_thread, stop_event, market_data
    if bot_thread and bot_thread.is_alive():
        return jsonify({"status": "error", "message": "Bot já está rodando."}), 400

    stop_event.clear()
    market_data = []
    bot_thread = Thread(target=run_bot_cycle)
    bot_thread.start()
    return jsonify({"status": "success", "message": "Bot iniciado."})

@app.route('/stop', methods=['POST'])
def stop_bot():
    global stop_event
    if not bot_thread or not bot_thread.is_alive():
        return jsonify({"status": "error", "message": "Bot não está rodando."}), 400
    
    stop_event.set()
    return jsonify({"status": "success", "message": "Sinal de parada enviado."})

# --- Eventos do SocketIO (sem alterações) ---

@socketio.on('connect')
def handle_connect():
    print('Cliente conectado')
    emit('log', {'type': 'system', 'message': 'Dashboard conectado ao servidor.'})

@socketio.on('disconnect')
def handle_disconnect():
    print('Cliente desconectado')

# --- Ponto de Entrada Principal ---

if __name__ == '__main__':
    print("Servidor do Bot de Trade iniciado em http://127.0.0.1:5000")
    print("Abra o arquivo HTML no seu navegador para ver o dashboard.")
    socketio.run(app, host='127.0.0.1', port=5000)
