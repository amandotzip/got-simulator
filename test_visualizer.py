"""
Test script to visualize the map
"""
from example import setup_simple_game
from visualizer import MapVisualizer

if __name__ == "__main__":
    print("Setting up game...")
    game, bot_ids = setup_simple_game()
    
    print("Creating visualizer...")
    visualizer = MapVisualizer(game)
    
    print("Generating visualization...")
    visualizer.visualize(title="GOT Game Map - Initial State", 
                        save_path="map_visualization.png")
    
    print("Done!")
