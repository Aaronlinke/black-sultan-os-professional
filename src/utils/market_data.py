"""Market data utilities for cryptocurrency prices."""
import random
from typing import Dict


def get_market_data() -> Dict:
    """
    Get current market data with realistic fluctuations.
    
    Returns:
        Dict containing price data for BTC, ETH, and BNB
    """
    base_prices = {'BTC': 67000, 'ETH': 2650, 'BNB': 580}
    current_prices = {}
    
    for symbol, base_price in base_prices.items():
        # Add realistic price fluctuation
        fluctuation = random.uniform(-0.05, 0.05)  # ±5%
        current_price = base_price * (1 + fluctuation)
        
        # Calculate 24h change
        change_24h = random.uniform(-0.08, 0.08)  # ±8%
        
        current_prices[symbol] = {
            'price': round(current_price, 2),
            'change_24h': round(change_24h * 100, 2),
            'volume_24h': random.randint(1000000, 5000000),
            'volatility': abs(change_24h)
        }
    
    return current_prices
