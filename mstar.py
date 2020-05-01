import heapq
import itertools

import networkx as nx


class Config:
    def __init__(self):
        self.cost = float('inf')
        self.collisions = set()
        self.back_set = []
        self.back_ptr = None


def Mstar(graph, v_I, v_W, v_F):
    # Dictionary for every configuration
    # List = [cost, collision set, back_set, back_ptr]
    configurations = {}
    phi_dictionary = {}
    policies = []
    for i in range(len(v_I)):
        policy = []
        for waypoint in v_W[i]:
            policy.append(nx.dijkstra_predecessor_and_distance(graph, waypoint))
        policy.append(nx.dijkstra_predecessor_and_distance(graph, v_F[i]))
        policies.append(policy)
    edge_weights = {}
    for node in graph:
        # The cost for waiting
        edge_weights[(node, node)] = 0
        for nbr in graph[node]:
            edge_weights[(node, nbr)] = graph.get_edge_data(node, nbr).get('weight', 1)
    configurations[v_I] = Config()
    configurations[v_I].cost = 0
    open = []
    heapq.heappush(open, (configurations[v_I].cost + heuristic_configuration(v_I, policies), v_I))
    while len(open) > 0:
        v_k = heapq.heappop(open)[1]
        if v_k == v_F:
            res = [v_F]
            while configurations[v_k].back_ptr is not None:
                res.append(configurations[v_k].back_ptr)
                v_k = configurations[v_k].back_ptr
            return res[::-1], configurations[v_F].cost
        v_k_collisions = phi_dictionary.get(v_k, None)
        if v_k_collisions is None:
            v_k_collisions = phi(v_k)
            phi_dictionary[v_k] = v_k_collisions
        if len(v_k_collisions) == 0:
            V_k = get_limited_neighbours(v_k, configurations, graph, policies)
            for v_l in V_k:
                v_l_collisions = phi_dictionary.get(v_l, None)
                if v_l_collisions is None:
                    v_l_collisions = phi(v_l)
                    phi_dictionary[v_l] = v_l_collisions
                configurations[v_l].collisions.update(v_l_collisions)
                configurations[v_l].back_set.append(v_k)
                backprop(v_k, configurations[v_l].collisions, open, configurations, policies)
                f = get_edge_weight(v_k, v_l, edge_weights)
                if len(v_l_collisions) == 0 and configurations[v_k].cost + f < configurations[v_l].cost:
                    configurations[v_l].cost = configurations[v_k].cost + f
                    configurations[v_l].back_ptr = v_k
                    heapq.heappush(open, (configurations[v_l].cost + heuristic_configuration(v_l, policies), v_l))
    return "No path exists, or I am a retard"


def get_limited_neighbours(v_k, configurations, graph, policy):
    V_k = []
    options = []
    for i in range(len(v_k)):
        vi_k = v_k[i]
        options_i = []
        if i in configurations[v_k].collisions:
            # ADD all the neighbours
            options_i.append(vi_k)
            for nbr in graph[vi_k]:
                options_i.append(nbr)
        else:
            source = v_k[i]
            # TODO the 0 indicates the waypoint which is now the target since there arent any xD
            successors = policy[i][0][0][source]
            if len(successors) == 0:
                options_i.append(source)
            else:
                for successor in successors:
                    options_i.append(successor)
        options.append(options_i)
    if len(options) == 1:
        option = options[0][0]
        if option not in configurations:
            configurations[option] = Config()
        V_k.append(options[0][0])
        return V_k
    for element in itertools.product(*options):
        if element not in configurations:
            configurations[element] = Config()
        V_k.append(element)
    return V_k


def backprop(v_k, C_l, open, configurations, policy):
    C_k = configurations[v_k].collisions
    if not C_l.issubset(C_k):
        C_k.update(C_l)
        if v_k not in [k for v, k in open]:
            heapq.heappush(open, (configurations[v_k].cost + heuristic_configuration(v_k, policy), v_k))
        for v_m in configurations[v_k].back_set:
            backprop(v_m, configurations[v_k].collisions, open, configurations, policy)


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
def heuristic_configuration(v_k, policies):
    # TODO the 0 indicates the waypoint which is now the target since there arent any xD
    return sum(policies[i][0][1][v_k[i]] for i in range(len(v_k)))
