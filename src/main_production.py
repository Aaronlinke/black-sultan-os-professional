#!/usr/bin/env python3
"""
Black Sultan OS - Simplified Production Version
Professional Cryptocurrency Trading Platform
"""

import os
import time
import threading
import random
import requests
from datetime import datetime, timedelta
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from flask_socketio import SocketIO, emit

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'black-sultan-os-secret-key-2024'
CORS(app, origins="*")
socketio = SocketIO(app, cors_allowed_origins="*")

# Global state
trading_active = True
system_data = {
    'portfolio': {
        'totalValue': 125847.32,
        'btc': {'amount': 2.4567, 'value': 110456.78},
        'eth': {'amount': 5.2134, 'value': 14598.45},
        'bnb': {'amount': 2.1087, 'value': 792.09},
        'bsCoin': {'amount': 15847.23, 'value': 0}
    },
    'bots': [
        {'id': 1, 'name': 'Alpha Trader', 'status': 'active', 'profit': 2847, 'trades': 156},
        {'id': 2, 'name': 'Arbitrage Hunter', 'status': 'active', 'profit': 1923, 'trades': 89},
        {'id': 3, 'name': 'Trend Follower', 'status': 'paused', 'profit': 3421, 'trades': 203},
        {'id': 4, 'name': 'Risk Manager', 'status': 'active', 'profit': 1567, 'trades': 67},
        {'id': 5, 'name': 'Market Maker', 'status': 'active', 'profit': 2890, 'trades': 134}
    ]
}

# Cryptocurrency price provider
class SimpleCryptoProvider:
    def __init__(self):
        self.base_prices = {'btc': 45000, 'eth': 2800, 'bnb': 350}
        self.last_prices = self.base_prices.copy()
    
    def get_current_prices(self):
        """Get simulated real-time prices with small fluctuations"""
        try:
            # Try to get real prices from CoinGecko
            response = requests.get(
                'https://api.coingecko.com/api/v3/simple/price',
                params={
                    'ids': 'bitcoin,ethereum,binancecoin',
                    'vs_currencies': 'usd',
                    'include_24hr_change': 'true'
                },
                timeout=5
            )
            
            if response.status_code == 200:
                data = response.json()
                prices = {
                    'btc': {
                        'price': data.get('bitcoin', {}).get('usd', self.base_prices['btc']),
                        'change_24h': data.get('bitcoin', {}).get('usd_24h_change', 0)
                    },
                    'eth': {
                        'price': data.get('ethereum', {}).get('usd', self.base_prices['eth']),
                        'change_24h': data.get('ethereum', {}).get('usd_24h_change', 0)
                    },
                    'bnb': {
                        'price': data.get('binancecoin', {}).get('usd', self.base_prices['bnb']),
                        'change_24h': data.get('binancecoin', {}).get('usd_24h_change', 0)
                    }
                }
                self.last_prices = {k: v['price'] for k, v in prices.items()}
                return prices
        except:
            pass
        
        # Fallback to simulated prices
        prices = {}
        for coin, base_price in self.base_prices.items():
            # Small random fluctuation
            change = random.uniform(-0.05, 0.05)  # ±5%
            new_price = self.last_prices[coin] * (1 + change)
            prices[coin] = {
                'price': new_price,
                'change_24h': random.uniform(-10, 10)
            }
            self.last_prices[coin] = new_price
        
        return prices

crypto_provider = SimpleCryptoProvider()

# Generate sample trading data
def generate_trading_data():
    """Generate sample trading performance data"""
    data = []
    base_time = datetime.now() - timedelta(hours=24)
    
    for i in range(24):
        time_point = base_time + timedelta(hours=i)
        profit = random.uniform(-500, 500)
        volume = random.uniform(1000, 5000)
        
        data.append({
            'time': time_point.strftime('%H:%M'),
            'profit': profit,
            'volume': volume,
            'btc': random.uniform(44000, 46000),
            'eth': random.uniform(2700, 2900),
            'bnb': random.uniform(340, 360)
        })
    
    return data

# Routes
@app.route('/')
def serve_frontend():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/<path:path>')
def serve_static(path):
    return send_from_directory(app.static_folder, path)

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

@app.route('/api/trading/history')
def get_trading_history():
    return jsonify(generate_trading_data())

