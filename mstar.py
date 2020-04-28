import time

import networkx as nx
from matplotlib.pyplot import show
import itertools


def Mstar(graph, v_I, v_F):
    # Dictionary for every configuration
    # List = [cost, collision set, back_set, back_ptr]
    configurations = {}
    policy = nx.floyd_warshall_predecessor_and_distance(G)
    configurations[v_I] = [0, set(), [], None]
    open = [v_I]
    while len(open) > 0:
        open.sort(key=lambda x: configurations[x][0] + heuristic_configuration(x, v_F, policy))
        v_k = open.pop(0)
        if v_k == v_F:
            res = [v_F]
            while configurations[v_k][3] is not None:
                res.append(configurations[v_k][3])
                v_k = configurations[v_k][3]
            return res[::-1], configurations[v_F][0]
        if next(phi(v_k), None) is None:
            print("HERE")
            V_k = get_limited_neighbours(v_k, v_F, configurations, graph, policy)
            for v_l in V_k:
                configurations[v_l][1].update(phi(v_l))
                configurations[v_l][2].append(v_k)
                backprop(v_k, configurations[v_l][1], open, configurations)
                f = get_edge_weight(v_k, v_l, graph)
                if next(phi(v_k), None) is None and configurations[v_k][0] + f < configurations[v_l][0]:
                    configurations[v_l][0] = configurations[v_k][0] + f
                    configurations[v_l][3] = v_k
                    open.append(v_l)
    return "No path exists, or I am a retard"


def get_limited_neighbours(v_k, v_F, configurations, graph, policy):
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
            source = v_k[i]
            target = v_F[i]
            if source == target:
                options_i.append(target)
            else:
                options_i.append(policy[0][target][source])
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
# Credit to Hytak
def phi(v_k):
    seen = set()
    double = list()
    for i, val in enumerate(v_k):
        if val in seen:
            double.append(val)
        else:
            seen.add(val)
    double = set(double)
    return (i for i, val in enumerate(v_k) if val in double)


def heuristic_configuration(v_k, v_F, policy):
    cost = 0
    for i in range(len(v_k)):
        source = v_k[i]
        target = v_F[i]
        cost += policy[1][target][source]
    return cost


G = nx.Graph()

G.add_edge('a', 'b')
G.add_edge('a', 'c', weight=0.4)
G.add_edge('c', 'd', weight=0.1)
G.add_edge('c', 'e', weight=0.7)
G.add_edge('c', 'f', weight=0.9)
G.add_edge('a', 'd', weight=0.3)
G.add_edge('b', 'f', weight=0.2)
G.add_edge('d', 'f', weight=0.4)

nx.draw_networkx(G)
show()

print(Mstar(G, ('e', 'b', 'a', 'c'), ('b', 'f', 'e', 'a')))

policy = nx.floyd_warshall_predecessor_and_distance(G)

print(policy[1]['a']['a'])
