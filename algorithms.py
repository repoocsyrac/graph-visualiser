
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