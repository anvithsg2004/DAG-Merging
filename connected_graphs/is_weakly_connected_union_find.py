import networkx as nx


def is_weakly_connected_union_find(G):
    """
    Checks if the directed graph G is weakly connected using Union-Find (Disjoint Set Union).
    Args:
        G (nx.DiGraph): A directed graph.
    Returns:
        bool: True if the graph is weakly connected, False otherwise.
    """
    # Convert to undirected graph
    undirected_G = G.to_undirected()
    print("Undirected Graph Edges:")
    print(list(undirected_G.edges()))

    # Initialize Union-Find structure
    parent = {node: node for node in undirected_G.nodes}
    print("\nInitial Parent Mapping:")
    print(parent)

    # Find operation with path compression
    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])  # Path compression
        return parent[node]

    # Union operation
    def union(node1, node2):
        root1, root2 = find(node1), find(node2)
        if root1 != root2:
            parent[root2] = root1
            print(f"Union: {node1} ({root1}) and {node2} ({root2}) -> Updated Parent Mapping:")
            print(parent)

    # Process all edges to perform unions
    print("\nProcessing Edges:")
    for u, v in undirected_G.edges():
        print(f"Processing Edge: ({u}, {v})")
        union(u, v)

    # Check if all nodes have the same root
    root = find(next(iter(undirected_G.nodes)))  # Arbitrary root node
    print("\nFinal Parent Mapping:")
    print(parent)

    all_connected = all(find(node) == root for node in undirected_G.nodes)
    print("\nConnectivity Check:")
    for node in undirected_G.nodes:
        print(f"Node: {node}, Root: {find(node)}")
    print(f"All Nodes Connected? {all_connected}")
    return all_connected


# Example Usage
G = nx.DiGraph()
G.add_edges_from([("A", "B"), ("B", "C"), ("D", "E")])  # Graph with two weakly connected components

is_weakly_connected = is_weakly_connected_union_find(G)
print("\nIs the graph weakly connected?", is_weakly_connected)
