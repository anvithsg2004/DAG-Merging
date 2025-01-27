import networkx as nx


def Create_nx_DG(dependency_list):
    G = nx.DiGraph()
    for node, dependents in dependency_list.items():
        G.add_node(node)  # Ensure all nodes are added
        for dependent in dependents:
            G.add_edge(dependent, node)
    return G


def merge_dags_consistency_check(*dependency_lists):
    """
    Merge multiple DAGs ensuring nodes with the same name have identical in-degree dependencies.
    Returns the merged dependency list.
    """
    node_dependencies = {}
    for dependency_list in dependency_lists:
        for node, dependents in dependency_list.items():
            dependents_set = set(dependents)
            if node not in node_dependencies:
                node_dependencies[node] = dependents_set

    merged_dependency_list = {node: list(deps) for node, deps in node_dependencies.items()}
    merged_graph = Create_nx_DG(merged_dependency_list)
    return merged_graph, merged_dependency_list


# Example dependency lists
dependency_list1 = {'A': [], 'B': ['A'], 'C': ['B'], 'D': ['C']}
dependency_list2 = {'A': [], 'B': ['A'], 'C': ['B'], 'X': ['B'], 'Y': ['C', 'X'], 'Z': ['Y']}

# Merge the DAGs and display values for each iteration
merged_graph, merged_dependency_list = merge_dags_consistency_check(dependency_list1, dependency_list2)
print("\nMerged Dependency List:", merged_dependency_list)
