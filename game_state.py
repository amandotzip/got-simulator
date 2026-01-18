"""
Game state representation for GOT Simulator
"""
from dataclasses import dataclass, field
from typing import Dict, List, Set
from enum import Enum


class OrderType(Enum):
    """Types of orders that can be placed"""
    MARCH = "march"        # Move units to adjacent location
    SUPPORT = "support"    # Support an adjacent location
    DEFEND = "defend"      # Defend current location
    RAID = "raid"          # Attack supply line
    CONSOLIDATE_POWER = "consolidate_power"  # Gather resources


class LocationType(Enum):
    """Types of locations on the map"""
    LAND = "land"          # Land location
    SEA = "sea"            # Sea location


class UnitType(Enum):
    """Types of units that can be placed on the map"""
    FOOTMAN = "footman"           # Basic land unit
    KNIGHT = "knight"             # Mounted land unit (faster)
    SIEGE_ENGINE = "siege_engine"  # Siege equipment (heavy)
    BOAT = "boat"                 # Naval unit (sea only)


class FortificationType(Enum):
    """Types of fortifications a location can have"""
    NONE = "none"              # No fortification
    CASTLE = "castle"          # Castle (moderate defense)
    STRONGHOLD = "stronghold"  # Stronghold (high defense)


@dataclass
class Location:
    """Represents a location on the map"""
    name: str
    x: float = 0  # For visualization only
    y: float = 0  # For visualization only
    location_type: LocationType = LocationType.LAND  # Land or sea
    owner: str = None  # Which bot controls this
    units: Dict[UnitType, int] = field(default_factory=lambda: {
        UnitType.FOOTMAN: 0,
        UnitType.KNIGHT: 0,
        UnitType.SIEGE_ENGINE: 0,
        UnitType.BOAT: 0
    })  # Units by type
    adjacent_locations: Set[str] = field(default_factory=set)  # Names of adjacent locations
    supply: int = 0  # Supply tokens (max varies per location)
    max_supply: int = 1  # Maximum supply this location can hold
    crowns: int = 0  # Crown tokens (income/wealth)
    fortification: FortificationType = FortificationType.NONE  # Castle/Stronghold status
    
    def __hash__(self):
        return hash(self.name)
    
    def get_total_units(self) -> int:
        """Get total unit count"""
        return sum(self.units.values())
    
    def has_units(self) -> bool:
        """Check if location has any units"""
        return self.get_total_units() > 0
    
    def add_units(self, unit_type: UnitType, count: int, owner: str = None) -> bool:
        """
        Add units of a specific type.
        If owner is provided, validates that only this owner's units are on the location.
        Returns True if successful, False if owner conflict.
        """
        # Validate owner consistency
        if owner is not None:
            if self.owner is None:
                self.owner = owner
            elif self.owner != owner:
                raise ValueError(
                    f"Cannot add {owner}'s units to {self.name}: "
                    f"already controlled by {self.owner}"
                )
        
        self.units[unit_type] = self.units.get(unit_type, 0) + count
        return True
    
    def remove_units(self, unit_type: UnitType, count: int) -> bool:
        """Remove units of a specific type. Returns True if successful."""
        current = self.units.get(unit_type, 0)
        if current >= count:
            self.units[unit_type] -= count
            return True
        return False
    
    def set_owner(self, new_owner: str) -> bool:
        """
        Change the owner of a location.
        Only allowed if location has no units (conquered locations must be cleared).
        Returns True if successful.
        """
        if self.has_units():
            raise ValueError(
                f"Cannot change owner of {self.name}: "
                f"still has {self.get_total_units()} units. "
                f"Remove all units before changing ownership."
            )
        self.owner = new_owner
        return True
    
    def add_supply(self, amount: int) -> bool:
        """Add supply to location (up to max). Returns True if successful."""
        if self.supply + amount > self.max_supply:
            self.supply = self.max_supply
            return False  # Could not add all
        self.supply += amount
        return True
    
    def remove_supply(self, amount: int) -> bool:
        """Remove supply from location. Returns True if successful."""
        if self.supply >= amount:
            self.supply -= amount
            return True
        return False
    
    def add_crowns(self, amount: int) -> bool:
        """Add crowns to location. Returns True."""
        self.crowns += amount
        return True
    
    def remove_crowns(self, amount: int) -> bool:
        """Remove crowns from location. Returns True if successful."""
        if self.crowns >= amount:
            self.crowns -= amount
            return True
        return False
    
    def get_defense_bonus(self) -> int:
        """Get defense bonus from fortification"""
        if self.fortification == FortificationType.STRONGHOLD:
            return 2
        elif self.fortification == FortificationType.CASTLE:
            return 1
        else:
            return 0
    
    def set_fortification(self, fort_type: FortificationType):
        """Set fortification type"""
        self.fortification = fort_type


