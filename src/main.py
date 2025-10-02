import os
import sys
import threading
import time
import json
from datetime import datetime, timedelta
import sqlite3
import requests
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pandas as pd

# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit
from src.models.user import db
from src.routes.user import user_bp
from src.routes.crypto_api import crypto_api_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'black-sultan-os-secret-key-2024'
CORS(app, origins="*")
socketio = SocketIO(app, cors_allowed_origins="*")

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(crypto_api_bp, url_prefix='/api/crypto')

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Global variables for the trading system
trading_active = True
system_metrics = {
    'cpu': 0,
    'memory': 0,
    'network': 0,
    'trades': 0
}

portfolio = {
    'totalValue': 125847.32,
    'btc': {'amount': 2.4567, 'value': 110456.78},
    'eth': {'amount': 5.2134, 'value': 14598.45},
    'bnb': {'amount': 2.1087, 'value': 792.09},
    'bsCoin': {'amount': 15847.23, 'value': 0}
}

bots = [
    {'id': 1, 'name': 'Alpha Trader', 'status': 'active', 'profit': 2847.32, 'trades': 1247},
    {'id': 2, 'name': 'Arbitrage Hunter', 'status': 'active', 'profit': 1923.45, 'trades': 892},
    {'id': 3, 'name': 'Trend Follower', 'status': 'paused', 'profit': 756.89, 'trades': 234},
    {'id': 4, 'name': 'Scalp Master', 'status': 'active', 'profit': 3421.67, 'trades': 2156},
    {'id': 5, 'name': 'Risk Manager', 'status': 'active', 'profit': 0, 'trades': 0}
]

# Trading Engine Classes
class CognitiveEthicsModule:
    def __init__(self):
        self.chaos_threshold = 70.0
        self.drawdown_threshold = 10.0
        
    def should_block_trade(self, market_volatility, current_drawdown, risk_level):
        if market_volatility > self.chaos_threshold:
            return True, "High market volatility detected"
        if current_drawdown > self.drawdown_threshold and risk_level == 'high':
            return True, "Excessive drawdown with high risk"
        return False, "Trade approved"

class PhoenixEngine:
    def __init__(self):
        self.consecutive_drawdowns = 0
        self.max_drawdowns = 5
        self.model_failures = 0
        
    def check_restart_conditions(self, is_drawdown, model_failed):
        if is_drawdown:
            self.consecutive_drawdowns += 1
        else:
            self.consecutive_drawdowns = 0
            
        if model_failed:
            self.model_failures += 1
            
        if self.consecutive_drawdowns >= self.max_drawdowns or self.model_failures > 0:
            return True
        return False
        
    def restart_system(self):
        self.consecutive_drawdowns = 0
        self.model_failures = 0
        return "System restarted and optimized"

class BlackBeastTradingEngine:
    def __init__(self):
        self.ethics_module = CognitiveEthicsModule()
        self.phoenix_engine = PhoenixEngine()
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)
        self.is_trained = False
        self.max_position_size = 0.01  # 1% of account
        self.stop_loss = 0.05  # 5%
        self.take_profit = 0.10  # 10%
        self.max_open_trades = 5
        self.current_trades = 0
        
    def train_model(self, historical_data):
        if len(historical_data) < 100:
            return False
            
        # Prepare features and targets
        df = pd.DataFrame(historical_data)
        features = ['open', 'high', 'low', 'volume']
        target = 'close'
        
        X = df[features].values
        y = df[target].values
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.model.fit(X_train, y_train)
        self.is_trained = True
        return True
        
    def predict_price(self, current_data):
        if not self.is_trained:
            return None
            
        features = np.array([[
            current_data['open'],
            current_data['high'],
            current_data['low'],
            current_data['volume']
        ]])
        
        return self.model.predict(features)[0]
        
    def execute_trade(self, symbol, action, amount):
        global portfolio, bots
        
        # Check ethics module
        market_volatility = np.random.uniform(0, 100)  # Simulated volatility
        current_drawdown = 5.0  # Simulated drawdown
        
        should_block, reason = self.ethics_module.should_block_trade(
            market_volatility, current_drawdown, 'moderate'
        )
        
        if should_block:
            return {'success': False, 'reason': reason}
            
        if self.current_trades >= self.max_open_trades:
            return {'success': False, 'reason': 'Maximum open trades reached'}
            
        # Simulate trade execution
        profit = np.random.uniform(-100, 500)  # Random profit/loss
        
        # Update bot profits
        active_bots = [bot for bot in bots if bot['status'] == 'active']
        if active_bots:
            bot = np.random.choice(active_bots)
            bot['profit'] += profit
            bot['trades'] += 1
            
        return {
            'success': True,
            'symbol': symbol,
            'action': action,
            'amount': amount,
            'profit': profit,
            'timestamp': datetime.now().isoformat()
        }

# Initialize trading engine
trading_engine = BlackBeastTradingEngine()

# Background tasks
def update_system_metrics():
    global system_metrics
    while True:
        system_metrics.update({
            'cpu': np.random.uniform(10, 90),
            'memory': np.random.uniform(20, 80),
            'network': np.random.uniform(100, 2000),
            'trades': np.random.randint(0, 100)
        })
        socketio.emit('system_metrics', system_metrics)
        time.sleep(3)

