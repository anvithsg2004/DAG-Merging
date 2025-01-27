import itertools
import networkx as nx

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


def in_degree_similarity_check(graphs):
    """
    Checks the in-degree similarity of nodes across multiple graphs.
    Args:
        graphs (list of nx.DiGraph): A list of directed graphs.
    Returns:
        dict: A dictionary containing nodes with in-degree discrepancies.
    """
    discrepancies = {}
    # Build in-degree maps for all graphs
    all_in_degree_maps = [build_in_degree_map(G) for G in graphs]
    print("In-Degree Maps for Graphs:")
    for idx, in_degree_map in enumerate(all_in_degree_maps, start=1):
        print(f"Graph {idx} In-Degree Map: {in_degree_map}")

    # Collect all node names across graphs
    node_names = set(itertools.chain(*[G.nodes for G in graphs]))
    print("\nAll Nodes:", node_names)

    # Check in-degree similarity for each node
    for node in node_names:
        print(f"\nChecking Node: {node}")
        in_degree_sets = []
        for idx, in_degree_map in enumerate(all_in_degree_maps, start=1):
            in_degree_set = in_degree_map.get(node, set())
            print(f"Graph {idx}: In-Degree of {node}: {in_degree_set}")
            if in_degree_set != set():
                in_degree_sets.append(in_degree_set)
        if not all(x == in_degree_sets[0] for x in in_degree_sets):
            discrepancies[node] = "In-degree similarity discrepancy found"
            print(f"Discrepancy Found for Node {node}: {in_degree_sets}")
        else:
            print(f"No Discrepancy for Node {node}: {in_degree_sets}")

    return discrepancies

def create_nx_dg(dependency_list):
    G = nx.DiGraph()
    for node, dependents in dependency_list.items():
        G.add_node(node)  # Ensure all nodes are added
        for dependent in dependents:
            G.add_edge(dependent, node)
    return G


dependency_list1 = {'A': [], 'B': ['A'], 'C': ['B'], 'D': ['C']}
dependency_list2 = {'A': [], 'B': ['A'], 'C': ['B'], 'X': ['B'], 'Y': ['C', 'X'], 'Z': ['Y']}
dependency_list3 = {'T': [], 'B': ['A'], 'C': ['B']}
# Create directed graphs from dependency lists
G1 = create_nx_dg(dependency_list1)
G2 = create_nx_dg(dependency_list2)
G3 = create_nx_dg(dependency_list3)
discrepancies = in_degree_similarity_check([G1, G2, G3])
print("\nDiscrepancies:", discrepancies)