@dataclass
class Order:
    """Represents an order placed by a bot"""
    order_type: OrderType
    location: Location
    target_location: Location = None  # For march/support/raid
    bot_id: str = None
    
    def __repr__(self):
        if self.target_location:
            return f"{self.bot_id}: {self.order_type.value} from {self.location.name} to {self.target_location.name}"
        else:
            return f"{self.bot_id}: {self.order_type.value} at {self.location.name}"


@dataclass
class PlayerStats:
    """Tracks statistics for a player"""
    bot_id: str
    territories: int = 0  # Number of territories controlled
    power: int = 0  # Power points (for winning)
    total_units: int = 0  # Total units alive
    units_killed: int = 0  # Total units lost in combat
    orders_executed: int = 0  # Number of orders successfully executed
    
    def get_score(self) -> int:
        """Calculate a simple score based on territory and power"""
        return (self.territories * 10) + self.power


@dataclass
class GameState:
    """Represents the current state of the game"""
    locations: Dict[str, Location] = field(default_factory=dict)
    bot_orders: Dict[str, List[Order]] = field(default_factory=dict)  # bot_id -> list of orders
    player_stats: Dict[str, PlayerStats] = field(default_factory=dict)  # bot_id -> stats
    turn: int = 0
    turn_order: List[str] = field(default_factory=list)  # Turn order (bot_id list)
    current_turn_index: int = 0  # Index in turn order
    active_bots: Set[str] = field(default_factory=set)  # Bots still in the game
    turn_history: List[Dict] = field(default_factory=list)  # Historical records of each turn
    
    def add_location(self, location: Location):
        """Add a location to the map"""
        self.locations[location.name] = location
    
    def connect_locations(self, loc1_name: str, loc2_name: str):
        """Create bidirectional adjacency between two locations"""
        if loc1_name in self.locations and loc2_name in self.locations:
            self.locations[loc1_name].adjacent_locations.add(loc2_name)
            self.locations[loc2_name].adjacent_locations.add(loc1_name)
    
    def get_adjacent_locations(self, location: Location) -> List[Location]:
        """Get locations adjacent to a given location"""
        return [self.locations[name] for name in location.adjacent_locations 
                if name in self.locations]
    
    def get_bot_locations(self, bot_id: str) -> List[Location]:
        """Get all locations controlled by a bot"""
        return [loc for loc in self.locations.values() if loc.owner == bot_id]
    
    def get_bot_units(self, bot_id: str) -> int:
        """Get total units a bot controls"""
        total = 0
        for loc in self.get_bot_locations(bot_id):
            total += loc.get_total_units()
        return total
    
    def initialize_player_stats(self, bot_id: str):
        """Initialize stats for a player"""
        if bot_id not in self.player_stats:
            self.player_stats[bot_id] = PlayerStats(bot_id=bot_id)
    
    def update_player_stats(self, bot_id: str):
        """Update player stats based on current game state"""
        self.initialize_player_stats(bot_id)
        stats = self.player_stats[bot_id]
        
        # Update territory count
        territories = self.get_bot_locations(bot_id)
        stats.territories = len(territories)
        
        # Update total units
        stats.total_units = self.get_bot_units(bot_id)
    
    def record_turn(self):
        """Record current turn state in history"""
        turn_data = {
            "turn": self.turn,
            "player_stats": {
                bot_id: {
                    "territories": stats.territories,
                    "power": stats.power,
                    "total_units": stats.total_units,
                    "score": stats.get_score()
                }
                for bot_id, stats in self.player_stats.items()
            }
        }
        self.turn_history.append(turn_data)
    
    def get_leaderboard(self) -> List[tuple]:
        """Get sorted leaderboard by score"""
        scores = [
            (bot_id, stats.get_score(), stats.territories, stats.total_units)
            for bot_id, stats in self.player_stats.items()
        ]
        return sorted(scores, key=lambda x: x[1], reverse=True)
    
    def set_turn_order(self, bot_order: List[str]):
        """Set the turn order for players"""
        self.turn_order = bot_order
        self.current_turn_index = 0
    
    def get_current_player(self) -> str:
        """Get the current player's turn"""
        if not self.turn_order:
            return None
        return self.turn_order[self.current_turn_index]
    
    def next_turn(self):
        """Move to next player's turn"""
        if not self.turn_order:
            return
        
        self.current_turn_index += 1
        if self.current_turn_index >= len(self.turn_order):
            # Completed a full round
            self.current_turn_index = 0
            self.turn += 1
    
    def reset_turn_order(self):
        """Reset turn order to the beginning"""
        self.current_turn_index = 0
