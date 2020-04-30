import cProfile
import heapq
import itertools
from dataclasses import dataclass

import networkx as nx


def Mstar(graph, v_I, v_F):
    # Dictionary for every configuration
    # List = [cost, collision set, back_set, back_ptr]
    configurations = {}
    phi_dictionary = {}
    policy = []
    for target in v_F:
        policy.append(nx.dijkstra_predecessor_and_distance(graph, target))
    edge_weights = {}
    for node in graph:
        # The cost for waiting
        edge_weights[(node, node)] = 0
        for nbr in graph[node]:
            edge_weights[(node, nbr)] = graph.get_edge_data(node, nbr).get('weight', 1)
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
        v_k_collisions = phi_dictionary.get(v_k, None)
        if v_k_collisions is None:
            v_k_collisions = phi(v_k)
            phi_dictionary[v_k] = v_k_collisions
        if len(v_k_collisions) == 0:
            V_k = get_limited_neighbours(v_k, configurations, graph, policy)
            for v_l in V_k:
                v_l_collisions = phi_dictionary.get(v_l, None)
                if v_l_collisions is None:
                    v_l_collisions = phi(v_l)
                    phi_dictionary[v_l] = v_l_collisions
                configurations[v_l][1].update(v_l_collisions)
                configurations[v_l][2].append(v_k)
                backprop(v_k, configurations[v_l][1], open, configurations, policy)
                f = get_edge_weight(v_k, v_l, edge_weights)
                if len(v_l_collisions) == 0 and configurations[v_k][0] + f < configurations[v_l][0]:
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


def get_edge_weight(v_k, v_l, edge_weights):
    return sum(edge_weights[(k, l)] for k, l in zip(v_k, v_l))


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
