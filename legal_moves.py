"""
Legal move generator - determines what orders a bot can place
"""
from typing import List, Dict
from game_state import GameState, Order, OrderType, Location


class LegalMoveGenerator:
    """Generates all legal orders a bot can place in a given state"""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
    
    def get_legal_orders(self, bot_id: str) -> List[Order]:
        """
        Get all legal orders a bot can place on their turn.
        A bot can place ONE order per location they control (1 order per location with units).
        Returns a dict with options for each location: location -> list of possible orders
        """
        legal_orders_by_location: Dict[str, List[Order]] = {}
        
        # Get all locations controlled by this bot that have units
        controlled_locations = self.game_state.get_bot_locations(bot_id)
        
        for location in controlled_locations:
            if not location.has_units():
                continue  # Skip locations without units
            
            # Get possible orders for this location (but bot will pick only 1)
            location_orders = self._get_orders_for_location(bot_id, location)
            if location_orders:
                legal_orders_by_location[location.name] = location_orders
        
        return legal_orders_by_location
    
    def _get_orders_for_location(self, bot_id: str, location: Location) -> List[Order]:
        """Get all possible orders for a specific location (bot picks 1)"""
        orders = []
        
        # Can always defend (hold position)
        orders.append(Order(
            order_type=OrderType.DEFEND,
            location=location,
            bot_id=bot_id
        ))
        
        # Can march or support to adjacent locations
        adjacent = self.game_state.get_adjacent_locations(location)
        
        for adj_location in adjacent:
            # MARCH: Move to uncontrolled or enemy location
            if adj_location.owner != bot_id:
                orders.append(Order(
                    order_type=OrderType.MARCH,
                    location=location,
                    target_location=adj_location,
                    bot_id=bot_id
                ))
            
            # SUPPORT: Support an adjacent friendly location
            if adj_location.owner == bot_id:
                orders.append(Order(
                    order_type=OrderType.SUPPORT,
                    location=location,
                    target_location=adj_location,
                    bot_id=bot_id
                ))
        
        return orders
    
    def is_legal_order(self, bot_id: str, order: Order) -> bool:
        """Check if a specific order is legal for a location"""
        legal_orders_by_location = self.get_legal_orders(bot_id)
        
        # Check if location has any legal orders
        if order.location.name not in legal_orders_by_location:
            return False
        
        # Check if this specific order is in the list
        location_orders = legal_orders_by_location[order.location.name]
        return order in location_orders
