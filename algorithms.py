
import heapq
import networkx as nx

# Finds the shortest path from start_node to target_node using Dijkstra's
def dijkstra(graph, start_node, target_node):
    distances = {node: float('inf') for node in graph.nodes}
    distances[start_node] = 0
    predecessors = {}  # Shortest path tree
    pq = [(0, start_node)] 

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node == target_node:
            break

        for neighbor in graph.neighbors(current_node):
            weight = graph[current_node][neighbor].get("weight", 1) 
            new_distance = current_distance + weight

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                predecessors[neighbor] = current_node
                heapq.heappush(pq, (new_distance, neighbor))

    # Reconstruct shortest path
    path = []
    node = target_node
    while node in predecessors:
        path.insert(0, node)
        node = predecessors[node]
    
    if path:
        path.insert(0, start_node)

    return path, distances.get(target_node, float('inf'))

# Finds minimum spanning tree
def find_mst(graph):
    return nx.minimum_spanning_tree(graph)

# Finds proper vertex colouring
def find_vertex_coloring(graph):
    return nx.coloring.greedy_color(graph, strategy="largest_first")

# Finds Euler tour
def find_eulerian_tour(graph):
    if not nx.is_eulerian(graph):
        return None  # No Eulerian tour exists
    return list(nx.eulerian_circuit(graph))

# Finds a Hamilton cycle using TSP heuristic
def find_hamiltonian_cycle(graph):
    cycle = nx.approximation.traveling_salesman_problem(graph, cycle=True)
    if len(set(cycle)) < len(graph.nodes):  # if not all nodes are visited
        return None  # then no Hamiltonian cycle exists
    return cycle

# Finds maximum matching
def find_maximum_matching(graph):
    return nx.max_weight_matching(graph, maxcardinality=True)