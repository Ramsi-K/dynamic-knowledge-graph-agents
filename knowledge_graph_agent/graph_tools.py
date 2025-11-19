import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Dict, Any
from datetime import datetime
import os

class KnowledgeBase:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_triplet(self, subject: str, predicate: str, object_: str):
        self.graph.add_edge(subject, object_, relation=predicate)

    def reset(self):
        self.graph.clear()

    def get_state(self) -> Dict[str, Any]:
        return {
            "nodes": list(self.graph.nodes()),
            "edges": [
                {"source": u, "target": v, "relation": d["relation"]}
                for u, v, d in self.graph.edges(data=True)
            ]
        }

# Global Knowledge Base instance
kb = KnowledgeBase()

def add_triplet(subject: str, predicate: str, object_: str) -> str:
    """
    Adds a fact (triplet) to the Knowledge Graph.
    
    Args:
        subject: The starting entity (e.g., "Harry Potter").
        predicate: The relationship (e.g., "is friend of").
        object_: The target entity (e.g., "Ron Weasley").
        
    Returns:
        A confirmation message.
    """
    kb.add_triplet(subject, predicate, object_)
    return f"Added: ({subject}) -[{predicate}]-> ({object_})"

def get_graph_state() -> Dict[str, Any]:
    """
    Retrieves the current state of the Knowledge Graph (nodes and edges).
    
    Returns:
        A dictionary containing a list of 'nodes' and 'edges'.
    """
    return kb.get_state()

def save_graph_image() -> str:
    """
    Generates a visualization of the current knowledge graph and saves it as a PNG file.
    The file is saved in the 'examples/' directory with a unique timestamp.
    Returns the path to the saved image.
    """
    G = kb.graph
    
    if G.number_of_nodes() == 0:
        return "Graph is empty. Nothing to visualize."
        
    plt.figure(figsize=(12, 8))
    pos = nx.spring_layout(G, k=0.5) # Removed iterations=50 as it's not in the new snippet
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_size=2000, node_color="lightblue", alpha=0.9)
    nx.draw_networkx_labels(G, pos, font_size=10, font_weight="bold")
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color="gray", arrows=True, arrowsize=20)
    edge_labels = nx.get_edge_attributes(G, "relation")
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    # Ensure examples directory exists
    os.makedirs("examples", exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"examples/graph_{timestamp}.png"
    
    plt.title("Knowledge Graph Visualization")
    plt.axis("off") # Keep axis off for cleaner visualization
    plt.tight_layout() # Keep tight layout
    plt.savefig(filename)
    plt.close()
    
    return filename
