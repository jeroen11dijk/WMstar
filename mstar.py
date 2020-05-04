import heapq
import itertools
import math
import networkx as nx

class Config:
    def __init__(self, targets):
        self.cost = float('inf')
        self.collisions = set()
        self.back_set = []
        self.targets = targets
        self.back_ptr = []

    def __str__(self):
        return str([self.cost, self.collisions, self.back_set, self.targets, self.back_ptr])

    def __repr__(self):
        return str([self.cost, self.collisions, self.back_set, self.targets, self.back_ptr])


def Mstar(graph, v_I, v_W, v_F):
    # Dictionary for every configuration
    n_agents = len(v_I)
    configurations = {}
    phi_dictionary = {}
    waypoint_policies = []
    policies = []
    for i in range(len(v_I)):
        policy_i = []
        if v_W[i] in graph:
            waypoint_policies.append(nx.dijkstra_predecessor_and_distance(graph, v_W[i]))
            policy_i.append(nx.dijkstra_predecessor_and_distance(graph, v_W[i]))
        else:
            waypoint_policies.append(None)
        policy_i.append(nx.dijkstra_predecessor_and_distance(graph, v_F[i]))
        policies.append(policy_i)
    edge_weights = {}
    for node in graph:
        # The cost for waiting
        edge_weights[(node, node)] = 0
        for nbr in graph[node]:
            edge_weights[(node, nbr)] = graph.get_edge_data(node, nbr).get('weight', 1)
    configurations[v_I] = Config([0] * n_agents)
    configurations[v_I].cost = 0
    open = []
    heapq.heappush(open, (configurations[v_I].cost + heuristic_configuration(v_I, v_W, configurations, policies), v_I))
    while len(open) > 0:
        v_k = heapq.heappop(open)[1]
        if v_k == v_F and all(configurations[v_F].targets[i] + 1 == len(policies[i]) for i in range(len(v_F))):
            res = []
            for config in configurations[v_F].back_ptr:
                res.append(config)
            res.append(v_F)
            return res, configurations[v_F].cost
        back_ptr_targets = configurations[configurations[v_k].back_ptr[-1]].targets if len(configurations[v_k].back_ptr) > 0 else [0] * n_agents
        for i in range(n_agents):
            if v_k[i] == v_W[i] or back_ptr_targets[i] == 1:
                configurations[v_k].targets[i] = 1
            else:
                configurations[v_k].targets[i] = 0
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

                v_k_targets = configurations[v_k].targets
                temp_targets = [0] * n_agents
                for i in range(n_agents):
                    if v_l[i] == v_W[i] or v_k_targets[i] == 1:
                        temp_targets[i] = 1
                    else:
                        temp_targets[i] = 0
                new_cost_v_l = configurations[v_k].cost + f + heuristic_configuration(v_l, v_W, configurations, policies, temp_targets)
                old_cost_v_l = configurations[v_l].cost + heuristic_configuration(v_l, v_W, configurations, policies)
                more_targets = math.isclose(new_cost_v_l, old_cost_v_l) and sum(configurations[v_l].targets) < sum(temp_targets)
                if len(v_l_collisions) == 0 and (new_cost_v_l < old_cost_v_l or more_targets):
                    configurations[v_l].cost = configurations[v_k].cost + f
                    configurations[v_l].back_ptr = configurations[v_k].back_ptr + [v_k]
                    configurations[v_l].targets = temp_targets
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
            policy = policies[i][target][0]
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


def backprop(v_k, v_W, C_l, open, configurations, policies):
    C_k = configurations[v_k].collisions
    if not C_l.issubset(C_k):
        C_k.update(C_l)
        if not any(v_k in configuration for configuration in open):
            heapq.heappush(open, (configurations[v_k].cost + heuristic_configuration(v_k, v_W, configurations, policies), v_k))
        for v_m in configurations[v_k].back_set:
            backprop(v_m, v_W, configurations[v_k].collisions, open, configurations, policies)


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


def heuristic_configuration(v_k, v_W, configurations, policies, targets=None):
    cost = 0
    for i in range(len(v_k)):
        target = configurations[v_k].targets[i] if targets is None else targets[i]
        if target == 0 and target == len(policies[i]) - 1:
            policy_costs_new = policies[i][target][1]
            cost += policy_costs_new[v_k[i]]
        elif target == 1 and target == len(policies[i]) - 1:
            policy_costs_new = policies[i][target][1]
            cost += policy_costs_new[v_k[i]]
        else:
            policy_costs_new = policies[i][target][1]
            cost += policy_costs_new[v_k[i]]
            policy_costs_new = policies[i][target + 1][1]
            cost += policy_costs_new[v_W[i]]
    return cost
