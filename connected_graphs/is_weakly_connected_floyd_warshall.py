import networkx as nx

def is_weakly_connected_floyd_warshall(G):
    """
    Checks if the directed graph G is weakly connected by running Floyd-Warshall on its undirected version.
    Args:
        G (nx.DiGraph): A directed graph.
    Returns:
        bool: True if the graph is weakly connected, False otherwise.
    """
    # Convert G to undirected
    undirected_G = G.to_undirected()
    print("Undirected Graph Edges:")
    print(list(undirected_G.edges()))

    # Run Floyd-Warshall algorithm to compute shortest path lengths
    print("\nRunning Floyd-Warshall Algorithm...")
    lengths = dict(nx.floyd_warshall(undirected_G))  # Returns shortest paths as a nested dictionary

    print("\nShortest Path Lengths:")
    for source, targets in lengths.items():
        print(f"From Node {source}:")
        for target, distance in targets.items():
            print(f"  To Node {target}: {distance}")

    # Check for infinite distances
    print("\nChecking for Disconnected Node Pairs:")
    for source, targets in lengths.items():
        for target, distance in targets.items():
            if distance == float('inf'):
                print(f"Disconnected Pair Found: {source} -> {target} (Distance: {distance})")
                return False  # Found a pair of nodes that are not connected

    print("All Node Pairs are Reachable. The graph is weakly connected.")
    return True


# Example Usage
G = nx.DiGraph()
G.add_edges_from([("A", "B"), ("B", "C"), ("D", "E")])  # Graph with two weakly connected components

is_weakly_connected = is_weakly_connected_floyd_warshall(G)
print("\nIs the graph weakly connected?", is_weakly_connected)
