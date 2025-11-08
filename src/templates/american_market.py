"""
American Market Template
Provides configurations and settings specific to US trading markets
"""

from datetime import time, datetime
from typing import Dict, List, Optional
import pytz


class AmericanMarketTemplate:
    """Template for American (US) market trading configurations"""
    
    def __init__(self):
        self.timezone = pytz.timezone('America/New_York')
        self.market_hours = {
            'pre_market': {'start': time(4, 0), 'end': time(9, 30)},
            'regular': {'start': time(9, 30), 'end': time(16, 0)},
            'after_hours': {'start': time(16, 0), 'end': time(20, 0)}
        }
        self.trading_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
        
    def is_market_open(self, check_time: Optional[datetime] = None) -> Dict:
        """Check if American market is currently open"""
        if check_time is None:
            check_time = datetime.now(self.timezone)
        
        # Convert to NY time if not already
        if check_time.tzinfo is None:
            check_time = self.timezone.localize(check_time)
        else:
            check_time = check_time.astimezone(self.timezone)
        
        day_name = check_time.strftime('%A')
        current_time = check_time.time()
        
        # Check if it's a trading day
        if day_name not in self.trading_days:
            return {
                'is_open': False,
                'session': 'closed',
                'reason': 'Weekend',
                'next_open': self._get_next_market_open(check_time)
            }
        
        # Check market sessions
        if self.market_hours['pre_market']['start'] <= current_time < self.market_hours['pre_market']['end']:
            return {
                'is_open': True,
                'session': 'pre_market',
                'reason': 'Pre-market trading hours',
                'closes_at': self.market_hours['pre_market']['end'].strftime('%H:%M')
            }
        elif self.market_hours['regular']['start'] <= current_time < self.market_hours['regular']['end']:
            return {
                'is_open': True,
                'session': 'regular',
                'reason': 'Regular trading hours',
                'closes_at': self.market_hours['regular']['end'].strftime('%H:%M')
            }
        elif self.market_hours['after_hours']['start'] <= current_time < self.market_hours['after_hours']['end']:
            return {
                'is_open': True,
                'session': 'after_hours',
                'reason': 'After-hours trading',
                'closes_at': self.market_hours['after_hours']['end'].strftime('%H:%M')
            }
        else:
            return {
                'is_open': False,
                'session': 'closed',
                'reason': 'Outside trading hours',
                'next_open': self._get_next_market_open(check_time)
            }
    
    def _get_next_market_open(self, current_time: datetime) -> str:
        """Calculate next market opening time"""
        # Simplified - returns next trading day at market open
        return "Next trading day at 09:30 ET"
    
    def get_market_config(self) -> Dict:
        """Get complete American market configuration"""
        return {
            'name': 'American Market',
            'region': 'United States',
            'timezone': 'America/New_York',
            'currency': 'USD',
            'market_hours': {
                'pre_market': '04:00-09:30 ET',
                'regular': '09:30-16:00 ET',
                'after_hours': '16:00-20:00 ET'
            },
            'trading_days': self.trading_days,
            'holidays': self._get_us_market_holidays(),
            'supported_assets': [
                'US Stocks (NYSE, NASDAQ)',
                'US Stock Options',
                'US Stock Futures',
                'Cryptocurrency (24/7)'
            ],
            'regulations': {
                'day_trading_rules': 'Pattern Day Trader (PDT) rules apply',
                'minimum_account': '$25,000 for day trading',
                'settlement': 'T+2 for stocks'
            }
        }
    
    def _get_us_market_holidays(self) -> List[str]:
        """Get list of US market holidays"""
        return [
            'New Year\'s Day',
            'Martin Luther King Jr. Day',
            'Presidents\' Day',
            'Good Friday',
            'Memorial Day',
            'Independence Day',
            'Labor Day',
            'Thanksgiving Day',
            'Christmas Day'
        ]
    
    def get_bot_template(self, strategy_type: str = 'conservative') -> Dict:
        """Get American market bot configuration template"""
        templates = {
            'conservative': {
                'name': 'American Conservative Bot',
                'description': 'Low-risk trading during US market hours',
                'trading_hours': 'Regular market hours only (09:30-16:00 ET)',
                'risk_level': 'low',
                'max_trade_size': 0.02,  # 2% of portfolio
                'max_daily_trades': 5,
                'target_assets': ['US Large Cap Stocks', 'Blue Chip Stocks'],
                'strategies': ['Buy and hold', 'Dividend investing', 'Value investing']
            },
            'aggressive': {
                'name': 'American Day Trader Bot',
                'description': 'Active day trading in US markets',
                'trading_hours': 'All sessions (04:00-20:00 ET)',
                'risk_level': 'high',
                'max_trade_size': 0.10,  # 10% of portfolio
                'max_daily_trades': 50,
                'target_assets': ['US Tech Stocks', 'Volatile Small Caps', 'Options'],
                'strategies': ['Scalping', 'Momentum trading', 'Breakout trading']
            },
            'balanced': {
                'name': 'American Balanced Bot',
                'description': 'Balanced approach for US markets',
                'trading_hours': 'Regular + pre-market (04:00-16:00 ET)',
                'risk_level': 'moderate',
                'max_trade_size': 0.05,  # 5% of portfolio
                'max_daily_trades': 15,
                'target_assets': ['US Mid Cap Stocks', 'ETFs', 'Index Funds'],
                'strategies': ['Swing trading', 'Trend following', 'Mean reversion']
            }
        }
        
        return templates.get(strategy_type, templates['balanced'])
    
    def get_cryptocurrency_template(self) -> Dict:
        """Get American-focused cryptocurrency trading template"""
        return {
            'name': 'American Crypto Trader',
            'description': 'Cryptocurrency trading with US compliance',
            'trading_hours': '24/7 (cryptocurrency markets)',
            'timezone_preference': 'America/New_York',
            'active_hours': '09:00-17:00 ET (align with US business hours)',
            'supported_exchanges': [
                'Coinbase (US-based)',
                'Kraken (US-regulated)',
                'Gemini (US-regulated)'
            ],
            'compliance': {
                'kyc_required': True,
                'tax_reporting': '1099-K for transactions over $600',
                'regulations': 'SEC and CFTC guidelines apply'
            },
            'popular_pairs': [
                'BTC/USD',
                'ETH/USD',
                'SOL/USD',
                'AVAX/USD'
            ],
            'risk_management': {
                'stop_loss': 0.05,  # 5%
                'take_profit': 0.15,  # 15%
                'max_position_size': 0.20  # 20% of portfolio
            }
        }
