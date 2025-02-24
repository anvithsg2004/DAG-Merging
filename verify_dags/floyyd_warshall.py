import networkx as nx


def is_dag_transitive_reduction(G):
    closure = nx.transitive_closure(G)
    for node in closure.nodes():
        if node in closure.neighbors(node):
            return False
    return True


def is_dag_floyd_warshall(G):
    """
    Checks if the directed graph G is a Directed Acyclic Graph (DAG) using the Floyd-Warshall Algorithm.
    Logs intermediate values during the execution.
    Args:
        G (nx.DiGraph): A directed graph.
    Returns:
        bool: True if the graph is a DAG (no cycles), False otherwise.
    """
    nodes = list(G.nodes())
    n = len(nodes)
    reach = [[0] * n for _ in range(n)]  # Reachability matrix

    print("Initial Reachability Matrix:")
    for row in reach:
        print(row)

    # Populate reachability matrix based on direct edges
    for i, u in enumerate(nodes):
        for v in G.neighbors(u):
            j = nodes.index(v)
            reach[i][j] = 1

    print("\nReachability Matrix After Initialization (Direct Edges):")
    for row in reach:
        print(row)

    # Apply Floyd-Warshall algorithm to compute reachability
    for k in range(n):
        print(f"\nConsidering Intermediate Node: {nodes[k]}")
        for i in range(n):
            for j in range(n):
                if reach[i][k] and reach[k][j]:
                    print(f"Path Found: {nodes[i]} -> {nodes[k]} -> {nodes[j]}")
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])

        print(f"\nReachability Matrix After Considering Node {nodes[k]}:")
        for row in reach:
            print(row)

    # Check for cycles (diagonal elements in the reachability matrix)
    for i in range(n):
        if reach[i][i] == 1:
            print(f"\nCycle detected at Node: {nodes[i]} (reach[{nodes[i]}][{nodes[i]}] = 1)")
            return False

    print("\nNo cycles detected. The graph is a DAG.")
    return True


# Example Usage
G = nx.DiGraph()
G.add_edges_from([("A", "B"), ("B", "C"), ("C", "A"), ("D", "E")])  # Graph with a cycle

is_dag = is_dag_floyd_warshall(G)
print("\nIs the graph a DAG?", is_dag)
