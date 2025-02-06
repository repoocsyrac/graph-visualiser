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

    # Add node where left mouse is pressed
    def add_node(self, event):
        node_id = len(self.nodes) + 1
        self.nodes[node_id] = (event.x, event.y)
        self.graph.add_node(node_id)
        self.canvas.create_oval(event.x-10, event.y-10, event.x+10, event.y+10, fill="medium blue", tags=f"node{node_id}")
        self.canvas.create_text(event.x, event.y, text=str(node_id), fill="white", font=("Arial", 12))

    