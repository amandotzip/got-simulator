"""
Bot decision-making system
Handles how bots choose between legal orders
"""
from abc import ABC, abstractmethod
from typing import List
import random
from game_state import GameState, Order


class BotStrategy(ABC):
    """Abstract base class for bot strategies"""
    
    def __init__(self, bot_id: str):
        self.bot_id = bot_id
    
    @abstractmethod
    def choose_orders(self, game_state: GameState, legal_orders: List[Order]) -> List[Order]:
        """
        Choose which orders to place from the list of legal options.
        Returns list of orders this bot will place.
        """
        pass


class RandomBot(BotStrategy):
    """Bot that chooses orders randomly from legal options"""
    
    def choose_orders(self, game_state: GameState, legal_orders: List[Order]) -> List[Order]:
        """Randomly select a subset of legal orders"""
        if not legal_orders:
            return []
        
        # For now, place random orders (could be optimized)
        num_orders = random.randint(0, len(legal_orders))
        return random.sample(legal_orders, num_orders)


class GreedyBot(BotStrategy):
    """Bot that greedily expands territory"""
    
    def choose_orders(self, game_state: GameState, legal_orders: List[Order]) -> List[Order]:
        """Prioritize marching/attacking over defending"""
        if not legal_orders:
            return []
        
        # Sort: MARCH orders first, then SUPPORT, then DEFEND
        from game_state import OrderType
        march_orders = [o for o in legal_orders if o.order_type == OrderType.MARCH]
        support_orders = [o for o in legal_orders if o.order_type == OrderType.SUPPORT]
        defend_orders = [o for o in legal_orders if o.order_type == OrderType.DEFEND]
        
        # Greedily pick march orders first, then support, then defend
        chosen = march_orders + support_orders[:len(march_orders)] + defend_orders[:1]
        return chosen[:len(legal_orders)]  # Don't exceed available orders


class RLBot(BotStrategy):
    """Placeholder for reinforcement learning bot"""
    
    def __init__(self, bot_id: str, q_table: dict = None):
        super().__init__(bot_id)
        self.q_table = q_table or {}
    
    def choose_orders(self, game_state: GameState, legal_orders: List[Order]) -> List[Order]:
        """
        Choose orders based on learned Q-values.
        For now, just random selection (to be implemented with RL training).
        """
        if not legal_orders:
            return []
        
        # TODO: Implement Q-learning logic
        # For now, choose randomly
        return [random.choice(legal_orders)]


class Bot:
    """Main bot class that uses a strategy"""
    
    def __init__(self, bot_id: str, strategy: BotStrategy):
        self.bot_id = bot_id
        self.strategy = strategy
    
    def take_turn(self, game_state: GameState, legal_orders: List[Order]) -> List[Order]:
        """Bot takes a turn and returns its orders"""
        return self.strategy.choose_orders(game_state, legal_orders)
    
    def set_strategy(self, strategy: BotStrategy):
        """Change the bot's strategy"""
        self.strategy = strategy
