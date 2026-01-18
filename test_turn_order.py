"""
Simple demo of turn order and 1-order-per-location system
"""
from game_state import GameState, Location, LocationType, UnitType
from legal_moves import LegalMoveGenerator

# Setup
game = GameState()

# Create locations
bot_ids = ["Stark", "Lannister", "Baratheon"]
for bot_id in bot_ids:
    for i in range(2):
        loc = Location(name=f"{bot_id}_{i}", location_type=LocationType.LAND, owner=bot_id)
        loc.add_units(UnitType.FOOTMAN, 2, owner=bot_id)
        game.add_location(loc)

# Set turn order
game.set_turn_order(bot_ids)

print("=== TURN ORDER & 1-ORDER-PER-LOCATION ===\n")

print("Turn Order:")
for i, bot in enumerate(game.turn_order, 1):
    print(f"  {i}. {bot}")

print(f"\nCurrent player: {game.get_current_player()}")
print(f"Turn: {game.turn}\n")

# Show legal orders
move_gen = LegalMoveGenerator(game)
stark_orders = move_gen.get_legal_orders("Stark")

print("Stark's Available Orders (1 per location):")
for location_name, orders in stark_orders.items():
    print(f"  {location_name}: {[str(o) for o in orders]}")

print("\n=== CHANGING TURN ORDER ===\n")

# Change turn order based on score
game.player_stats["Stark"].power = 5
game.player_stats["Lannister"].power = 3
game.player_stats["Baratheon"].power = 2

new_order = sorted(bot_ids, key=lambda x: game.player_stats[x].power, reverse=True)
game.set_turn_order(new_order)

print(f"New turn order (by power): {game.turn_order}")
print(f"Current player: {game.get_current_player()}")
