import tkinter as tk
import networkx as nx
from algorithms import dijkstra
import time
import random
from tkinter import messagebox
from algorithms import find_eulerian_tour
from algorithms import find_hamiltonian_cycle
from algorithms import find_maximum_matching
from algorithms import find_mst
from algorithms import find_vertex_coloring

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

        # Initialize dragging attributes
        self.is_dragging = False  
        self.dragging_node = None  
        self.start_x = 0  
        self.start_y = 0  
        self.drag_start_time = 0  
        
        self.canvas.bind("<Button-1>", self.left_click)
        self.canvas.bind("<Button-3>", self.add_edge)
        self.canvas.bind("<B1-Motion>", self.handle_drag)

        # Algorithm buttons
        self.control_frame = tk.Frame(root, width=800, height=100, bg="NavajoWhite3")
        self.control_frame.pack(side=tk.BOTTOM, fill="both", expand=True)
        self.select_nodes_button = tk.Button(self.control_frame, text="Run Dijkstra", command=self.toggle_select_mode)
        self.select_nodes_button.pack(side=tk.LEFT)
        self.mst_button = tk.Button(self.control_frame, text="Find Minimum Spanning Tree", command=self.visualise_mst)
        self.mst_button.pack(side=tk.LEFT)
        self.euler_button = tk.Button(self.control_frame, text="Find Euler Tour", command=self.visualise_eulerian_tour)
        self.euler_button.pack(side=tk.LEFT)
        self.hamilton_button = tk.Button(self.control_frame, text="Find Hamilton Cycle", command=self.visualise_hamiltonian_cycle)
        self.hamilton_button.pack(side=tk.LEFT)
        self.colouring_button = tk.Button(self.control_frame, text="Find Proper Colouring", command=self.visualise_vertex_coloring)
        self.colouring_button.pack(side=tk.LEFT)

        # Reset buttons
        self.unhighlight_button = tk.Button(self.control_frame, text="Unhighlight Path", command=self.unhighlight_path)
        self.unhighlight_button.pack(side=tk.RIGHT)

        self.clear_edges_button = tk.Button(self.control_frame, text="Delete All Edges", command=self.clear_edges)
        self.clear_edges_button.pack(side=tk.RIGHT)

        self.clear_all_button = tk.Button(self.control_frame, text="Delete All Nodes & Edges", command=self.clear_all)
        self.clear_all_button.pack(side=tk.RIGHT)

        # Predefined graph buttons
        self.complete_graph_btn = tk.Button(self.control_frame, text="Complete Graph (Kn)", command=lambda: self.create_complete_graph(5))
        self.complete_graph_btn.pack(side=tk.LEFT)

        #self.grid_graph_btn = tk.Button(self.control_frame, text="Grid Graph (3x3)", command=lambda: self.create_grid_graph(3, 3))
        #self.grid_graph_btn.pack(side=tk.LEFT)

        #self.cycle_graph_btn = tk.Button(self.control_frame, text="Cycle Graph (Cn)", command=lambda: self.create_cycle_graph(6))
        #self.cycle_graph_btn.pack(side=tk.LEFT)

    def left_click(self, event):
        if self.selecting_nodes:
            self.select_node(event)
        else:
            self.is_dragging = False
            self.start_x = event.x
            self.start_y = event.y
            self.drag_start_time = time.time()

            # Check if user clicked an existing node
            for node_id, (x, y) in self.nodes.items():
                if abs(event.x - x) < 15 and abs(event.y - y) < 15:
                    self.start_drag(event, node_id)
                    return  # don't add a new node

            # If no node was clicked, add a new node
            self.root.after(150, lambda: self.add_node(event))

    # Add node where left mouse is pressed
    def add_node(self, event):
        if self.selecting_nodes:
            return
        
        if self.is_dragging:
            self.is_dragging = False
            return
            
        node_id = len(self.nodes) + 1
        self.nodes[node_id] = (event.x, event.y)
        self.graph.add_node(node_id)
        node = self.canvas.create_oval(event.x-10, event.y-10, event.x+10, event.y+10, fill="medium blue", tags=f"node{node_id}")
        self.canvas.create_text(event.x, event.y, text=str(node_id), fill="white", font=("Arial", 12), tags=(f"label{node_id}", "label"))
        self.make_draggable(node_id)

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
            self.canvas.create_line(x1, y1, x2, y2, fill="red4", tags=(f"edge{self.selected_node}-{clicked_node}", "edge"))

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
            self.show_error("No path exists between these nodes!")
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

    # Removes all nodes and edges from graph
    def clear_all(self):
        self.canvas.delete("all") 
        self.nodes = {}
        self.edges = []
        self.graph.clear()

    # Makes node draggable
    def make_draggable(self, node_id):
        self.canvas.tag_bind(f"node{node_id}", "<ButtonPress-1>", lambda event, n=node_id: self.start_drag(event, n))
        self.canvas.tag_bind(f"node{node_id}", "<B1-Motion>", lambda event, n=node_id: self.drag_node(event, n))

    # Starts dragging a node
    def start_drag(self, event, node_id):
        self.dragging_node = node_id
        self.start_x = event.x
        self.start_y = event.y
        self.drag_start_time = time.time()  # Record when the drag starts
        self.is_dragging = False
    

    def handle_drag(self, event):
        if self.dragging_node is None:
            return

        dx = abs(event.x - self.start_x)
        dy = abs(event.y - self.start_y)

        # Check if movement is significant
        if dx > 5 or dy > 5:
            self.is_dragging = True

        # Move the node
        self.nodes[self.dragging_node] = (event.x, event.y)
        self.canvas.coords(f"node{self.dragging_node}", event.x-10, event.y-10, event.x+10, event.y+10)
        self.canvas.coords(f"label{self.dragging_node}", event.x, event.y)

        # Update all connected edges
        for neighbor in self.graph.neighbors(self.dragging_node):
            x1, y1 = self.nodes[self.dragging_node]
            x2, y2 = self.nodes[neighbor]

            edge_tag = f"edge{self.dragging_node}-{neighbor}" if self.canvas.find_withtag(f"edge{self.dragging_node}-{neighbor}") else f"edge{neighbor}-{self.dragging_node}"
            self.canvas.coords(edge_tag, x1, y1, x2, y2)

            #weight_tag = f"weight{self.dragging_node}-{neighbor}" if self.canvas.find_withtag(f"weight{self.dragging_node}-{neighbor}") else f"weight{neighbor}-{self.dragging_node}"
            #self.canvas.coords(weight_tag, (x1 + x2) / 2, (y1 + y2) / 2)


    def create_complete_graph(self, n):
        self.clear_all()

        # Randomly distribute nodes
        for i in range(n):
            x, y = random.randint(100, 700), random.randint(100, 400)
            self.nodes[i+1] = (x, y)
            self.graph.add_node(i+1)
            self.canvas.create_oval(x-10, y-10, x+10, y+10, fill="medium blue", tags=f"node{i+1}")
            self.canvas.create_text(x, y, text=str(i+1), fill="white", font=("Arial", 12), tags=(f"label{i+1}", "label"))

        # Connect all nodes
        for i in self.nodes:
            for j in self.nodes:
                if i < j:
                    #weight = random.randint(1, 10)  # Random weight
                    #self.graph.add_edge(i, j, weight=weight)
                    self.graph.add_edge(i, j)
                    x1, y1 = self.nodes[i]
                    x2, y2 = self.nodes[j]
                    self.canvas.create_line(x1, y1, x2, y2, fill="black", tags=f"edge{i}-{j}")
                    #self.canvas.create_text((x1+x2)/2, (y1+y2)/2, text=str(weight), font=("Arial", 10), tags=f"weight{i}-{j}")


    def visualise_mst(self):
        mst = find_mst(self.graph)
        for u, v in mst.edges:
            x1, y1 = self.nodes[u]
            x2, y2 = self.nodes[v]
            self.canvas.create_line(x1, y1, x2, y2, fill="SpringGreen2", width=2, tags=f"mst{u}-{v}")
        
    def visualise_vertex_coloring(self):
        colors = find_vertex_coloring(self.graph)
        color_palette = ["red", "blue", "green", "yellow", "orange", "purple"]

        for node, color_index in colors.items():
            self.canvas.itemconfig(f"node{node}", fill=color_palette[color_index % len(color_palette)])

    def visualise_eulerian_tour(self):
        tour = find_eulerian_tour(self.graph)
        if tour is None:
            self.show_error("No Eulerian Tour exists!")
            return

        for (u, v) in tour:
            x1, y1 = self.nodes[u]
            x2, y2 = self.nodes[v]
            self.canvas.create_line(x1, y1, x2, y2, fill="orange", width=2, tags=f"eulerian{u}-{v}")

    def visualise_hamiltonian_cycle(self):
        cycle = find_hamiltonian_cycle(self.graph)
        if cycle is None:
            self.show_error("No Hamiltonian Cycle exists!")
            return

        for i in range(len(cycle) - 1):
            x1, y1 = self.nodes[cycle[i]]
            x2, y2 = self.nodes[cycle[i+1]]
            self.canvas.create_line(x1, y1, x2, y2, fill="cyan", width=2, tags=f"hamiltonian{cycle[i]}-{cycle[i+1]}")

    def visualise_maximum_matching(self):
        matching = find_maximum_matching(self.graph)

        for u, v in matching:
            x1, y1 = self.nodes[u]
            x2, y2 = self.nodes[v]
            self.canvas.create_line(x1, y1, x2, y2, fill="pink", width=3, tags=f"matching{u}-{v}")

    def show_error(self, message):
        messagebox.showerror("Error", message)