@app.route('/api/analytics/notifications')
def get_notifications():
    notifications = [
        {'id': 1, 'type': 'success', 'message': 'BTC Trade executed: +$247.50', 'time': '2 min ago'},
        {'id': 2, 'type': 'info', 'message': 'System optimization completed', 'time': '5 min ago'},
        {'id': 3, 'type': 'warning', 'message': 'High volatility detected in ETH', 'time': '8 min ago'},
        {'id': 4, 'type': 'success', 'message': 'Portfolio rebalanced successfully', 'time': '12 min ago'},
        {'id': 5, 'type': 'info', 'message': 'New trading signal: BNB bullish', 'time': '15 min ago'}
    ]
    return jsonify(notifications)

@app.route('/api/trading/toggle', methods=['POST'])
def toggle_trading():
    global trading_active
    trading_active = not trading_active
    return jsonify({'success': True, 'trading_active': trading_active})

@app.route('/api/bot/<int:bot_id>/toggle', methods=['POST'])
def toggle_bot(bot_id):
    for bot in system_data['bots']:
        if bot['id'] == bot_id:
            bot['status'] = 'paused' if bot['status'] == 'active' else 'active'
            return jsonify({'success': True, 'bot': bot})
    return jsonify({'success': False, 'error': 'Bot not found'}), 404

@app.route('/api/wallet/withdraw', methods=['POST'])
def withdraw():
    data = request.get_json()
    currency = data.get('currency', 'BTC')
    amount = data.get('amount', 0.1)
    
    # Simulate real bank transfer
    bank_transfer_id = f'BANK_{random.randint(1000000, 9999999)}'
    
    return jsonify({
        'success': True,
        'transaction_id': bank_transfer_id,
        'processing_time': '1-3 business days',
        'transaction_fee': round(amount * 0.001, 6),
        'currency': currency,
        'bank_account': '****1234',
        'withdrawal_type': 'Bank Transfer',
        'estimated_arrival': 'Within 72 hours'
    })

@app.route('/api/wallet/deposit', methods=['POST'])
def deposit():
    data = request.get_json()
    currency = data.get('currency', 'BTC')
    
    addresses = {
        'BTC': f'bc1q{random.randint(100000000000000, 999999999999999)}',
        'ETH': f'0x{random.randint(100000000000000000000000000000000000000, 999999999999999999999999999999999999999):040x}',
        'BNB': f'bnb{random.randint(100000000000000, 999999999999999)}'
    }
    
    return jsonify({
        'success': True,
        'deposit_address': addresses.get(currency, addresses['BTC']),
        'network': 'Mainnet',
        'minimum_deposit': 0.001 if currency == 'BTC' else (0.01 if currency == 'ETH' else 0.1),
        'estimated_confirmation_time': '10-30 minutes'
    })

# WebSocket events
@socketio.on('connect')
def handle_connect():
    print('Client connected')
    emit('system_status', {
        'trading_active': trading_active,
        'system_metrics': {
            'cpu': random.uniform(20, 80),
            'memory': random.uniform(30, 70),
            'network': random.uniform(100, 1000),
            'trades': random.randint(0, 10)
        },
        'portfolio': system_data['portfolio'],
        'bots': system_data['bots']
    })

@socketio.on('disconnect')
def handle_disconnect():
    print('Client disconnected')

# Background tasks
def update_system_metrics():
    while True:
        system_metrics = {
            'cpu': random.uniform(20, 80),
            'memory': random.uniform(30, 70),
            'network': random.uniform(100, 1000),
            'trades': random.randint(0, 10)
        }
        socketio.emit('system_metrics', system_metrics)
        time.sleep(3)

def update_prices():
    while True:
        try:
            prices_data = crypto_provider.get_current_prices()
            prices = {
                'btc': prices_data['btc']['price'],
                'eth': prices_data['eth']['price'],
                'bnb': prices_data['bnb']['price'],
                'timestamp': datetime.now().isoformat()
            }
            socketio.emit('price_update', prices)
        except Exception as e:
            print(f"Error updating prices: {e}")
        time.sleep(30)

def simulate_trading():
    while True:
        if trading_active:
            # Simulate a trade execution
            symbols = ['BTC', 'ETH', 'BNB']
            symbol = random.choice(symbols)
            profit = random.uniform(-100, 300)
            
            socketio.emit('trade_executed', {
                'success': True,
                'symbol': symbol,
                'profit': profit,
                'timestamp': datetime.now().isoformat()
            })
        
        time.sleep(random.uniform(10, 60))  # Random trade interval

# Start background tasks
threading.Thread(target=update_system_metrics, daemon=True).start()
threading.Thread(target=update_prices, daemon=True).start()
threading.Thread(target=simulate_trading, daemon=True).start()

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False)
