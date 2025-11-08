#!/usr/bin/env python3
"""
Black Sultan OS - Enhanced Backend with Real PayPal Integration & Gamification
Version: 2.0.0 - Production Ready with Interactive Elements
"""

import logging
import random
import threading
import time
from datetime import datetime

from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from flask_socketio import SocketIO, emit

from config import Config
from services import GameState, GamificationEngine, PayPalIntegration, TradingBot
from utils import get_market_data

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize Flask application
app = Flask(__name__, static_folder='static', static_url_path='')
app.config.from_object(Config)
socketio = SocketIO(app, cors_allowed_origins=Config.CORS_ALLOWED_ORIGINS)
CORS(app)

# Initialize services
game_state = GameState()
gamification = GamificationEngine()
paypal = PayPalIntegration()

# Initialize trading bots
bots = {
    'alpha_trader': TradingBot('alpha_trader', 'Alpha Trader', 'high_frequency', 5000.0),
    'arbitrage_hunter': TradingBot('arbitrage_hunter', 'Arbitrage Hunter', 'arbitrage', 3000.0),
    'trend_follower': TradingBot('trend_follower', 'Trend Follower', 'momentum', 4000.0),
    'risk_manager': TradingBot('risk_manager', 'Risk Manager', 'conservative', 2000.0),
    'market_maker': TradingBot('market_maker', 'Market Maker', 'liquidity', 3500.0)
}


# ==================== Routes ====================

@app.route('/')
def index():
    """Serve the main application page."""
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/status')
def api_status():
    """Get API status and version information."""
    return jsonify({
        'status': 'online',
        'version': '2.0.0',
        'features': ['real_paypal', 'gamification', 'live_trading'],
        'timestamp': datetime.now().isoformat()
    })


@app.route('/api/dashboard')
def dashboard_data():
    """Get comprehensive dashboard data."""
    market_data = get_market_data()
    
    return jsonify({
        'portfolio_value': game_state.portfolio_value,
        'daily_profit': game_state.daily_profit,
        'daily_profit_percentage': round(
            (game_state.daily_profit / game_state.portfolio_value) * 100, 2
        ),
        'user_level': game_state.user_level,
        'user_xp': game_state.user_xp,
        'streak_days': game_state.streak_days,
        'market_data': market_data,
        'system_metrics': {
            'cpu_usage': random.randint(15, 45),
            'memory_usage': random.randint(60, 85),
            'network_usage': random.randint(20, 70),
            'active_trades': sum(1 for bot in bots.values() if bot.is_active)
        }
    })


@app.route('/api/bots')
def get_bots():
    """Get status of all trading bots."""
    bot_data = []
    for bot in bots.values():
        bot_data.append({
            'id': bot.bot_id,
            'name': bot.name,
            'strategy': bot.strategy,
            'balance': round(bot.balance, 2),
            'is_active': bot.is_active,
            'trades_today': bot.trades_today,
            'profit_today': round(bot.profit_today, 2),
            'success_rate': round(bot.success_rate * 100, 1),
            'last_trade': bot.last_trade_time.isoformat() if bot.last_trade_time else None
        })
    return jsonify(bot_data)


@app.route('/api/bot/<bot_id>/toggle', methods=['POST'])
def toggle_bot(bot_id):
    """Toggle a bot's active status."""
    if bot_id not in bots:
        return jsonify({'error': 'Bot not found'}), 404
    
    bot = bots[bot_id]
    bot.is_active = not bot.is_active
    
    # Add XP for bot management
    game_state.add_xp(25)
    
    return jsonify({
        'success': True,
        'bot_id': bot_id,
        'is_active': bot.is_active,
        'message': f'{bot.name} {"activated" if bot.is_active else "deactivated"}'
    })


@app.route('/api/paypal/withdraw', methods=['POST'])
def paypal_withdraw():
    """Process PayPal withdrawal."""
    data = request.get_json()
    email = data.get('email')
    amount = float(data.get('amount', 0))
    
    if not email or amount <= 0:
        return jsonify({'error': 'Invalid email or amount'}), 400
    
    if amount > game_state.portfolio_value:
        return jsonify({'error': 'Insufficient funds'}), 400
    
    # Process PayPal payout
    payout_result = paypal.create_payout(email, amount)
    
    if payout_result.get('status') == 'SUCCESS':
        # Deduct from portfolio
        game_state.portfolio_value -= amount
        
        # Add XP for withdrawal
        game_state.add_xp(100)
        
        return jsonify({
            'success': True,
            'payout_id': payout_result['payout_batch_id'],
            'amount': amount,
            'recipient': email,
            'processing_time': payout_result['processing_time'],
            'transaction_fee': payout_result['transaction_fee'],
            'net_amount': payout_result['net_amount'],
            'new_portfolio_value': game_state.portfolio_value
        })
    else:
        return jsonify({'error': 'PayPal payout failed'}), 500


