"""Game state management for Black Sultan OS."""


class GameState:
    """Manages the global game state including portfolio, levels, and achievements."""
    
    def __init__(self):
        """Initialize game state with default values."""
        self.portfolio_value = 125848.07
        self.daily_profit = 2847.50
        self.user_level = 15
        self.user_xp = 8750
        self.streak_days = 12
        self.total_trades = 1247
        self.successful_trades = 1089
        self.achievements = []
        self.active_challenges = []
        self.spin_wheel_available = True
        self.last_spin_time = None
        self.scratch_cards_available = 3
        self.daily_bonus_claimed = False
        
    def add_xp(self, amount: int) -> bool:
        """
        Add XP to the user and check for level up.
        
        Args:
            amount: Amount of XP to add
            
        Returns:
            bool: True if level up occurred, False otherwise
        """
        self.user_xp += amount
        # Level up every 1000 XP
        new_level = (self.user_xp // 1000) + 1
        if new_level > self.user_level:
            self.user_level = new_level
            return True  # Level up occurred
        return False
    
    def add_profit(self, amount: float) -> None:
        """
        Add profit to the portfolio.
        
        Args:
            amount: Amount to add (can be negative for losses)
        """
        self.portfolio_value += amount
        self.daily_profit += amount
