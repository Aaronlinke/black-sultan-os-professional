import requests
import time
from datetime import datetime, timedelta
from flask import Blueprint, jsonify
import threading
import json

crypto_api_bp = Blueprint('crypto_api', __name__)

# Global variables for caching
price_cache = {}
cache_timestamp = 0
CACHE_DURATION = 30  # seconds

class CryptoDataProvider:
    def __init__(self):
        self.coingecko_base = "https://api.coingecko.com/api/v3"
        self.binance_base = "https://api.binance.com/api/v3"
        self.last_request_time = 0
        self.rate_limit_delay = 1  # seconds between requests
        
    def get_coingecko_prices(self, coins=['bitcoin', 'ethereum', 'binancecoin']):
        """Get current prices from CoinGecko API (free tier)"""
        try:
            # Rate limiting
            current_time = time.time()
            if current_time - self.last_request_time < self.rate_limit_delay:
                time.sleep(self.rate_limit_delay)
            
            comma_separated_coins = ','.join(coins)
            api_endpoint_url = f"{self.coingecko_base}/simple/price"
            api_request_params = {
                'ids': comma_separated_coins,
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_24hr_vol': 'true',
                'include_market_cap': 'true'
            }
            
            api_response = requests.get(api_endpoint_url, params=api_request_params, timeout=10)
            self.last_request_time = time.time()
            
            if api_response.status_code == 200:
                price_data = api_response.json()
                return {
                    'btc': {
                        'price': price_data.get('bitcoin', {}).get('usd', 45000),
                        'change_24h': price_data.get('bitcoin', {}).get('usd_24h_change', 0),
                        'volume_24h': price_data.get('bitcoin', {}).get('usd_24h_vol', 0),
                        'market_cap': price_data.get('bitcoin', {}).get('usd_market_cap', 0)
                    },
                    'eth': {
                        'price': price_data.get('ethereum', {}).get('usd', 2800),
                        'change_24h': price_data.get('ethereum', {}).get('usd_24h_change', 0),
                        'volume_24h': price_data.get('ethereum', {}).get('usd_24h_vol', 0),
                        'market_cap': price_data.get('ethereum', {}).get('usd_market_cap', 0)
                    },
                    'bnb': {
                        'price': price_data.get('binancecoin', {}).get('usd', 350),
                        'change_24h': price_data.get('binancecoin', {}).get('usd_24h_change', 0),
                        'volume_24h': price_data.get('binancecoin', {}).get('usd_24h_vol', 0),
                        'market_cap': price_data.get('binancecoin', {}).get('usd_market_cap', 0)
                    }
                }
            else:
                print(f"CoinGecko API error: {api_response.status_code}")
                return self.get_fallback_prices()
                
        except Exception as api_error:
            print(f"Error fetching CoinGecko prices: {api_error}")
            return self.get_fallback_prices()
    
    def get_binance_prices(self):
        """Get current prices from Binance API (backup)"""
        try:
            trading_pair_symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
            cryptocurrency_prices = {}
            
            for trading_pair_symbol in trading_pair_symbols:
                api_endpoint_url = f"{self.binance_base}/ticker/24hr"
                ticker_params = {'symbol': trading_pair_symbol}
                
                ticker_response = requests.get(api_endpoint_url, params=ticker_params, timeout=10)
                if ticker_response.status_code == 200:
                    ticker_data = ticker_response.json()
                    coin_symbol = trading_pair_symbol.replace('USDT', '').lower()
                    cryptocurrency_prices[coin_symbol] = {
                        'price': float(ticker_data.get('lastPrice', 0)),
                        'change_24h': float(ticker_data.get('priceChangePercent', 0)),
                        'volume_24h': float(ticker_data.get('volume', 0)),
                        'market_cap': 0  # Not available from Binance
                    }
                    
                time.sleep(0.1)  # Small delay between requests
                
            return cryptocurrency_prices
            
        except Exception as api_error:
            print(f"Error fetching Binance prices: {api_error}")
            return self.get_fallback_prices()
    
    def get_fallback_prices(self):
        """Fallback prices when APIs are unavailable"""
        return {
            'btc': {'price': 45000, 'change_24h': 2.5, 'volume_24h': 25000000000, 'market_cap': 880000000000},
            'eth': {'price': 2800, 'change_24h': 1.8, 'volume_24h': 15000000000, 'market_cap': 340000000000},
            'bnb': {'price': 350, 'change_24h': -0.5, 'volume_24h': 2000000000, 'market_cap': 52000000000}
        }
    
    def get_historical_data(self, coin_id, days=7):
        """Get historical price data from CoinGecko"""
        try:
            market_chart_url = f"{self.coingecko_base}/coins/{coin_id}/market_chart"
            chart_request_params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'hourly' if days <= 7 else 'daily'
            }
            
            chart_response = requests.get(market_chart_url, params=chart_request_params, timeout=15)
            if chart_response.status_code == 200:
                chart_data = chart_response.json()
                historical_prices = chart_data.get('prices', [])
                historical_volumes = chart_data.get('total_volumes', [])
                
                formatted_historical_data = []
                for index, (price_timestamp, price_value) in enumerate(historical_prices):
                    volume_value = historical_volumes[index][1] if index < len(historical_volumes) else 0
                    formatted_historical_data.append({
                        'timestamp': price_timestamp,
                        'price': price_value,
                        'volume': volume_value,
                        'date': datetime.fromtimestamp(price_timestamp/1000).strftime('%Y-%m-%d %H:%M')
                    })
                
                return formatted_historical_data
            else:
                print(f"Historical data API error: {chart_response.status_code}")
                return []
                
        except Exception as api_error:
            print(f"Error fetching historical data: {api_error}")
            return []