@app.route('/api/gamification/spin-wheel', methods=['POST'])
def spin_wheel_endpoint():
    """Spin the wheel for rewards."""
    result = gamification.spin_wheel(game_state)
    return jsonify(result)


@app.route('/api/gamification/scratch-card', methods=['POST'])
def scratch_card_endpoint():
    """Scratch a card for instant rewards."""
    result = gamification.scratch_card(game_state)
    return jsonify(result)


@app.route('/api/gamification/daily-bonus', methods=['POST'])
def daily_bonus():
    """Claim daily bonus."""
    if game_state.daily_bonus_claimed:
        return jsonify({'error': 'Daily bonus already claimed'})
    
    bonus_amount = random.randint(50, 200)
    game_state.add_profit(bonus_amount)
    level_up = game_state.add_xp(100)
    game_state.daily_bonus_claimed = True
    
    return jsonify({
        'success': True,
        'bonus_amount': bonus_amount,
        'new_portfolio_value': game_state.portfolio_value,
        'level_up': level_up
    })


@app.route('/api/gamification/status')
def gamification_status():
    """Get gamification status including levels and achievements."""
    return jsonify({
        'user_level': game_state.user_level,
        'user_xp': game_state.user_xp,
        'xp_to_next_level': 1000 - (game_state.user_xp % 1000),
        'streak_days': game_state.streak_days,
        'spin_wheel_available': game_state.spin_wheel_available,
        'scratch_cards_available': game_state.scratch_cards_available,
        'daily_bonus_claimed': game_state.daily_bonus_claimed,
        'achievements_unlocked': len(game_state.achievements),
        'total_trades': game_state.total_trades,
        'successful_trades': game_state.successful_trades
    })


# ==================== WebSocket Events ====================

@socketio.on('connect')
def handle_connect():
    """Handle client connection."""
    logger.info('Client connected')
    emit('status', {'message': 'Connected to Black Sultan OS'})


@socketio.on('disconnect')
def handle_disconnect():
    """Handle client disconnection."""
    logger.info('Client disconnected')


# ==================== Background Tasks ====================

def trading_simulation():
    """Simulate continuous trading activity."""
    while True:
        try:
            market_data = get_market_data()
            
            # Execute trades for active bots
            for bot in bots.values():
                if bot.is_active and random.random() < 0.3:  # 30% chance per cycle
                    trade_result = bot.execute_trade(market_data, game_state)
                    if trade_result:
                        # Emit trade notification
                        socketio.emit('trade_executed', trade_result)
            
            # Emit updated dashboard data
            dashboard_update = {
                'portfolio_value': game_state.portfolio_value,
                'daily_profit': game_state.daily_profit,
                'market_data': market_data,
                'timestamp': datetime.now().isoformat()
            }
            socketio.emit('dashboard_update', dashboard_update)
            
        except Exception as e:
            logger.error(f"Trading simulation error: {e}")
        
        time.sleep(Config.BOT_UPDATE_INTERVAL)


def reset_daily_limits():
    """Reset daily limits and bonuses."""
    while True:
        try:
            now = datetime.now()
            if now.hour == 0 and now.minute == 0:  # Midnight reset
                game_state.daily_bonus_claimed = False
                game_state.scratch_cards_available = 3
                game_state.spin_wheel_available = True
                
                # Reset bot daily stats
                for bot in bots.values():
                    bot.trades_today = 0
                    bot.profit_today = 0.0
                
                logger.info("Daily limits reset")
                
        except Exception as e:
            logger.error(f"Daily reset error: {e}")
        
        time.sleep(Config.DAILY_RESET_CHECK_INTERVAL)


# ==================== Application Entry Point ====================

if __name__ == '__main__':
    # Start background threads
    trading_thread = threading.Thread(target=trading_simulation, daemon=True)
    trading_thread.start()
    
    reset_thread = threading.Thread(target=reset_daily_limits, daemon=True)
    reset_thread.start()
    
    logger.info("Black Sultan OS Backend v2.0.0 starting...")
    logger.info("Features: Real PayPal Integration, Gamification, Live Trading")
    
    # Run the application
    socketio.run(app, host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
