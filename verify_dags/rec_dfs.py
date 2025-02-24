import networkx as nx


def is_dag_dfs_rec_stack(G):
    """
    Checks if the directed graph G is a Directed Acyclic Graph (DAG) using DFS and recursion stack.
    Args:
        G (nx.DiGraph): A directed graph.
    Returns:
        bool: True if the graph is a DAG (no cycles), False otherwise.
    """
    visited = set()
    rec_stack = set()

    def dfs(node):
        print(f"Visiting Node: {node}")
        if node not in visited:
            visited.add(node)
            rec_stack.add(node)
            print(f"Visited: {visited}")
            print(f"Recursion Stack: {rec_stack}")

            for neighbor in G.neighbors(node):
                print(f"Exploring Neighbor: {neighbor} of Node: {node}")
                if neighbor not in visited:
                    print(f"Neighbor {neighbor} not visited. Recursing...")
                    if dfs(neighbor):
                        print(f"Cycle detected via Neighbor: {neighbor}")
                        return True
                elif neighbor in rec_stack:
                    print(f"Cycle detected! Neighbor {neighbor} is in the Recursion Stack.")
                    return True

            rec_stack.remove(node)
            print(f"Backtracking from Node: {node}. Updated Recursion Stack: {rec_stack}")
        return False

    print("Starting DFS for Cycle Detection:")
    for node in G.nodes():
        if node not in visited:
            print(f"\nStarting DFS from Node: {node}")
            if dfs(node):
                print(f"Cycle detected starting from Node: {node}")
                return False
    print("No cycles detected. The graph is a DAG.")
    return True


# Example Usage
G = nx.DiGraph()
G.add_edges_from([("A", "B"), ("B", "C"), ("C", "A"), ("D", "E")])  # Graph with a cycle

is_dag = is_dag_dfs_rec_stack(G)
print("\nIs the graph a DAG?", is_dag)