# Initialize crypto data provider
crypto_provider = CryptoDataProvider()

def update_price_cache():
    """Background task to update price cache"""
    global price_cache, cache_timestamp
    
    while True:
        try:
            # Try CoinGecko first, fallback to Binance
            fetched_prices = crypto_provider.get_coingecko_prices()
            if not fetched_prices or all(coin_data['price'] == 0 for coin_data in fetched_prices.values()):
                fetched_prices = crypto_provider.get_binance_prices()
            
            price_cache = fetched_prices
            cache_timestamp = time.time()
            
            print(f"Updated price cache at {datetime.now()}")
            
        except Exception as cache_update_error:
            print(f"Error updating price cache: {cache_update_error}")
        
        time.sleep(CACHE_DURATION)

# Start background price update thread
threading.Thread(target=update_price_cache, daemon=True).start()

@crypto_api_bp.route('/prices/current')
def get_current_prices():
    """Get current cryptocurrency prices"""
    global price_cache, cache_timestamp
    
    # Check if cache is fresh
    if time.time() - cache_timestamp > CACHE_DURATION or not price_cache:
        # Force update if cache is stale
        refreshed_prices = crypto_provider.get_coingecko_prices()
        price_cache = refreshed_prices
        cache_timestamp = time.time()
    
    return jsonify({
        'success': True,
        'data': price_cache,
        'timestamp': datetime.now().isoformat(),
        'cache_age': time.time() - cache_timestamp
    })

@crypto_api_bp.route('/prices/historical/<coin>')
def get_historical_prices(coin):
    """Get historical price data for a specific coin"""
    coin_symbol_to_id_map = {
        'btc': 'bitcoin',
        'eth': 'ethereum', 
        'bnb': 'binancecoin'
    }
    
    coingecko_coin_id = coin_symbol_to_id_map.get(coin.lower())
    if not coingecko_coin_id:
        return jsonify({'success': False, 'error': 'Invalid coin symbol'}), 400
    
    requested_days = request.args.get('days', 7, type=int)
    historical_price_data = crypto_provider.get_historical_data(coingecko_coin_id, requested_days)
    
    return jsonify({
        'success': True,
        'coin': coin.upper(),
        'days': requested_days,
        'data': historical_price_data,
        'timestamp': datetime.now().isoformat()
    })

