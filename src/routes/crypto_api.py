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
            
            coins_str = ','.join(coins)
            url = f"{self.coingecko_base}/simple/price"
            params = {
                'ids': coins_str,
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_24hr_vol': 'true',
                'include_market_cap': 'true'
            }
            
            response = requests.get(url, params=params, timeout=10)
            self.last_request_time = time.time()
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'btc': {
                        'price': data.get('bitcoin', {}).get('usd', 45000),
                        'change_24h': data.get('bitcoin', {}).get('usd_24h_change', 0),
                        'volume_24h': data.get('bitcoin', {}).get('usd_24h_vol', 0),
                        'market_cap': data.get('bitcoin', {}).get('usd_market_cap', 0)
                    },
                    'eth': {
                        'price': data.get('ethereum', {}).get('usd', 2800),
                        'change_24h': data.get('ethereum', {}).get('usd_24h_change', 0),
                        'volume_24h': data.get('ethereum', {}).get('usd_24h_vol', 0),
                        'market_cap': data.get('ethereum', {}).get('usd_market_cap', 0)
                    },
                    'bnb': {
                        'price': data.get('binancecoin', {}).get('usd', 350),
                        'change_24h': data.get('binancecoin', {}).get('usd_24h_change', 0),
                        'volume_24h': data.get('binancecoin', {}).get('usd_24h_vol', 0),
                        'market_cap': data.get('binancecoin', {}).get('usd_market_cap', 0)
                    }
                }
            else:
                print(f"CoinGecko API error: {response.status_code}")
                return self.get_fallback_prices()
                
        except Exception as e:
            print(f"Error fetching CoinGecko prices: {e}")
            return self.get_fallback_prices()
    
    def get_binance_prices(self):
        """Get current prices from Binance API (backup)"""
        try:
            symbols = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT']
            prices = {}
            
            for symbol in symbols:
                url = f"{self.binance_base}/ticker/24hr"
                params = {'symbol': symbol}
                
                response = requests.get(url, params=params, timeout=10)
                if response.status_code == 200:
                    data = response.json()
                    coin = symbol.replace('USDT', '').lower()
                    prices[coin] = {
                        'price': float(data.get('lastPrice', 0)),
                        'change_24h': float(data.get('priceChangePercent', 0)),
                        'volume_24h': float(data.get('volume', 0)),
                        'market_cap': 0  # Not available from Binance
                    }
                    
                time.sleep(0.1)  # Small delay between requests
                
            return prices
            
        except Exception as e:
            print(f"Error fetching Binance prices: {e}")
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
            url = f"{self.coingecko_base}/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': days,
                'interval': 'hourly' if days <= 7 else 'daily'
            }
            
            response = requests.get(url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                prices = data.get('prices', [])
                volumes = data.get('total_volumes', [])
                
                historical_data = []
                for i, (timestamp, price) in enumerate(prices):
                    volume = volumes[i][1] if i < len(volumes) else 0
                    historical_data.append({
                        'timestamp': timestamp,
                        'price': price,
                        'volume': volume,
                        'date': datetime.fromtimestamp(timestamp/1000).strftime('%Y-%m-%d %H:%M')
                    })
                
                return historical_data
            else:
                print(f"Historical data API error: {response.status_code}")
                return []
                
        except Exception as e:
            print(f"Error fetching historical data: {e}")
            return []

# Initialize crypto data provider
crypto_provider = CryptoDataProvider()

def update_price_cache():
    """Background task to update price cache"""
    global price_cache, cache_timestamp
    
    while True:
        try:
            # Try CoinGecko first, fallback to Binance
            prices = crypto_provider.get_coingecko_prices()
            if not prices or all(p['price'] == 0 for p in prices.values()):
                prices = crypto_provider.get_binance_prices()
            
            price_cache = prices
            cache_timestamp = time.time()
            
            print(f"Updated price cache at {datetime.now()}")
            
        except Exception as e:
            print(f"Error updating price cache: {e}")
        
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
        prices = crypto_provider.get_coingecko_prices()
        price_cache = prices
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
    coin_map = {
        'btc': 'bitcoin',
        'eth': 'ethereum', 
        'bnb': 'binancecoin'
    }
    
    coin_id = coin_map.get(coin.lower())
    if not coin_id:
        return jsonify({'success': False, 'error': 'Invalid coin symbol'}), 400
    
    days = request.args.get('days', 7, type=int)
    historical_data = crypto_provider.get_historical_data(coin_id, days)
    
    return jsonify({
        'success': True,
        'coin': coin.upper(),
        'days': days,
        'data': historical_data,
        'timestamp': datetime.now().isoformat()
    })

@crypto_api_bp.route('/market/summary')
def get_market_summary():
    """Get overall market summary"""
    try:
        url = f"{crypto_provider.coingecko_base}/global"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json().get('data', {})
            return jsonify({
                'success': True,
                'data': {
                    'total_market_cap_usd': data.get('total_market_cap', {}).get('usd', 0),
                    'total_volume_24h_usd': data.get('total_volume', {}).get('usd', 0),
                    'bitcoin_dominance': data.get('market_cap_percentage', {}).get('btc', 0),
                    'active_cryptocurrencies': data.get('active_cryptocurrencies', 0),
                    'markets': data.get('markets', 0),
                    'market_cap_change_24h': data.get('market_cap_change_percentage_24h_usd', 0)
                },
                'timestamp': datetime.now().isoformat()
            })
        else:
            return jsonify({'success': False, 'error': 'Market data unavailable'}), 503
            
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@crypto_api_bp.route('/trading/signals/<coin>')
def get_trading_signals(coin):
    """Generate basic trading signals based on price data"""
    try:
        coin_map = {
            'btc': 'bitcoin',
            'eth': 'ethereum', 
            'bnb': 'binancecoin'
        }
        
        coin_id = coin_map.get(coin.lower())
        if not coin_id:
            return jsonify({'success': False, 'error': 'Invalid coin symbol'}), 400
        
        # Get recent price data
        historical_data = crypto_provider.get_historical_data(coin_id, 7)
        if len(historical_data) < 20:
            return jsonify({'success': False, 'error': 'Insufficient data for analysis'}), 400
        
        prices = [item['price'] for item in historical_data[-20:]]
        
        # Simple moving averages
        sma_5 = sum(prices[-5:]) / 5
        sma_10 = sum(prices[-10:]) / 10
        sma_20 = sum(prices) / len(prices)
        
        current_price = prices[-1]
        
        # Generate signals
        signals = []
        if sma_5 > sma_10 > sma_20:
            signals.append({'type': 'BUY', 'strength': 'STRONG', 'reason': 'Bullish trend - all MAs aligned'})
        elif sma_5 > sma_10:
            signals.append({'type': 'BUY', 'strength': 'WEAK', 'reason': 'Short-term bullish'})
        elif sma_5 < sma_10 < sma_20:
            signals.append({'type': 'SELL', 'strength': 'STRONG', 'reason': 'Bearish trend - all MAs aligned'})
        elif sma_5 < sma_10:
            signals.append({'type': 'SELL', 'strength': 'WEAK', 'reason': 'Short-term bearish'})
        else:
            signals.append({'type': 'HOLD', 'strength': 'NEUTRAL', 'reason': 'Sideways movement'})
        
        # Volatility analysis
        price_changes = [abs(prices[i] - prices[i-1]) / prices[i-1] for i in range(1, len(prices))]
        avg_volatility = sum(price_changes) / len(price_changes)
        
        return jsonify({
            'success': True,
            'coin': coin.upper(),
            'current_price': current_price,
            'analysis': {
                'sma_5': sma_5,
                'sma_10': sma_10,
                'sma_20': sma_20,
                'volatility': avg_volatility * 100,
                'trend': 'BULLISH' if sma_5 > sma_20 else 'BEARISH' if sma_5 < sma_20 else 'NEUTRAL'
            },
            'signals': signals,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
