"""Gamification engine for user engagement features."""
import random
from datetime import datetime
from typing import Dict


class GamificationEngine:
    """Gamification System for rewards and achievements."""
    
    def __init__(self):
        """Initialize gamification engine with achievements."""
        self.achievements = [
            {
                'id': 'first_trade',
                'name': 'First Trade',
                'description': 'Complete your first trade',
                'xp': 100
            },
            {
                'id': 'profit_master',
                'name': 'Profit Master',
                'description': 'Earn $1000 in profits',
                'xp': 500
            },
            {
                'id': 'streak_warrior',
                'name': 'Streak Warrior',
                'description': 'Maintain a 7-day trading streak',
                'xp': 300
            },
            {
                'id': 'bot_commander',
                'name': 'Bot Commander',
                'description': 'Activate all 5 trading bots',
                'xp': 250
            }
        ]
        
    def spin_wheel(self, game_state) -> Dict:
        """
        Spin the wheel for random rewards.
        
        Args:
            game_state: Reference to the global game state
            
        Returns:
            Dict containing reward information
        """
        if not game_state.spin_wheel_available:
            return {'error': 'Spin wheel not available. Try again in 24 hours.'}
        
        rewards = [
            {'type': 'cash', 'amount': 50, 'probability': 0.3},
            {'type': 'cash', 'amount': 100, 'probability': 0.2},
            {'type': 'cash', 'amount': 250, 'probability': 0.1},
            {'type': 'xp', 'amount': 200, 'probability': 0.25},
            {'type': 'multiplier', 'amount': 1.5, 'probability': 0.1},
            {'type': 'free_spin', 'amount': 1, 'probability': 0.05}
        ]
        
        # Select reward based on probability
        rand = random.random()
        cumulative_prob = 0
        selected_reward = None
        
        for reward in rewards:
            cumulative_prob += reward['probability']
            if rand <= cumulative_prob:
                selected_reward = reward
                break
        
        if not selected_reward:
            selected_reward = rewards[0]  # Fallback
        
        # Apply reward
        if selected_reward['type'] == 'cash':
            game_state.add_profit(selected_reward['amount'])
        elif selected_reward['type'] == 'xp':
            level_up = game_state.add_xp(selected_reward['amount'])
            selected_reward['level_up'] = level_up
        
        # Set cooldown (24 hours)
        game_state.spin_wheel_available = False
        game_state.last_spin_time = datetime.now()
        
        return {
            'success': True,
            'reward': selected_reward,
            'new_portfolio_value': game_state.portfolio_value,
            'new_xp': game_state.user_xp,
            'new_level': game_state.user_level
        }
    
    def scratch_card(self, game_state) -> Dict:
        """
        Scratch a card for instant rewards.
        
        Args:
            game_state: Reference to the global game state
            
        Returns:
            Dict containing reward information
        """
        if game_state.scratch_cards_available <= 0:
            return {'error': 'No scratch cards available'}
        
        game_state.scratch_cards_available -= 1
        
        # Random reward
        rewards = [25, 50, 75, 100, 150, 200]
        reward_amount = random.choice(rewards)
        
        game_state.add_profit(reward_amount)
        level_up = game_state.add_xp(50)
        
        return {
            'success': True,
            'reward_amount': reward_amount,
            'cards_remaining': game_state.scratch_cards_available,
            'new_portfolio_value': game_state.portfolio_value,
            'level_up': level_up
        }