@crypto_api_bp.route('/market/summary')
def get_market_summary():
    """Get overall market summary"""
    try:
        global_market_url = f"{crypto_provider.coingecko_base}/global"
        market_response = requests.get(global_market_url, timeout=10)
        
        if market_response.status_code == 200:
            global_market_data = market_response.json().get('data', {})
            return jsonify({
                'success': True,
                'data': {
                    'total_market_cap_usd': global_market_data.get('total_market_cap', {}).get('usd', 0),
                    'total_volume_24h_usd': global_market_data.get('total_volume', {}).get('usd', 0),
                    'bitcoin_dominance': global_market_data.get('market_cap_percentage', {}).get('btc', 0),
                    'active_cryptocurrencies': global_market_data.get('active_cryptocurrencies', 0),
                    'markets': global_market_data.get('markets', 0),
                    'market_cap_change_24h': global_market_data.get('market_cap_change_percentage_24h_usd', 0)
                },
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'success': False, 'error': 'Market data unavailable'}), 503
            
    except Exception as market_summary_error:
        return jsonify({'success': False, 'error': str(market_summary_error)}), 500

@crypto_api_bp.route('/trading/signals/<coin>')
def get_trading_signals(coin):
    """Generate basic trading signals based on price data"""
    try:
        coin_symbol_to_id_map = {
            'btc': 'bitcoin',
            'eth': 'ethereum', 
            'bnb': 'binancecoin'
        }
        
        coingecko_coin_id = coin_symbol_to_id_map.get(coin.lower())
        if not coingecko_coin_id:
            return jsonify({'success': False, 'error': 'Invalid coin symbol'}), 400
        
        # Get recent price data
        historical_price_data = crypto_provider.get_historical_data(coingecko_coin_id, 7)
        if len(historical_price_data) < 20:
            return jsonify({'success': False, 'error': 'Insufficient data for analysis'}), 400
        
        recent_prices = [data_point['price'] for data_point in historical_price_data[-20:]]
        
        # Simple moving averages
        simple_moving_average_5 = sum(recent_prices[-5:]) / 5
        simple_moving_average_10 = sum(recent_prices[-10:]) / 10
        simple_moving_average_20 = sum(recent_prices) / len(recent_prices)
        
        latest_price = recent_prices[-1]
        
        # Generate signals
        trading_signals = []
        if simple_moving_average_5 > simple_moving_average_10 > simple_moving_average_20:
            trading_signals.append({'type': 'BUY', 'strength': 'STRONG', 'reason': 'Bullish trend - all MAs aligned'})
        elif simple_moving_average_5 > simple_moving_average_10:
            trading_signals.append({'type': 'BUY', 'strength': 'WEAK', 'reason': 'Short-term bullish'})
        elif simple_moving_average_5 < simple_moving_average_10 < simple_moving_average_20:
            trading_signals.append({'type': 'SELL', 'strength': 'STRONG', 'reason': 'Bearish trend - all MAs aligned'})
        elif simple_moving_average_5 < simple_moving_average_10:
            trading_signals.append({'type': 'SELL', 'strength': 'WEAK', 'reason': 'Short-term bearish'})
        else:
            trading_signals.append({'type': 'HOLD', 'strength': 'NEUTRAL', 'reason': 'Sideways movement'})
        
        # Volatility analysis
        percentage_price_changes = [abs(recent_prices[i] - recent_prices[i-1]) / recent_prices[i-1] for i in range(1, len(recent_prices))]
        average_volatility = sum(percentage_price_changes) / len(percentage_price_changes)
        
        return jsonify({
            'success': True,
            'coin': coin.upper(),
            'current_price': latest_price,
            'analysis': {
                'sma_5': simple_moving_average_5,
                'sma_10': simple_moving_average_10,
                'sma_20': simple_moving_average_20,
                'volatility': average_volatility * 100,
                'trend': 'BULLISH' if simple_moving_average_5 > simple_moving_average_20 else 'BEARISH' if simple_moving_average_5 < simple_moving_average_20 else 'NEUTRAL'
            },
            'signals': trading_signals,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as trading_signal_error:
        return jsonify({'success': False, 'error': str(trading_signal_error)}), 500
