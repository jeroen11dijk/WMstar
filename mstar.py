import cProfile
import heapq
import itertools
import time
from dataclasses import dataclass

import networkx as nx
from matplotlib.pyplot import show


@dataclass
class ConfigurationInfo:
    cost: float
    collision_set: set
    back_set: []
    back_ptr: ()


def Mstar(graph, v_I, v_F):
    # Dictionary for every configuration
    # List = [cost, collision set, back_set, back_ptr]
    configurations = {}
    policy = []
    for target in v_F:
        policy.append(nx.dijkstra_predecessor_and_distance(G, target))
    configurations[v_I] = [0, set(), [], None]
    open = []
    heapq.heappush(open, (configurations[v_I][0] + heuristic_configuration(v_I, policy), v_I))
    while len(open) > 0:
        v_k = heapq.heappop(open)[1]
        if v_k == v_F:
            res = [v_F]
            while configurations[v_k][3] is not None:
                res.append(configurations[v_k][3])
                v_k = configurations[v_k][3]
            return res[::-1], configurations[v_F][0]
        if len(phi(v_k)) == 0:
            V_k = get_limited_neighbours(v_k, configurations, graph, policy)
            for v_l in V_k:
                collisions = phi(v_l)
                configurations[v_l][1].update(collisions)
                configurations[v_l][2].append(v_k)
                backprop(v_k, configurations[v_l][1], open, configurations, policy)
                f = get_edge_weight(v_k, v_l, graph)
                if len(collisions) == 0 and configurations[v_k][0] + f < configurations[v_l][0]:
                    configurations[v_l][0] = configurations[v_k][0] + f
                    configurations[v_l][3] = v_k
                    heapq.heappush(open, (configurations[v_l][0] + heuristic_configuration(v_l, policy), v_l))
    return "No path exists, or I am a retard"


def get_limited_neighbours(v_k, configurations, graph, policy):
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
            successors = policy[i][0][source]
            if len(successors) == 0:
                options_i.append(source)
            else:
                for successor in successors:
                    options_i.append(successor)
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


def backprop(v_k, C_l, open, configurations, policy):
    C_k = configurations[v_k][1]
    if not C_l.issubset(C_k):
        C_k.update(C_l)
        if v_k not in [k for v, k in open]:
            heapq.heappush(open, (configurations[v_k][0] + heuristic_configuration(v_k, policy), v_k))
        for v_m in configurations[v_k][2]:
            backprop(v_m, configurations[v_k][1], open, configurations, policy)


def get_edge_weight(v_k, v_l, graph):
    return sum(graph.get_edge_data(k, l).get('weight', 1) for k, l in zip(v_k, v_l) if k != l)


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
    return [i for i, val in enumerate(v_k) if val in double]


# Credit to Hytak
def heuristic_configuration(v_k, policy):
    return sum(policy[i][1][v_k[i]] for i in range(len(v_k)))


G = nx.Graph()

G.add_edge('a', 'b')
G.add_edge('a', 'c', weight=0.4)
G.add_edge('c', 'd', weight=0.1)
G.add_edge('c', 'e', weight=0.7)
G.add_edge('c', 'f', weight=0.9)
G.add_edge('a', 'd', weight=0.3)
G.add_edge('b', 'f', weight=0.2)
G.add_edge('g', 'e', weight=0.7)
G.add_edge('g', 'a', weight=0.5)
G.add_edge('c', 'h', weight=0.1)
G.add_edge('h', 'd', weight=0.6)
G.add_edge('i', 'a', weight=0.3)
G.add_edge('i', 'c', weight=0.9)
G.add_edge('j', 'c', weight=0.1)
G.add_edge('h', 'k', weight=0.6)
G.add_edge('a', 'k', weight=0.7)
G.add_edge('b', 'h', weight=0.4)
G.add_edge('l', 'a', weight=0.1)
G.add_edge('l', 'h', weight=0.3)
G.add_edge('m', 'c', weight=0.8)
G.add_edge('m', 'f', weight=0.3)
G.add_edge('n', 'g', weight=0.7)
G.add_edge('n', 'h', weight=0.9)
G.add_edge('n', 'a', weight=0.5)
G.add_edge('o', 'a', weight=0.3)
G.add_edge('o', 'b', weight=0.1)
G.add_edge('o', 'k', weight=0.2)
G.add_edge('o', 'n', weight=0.9)

# nx.draw_networkx(G)
# show()
v_I = ('j', 'm', 'b', 'a', 'c', 'f')
v_F = ('l', 'b', 'h', 'j', 'g', 'o')

# print(Mstar(G, v_I, v_F))
cProfile.run('Mstar(G, v_I, v_F)')