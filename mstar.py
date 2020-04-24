import networkx as nx
from matplotlib.pyplot import show


def Mstar(graph, v_I, v_F):
    policies = []
    # Dictionary for every configuration
    # List = [cost, collision set, back_set, back_ptr]
    configurations = {}
    for i in range(len(v_F)):
        opt = {}
        for node in G:
            path = nx.astar_path(G, node, v_F[i], heuristic_nodes)
            weight = sum(G[u][v].get('weight', 1) for u, v in zip(path[:-1], path[1:]))
            opt[node] = (path, weight)
        policies.append(opt)
    configurations[v_I] = [0, set(), [], None]
    open = [v_I]
    while len(open) > 0:
        open.sort(key=lambda x: configurations[x][0] + heuristic_configuration(x, policies))
        v_k = open.pop()
        if v_k == v_F:
            res = []
            while configurations[v_k][3] is not None:
                res.append(configurations[v_k][3])
                v_k = configurations[v_k][3]
            return res[::-1]
        if len(phi(v_k)) == 0:
            V_k = get_limited_neighbours_new(v_k, configurations, graph, policies)
            for v_l in V_k:
                configurations[v_l][1].update(phi(v_l))
                configurations[v_l][2].append(v_k)
                backprop(v_k, configurations[v_l][1], open, configurations)
                f = get_edge_weight(v_k, v_l, graph)
                if len(phi(v_l)) == 0 and configurations[v_k][0] + f < configurations[v_l][0]:
                    configurations[v_l][0] = configurations[v_k][0] + f
                    configurations[v_l][3] = v_k
                    open.append(v_l)
    return "No path exists, or I am a retard"


def get_limited_neighbours_new(v_k, configurations, graph, policies):
    V_k = []
    for i in range(len(v_k)):
        vi_k = v_k[i]
        if vi_k in configurations[v_k][1]:
            # ADD all the neighbours
            for nbr in graph[vi_k]:
                v_k_list = list(v_k)
                v_k_list[i] = nbr
                new_configuration = tuple(v_k_list)
                if new_configuration not in configurations:
                    configurations[new_configuration] = [float('inf'), set(), [], None]
                V_k.append(new_configuration)
        else:
            path = policies[i][v_k[i]][0]
            v_k_list = list(v_k)
            v_k_list[i] = path[1] if len(path) > 1 else path[0]
            new_configuration = tuple(v_k_list)
            if new_configuration not in configurations:
                configurations[new_configuration] = [float('inf'), set(), [], None]
            V_k.append(new_configuration)
    return V_k


def get_limited_neighbours_old(v_k, configurations, graph, policies):
    V_k = []
    for i in range(len(v_k)):
        vi_k = v_k[i]
        if vi_k in configurations[v_k][1]:
            # ADD all the neighbours
            for nbr in graph[vi_k]:
                v_k_list = list(v_k)
                v_k_list[i] = nbr
                new_configuration = tuple(v_k_list)
                if new_configuration not in configurations:
                    configurations[new_configuration] = [float('inf'), set(), [], None]
                V_k.append(new_configuration)
        else:
            path = policies[i][v_k[i]][0]
            v_k_list = list(v_k)
            v_k_list[i] = path[1] if len(path) > 1 else path[0]
            new_configuration = tuple(v_k_list)
            if new_configuration not in configurations:
                configurations[new_configuration] = [float('inf'), set(), [], None]
            V_k.append(new_configuration)
    return V_k


def backprop(v_k, C_l, open, configurations):
    C_k = configurations[v_k][1]
    if not C_l.issubset(C_k):
        C_k.update(C_l)
        if v_k not in open:
            open.append(v_k)
        for v_m in configurations[v_k][2]:
            backprop(v_m, configurations[v_k][1], open, configurations)


def get_edge_weight(v_k, v_l, graph):
    if v_k[0] != v_l[0]:
        egde_data = graph.get_edge_data(v_k[0], v_l[0])
        return egde_data.get('weight') if egde_data.get('weight') is not None else 1
    elif v_k[1] != v_l[1]:
        egde_data = graph.get_edge_data(v_k[1], v_l[1])
        return egde_data.get('weight') if egde_data.get('weight') is not None else 1
    else:
        return 1

# Check for collisions
def phi(v_k):
    seen = []
    collisions = []
    for pos in v_k:
        if pos in seen:
            collisions.append(pos)
        seen.append(pos)
    return collisions


def heuristic_configuration(v_k, policies):
    cost = 0
    for i in range(len(v_k)):
        cost += policies[i][v_k[i]][1]
    return cost


def heuristic_nodes(u, v):
    return abs((u[0] - v[0])) + abs((u[1] - v[1]))


G = nx.grid_2d_graph(4, 4)

v_I = ((0, 0), (0, 1))
v_F = ((2, 3), (0, 3))

print(Mstar(G, v_I, v_F))
