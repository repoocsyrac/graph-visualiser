import tkinter as tk
import networkx as nx

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=500, bg="linen")
        self.canvas.pack()

        self.graph = nx.Graph()
        self.nodes = {}
        self.edges = []
        
        self.canvas.bind("<Button-1>", self.add_node)
        self.canvas.bind("<Button-3>", self.add_edge)

    # Add node where left mouse is pressed
    def add_node(self, event):
        node_id = len(self.nodes) + 1
        self.nodes[node_id] = (event.x, event.y)
        self.graph.add_node(node_id)
        self.canvas.create_oval(event.x-10, event.y-10, event.x+10, event.y+10, fill="medium blue", tags=f"node{node_id}")
        self.canvas.create_text(event.x, event.y, text=str(node_id), fill="white", font=("Arial", 12))

    # Add edge between 2 nodes when right mouse is pressed
    def add_edge(self, event):
        clicked_node = None
        # Find which node was clicked
        for node_id, (x, y) in self.nodes.items():
            if abs(event.x - x) < 15 and abs(event.y - y) < 15:
                clicked_node = node_id
                break

        if clicked_node is None:
            return 

        # If no selected node, set the first selected node
        if not hasattr(self, "selected_node") or self.selected_node is None:
            self.selected_node = clicked_node
            return

        # If a second node was clicked, create edge
        if self.selected_node != clicked_node:
            self.graph.add_edge(self.selected_node, clicked_node)
            self.edges.append((self.selected_node, clicked_node))
            # Draw the edge
            x1, y1 = self.nodes[self.selected_node]
            x2, y2 = self.nodes[clicked_node]
            self.canvas.create_line(x1, y1, x2, y2, fill="red4")

        # Reset the selected node
        self.selected_node = None


    