"""
Graph visualizer for the GOT game map
"""
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import networkx as nx
from game_state import GameState, LocationType
from typing import Dict, Tuple


class MapVisualizer:
    """Visualizes the game map as a graph"""
    
    def __init__(self, game_state: GameState):
        self.game_state = game_state
        self.graph = nx.Graph()
        self._build_graph()
    
    def _build_graph(self):
        """Build networkx graph from game state"""
        # Add nodes
        for location in self.game_state.locations.values():
            self.graph.add_node(location.name)
        
        # Add edges (adjacencies)
        for location in self.game_state.locations.values():
            for adjacent_name in location.adjacent_locations:
                self.graph.add_edge(location.name, adjacent_name)
    
    def visualize(self, figsize: Tuple[int, int] = (12, 8), 
                  title: str = "GOT Game Map", save_path: str = None):
        """
        Visualize the map with node colors representing owners
        
        Args:
            figsize: Figure size (width, height)
            title: Title of the visualization
            save_path: Path to save the image (optional)
        """
        fig, ax = plt.subplots(figsize=figsize)
        
        # Use spring layout for better positioning
        pos = nx.spring_layout(self.graph, k=2, iterations=50, seed=42)
        
        # Color mapping for bots
        color_map = {
            "Stark": "#2c3e50",      # Dark gray/blue
            "Lannister": "#f39c12",  # Gold
            "Baratheon": "#3498db",  # Blue
            "Greyjoy": "#34495e",    # Dark gray
            "Tyrell": "#27ae60",     # Green
            "Martell": "#e74c3c",    # Red
            "Targaryen": "#9b59b6",  # Purple
        }
        
        # Get node colors and sizes
        node_colors = []
        node_sizes = []
        
        for node in self.graph.nodes():
            location = self.game_state.locations[node]
            owner = location.owner
            
            # Color by owner
            node_colors.append(color_map.get(owner, "#95a5a6"))
            
            # Size by total unit count (with minimum size)
            total_units = location.get_total_units()
            size = 300 + (total_units * 100)
            node_sizes.append(size)
        
        # Draw land nodes (circles)
        land_nodes = [node for node in self.graph.nodes() 
                     if self.game_state.locations[node].location_type == LocationType.LAND]
        land_colors = [node_colors[list(self.graph.nodes()).index(node)] for node in land_nodes]
        land_sizes = [node_sizes[list(self.graph.nodes()).index(node)] for node in land_nodes]
        
        nx.draw_networkx_nodes(
            self.graph, pos,
            nodelist=land_nodes,
            node_color=land_colors,
            node_size=land_sizes,
            ax=ax,
            alpha=0.9,
            edgecolors='black',
            linewidths=2,
            node_shape='o'
        )
        
        # Draw sea nodes (squares)
        sea_nodes = [node for node in self.graph.nodes() 
                    if self.game_state.locations[node].location_type == LocationType.SEA]
        sea_colors = [node_colors[list(self.graph.nodes()).index(node)] for node in sea_nodes]
        sea_sizes = [node_sizes[list(self.graph.nodes()).index(node)] for node in sea_nodes]
        
        if sea_nodes:
            nx.draw_networkx_nodes(
                self.graph, pos,
                nodelist=sea_nodes,
                node_color=sea_colors,
                node_size=sea_sizes,
                ax=ax,
                alpha=0.9,
                edgecolors='cyan',
                linewidths=3,
                node_shape='s'
            )
        
        # Draw edges
        nx.draw_networkx_edges(
            self.graph, pos,
            width=2,
            alpha=0.6,
            ax=ax,
            edge_color='gray'
        )
        
        # Draw labels
        nx.draw_networkx_labels(
            self.graph, pos,
            font_size=9,
            font_weight='bold',
            ax=ax
        )
        
        # Add unit counts as text
        unit_labels = {}
        for node in self.graph.nodes():
            location = self.game_state.locations[node]
            total = location.get_total_units()
            unit_labels[node] = f"{total}"
        
        # Draw unit counts slightly offset from nodes
        label_pos = {k: (v[0], v[1] - 0.1) for k, v in pos.items()}
        for node, (x, y) in label_pos.items():
            ax.text(x, y, unit_labels[node], 
                   ha='center', va='center',
                   fontsize=8, color='white', weight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', 
                            facecolor='black', alpha=0.7))
        
        ax.set_title(title, fontsize=16, fontweight='bold', pad=20)
        ax.axis('off')
        
        # Add legend
        from matplotlib.patches import Patch
        legend_elements = [
            Patch(facecolor=color_map[bot], edgecolor='black', label=bot)
            for bot in ["Stark", "Lannister", "Baratheon", "Greyjoy", "Tyrell", "Martell"]
            if bot in [loc.owner for loc in self.game_state.locations.values()]
        ]
        ax.legend(handles=legend_elements, loc='upper left', fontsize=10)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=150, bbox_inches='tight')
            print(f"Map saved to {save_path}")
        
        plt.show()
    
    def visualize_turn(self, turn_number: int, figsize: Tuple[int, int] = (12, 8),
                       save_path: str = None):
        """Visualize the map at a specific turn"""
        title = f"GOT Game Map - Turn {turn_number}"
        self.visualize(figsize=figsize, title=title, save_path=save_path)
