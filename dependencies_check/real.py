import networkx as nx
import hashlib
import itertools
from collections import defaultdict
import numpy as np
import copy


def create_nx_dg(dependency_list):
    G = nx.DiGraph()
    for node, dependents in dependency_list.items():
        G.add_node(node)  # Ensure all nodes are added
        for dependent in dependents:
            G.add_edge(dependent, node)
    return G

def build_in_degree_map(G):
    in_degree_map = {}
    for node in G.nodes:
        in_degree_map[node] = set(G.predecessors(node))
    return in_degree_map



# In-Degree Similarity Check
def in_degree_similarity_check(graphs):
    discrepancies = {}
    all_in_degree_maps = [build_in_degree_map(G) for G in graphs]
    node_names = set(itertools.chain(*[G.nodes for G in graphs]))
    for node in node_names:
        in_degree_sets = []
        for in_degree_map in all_in_degree_maps:
            in_degree_set = in_degree_map.get(node, set())
            if in_degree_set != set():
                in_degree_sets.append(in_degree_set)
        if not all(x == in_degree_sets[0] for x in in_degree_sets):
            discrepancies[node] = "In-degree similarity discrepancy found"
    return discrepancies



# Adjacency Matrix Comparison
def adjacency_matrix_comparison(graphs):
    discrepancies = {}
    # Collect all node names across all graphs
    node_names = set(itertools.chain(*[G.nodes for G in graphs]))
    node_list = sorted(node_names)
    adj_matrices = []
    for G in graphs:
        G_copy = copy.deepcopy(G)
        missing_nodes = set(node_list) - set(G_copy.nodes())
        G_copy.add_nodes_from(missing_nodes)
        adj_matrix = nx.to_numpy_array(G_copy, nodelist=node_list)
        adj_matrices.append(adj_matrix)
    node_indices = {node: idx for idx, node in enumerate(node_list)}
    for node in node_list:
        idx = node_indices[node]
        columns = []
        for adj_matrix in adj_matrices:
            column = adj_matrix[:, idx]
            if np.any(column):
                columns.append(column)
        if not all(np.array_equal(columns[0], col) for col in columns):
            discrepancies[node] = "Adjacency matrix discrepancy found"
    return discrepancies


def hash_in_degree_set(in_degree_set):
    sorted_in_degree = sorted(in_degree_set)
    in_degree_str = ",".join(sorted_in_degree)
    return hashlib.md5(in_degree_str.encode()).hexdigest()



# Signature Hashing
def signature_hashing_comparison(graphs):
    discrepancies = {}
    in_degree_hashes = defaultdict(set)
    for G in graphs:
        in_degree_map = build_in_degree_map(G)
        node_names = set(itertools.chain(*[G.nodes for G in graphs]))
        for node in node_names:
            in_degree_set = in_degree_map.get(node, set())
            hash_signature = hash_in_degree_set(in_degree_set)
            if in_degree_set != set():
                in_degree_hashes[node].add(hash_signature)

    discrepancies = {node: "Signature hashing discrepancy" for node, hashes in in_degree_hashes.items()
                     if len(hashes) > 1}
    return discrepancies

if __name__ == "__main__":
    # Define multiple dependency lists with different structures
    dependency_list1 = {'A': [], 'B': ['A'], 'C': ['B'], 'D': ['C']}
    dependency_list2 = {'A': [], 'B': ['A'], 'C': ['B'], 'X': ['B'], 'Y': ['C', 'X'], 'Z': ['Y']}
    # Create directed graphs from dependency lists
    G1 = create_nx_dg(dependency_list1)
    G2 = create_nx_dg(dependency_list2)


    # List of all graphs for testing
    graphs = [G1, G2]
    # Run each algorithm and print discrepancies
    print("In-Degree Similarity Check:", in_degree_similarity_check(graphs).keys())
    print("Adjacency Matrix Comparison:", adjacency_matrix_comparison(graphs).keys())
    print("Signature Hashing Comparison:", signature_hashing_comparison(graphs).keys())
