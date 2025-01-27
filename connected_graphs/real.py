import networkx as nx

def Create_nx_dg(dependency_list):
    # Create a directed graph
    G = nx.DiGraph()

    # Add edges based on the dependency list
    for node, dependents in dependency_list.items():
        for dependent in dependents:
            G.add_edge(dependent, node)

    return G

# Conversion to Undirected Graph with DFS/BFS
def is_weakly_connected_dfs_bfs(G):
    undirected_G = G.to_undirected()  # Ignore edge directions
    # Perform DFS from an arbitrary node and check reachability
    start_node = next(iter(undirected_G.nodes))
    visited_nodes = set()

    def dfs(node):
        visited_nodes.add(node)
        for neighbor in undirected_G.neighbors(node):
            if neighbor not in visited_nodes:
                dfs(neighbor)

    dfs(start_node)
    return len(visited_nodes) == len(G.nodes)  # Check if the undirected version is connected

# Floyd-Warshall Algorithm
def is_weakly_connected_floyd_warshall(G):
    # Convert G to undirected
    undirected_G = G.to_undirected()
    # Run Floyd-Warshall to get shortest paths in undirected version
    lengths = nx.floyd_warshall(undirected_G)
    # Check for infinite distances
    for source, targets in lengths.items():
        for target, distance in targets.items():
            if distance == float('inf'):
                return False  # Found a pair of nodes that are not connected
    return True  # All node pairs are reachable


# Union-Find Algorithm (Disjoint Set Union)
def is_weakly_connected_union_find(G):
    undirected_G = G.to_undirected()
    parent = {node: node for node in undirected_G.nodes}

    def find(node):
        if parent[node] != node:
            parent[node] = find(parent[node])
        return parent[node]

    def union(node1, node2):
        root1, root2 = find(node1), find(node2)
        if root1 != root2:
            parent[root2] = root1

    for u, v in undirected_G.edges():
        union(u, v)

    # Check if all nodes have the same root
    root = find(next(iter(undirected_G.nodes)))
    return all(find(node) == root for node in undirected_G.nodes)

# Main Execution
if __name__ == "__main__":
    dependency_list1 = {
        'A': [],
        'B': ['A'],
        'C': ['A'],
        'D': ['B', 'C'],
    }
    dependency_list2 = {
        'A': ['D'],
        'B': ['A'],
        'C': ['A'],
        'D': ['B', 'C'],
    }
    dependency_list3 = {
        'A': [],
        'B': ['A'],
        'C': ['A'],
        'D': ['B', 'C'],
        'X': ['Y'],
        'Y': ['X']
    }
    L = [dependency_list1, dependency_list2, dependency_list3]
    for i in L:

        G = Create_nx_dg(i)

        # Check weak connectivity with each algorithm
        print("Weakly Connected (DFS/BFS):", is_weakly_connected_dfs_bfs(G))
        print("Weakly Connected (Floyd-Warshall):", is_weakly_connected_floyd_warshall(G))
        print("Weakly Connected (Union-Find):", is_weakly_connected_union_find(G))
        print()
        print()
        print()