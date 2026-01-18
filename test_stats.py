"""
Test player stats tracking (simplified)
"""
from game_state import GameState, Location, LocationType, UnitType, PlayerStats

if __name__ == "__main__":
    game = GameState()
    
    # Create simple test locations
    bot_ids = ["Stark", "Lannister", "Baratheon"]
    for bot_id in bot_ids:
        game.initialize_player_stats(bot_id)
        
        # Add some locations for each bot
        for i in range(3):
            loc = Location(name=f"{bot_id}_Region_{i}", location_type=LocationType.LAND)
            loc.owner = bot_id
            loc.add_units(UnitType.FOOTMAN, 2 + i, owner=bot_id)
            game.add_location(loc)
    
    print("=== PLAYER STATS TRACKING ===\n")
    
    # Update stats
    print("Initial State:")
    print("-" * 70)
    for bot_id in bot_ids:
        game.update_player_stats(bot_id)
    
    for bot_id in bot_ids:
        stats = game.player_stats[bot_id]
        print(f"{bot_id:12} | Territories: {stats.territories:2} | Units: {stats.total_units:2} | Score: {stats.get_score():3}")
    
    print("\n" + "=" * 70 + "\n")
    
    # Simulate power gains (from winning battles)
    game.player_stats["Stark"].power = 5
    game.player_stats["Lannister"].power = 3
    game.player_stats["Baratheon"].power = 2
    
    print("After Battles (power awarded):")
    print("-" * 70)
    for bot_id in bot_ids:
        stats = game.player_stats[bot_id]
        print(f"{bot_id:12} | Territories: {stats.territories:2} | Units: {stats.total_units:2} | Power: {stats.power:2} | Score: {stats.get_score():3}")
    
    print("\n" + "=" * 70 + "\n")
    
    # Show leaderboard
    print("Leaderboard (sorted by score):")
    print("-" * 70)
    leaderboard = game.get_leaderboard()
    for rank, (bot_id, score, territories, units) in enumerate(leaderboard, 1):
        print(f"{rank}. {bot_id:12} | Score: {score:3} | Territories: {territories:2} | Units: {units:2}")
    
    print("\n" + "=" * 70 + "\n")
    
    # Record turn history
    game.record_turn()
    print("Turn History recorded:")
    print("-" * 70)
    print(f"Turn 0 snapshot saved with {len(game.player_stats)} players")
    if game.turn_history:
        last_turn = game.turn_history[-1]
        for bot_id, stats in last_turn['player_stats'].items():
            print(f"  {bot_id:12} | Score: {stats['score']:3} | Territories: {stats['territories']:2}")
