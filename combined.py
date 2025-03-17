import networkx as nx
import itertools
from pyvis.network import Network


# Create a directed graph from a dependency list
def create_nx_dg(dependency_list):
    G = nx.DiGraph()
    for node, dependents in dependency_list.items():
        G.add_node(node)  # Ensure all nodes are added
        for dependent in dependents:
            G.add_edge(dependent, node)
    return G


# 1. Weak Connectivity Check: DFS/BFS
def is_weakly_connected_dfs_bfs(G):
    undirected_G = G.to_undirected()  # Convert to undirected graph
    start_node = next(iter(undirected_G.nodes))  # Get any starting node
    visited = set()

    def dfs(node):
        visited.add(node)
        for neighbor in undirected_G.neighbors(node):
            if neighbor not in visited:
                dfs(neighbor)

    dfs(start_node)
    return len(visited) == len(G.nodes)  # Check if all nodes are visited


# 2. Acyclic Verification: DFS with Recursion Stack
def is_dag_dfs_rec_stack(G):
    visited = set()
    rec_stack = set()

    def dfs(node):
        if node not in visited:
            visited.add(node)
            rec_stack.add(node)
            for neighbor in G.neighbors(node):
                if neighbor not in visited and dfs(neighbor):
                    return True
                elif neighbor in rec_stack:
                    return True
            rec_stack.remove(node)
        return False

    for node in G.nodes():
        if dfs(node):
            return False
    return True


# 3. Dependency Consistency Check: In-Degree Similarity
def build_in_degree_map(G):
    return {node: set(G.predecessors(node)) for node in G.nodes}


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
        if in_degree_sets and not all(x == in_degree_sets[0] for x in in_degree_sets):
            discrepancies[node] = "In-degree similarity discrepancy found"
    return discrepancies


# 4. DAG Merging: Dependency Aggregation Algorithm
def merge_dags_consistency_check(*dependency_lists):
    node_dependencies = {}
    for dependency_list in dependency_lists:
        for node, dependents in dependency_list.items():
            dependents_set = set(dependents)
            if node not in node_dependencies:
                node_dependencies[node] = dependents_set
            else:
                node_dependencies[node] = node_dependencies[node].union(dependents_set)

    merged_dependency_list = {node: list(deps) for node, deps in node_dependencies.items()}
    merged_graph = create_nx_dg(merged_dependency_list)
    return merged_graph, merged_dependency_list


# Function to plot a graph using pyvis
def plot_graph_pyvis(G, file_name):
    net = Network(height='750px', width='100%', directed=True, notebook=False)
    net.from_nx(G)
    net.show(file_name, notebook=False)
    print(f"Graph has been plotted and saved as '{file_name}'.")


