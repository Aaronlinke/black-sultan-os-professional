"""
Market Templates Module
Provides pre-configured templates for different trading markets and strategies
"""

from .american_market import AmericanMarketTemplate
from .trading_strategies import TradingStrategyTemplates

__all__ = ['AmericanMarketTemplate', 'TradingStrategyTemplates']