def update_prices():
    from src.routes.crypto_api import crypto_provider
    while True:
        try:
            # Get real prices from crypto API
            real_prices = crypto_provider.get_coingecko_prices()
            prices = {
                'btc': real_prices['btc']['price'],
                'eth': real_prices['eth']['price'],
                'bnb': real_prices['bnb']['price'],
                'timestamp': datetime.now().isoformat()
            }
            socketio.emit('price_update', prices)
        except Exception as e:
            print(f"Error updating prices: {e}")
            # Fallback to simulated prices
            prices = {
                'btc': 45000 + np.random.uniform(-2000, 2000),
                'eth': 2800 + np.random.uniform(-200, 200),
                'bnb': 350 + np.random.uniform(-50, 50),
                'timestamp': datetime.now().isoformat()
            }
            socketio.emit('price_update', prices)
        time.sleep(30)  # Update every 30 seconds to respect API limits

def auto_trading_loop():
    global trading_active
    while True:
        if trading_active:
            # Simulate automatic trading
            symbols = ['BTC', 'ETH', 'BNB']
            actions = ['buy', 'sell']
            
            symbol = np.random.choice(symbols)
            action = np.random.choice(actions)
            amount = np.random.uniform(0.01, 0.1)
            
            result = trading_engine.execute_trade(symbol, action, amount)
            
            if result['success']:
                socketio.emit('trade_executed', result)
                
        time.sleep(5)

# API Routes
@app.route('/api/system/status')
def get_system_status():
    return jsonify({
        'trading_active': trading_active,
        'system_metrics': system_metrics,
        'portfolio': portfolio,
        'bots': bots,
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/trading/toggle', methods=['POST'])
def toggle_trading():
    global trading_active
    trading_active = not trading_active
    return jsonify({
        'trading_active': trading_active,
        'message': f"Trading {'activated' if trading_active else 'deactivated'}"
    })

@app.route('/api/bot/<int:bot_id>/toggle', methods=['POST'])
def toggle_bot(bot_id):
    global bots
    bot = next((b for b in bots if b['id'] == bot_id), None)
    if bot:
        bot['status'] = 'paused' if bot['status'] == 'active' else 'active'
        return jsonify({
            'success': True,
            'bot': bot,
            'message': f"Bot {bot['name']} {'activated' if bot['status'] == 'active' else 'paused'}"
        })
    return jsonify({'success': False, 'message': 'Bot not found'}), 404

@app.route('/api/wallet/deposit', methods=['POST'])
def deposit_funds():
    data = request.json
    currency = data.get('currency')
    amount = data.get('amount', 0)
    
    # Generate deposit address (simulated)
    addresses = {
        'BTC': '1A1zP1eP5QGefi2DMPTfTL5SLmv7DivfNa',
        'ETH': '0x742d35Cc6634C0532925a3b8D4C0d886E682C4b1',
        'BNB': 'bnb1grpf0955h0ykzq3ar5nmum7y6gdfl6lxfn46h2'
    }
    
    return jsonify({
        'success': True,
        'currency': currency,
        'amount': amount,
        'deposit_address': addresses.get(currency, 'Unknown'),
        'network': currency,
        'estimated_confirmation_time': '10-30 minutes',
        'minimum_deposit': 0.001 if currency == 'BTC' else 0.01
    })

@app.route('/api/wallet/withdraw', methods=['POST'])
def withdraw_funds():
    data = request.json
    currency = data.get('currency')
    amount = data.get('amount', 0)
    address = data.get('address', '')
    
    # Simulate withdrawal processing
    return jsonify({
        'success': True,
        'currency': currency,
        'amount': amount,
        'destination_address': address,
        'transaction_fee': 0.001 if currency == 'BTC' else 0.005,
        'processing_time': '2-5 business days',
        'transaction_id': f"tx_{int(time.time())}"
    })

@app.route('/api/trading/history')
def get_trading_history():
    # Generate sample trading history
    history = []
    for i in range(24):
        timestamp = datetime.now() - timedelta(hours=i)
        history.append({
            'time': timestamp.strftime('%H:%M'),
            'btc': 45000 + np.random.uniform(-1000, 1000),
            'eth': 2800 + np.random.uniform(-100, 100),
            'bnb': 350 + np.random.uniform(-25, 25),
            'volume': np.random.uniform(500000, 1500000),
            'profit': (np.random.random() - 0.5) * 1000
        })
    
    return jsonify(history[::-1])  # Reverse to get chronological order

@app.route('/api/analytics/notifications')
def get_notifications():
    notifications = [
        {
            'id': 1,
            'type': 'success',
            'message': f'BTC Trade executed: +${np.random.uniform(100, 500):.2f}',
            'time': f'{np.random.randint(1, 10)} min ago'
        },
        {
            'id': 2,
            'type': 'warning',
            'message': 'High volatility detected in ETH',
            'time': f'{np.random.randint(5, 15)} min ago'
        },
        {
            'id': 3,
            'type': 'info',
            'message': 'System optimization completed',
            'time': f'{np.random.randint(10, 30)} min ago'
        }
    ]
    return jsonify(notifications)

# WebSocket events
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('system_status', {
        'trading_active': trading_active,
        'system_metrics': system_metrics,
        'portfolio': portfolio,
        'bots': bots
    })

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Initialize database and start background tasks
with app.app_context():
    db.create_all()

# Start background threads
threading.Thread(target=update_system_metrics, daemon=True).start()
threading.Thread(target=update_prices, daemon=True).start()
threading.Thread(target=auto_trading_loop, daemon=True).start()

# Static file serving
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
        return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)
