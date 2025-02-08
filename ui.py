import tkinter as tk
import networkx as nx
from algorithms import dijkstra

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=800, height=500, bg="NavajoWhite")
        self.canvas.pack()

        self.graph = nx.Graph()
        self.nodes = {}
        self.edges = []

        self.selected_nodes = []  # Store start & target nodes
        self.selecting_nodes = False  # Toggle selection mode
        
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.add_edge)

        # Algorithm buttons
        self.control_frame = tk.Frame(root, width=800, height=100, bg="NavajoWhite3")
        self.control_frame.pack(side=tk.BOTTOM, fill="both", expand=True)
        self.select_nodes_button = tk.Button(self.control_frame, text="Run Dijkstra", command=self.toggle_select_mode)
        self.select_nodes_button.pack(side=tk.LEFT)
        self.dijkstra_button = tk.Button(self.control_frame, text="-", command=self.run_dijkstra)
        self.dijkstra_button.pack(side=tk.LEFT)

        # Reset buttons
        self.unhighlight_button = tk.Button(self.control_frame, text="Unhighlight Path", command=self.unhighlight_path)
        self.unhighlight_button.pack(side=tk.RIGHT)

        self.clear_edges_button = tk.Button(self.control_frame, text="Delete All Edges", command=self.clear_edges)
        self.clear_edges_button.pack(side=tk.RIGHT)

        self.clear_all_button = tk.Button(self.control_frame, text="Delete All Nodes & Edges", command=self.clear_all)
        self.clear_all_button.pack(side=tk.RIGHT)

    def left_click(self, event):
        if self.selecting_nodes:
            self.select_node(event)
        else:
            self.add_node(event)

    # Add node where left mouse is pressed
    def add_node(self, event):
        if self.selecting_nodes:
            return
        
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
            self.canvas.create_line(x1, y1, x2, y2, fill="red4", tags="edge")

        # Reset the selected node
        self.selected_node = None

    

    # Runs Dijkstra's and highlights shortest path
    def run_dijkstra(self):
        if len(self.selected_nodes) != 2:
            print("You must select two nodes first.")
            return

        start_node, target_node = self.selected_nodes
        path, distance = dijkstra(self.graph, start_node, target_node)

        if not path:
            print(f"No path found from {start_node} to {target_node}")
            return

        print(f"Shortest path from {start_node} to {target_node}: {path} (Distance: {distance})")

        # Highlight shortest path
        for i in range(len(path) - 1):
            node1, node2 = path[i], path[i+1]
            x1, y1 = self.nodes[node1]
            x2, y2 = self.nodes[node2]
            self.canvas.create_line(x1, y1, x2, y2, fill="SpringGreen2", width=3, tags="highlight")
        
        self.selected_nodes = []


    # Toggles node selection mode for dijkstras
    def toggle_select_mode(self):
        self.selecting_nodes = not self.selecting_nodes

        if self.selecting_nodes:
            self.select_nodes_button.config(text="Selecting... (Click 2 Nodes)")
        else:
            self.select_nodes_button.config(text="Run Dijkstra")

        self.selected_nodes = []

    # Selects a start and target node when in selection mode
    def select_node(self, event):
        if not self.selecting_nodes:
            return

        for node_id, (x, y) in self.nodes.items():
            if abs(event.x - x) < 15 and abs(event.y - y) < 15:
                if node_id not in self.selected_nodes:
                    self.selected_nodes.append(node_id)
                    self.canvas.itemconfig(f"node{node_id}", fill="cyan")  # Highlight 

                if len(self.selected_nodes) == 2:
                    self.run_dijkstra()
                    self.selecting_nodes = False
                    self.select_nodes_button.config(text="Run Dijkstra")
                break

    # Unhighlights path
    def unhighlight_path(self):
        self.canvas.delete("highlight")
        self.selected_nodes = []
        for node_id in self.nodes:
            self.canvas.itemconfig(f"node{node_id}", fill="medium blue")  # Change back to default


    # Removes all edges from graph
    def clear_edges(self):
        self.canvas.delete("edge")
        self.edges = [] 
        self.graph.clear_edges()

    def clear_all(self):
        self.canvas.delete("all") 
        self.nodes = {}
        self.edges = []
        self.graph.clear()



    