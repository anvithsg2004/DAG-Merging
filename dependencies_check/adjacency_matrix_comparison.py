import networkx as nx
import numpy as np
import copy
import itertools

def adjacency_matrix_comparison(graphs):
    """
    Compares adjacency matrices of multiple graphs to detect discrepancies.
    Args:
        graphs (list of nx.DiGraph): List of directed graphs.
    Returns:
        dict: Dictionary of nodes with discrepancies.
    """
    discrepancies = {}
    # Collect all node names across graphs
    node_names = set(itertools.chain(*[G.nodes for G in graphs]))
    node_list = sorted(node_names)  # Ensure consistent node ordering
    print("Node List (sorted):", node_list)

    adj_matrices = []

    # Generate adjacency matrices for all graphs
    for idx, G in enumerate(graphs, start=1):
        G_copy = copy.deepcopy(G)
        missing_nodes = set(node_list) - set(G_copy.nodes())
        if missing_nodes:
            print(f"Graph {idx}: Adding missing nodes {missing_nodes}")
        G_copy.add_nodes_from(missing_nodes)
        adj_matrix = nx.to_numpy_array(G_copy, nodelist=node_list)
        adj_matrices.append(adj_matrix)
        print(f"Adjacency Matrix for Graph {idx}:\n{adj_matrix}")

    # Build node index mapping
    node_indices = {node: idx for idx, node in enumerate(node_list)}
    print("\nNode Indices Mapping:", node_indices)

    # Compare adjacency matrices column by column
    for node in node_list:
        idx = node_indices[node]
        columns = []
        print(f"\nChecking Node: {node} (Index: {idx})")
        for graph_idx, adj_matrix in enumerate(adj_matrices, start=1):
            column = adj_matrix[:, idx]
            if np.any(column):
                columns.append(column)
            print(f"Graph {graph_idx} Column for Node {node}:\n{column}")

        if not all(np.array_equal(columns[0], col) for col in columns):
            discrepancies[node] = "Adjacency matrix discrepancy found"
            print(f"Discrepancy Found for Node {node}: {columns}")
        else:
            print(f"No Discrepancy for Node {node}: {columns}")

    return discrepancies

def create_nx_dg(dependency_list):
    G = nx.DiGraph()
    for node, dependents in dependency_list.items():
        G.add_node(node)  # Ensure all nodes are added
        for dependent in dependents:
            G.add_edge(dependent, node)
    return G


# Example Usage
# Example Usage
dependency_list1 = {'A': [], 'B': ['A'], 'C': ['B'], 'D': ['C']}
dependency_list2 = {'A': [], 'B': ['A'], 'X': ['B'], 'Y': ['C', 'X'], 'C': ['B'], 'Z': ['Y']}
# Create directed graphs from dependency lists

G1 = create_nx_dg(dependency_list1)
G2 = create_nx_dg(dependency_list2)
discrepancies = adjacency_matrix_comparison([G1, G2])
print("\nDiscrepancies:", discrepancies)
