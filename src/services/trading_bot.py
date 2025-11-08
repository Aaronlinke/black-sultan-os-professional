"""Trading bot implementation with real trading logic."""
import random
from datetime import datetime
from typing import Dict, Optional


class TradingBot:
    """Enhanced Bot Management with Real Trading Logic."""
    
    def __init__(self, bot_id: str, name: str, strategy: str, initial_balance: float):
        """
        Initialize a trading bot.
        
        Args:
            bot_id: Unique identifier for the bot
            name: Display name for the bot
            strategy: Trading strategy (e.g., 'high_frequency', 'arbitrage')
            initial_balance: Starting balance in USD
        """
        self.bot_id = bot_id
        self.name = name
        self.strategy = strategy
        self.balance = initial_balance
        self.is_active = True
        self.trades_today = 0
        self.profit_today = 0.0
        self.total_trades = 0
        self.success_rate = 0.87  # 87% success rate
        self.last_trade_time = None
        self.risk_level = "moderate"
        
    def execute_trade(self, market_data: Dict, game_state=None) -> Optional[Dict]:
        """
        Execute a trade based on strategy and market conditions.
        
        Args:
            market_data: Current market data including prices and volatility
            game_state: Reference to the global game state
            
        Returns:
            Dict containing trade result or None if trade wasn't executed
        """
        if not self.is_active:
            return None
            
        # Simulate trading logic based on strategy
        trade_amount = min(self.balance * 0.01, 100)  # Max 1% of balance or $100
        
        # Calculate success based on market conditions and strategy
        market_volatility = market_data.get('volatility', 0.5)
        success_probability = self.success_rate * (1 - market_volatility * 0.3)
        
        is_successful = random.random() < success_probability
        
        if is_successful:
            profit = trade_amount * random.uniform(0.02, 0.08)  # 2-8% profit
            self.balance += profit
            self.profit_today += profit
            if game_state:
                game_state.add_profit(profit)
        else:
            loss = trade_amount * random.uniform(0.01, 0.05)  # 1-5% loss
            self.balance -= loss
            self.profit_today -= loss
            if game_state:
                game_state.add_profit(-loss)
        
        self.trades_today += 1
        self.total_trades += 1
        self.last_trade_time = datetime.now()
        
        trade_result = {
            'bot_id': self.bot_id,
            'timestamp': self.last_trade_time.isoformat(),
            'amount': trade_amount,
            'profit': profit if is_successful else -loss,
            'successful': is_successful,
            'new_balance': self.balance
        }
        
        # Add XP for successful trades
        if is_successful and game_state:
            game_state.add_xp(10)
        
        return trade_result
