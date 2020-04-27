import time

import networkx as nx
from matplotlib.pyplot import show
import itertools


def Mstar(graph, v_I, v_F):
    policies = []
    # Dictionary for every configuration
    # List = [cost, collision set, back_set, back_ptr]
    configurations = {}
    for i in range(len(v_F)):
        opt = {}
        for node in G:
            path = nx.astar_path(G, node, v_F[i])
            weight = sum(G[u][v].get('weight', 1) for u, v in zip(path[:-1], path[1:]))
            opt[node] = (path, weight)
        policies.append(opt)
    configurations[v_I] = [0, set(), [], None]
    open = [v_I]
    while len(open) > 0:
        open.sort(key=lambda x: configurations[x][0] + heuristic_configuration(x, policies))
        v_k = open.pop(0)
        if v_k == v_F:
            res = [v_F]
            while configurations[v_k][3] is not None:
                res.append(configurations[v_k][3])
                v_k = configurations[v_k][3]
            return res[::-1]
        if len(phi(v_k)) == 0:
            V_k = get_limited_neighbours(v_k, configurations, graph, policies)
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


def get_limited_neighbours(v_k, configurations, graph, policies):
    V_k = []
    options = []
    for i in range(len(v_k)):
        vi_k = v_k[i]
        options_i = []
        if i in configurations[v_k][1]:
            # ADD all the neighbours
            options_i.append(vi_k)
            for nbr in graph[vi_k]:
                options_i.append(nbr)
        else:
            path = policies[i][v_k[i]][0]
            options_i.append(path[1] if len(path) > 1 else path[0])
        options.append(options_i)
    if len(options) == 1:
        option = options[0][0]
        if option not in configurations:
            configurations[option] = [float('inf'), set(), [], None]
        V_k.append(options[0][0])
        return V_k
    for element in itertools.product(*options):
        if element not in configurations:
            configurations[element] = [float('inf'), set(), [], None]
        V_k.append(element)
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
    cost = 0
    for i in range(len(v_k)):
        if v_k[i] != v_l[i]:
            egde_data = graph.get_edge_data(v_k[i], v_l[i])
            cost += egde_data.get('weight') if egde_data.get('weight') is not None else 1
        else:
            cost += 1
    return cost


# Check for collisions
def phi(v_k):
    observed = {}
    for i, val in enumerate(v_k):
        if val in observed:
            observed[val].append(i)
        else:
            observed[val] = [i]
    return [item for sublist in (val for val in observed.values() if len(val) - 1) for item in sublist]


def heuristic_configuration(v_k, policies):
    cost = 0
    for i in range(len(v_k)):
        cost += policies[i][v_k[i]][1]
    return cost

G = nx.grid_2d_graph(4, 4)

v_I = ((2, 1), (0, 1), (1, 2))
v_F = ((0, 1), (2, 1), (1, 0))

nx.draw_networkx(G)
show()

# print(Mstar(G, v_I, v_F))

G = nx.Graph()

G.add_edge('a', 'b')
G.add_edge('a', 'c', weight=12)
G.add_edge('c', 'd', weight=0.1)
G.add_edge('c', 'e', weight=0.7)
G.add_edge('c', 'f', weight=0.9)
G.add_edge('a', 'd', weight=0.3)

nx.draw_networkx(G)
show()

print(Mstar(G, ('e', 'b'), ('b', 'f')))
