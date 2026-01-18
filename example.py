"""
Example usage of the GOT Simulator
Shows how bots choose between legal orders
"""
from game_state import GameState, Location, LocationType, UnitType
from legal_moves import LegalMoveGenerator
from bot import Bot, RandomBot, GreedyBot
from visualizer import MapVisualizer


def setup_simple_game():
    """Create a simple irregular map with 6 bots"""
    game = GameState()
    
    # Create locations (x, y are just for visualization)
    # Format: (name, x, y, location_type)
    locations_data = [
        ("Banefort", 0, 2, LocationType.LAND),
        ("Riverrun", -1, 1, LocationType.LAND),
        ("Goldentooth", 0, 1, LocationType.LAND),
        ("Lannisport", 1, 1, LocationType.LAND),
        ("Stony Sept", 0, 0, LocationType.LAND),
    ]
    
    bot_ids = ["Stark", "Lannister", "Baratheon", "Greyjoy", "Tyrell", "Martell"]
    
    # Add all locations
    for i, (name, x, y, loc_type) in enumerate(locations_data):
        location = Location(name=name, x=x, y=y, location_type=loc_type)
        owner = bot_ids[i % len(bot_ids)]
        location.owner = owner
        
        # Add units based on location type (with owner validation)
        if loc_type == LocationType.SEA:
            location.add_units(UnitType.BOAT, 2, owner=owner)  # Sea locations get boats
        else:
            location.add_units(UnitType.FOOTMAN, 2, owner=owner)  # Land locations start with footmen
            if i % 3 == 0:
                location.add_units(UnitType.KNIGHT, 1, owner=owner)  # Some locations have knights
        
        game.add_location(location)
    
    # Define adjacencies (graph connections)
    adjacencies = {
        "Banefort": ["Lannisport"],
        "Riverrun": ["Stony Sept"],
        "Goldentooth": ["Lannisport", "Stony Sept"],
        "Lannisport": ["Banefort"],
        "Stony Sept": ["Goldentooth", "Riverrun"],
    }
    
    # Connect locations
    for loc_name, adjacent_names in adjacencies.items():
        for adj_name in adjacent_names:
            if adj_name not in game.locations[loc_name].adjacent_locations:
                game.connect_locations(loc_name, adj_name)
    
    game.active_bots = set(bot_ids)
    return game, bot_ids


def simulate_turn(game: GameState, bots: dict):
    """Simulate one turn of the game"""
    print(f"\n=== TURN {game.turn} ===\n")
    
    move_gen = LegalMoveGenerator(game)
    
    for bot_id in game.active_bots:
        bot = bots[bot_id]
        legal_orders = move_gen.get_legal_orders(bot_id)
        
        print(f"{bot_id}'s turn:")
        print(f"  Legal orders available: {len(legal_orders)}")
        
        for order in legal_orders:  # Show first 3
            print(f"    - {order}")
        
        if len(legal_orders) > 3:
            print(f"    ... and {len(legal_orders) - 3} more")
        
        # Bot chooses orders
        chosen_orders = bot.take_turn(game, legal_orders)
        print(f"  Chosen orders: {len(chosen_orders)}")
        for order in chosen_orders:
            print(f"    - {order}")
        
        game.bot_orders[bot_id] = chosen_orders
        print()
    
    game.turn += 1


def main():
    """Main simulation loop"""
    print("GOT Simulator - Bot Decision Making Example\n")
    
    game, bot_ids = setup_simple_game()
    
    # Create bots with different strategies
    bots = {
        bot_ids[0]: Bot(bot_ids[0], RandomBot(bot_ids[0])),
        bot_ids[1]: Bot(bot_ids[1], GreedyBot(bot_ids[1])),
        bot_ids[2]: Bot(bot_ids[2], RandomBot(bot_ids[2])),
        bot_ids[3]: Bot(bot_ids[3], GreedyBot(bot_ids[3])),
        bot_ids[4]: Bot(bot_ids[4], RandomBot(bot_ids[4])),
        bot_ids[5]: Bot(bot_ids[5], GreedyBot(bot_ids[5])),
    }
    
    # Visualize the initial map
    print("\nGenerating map visualization...\n")
    visualizer = MapVisualizer(game)
    visualizer.visualize(title="GOT Game Map - Initial State", save_path="map_visualization.png")
    
    # Simulate a few turns
    for _ in range(3):
        simulate_turn(game, bots)


if __name__ == "__main__":
    main()
