"""
Trading Strategy Templates
Provides pre-configured trading strategy templates for various approaches
"""

from typing import Dict, List
from enum import Enum


class StrategyType(Enum):
    """Enumeration of available strategy types"""
    SCALPING = "scalping"
    DAY_TRADING = "day_trading"
    SWING_TRADING = "swing_trading"
    POSITION_TRADING = "position_trading"
    ARBITRAGE = "arbitrage"
    MOMENTUM = "momentum"
    MEAN_REVERSION = "mean_reversion"
    BREAKOUT = "breakout"


class TradingStrategyTemplates:
    """Collection of trading strategy templates"""
    
    @staticmethod
    def get_all_strategies() -> List[str]:
        """Get list of all available strategy templates"""
        return [strategy.value for strategy in StrategyType]
    
    @staticmethod
    def get_strategy(strategy_name: str) -> Dict:
        """Get a specific strategy template by name"""
        strategies = {
            'scalping': TradingStrategyTemplates._scalping_strategy(),
            'day_trading': TradingStrategyTemplates._day_trading_strategy(),
            'swing_trading': TradingStrategyTemplates._swing_trading_strategy(),
            'position_trading': TradingStrategyTemplates._position_trading_strategy(),
            'arbitrage': TradingStrategyTemplates._arbitrage_strategy(),
            'momentum': TradingStrategyTemplates._momentum_strategy(),
            'mean_reversion': TradingStrategyTemplates._mean_reversion_strategy(),
            'breakout': TradingStrategyTemplates._breakout_strategy()
        }
        
        return strategies.get(strategy_name, strategies['day_trading'])
    
    @staticmethod
    def _scalping_strategy() -> Dict:
        """Ultra-short-term trading strategy"""
        return {
            'name': 'Scalping Strategy',
            'description': 'Quick trades to capture small price movements',
            'timeframe': '1-5 minutes',
            'holding_period': 'Seconds to minutes',
            'trades_per_day': '50-200+',
            'risk_per_trade': '0.1-0.5%',
            'profit_target': '0.1-0.5% per trade',
            'indicators': [
                {'name': 'Moving Average', 'period': 5},
                {'name': 'RSI', 'period': 14, 'overbought': 70, 'oversold': 30},
                {'name': 'Bollinger Bands', 'period': 20}
            ],
            'entry_conditions': [
                'Price crosses above short-term MA',
                'Volume spike detected',
                'RSI shows momentum'
            ],
            'exit_conditions': [
                'Quick profit target hit (0.3%)',
                'Stop loss triggered (-0.2%)',
                'Time-based exit (< 5 minutes)'
            ],
            'best_for': 'High liquidity markets',
            'requirements': {
                'min_capital': 1000,
                'time_commitment': 'Full-time monitoring',
                'experience_level': 'Advanced',
                'tools_needed': ['Fast execution platform', 'Level 2 data', 'Direct market access']
            }
        }
    
    @staticmethod
    def _day_trading_strategy() -> Dict:
        """Intraday trading strategy"""
        return {
            'name': 'Day Trading Strategy',
            'description': 'Open and close positions within the same trading day',
            'timeframe': '5-60 minutes',
            'holding_period': 'Minutes to hours (never overnight)',
            'trades_per_day': '5-20',
            'risk_per_trade': '1-2%',
            'profit_target': '1-3% per trade',
            'indicators': [
                {'name': 'VWAP', 'description': 'Volume Weighted Average Price'},
                {'name': 'Moving Average', 'periods': [9, 20, 50]},
                {'name': 'MACD', 'fast': 12, 'slow': 26, 'signal': 9}
            ],
            'entry_conditions': [
                'Price breaks above VWAP with volume',
                'MACD crossover in trend direction',
                'Support/resistance confirmation'
            ],
            'exit_conditions': [
                'Profit target reached (2%)',
                'Stop loss hit (-1.5%)',
                'End of trading day (close all positions)'
            ],
            'best_for': 'Active traders during market hours',
            'requirements': {
                'min_capital': 25000,  # US PDT rule
                'time_commitment': 'Full market hours',
                'experience_level': 'Intermediate to Advanced',
                'tools_needed': ['Real-time data', 'Level 2 quotes', 'Fast internet']
            }
        }
    
    @staticmethod
    def _swing_trading_strategy() -> Dict:
        """Multi-day trading strategy"""
        return {
            'name': 'Swing Trading Strategy',
            'description': 'Capture price swings over several days to weeks',
            'timeframe': '1 hour to 4 hours',
            'holding_period': '2-10 days',
            'trades_per_week': '3-10',
            'risk_per_trade': '2-5%',
            'profit_target': '5-15% per trade',
            'indicators': [
                {'name': 'Moving Average', 'periods': [20, 50, 200]},
                {'name': 'Fibonacci Retracement', 'levels': [23.6, 38.2, 50, 61.8]},
                {'name': 'Stochastic Oscillator', 'k_period': 14, 'd_period': 3}
            ],
            'entry_conditions': [
                'Price bounces off support level',
                'Bullish candlestick pattern',
                'RSI showing oversold (< 30) and turning up'
            ],
            'exit_conditions': [
                'Resistance level reached',
                'Profit target hit (10%)',
                'Stop loss triggered (-3%)',
                'Bearish reversal pattern'
            ],
            'best_for': 'Part-time traders',
            'requirements': {
                'min_capital': 5000,
                'time_commitment': '1-2 hours daily',
                'experience_level': 'Intermediate',
                'tools_needed': ['Charting software', 'End-of-day data']
            }
        }
    
    @staticmethod
    def _position_trading_strategy() -> Dict:
        """Long-term trading strategy"""
        return {
            'name': 'Position Trading Strategy',
            'description': 'Long-term trades based on major trends',
            'timeframe': 'Daily to weekly charts',
            'holding_period': 'Weeks to months',
            'trades_per_month': '1-5',
            'risk_per_trade': '2-10%',
            'profit_target': '20-50%+ per trade',
            'indicators': [
                {'name': 'Moving Average', 'periods': [50, 100, 200]},
                {'name': 'Trend Lines', 'description': 'Long-term support and resistance'},
                {'name': 'Fundamental Analysis', 'description': 'Economic indicators and news'}
            ],
            'entry_conditions': [
                'Strong long-term trend established',
                'Price pullback to major support',
                'Fundamental catalysts align'
            ],
            'exit_conditions': [
                'Trend reversal confirmed',
                'Major resistance reached',
                'Fundamental change in market conditions',
                'Profit target achieved (30%+)'
            ],
            'best_for': 'Patient investors with long-term view',
            'requirements': {
                'min_capital': 10000,
                'time_commitment': 'Few hours weekly',
                'experience_level': 'All levels',
                'tools_needed': ['Research tools', 'Economic calendar', 'News sources']
            }
        }
    
    @staticmethod
    def _arbitrage_strategy() -> Dict:
        """Price discrepancy exploitation strategy"""
        return {
            'name': 'Arbitrage Strategy',
            'description': 'Exploit price differences across markets',
            'timeframe': 'Real-time',
            'holding_period': 'Seconds to minutes',
            'trades_per_day': '10-100+',
            'risk_per_trade': '0.1-1%',
            'profit_target': '0.1-0.5% per trade',
            'types': [
                'Spatial arbitrage (different exchanges)',
                'Temporal arbitrage (time-based)',
                'Statistical arbitrage (mean reversion)',
                'Triangular arbitrage (currency pairs)'
            ],
            'entry_conditions': [
                'Price discrepancy > transaction costs',
                'Sufficient liquidity on both sides',
                'Quick execution possible'
            ],
            'exit_conditions': [
                'Positions balanced (both sides filled)',
                'Price convergence',
                'Risk of reversal'
            ],
            'best_for': 'Algorithmic traders with fast execution',
            'requirements': {
                'min_capital': 10000,
                'time_commitment': 'Automated (algorithmic)',
                'experience_level': 'Advanced',
                'tools_needed': ['Multiple exchange accounts', 'API access', 'Low-latency connection', 'Automation']
            }
        }
    
    @staticmethod
    def _momentum_strategy() -> Dict:
        """Trend-following momentum strategy"""
        return {
            'name': 'Momentum Strategy',
            'description': 'Follow strong price movements',
            'timeframe': '15 minutes to 4 hours',
            'holding_period': 'Hours to days',
            'trades_per_week': '5-15',
            'risk_per_trade': '2-3%',
            'profit_target': '5-10% per trade',
            'indicators': [
                {'name': 'Rate of Change (ROC)', 'period': 12},
                {'name': 'Moving Average Convergence', 'description': 'Multiple MA crossovers'},
                {'name': 'Volume', 'description': 'Confirm momentum with volume'}
            ],
            'entry_conditions': [
                'Strong price momentum (ROC > threshold)',
                'Volume increasing',
                'Price breaking key resistance',
                'News catalyst or market event'
            ],
            'exit_conditions': [
                'Momentum slowing (ROC declining)',
                'Volume drying up',
                'Profit target reached',
                'Trailing stop triggered'
            ],
            'best_for': 'Traders who can act quickly on strong moves',
            'requirements': {
                'min_capital': 5000,
                'time_commitment': 'Active monitoring',
                'experience_level': 'Intermediate',
                'tools_needed': ['Real-time data', 'Alerts', 'Fast execution']
            }
        }
    
    @staticmethod
    def _mean_reversion_strategy() -> Dict:
        """Mean reversion trading strategy"""
        return {
            'name': 'Mean Reversion Strategy',
            'description': 'Trade based on prices returning to average',
            'timeframe': '1 hour to daily',
            'holding_period': '1-5 days',
            'trades_per_week': '5-10',
            'risk_per_trade': '2-4%',
            'profit_target': '3-8% per trade',
            'indicators': [
                {'name': 'Bollinger Bands', 'period': 20, 'std_dev': 2},
                {'name': 'RSI', 'period': 14, 'overbought': 70, 'oversold': 30},
                {'name': 'Moving Average', 'period': 50}
            ],
            'entry_conditions': [
                'Price touches or exceeds lower Bollinger Band',
                'RSI shows oversold (< 30)',
                'Price significantly below moving average',
                'No major news or trend change'
            ],
            'exit_conditions': [
                'Price returns to middle band or MA',
                'RSI returns to neutral (50)',
                'Profit target reached',
                'Stop loss if trend continues down'
            ],
            'best_for': 'Range-bound or stable markets',
            'requirements': {
                'min_capital': 3000,
                'time_commitment': '1-2 hours daily',
                'experience_level': 'Beginner to Intermediate',
                'tools_needed': ['Charting software', 'Statistical tools']
            }
        }
    
    @staticmethod
    def _breakout_strategy() -> Dict:
        """Breakout trading strategy"""
        return {
            'name': 'Breakout Strategy',
            'description': 'Trade when price breaks key levels',
            'timeframe': '15 minutes to 4 hours',
            'holding_period': 'Hours to days',
            'trades_per_week': '3-8',
            'risk_per_trade': '2-4%',
            'profit_target': '5-15% per trade',
            'indicators': [
                {'name': 'Support/Resistance Levels', 'description': 'Key price levels'},
                {'name': 'Volume', 'description': 'Confirm breakout with volume spike'},
                {'name': 'ATR', 'description': 'Average True Range for volatility'}
            ],
            'entry_conditions': [
                'Price breaks above resistance with volume',
                'Consolidation pattern completes',
                'Volume at least 1.5x average',
                'Candlestick pattern confirms breakout'
            ],
            'exit_conditions': [
                'Measured move target reached',
                'Volume decreases significantly',
                'False breakout detected (price returns)',
                'Stop loss below breakout level'
            ],
            'best_for': 'Trending markets with clear levels',
            'requirements': {
                'min_capital': 5000,
                'time_commitment': 'Active during breakout times',
                'experience_level': 'Intermediate',
                'tools_needed': ['Level 2 data', 'Volume analysis', 'Alert system']
            }
        }
    
    @staticmethod
    def get_strategy_comparison() -> List[Dict]:
        """Get a comparison of all strategies"""
        return [
            {
                'strategy': 'Scalping',
                'risk': 'Low per trade, High overall',
                'time_commitment': 'Very High',
                'capital_requirement': 'Low',
                'experience_needed': 'Advanced'
            },
            {
                'strategy': 'Day Trading',
                'risk': 'Medium',
                'time_commitment': 'High',
                'capital_requirement': 'High ($25k+)',
                'experience_needed': 'Advanced'
            },
            {
                'strategy': 'Swing Trading',
                'risk': 'Medium',
                'time_commitment': 'Medium',
                'capital_requirement': 'Medium',
                'experience_needed': 'Intermediate'
            },
            {
                'strategy': 'Position Trading',
                'risk': 'Medium to High',
                'time_commitment': 'Low',
                'capital_requirement': 'Medium to High',
                'experience_needed': 'All Levels'
            },
            {
                'strategy': 'Arbitrage',
                'risk': 'Very Low',
                'time_commitment': 'Low (automated)',
                'capital_requirement': 'Medium to High',
                'experience_needed': 'Advanced'
            },
            {
                'strategy': 'Momentum',
                'risk': 'Medium to High',
                'time_commitment': 'Medium to High',
                'capital_requirement': 'Medium',
                'experience_needed': 'Intermediate'
            },
            {
                'strategy': 'Mean Reversion',
                'risk': 'Medium',
                'time_commitment': 'Low to Medium',
                'capital_requirement': 'Low to Medium',
                'experience_needed': 'Beginner to Intermediate'
            },
            {
                'strategy': 'Breakout',
                'risk': 'Medium',
                'time_commitment': 'Medium',
                'capital_requirement': 'Medium',
                'experience_needed': 'Intermediate'
            }
        ]
