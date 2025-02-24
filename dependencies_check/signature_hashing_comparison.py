import hashlib
from collections import defaultdict
import itertools
import networkx as nx


def hash_in_degree_set(in_degree_set):
    """
    Hashes the in-degree set using MD5 for comparison.
    Args:
        in_degree_set (set): Set of in-degree nodes for a given node.
    Returns:
        str: MD5 hash of the sorted in-degree set.
    """
    sorted_in_degree = sorted(in_degree_set)
    in_degree_str = ",".join(sorted_in_degree)
    return hashlib.md5(in_degree_str.encode()).hexdigest()


def build_in_degree_map(G):
    """
    Builds a map of in-degrees for the nodes in the graph.
    Args:
        G (nx.DiGraph): A directed graph.
    Returns:
        dict: A dictionary where keys are nodes, and values are sets of their predecessors.
    """
    in_degree_map = {}
    for node in G.nodes:
        in_degree_map[node] = set(G.predecessors(node))
    return in_degree_map


def signature_hashing_comparison(graphs):
    """
    Compares graphs using hash signatures of in-degree sets for each node.
    Args:
        graphs (list of nx.DiGraph): List of directed graphs.
    Returns:
        dict: Dictionary of nodes with discrepancies in their in-degree hash signatures.
    """
    discrepancies = {}
    in_degree_hashes = defaultdict(set)

    # Iterate through each graph and compute in-degree hashes
    print("Computing In-Degree Hashes for Graphs:")
    for graph_idx, G in enumerate(graphs, start=1):
        print(f"\nGraph {graph_idx}:")
        in_degree_map = build_in_degree_map(G)
        print(f"In-Degree Map: {in_degree_map}")
        node_names = set(itertools.chain(*[G.nodes for G in graphs]))

        for node in node_names:
            in_degree_set = in_degree_map.get(node, set())
            hash_signature = hash_in_degree_set(in_degree_set)
            if in_degree_set != set():
                in_degree_hashes[node].add(hash_signature)
            print(f"Node: {node}, In-Degree Set: {in_degree_set}, Hash: {hash_signature}")

    # Check for discrepancies
    print("\nChecking for Discrepancies:")
    for node, hashes in in_degree_hashes.items():
        print(f"Node: {node}, Hashes: {hashes}")
        if len(hashes) > 1:
            discrepancies[node] = "Signature hashing discrepancy"
            print(f"Discrepancy Found for Node {node}: {hashes}")

    return discrepancies


# Example Usage
G1 = nx.DiGraph()
G1.add_edges_from([("A", "B"), ("B", "C")])

G2 = nx.DiGraph()
G2.add_edges_from([("A", "B"), ("C", "B")])

discrepancies = signature_hashing_comparison([G1, G2])
print("\nDiscrepancies:", discrepancies)
