import networkx as nx

def is_weakly_connected_dfs_bfs(G):
    """
    Checks if the directed graph G is weakly connected by converting it to an undirected graph
    and performing DFS.
    Args:
        G (nx.DiGraph): A directed graph.
    Returns:
        bool: True if the graph is weakly connected, False otherwise.
    """
    undirected_G = G.to_undirected()  # Convert to undirected graph
    print("Undirected Graph Edges:")
    print(list(undirected_G.edges()))

    # Perform DFS from an arbitrary starting node
    start_node = next(iter(undirected_G.nodes))  # Get an arbitrary node
    print(f"\nStarting DFS from Node: {start_node}")
    visited_nodes = set()

    def dfs(node):
        visited_nodes.add(node)
        print(f"Visiting Node: {node}")
        for neighbor in undirected_G.neighbors(node):
            if neighbor not in visited_nodes:
                print(f"Exploring Neighbor: {neighbor} of Node: {node}")
                dfs(neighbor)

    dfs(start_node)

    # Check if all nodes were visited
    all_nodes_reachable = len(visited_nodes) == len(G.nodes)
    print("\nVisited Nodes:", visited_nodes)
    print(f"All Nodes Reachable? {all_nodes_reachable}")
    return all_nodes_reachable


# Example Usage
G = nx.DiGraph()
G.add_edges_from([("A", "B"), ("B", "C"), ("D", "E")])  # Graph with two weakly connected components

is_weakly_connected = is_weakly_connected_dfs_bfs(G)
print("\nIs the graph weakly connected?", is_weakly_connected)
