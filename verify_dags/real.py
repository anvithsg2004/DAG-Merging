import networkx as nx


# Create a directed graph from a dependency list
def Create_nx_DG(dependency_list):
    G = nx.DiGraph()
    for node, dependents in dependency_list.items():
        for dependent in dependents:
            G.add_edge(dependent, node)
    return G



# DFS with Recursion Stack
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



# Matrix Approach (Floyd-Warshall)
def is_dag_floyd_warshall(G):
    nodes = list(G.nodes())
    n = len(nodes)
    reach = [[0] * n for _ in range(n)]

    # Populate reachability matrix
    for i, u in enumerate(nodes):
        for v in G.neighbors(u):
            j = nodes.index(v)
            reach[i][j] = 1

    # Apply Floyd-Warshall algorithm
    for k in range(n):
        for i in range(n):
            for j in range(n):
                reach[i][j] = reach[i][j] or (reach[i][k] and reach[k][j])

    for i in range(n):
        if reach[i][i] == 1:
            return False
    return True





# Main code to test all algorithms
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

        G = Create_nx_DG(i)

        print("Kahn’s Algorithm:", is_dag_kahn(G))
        #print("DFS-based Topological Sort:", is_dag_dfs_topological(G))
        print("DFS with Recursion Stack:", is_dag_dfs_rec_stack(G))
        #print("Union-Find (Adapted):", is_dag_union_find(G))
        #print("In-Degree Counting:", is_dag_in_degree(G))
        print("Matrix Approach (Floyd-Warshall):", is_dag_floyd_warshall(G))
        print("Tarjan’s SCC Algorithm:", is_dag_tarjan(G))
        print()
        print()
        print()
