import heapq
import itertools

import networkx as nx


class Config:
    def __init__(self, targets):
        self.cost = float('inf')
        self.collisions = set()
        self.back_set = []
        self.targets = targets
        self.back_ptr = None


def Mstar(graph, v_I, v_W, v_F):
    # Dictionary for every configuration
    n_agents = len(v_I)
    configurations = {}
    phi_dictionary = {}
    waypoint_policies = []
    target_policies = []
    for i in range(len(v_I)):
        if v_W[i] in graph:
            waypoint_policies.append(nx.dijkstra_predecessor_and_distance(graph, v_W[i]))
        else:
            waypoint_policies.append(None)
        target_policies.append(nx.dijkstra_predecessor_and_distance(graph, v_F[i]))
    policies = [waypoint_policies, target_policies]
    edge_weights = {}
    for node in graph:
        # The cost for waiting
        edge_weights[(node, node)] = 0
        for nbr in graph[node]:
            edge_weights[(node, nbr)] = graph.get_edge_data(node, nbr).get('weight', 1)
    targets = [0] * n_agents
    for i in range(n_agents):
        if waypoint_policies[i] is None:
            targets[i] = 1
    configurations[v_I] = Config(targets)
    configurations[v_I].cost = 0
    open = []
    heapq.heappush(open, (configurations[v_I].cost + heuristic_configuration(v_I, v_W, configurations, policies), v_I))
    while len(open) > 0:
        v_k = heapq.heappop(open)[1]
        # print(configurations[v_k].targets)
        if v_k == v_F and 0 not in configurations[v_F].targets:
            res = [v_F]
            while configurations[v_k].back_ptr is not None:
                res.append(configurations[v_k].back_ptr)
                v_k = configurations[v_k].back_ptr
            return res[::-1], configurations[v_F].cost
        for i in range(n_agents):
            if v_k[i] == v_W[i]:
                configurations[v_k].targets[i] = 1
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
                backprop(v_k, v_W, configurations[v_l].collisions, open, configurations, policies)
                f = get_edge_weight(v_k, v_l, edge_weights)
                if len(v_l_collisions) == 0 and configurations[v_k].cost + f < configurations[v_l].cost:
                    configurations[v_l].cost = configurations[v_k].cost + f
                    if configurations[v_l].back_ptr is None:
                        combined_targets = zip(configurations[v_l].targets, configurations[v_k].targets)
                        configurations[v_l].targets = [max(x) for x in combined_targets]
                        configurations[v_l].back_ptr = v_k
                    else:
                        configurations[v_l].back_ptr = v_k
                        backtrace = [configurations[v_l].targets]
                        back_config = v_k
                        while configurations[back_config].back_ptr is not None:
                            backtrace.append(configurations[back_config].targets)
                            back_config = configurations[back_config].back_ptr
                        combined_targets = zip(*backtrace)
                        configurations[v_l].targets = [max(x) for x in combined_targets]
                    heapq.heappush(open, (configurations[v_l].cost + heuristic_configuration(v_l, v_W, configurations, policies), v_l))
    return "No path exists, or I am a retard"


def get_limited_neighbours(v_k, configurations, graph, policies):
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
            target = configurations[v_k].targets[i]
            policy = policies[target][i][0]
            successors = policy[v_k[i]]
            if len(successors) == 0:
                options_i.append(source)
            else:
                for successor in successors:
                    options_i.append(successor)
        options.append(options_i)
    if len(options) == 1:
        option = options[0][0]
        if option not in configurations:
            configurations[option] = Config([0] * len(v_k))
        V_k.append(options[0][0])
        return V_k
    for element in itertools.product(*options):
        if element not in configurations:
            configurations[element] = Config([0] * len(v_k))
        V_k.append(element)
    return V_k


def backprop(v_k, v_W, C_l, open, configurations, policy):
    C_k = configurations[v_k].collisions
    if not C_l.issubset(C_k):
        C_k.update(C_l)
        if not any(v_k in configuration for configuration in open):
            heapq.heappush(open, (configurations[v_k].cost + heuristic_configuration(v_k, v_W, configurations, policy), v_k))
        for v_m in configurations[v_k].back_set:
            backprop(v_m, v_W, configurations[v_k].collisions, open, configurations, policy)


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
def heuristic_configuration(v_k, v_W, configurations, policies):
    # return sum(policies[configurations[v_k].targets[i]][i][1][v_k[i]] for i in range(len(v_k)))
    cost = 0
    for i in range(len(v_k)):
        target = configurations[v_k].targets[i]
        if target == 0:
            policy_costs = policies[0][i][1]
            cost += policy_costs[v_k[i]]
            policy_costs = policies[1][i][1]
            cost += policy_costs[v_W[i]]
        else:
            policy_costs = policies[1][i][1]
            cost += policy_costs[v_k[i]]
    return cost
