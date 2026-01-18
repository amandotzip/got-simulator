"""
Test supply, crowns, and fortifications
"""
from game_state import Location, LocationType, FortificationType

if __name__ == "__main__":
    print("=== LOCATION RESOURCES & FORTIFICATIONS ===\n")
    
    # Create locations with different configurations
    locations = [
        ("Northern Frontier", FortificationType.NONE, 2),        # No fort, 2 supply
        ("Castle Town", FortificationType.CASTLE, 3),            # Castle, 3 supply
        ("Stronghold Peak", FortificationType.STRONGHOLD, 5),    # Stronghold, 5 supply
    ]
    
    locs = []
    for name, fort_type, max_supply in locations:
        loc = Location(
            name=name,
            location_type=LocationType.LAND,
            owner="Stark",
            max_supply=max_supply,
            fortification=fort_type
        )
        loc.add_supply(max_supply)  # Fill with supply
        loc.add_crowns(10)           # Start with 10 crowns
        locs.append(loc)
    
    print("Location Details:")
    print("-" * 80)
    print(f"{'Location':<20} | {'Fort':<12} | {'Supply':<8} | {'Max':<4} | {'Crowns':<8} | {'Defense':<8}")
    print("-" * 80)
    
    for loc in locs:
        fort_name = loc.fortification.value.upper()
        defense = loc.get_defense_bonus()
        print(f"{loc.name:<20} | {fort_name:<12} | {loc.supply:<8} | {loc.max_supply:<4} | {loc.crowns:<8} | +{defense}")
    
    print("\n" + "=" * 80 + "\n")
    
    # Simulate resource management
    print("After Resource Collection & Spending:")
    print("-" * 80)
    
    # Northern Frontier uses supply
    locs[0].remove_supply(1)
    locs[0].remove_crowns(3)
    
    # Castle Town collects crowns from fortification
    locs[1].add_crowns(2)
    
    # Stronghold produces lots of resources
    locs[2].add_supply(1)  # Try to exceed max
    locs[2].add_crowns(5)
    
    print(f"{'Location':<20} | {'Fort':<12} | {'Supply':<8} | {'Max':<4} | {'Crowns':<8} | {'Defense':<8}")
    print("-" * 80)
    
    for loc in locs:
        fort_name = loc.fortification.value.upper()
        defense = loc.get_defense_bonus()
        print(f"{loc.name:<20} | {fort_name:<12} | {loc.supply:<8} | {loc.max_supply:<4} | {loc.crowns:<8} | +{defense}")
    
    print("\n" + "=" * 80 + "\n")
    
    # Show fortification upgrade
    print("Fortification Upgrades:")
    print("-" * 80)
    
    test_loc = Location(name="Test Keep", location_type=LocationType.LAND, owner="Lannister")
    
    states = [
        FortificationType.NONE,
        FortificationType.CASTLE,
        FortificationType.STRONGHOLD,
    ]
    
    for fort_state in states:
        test_loc.set_fortification(fort_state)
        print(f"State: {fort_state.value:12} | Defense Bonus: +{test_loc.get_defense_bonus()}")
    
    print("\n" + "=" * 80 + "\n")
    
    # Show supply mechanics
    print("Supply Mechanics:")
    print("-" * 80)
    
    supply_loc = Location(name="Supply Depot", max_supply=3)
    
    print(f"Initial supply: {supply_loc.supply}/{supply_loc.max_supply}")
    
    supply_loc.add_supply(2)
    print(f"After +2 supply: {supply_loc.supply}/{supply_loc.max_supply}")
    
    supply_loc.add_supply(2)  # Try to add more than max
    print(f"After +2 more (capped): {supply_loc.supply}/{supply_loc.max_supply}")
    
    supply_loc.remove_supply(1)
    print(f"After -1 supply: {supply_loc.supply}/{supply_loc.max_supply}")
