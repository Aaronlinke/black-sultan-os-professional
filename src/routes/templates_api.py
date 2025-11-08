"""
Templates API Routes
Provides endpoints for accessing trading templates and market configurations
"""

from flask import Blueprint, jsonify, request
from templates.american_market import AmericanMarketTemplate
from templates.trading_strategies import TradingStrategyTemplates
from datetime import datetime

templates_api_bp = Blueprint('templates_api', __name__)

# Initialize template providers
american_market = AmericanMarketTemplate()
strategy_templates = TradingStrategyTemplates()


@templates_api_bp.route('/templates/markets/american', methods=['GET'])
def get_american_market_config():
    """Get American market configuration template"""
    try:
        config = american_market.get_market_config()
        market_status = american_market.is_market_open()
        
        return jsonify({
            'success': True,
            'data': {
                'config': config,
                'current_status': market_status,
                'timestamp': datetime.now().isoformat()
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@templates_api_bp.route('/templates/markets/american/status', methods=['GET'])
def get_american_market_status():
    """Get current American market status"""
    try:
        status = american_market.is_market_open()
        return jsonify({
            'success': True,
            'data': status,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@templates_api_bp.route('/templates/bots/american', methods=['GET'])
def get_american_bot_templates():
    """Get American market bot templates"""
    try:
        strategy_type = request.args.get('strategy', 'balanced')
        bot_template = american_market.get_bot_template(strategy_type)
        
        return jsonify({
            'success': True,
            'data': bot_template,
            'available_strategies': ['conservative', 'balanced', 'aggressive'],
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@templates_api_bp.route('/templates/bots/american/crypto', methods=['GET'])
def get_american_crypto_template():
    """Get American-focused cryptocurrency trading template"""
    try:
        crypto_template = american_market.get_cryptocurrency_template()
        return jsonify({
            'success': True,
            'data': crypto_template,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@templates_api_bp.route('/templates/strategies', methods=['GET'])
def get_all_strategies():
    """Get list of all available trading strategies"""
    try:
        strategies = strategy_templates.get_all_strategies()
        return jsonify({
            'success': True,
            'data': {
                'strategies': strategies,
                'total_count': len(strategies)
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@templates_api_bp.route('/templates/strategies/<strategy_name>', methods=['GET'])
def get_strategy_details(strategy_name):
    """Get detailed configuration for a specific strategy"""
    try:
        strategy = strategy_templates.get_strategy(strategy_name)
        
        if not strategy:
            return jsonify({
                'success': False,
                'error': f'Strategy "{strategy_name}" not found'
            }), 404
        
        return jsonify({
            'success': True,
            'data': strategy,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@templates_api_bp.route('/templates/strategies/comparison', methods=['GET'])
def get_strategy_comparison():
    """Get comparison of all trading strategies"""
    try:
        comparison = strategy_templates.get_strategy_comparison()
        return jsonify({
            'success': True,
            'data': comparison,
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@templates_api_bp.route('/templates/search', methods=['GET'])
def search_templates():
    """Search templates by criteria"""
    try:
        # Get search parameters
        risk_level = request.args.get('risk_level', '').lower()
        experience = request.args.get('experience', '').lower()
        time_commitment = request.args.get('time_commitment', '').lower()
        min_capital = request.args.get('min_capital', type=int)
        
        # Get all strategies
        all_strategies = strategy_templates.get_all_strategies()
        results = []
        
        for strategy_name in all_strategies:
            strategy = strategy_templates.get_strategy(strategy_name)
            
            # Apply filters
            matches = True
            
            if min_capital and strategy.get('requirements', {}).get('min_capital', 0) > min_capital:
                matches = False
            
            if experience and experience not in strategy.get('requirements', {}).get('experience_level', '').lower():
                matches = False
            
            if matches:
                results.append({
                    'name': strategy['name'],
                    'description': strategy['description'],
                    'risk_per_trade': strategy['risk_per_trade'],
                    'experience_level': strategy.get('requirements', {}).get('experience_level'),
                    'min_capital': strategy.get('requirements', {}).get('min_capital')
                })
        
        return jsonify({
            'success': True,
            'data': {
                'results': results,
                'total_found': len(results),
                'filters_applied': {
                    'risk_level': risk_level or 'any',
                    'experience': experience or 'any',
                    'time_commitment': time_commitment or 'any',
                    'min_capital': min_capital or 'any'
                }
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


@templates_api_bp.route('/templates/recommended', methods=['GET'])
def get_recommended_templates():
    """Get recommended templates based on user profile"""
    try:
        # Get user parameters
        capital = request.args.get('capital', type=float, default=5000)
        experience = request.args.get('experience', 'beginner').lower()
        time_available = request.args.get('time_available', 'part-time').lower()
        
        recommendations = []
        
        # Recommendation logic
        if capital < 3000:
            if experience in ['beginner', 'intermediate']:
                recommendations.append({
                    'strategy': 'mean_reversion',
                    'reason': 'Lower capital requirement and good for beginners',
                    'priority': 1
                })
        
        if capital >= 25000 and experience == 'advanced' and time_available == 'full-time':
            recommendations.append({
                'strategy': 'day_trading',
                'reason': 'Meets PDT rule capital requirement and experience level',
                'priority': 1
            })
        
        if time_available == 'part-time':
            recommendations.append({
                'strategy': 'swing_trading',
                'reason': 'Requires less time commitment',
                'priority': 2
            })
        
        # Always include position trading as a low-risk option
        recommendations.append({
            'strategy': 'position_trading',
            'reason': 'Low time commitment, suitable for any experience level',
            'priority': 3
        })
        
        # Sort by priority
        recommendations.sort(key=lambda x: x['priority'])
        
        # Get full details for recommended strategies
        detailed_recommendations = []
        for rec in recommendations:
            strategy = strategy_templates.get_strategy(rec['strategy'])
            detailed_recommendations.append({
                'recommendation': rec,
                'strategy_details': strategy
            })
        
        return jsonify({
            'success': True,
            'data': {
                'user_profile': {
                    'capital': capital,
                    'experience': experience,
                    'time_available': time_available
                },
                'recommendations': detailed_recommendations
            },
            'timestamp': datetime.now().isoformat()
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500