# Main Function
if __name__ == "__main__":

    # Passes all the tests.
    dependency_list1 = {'A': [], 'B': ['A'], 'C': ['B'], 'D': ['C']}
    dependency_list2 = {'A': [], 'B': ['A'], 'C': ['B'], 'X': ['B'], 'Y': ['C'], 'Z': ['Y']}

    # Has Cycle in one of the graphs.
    # dependency_list1 = {'A': ['C'], 'B': ['A'], 'C': ['B']}
    # dependency_list2 = {'A': [], 'B': ['A'], 'C': ['B']}

    # This has inconsistency.
    # dependency_list1 = {'A': [], 'B': ['A'], 'C': ['B']}
    # dependency_list2 = {'A': [], 'B': ['A'], 'C': ['X'], 'X': []}

    # Not weakly connected
    # dependency_list1 = {'A': ['B'], 'B': ['C'], 'C': ['F'], 'F': ['D'], 'D': ['E'], 'E': ['A']}
    # dependency_list2 = {'A': ['B'], 'B': [], 'C': ['D'], 'D': []}

    # Pair 1: Completely separate graphs
    # dependency_list1 = {'X': [], 'Y': ['X'], 'Z': ['Y']}
    # dependency_list2 = {'A': [], 'B': ['A'], 'C': ['B']}

    # Pair 2: Overlapping nodes with different dependencies
    # dependency_list1 = {'A': ['B'], 'B': ['C'], 'C': []}
    # dependency_list2 = {'A': ['C'], 'B': ['A'], 'C': []}

    # Pair 3: One graph is a subset of the other
    # dependency_list1 = {'A': [], 'B': ['A'], 'C': ['B']}
    # dependency_list2 = {'A': [], 'B': ['A']}

    # Pair 4: Merging would create a cycle
    # dependency_list1 = {'A': ['B'], 'B': []}
    # dependency_list2 = {'B': ['A'], 'A': []}

    # Pair 5: Conflicting dependencies for a node
    # dependency_list1 = {'A': ['B'], 'B': []}
    # dependency_list2 = {'A': ['C'], 'C': []}

    # Pair 6: Nodes with no dependencies
    # dependency_list1 = {'A': [], 'B': [], 'C': []}
    # dependency_list2 = {'X': [], 'Y': [], 'Z': []}

    # Pair 7: Multiple root nodes
    # dependency_list1 = {'A': [], 'B': [], 'C': ['A', 'B']}
    # dependency_list2 = {'X': [], 'Y': ['X'], 'Z': ['X']}

    # Pair 8: Complex dependencies
    # dependency_list1 = {'A': ['B', 'C'], 'B': ['D'], 'C': ['D'], 'D': []}
    # dependency_list2 = {'X': ['Y', 'Z'], 'Y': ['W'], 'Z': ['W'], 'W': []}

    # Pair 9: One graph has a cycle (should fail DAG check)
    # dependency_list1 = {'A': ['B'], 'B': ['C'], 'C': ['A']}
    # dependency_list2 = {'X': ['Y'], 'Y': ['Z'], 'Z': []}

    # Pair 10: Shared nodes with different dependency directions
    # dependency_list1 = {'A': ['B'], 'B': ['C'], 'C': []}
    # dependency_list2 = {'A': ['C'], 'B': ['A'], 'C': []}

    # Pair 11: Nodes with multiple parents
    # dependency_list1 = {'A': ['B', 'C'], 'B': [], 'C': []}
    # dependency_list2 = {'B': ['D'], 'C': ['D'], 'D': []}

    # Pair 12: Large number of nodes
    # dependency_list1 = {f'A{i}': [f'A{i + 1}'] for i in range(10)}
    # dependency_list2 = {f'B{i}': [f'B{i + 1}'] for i in range(10)}

    # Pair 13: Nodes with no dependencies in one graph but do in another
    # dependency_list1 = {'A': [], 'B': [], 'C': []}
    # dependency_list2 = {'A': ['B'], 'B': ['C'], 'C': []}

    # Pair 14: Nodes with different numbers of dependencies
    # dependency_list1 = {'A': ['B', 'C', 'D'], 'B': [], 'C': [], 'D': []}
    # dependency_list2 = {'A': ['B'], 'B': ['C'], 'C': ['D'], 'D': []}

    # Pair 15: Complex web that might create a cycle when merged
    # dependency_list1 = {'A': ['B'], 'B': ['C'], 'C': ['D'], 'D': []}
    # dependency_list2 = {'D': ['A'], 'B': ['E'], 'E': []}

    # Combine into a list of dependency dictionaries
    dependency_lists = [dependency_list1, dependency_list2]

    # Create graphs from dependency lists
    graphs = [create_nx_dg(dep_list) for dep_list in dependency_lists]

    # Plot the initial dependency graphs
    for idx, G in enumerate(graphs, start=1):
        file_name = f"dependency_graph_{idx}.html"
        plot_graph_pyvis(G, file_name)

    # 1. Weak Connectivity Check
    for idx, G in enumerate(graphs, start=1):
        result = is_weakly_connected_dfs_bfs(G)
        print(f"Graph {idx} Weakly Connected: {result}")
        if not result:
            print(f"Graph {idx} is not weakly connected. Stopping execution.")
            exit()

    # 2. Acyclicity Verification
    for idx, G in enumerate(graphs, start=1):
        result = is_dag_dfs_rec_stack(G)
        print(f"Graph {idx} Is DAG: {result}")
        if not result:
            print(f"Graph {idx} is not a DAG. Stopping execution.")
            exit()

    # 3. Dependency Consistency Check
    discrepancies = in_degree_similarity_check(graphs)
    if discrepancies:
        print("Dependency Consistency Check failed with discrepancies:", discrepancies)
        print("Stopping execution.")
        exit()
    else:
        print("Dependency Consistency Check: Passed")

    # 4. DAG Merging
    merged_graph, merged_dependencies = merge_dags_consistency_check(*dependency_lists)
    print("\nMerged Dependency List:", merged_dependencies)
    print("Merged DAG Nodes:", list(merged_graph.nodes))
    print("Merged DAG Edges:", list(merged_graph.edges))

    # Check if the merged graph is a DAG
    if is_dag_dfs_rec_stack(merged_graph):
        print("\nMerged graph is a DAG. Proceeding to plot.")
        # Plot the merged DAG using pyvis
        plot_graph_pyvis(merged_graph, 'merged_dag.html')
    else:
        print("\nMerged graph is not a DAG. Cannot plot.")
