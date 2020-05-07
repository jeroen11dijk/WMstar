import heapq
import itertools
import math
from functools import lru_cache

import networkx as nx


class Config:
    def __init__(self, target_indices):
        self.cost = float('inf')
        self.collisions = set()
        self.back_set = []
        self.target_indices = target_indices
        self.back_ptr = []

    def __str__(self):
        return str([self.cost, self.collisions, self.back_set, self.target_indices, self.back_ptr])

    def __repr__(self):
        return str([self.cost, self.collisions, self.back_set, self.target_indices, self.back_ptr])


class Mstar:
    def __init__(self, graph, v_I, v_W, v_F):
        self.graph = graph
        self.v_I = v_I
        self.v_W = v_W
        self.v_F = v_F
        self.n_agents = len(v_I)
        self.configurations = {}
        self.phi_dictionary = {}
        self.policies = []
        self.distances = []
        self.targets = []
        for i in range(self.n_agents):
            policy_i = []
            distance_i = []
            targets_i = []
            if v_W[i] in graph:
                predecessor, distance = nx.dijkstra_predecessor_and_distance(graph, v_W[i])
                policy_i.append(predecessor)
                distance_i.append(distance)
                targets_i.append(v_W[i])
            predecessor, distance = nx.dijkstra_predecessor_and_distance(graph, v_F[i])
            policy_i.append(predecessor)
            distance_i.append(distance)
            targets_i.append(v_F[i])
            self.policies.append(policy_i)
            self.distances.append(distance_i)
            self.targets.append(targets_i)
        self.open = []
        self.configurations[v_I] = Config([0] * self.n_agents)
        self.configurations[v_I].cost = 0
        heapq.heappush(self.open, (
        self.configurations[v_I].cost + self.heuristic_configuration(v_I, tuple([0] * self.n_agents)), v_I))

    def solve(self):
        configurations = self.configurations
        while len(self.open) > 0:
            v_k = heapq.heappop(self.open)[1]
            if v_k == self.v_F and all(
                    configurations[self.v_F].target_indices[i] + 1 == len(self.policies[i]) for i in
                    range(len(self.v_F))):
                configurations[self.v_F].back_ptr.append(self.v_F)
                res = []
                for i in range(self.n_agents):
                    res.append([list(config[i]) for config in configurations[self.v_F].back_ptr])
                return res, configurations[self.v_F].cost
            back_ptr_target_indices = configurations[configurations[v_k].back_ptr[-1]].target_indices if len(
                configurations[v_k].back_ptr) > 0 else [0] * self.n_agents
            for i in range(self.n_agents):
                if v_k[i] == self.v_W[i] or back_ptr_target_indices[i] == 1:
                    configurations[v_k].target_indices[i] = 1
                else:
                    configurations[v_k].target_indices[i] = 0
            v_k_collisions = self.phi(v_k)
            if len(v_k_collisions) == 0:
                V_k = self.get_limited_neighbours(v_k)
                for v_l in V_k:
                    v_l_collisions = self.phi(v_l)
                    configurations[v_l].collisions.update(v_l_collisions)
                    configurations[v_l].back_set.append(v_k)
                    self.backprop(v_k, configurations[v_l].collisions)
                    f = self.get_edge_weight(v_k, v_l)

                    v_k_target_indices = configurations[v_k].target_indices
                    v_l_target_indices = tuple(configurations[v_l].target_indices)
                    temp_target_indices = [0] * self.n_agents
                    for i in range(self.n_agents):
                        if v_l[i] == self.v_W[i] or v_k_target_indices[i] == 1:
                            temp_target_indices[i] = 1
                        else:
                            temp_target_indices[i] = 0
                    new_cost_v_l = configurations[v_k].cost + f + self.heuristic_configuration(v_l, tuple(
                        temp_target_indices))
                    old_cost_v_l = configurations[v_l].cost + self.heuristic_configuration(v_l, v_l_target_indices)
                    more_targets = math.isclose(new_cost_v_l, old_cost_v_l) and sum(
                        configurations[v_l].target_indices) < sum(
                        temp_target_indices)
                    if len(v_l_collisions) == 0 and (new_cost_v_l < old_cost_v_l or more_targets):
                        configurations[v_l].cost = configurations[v_k].cost + f
                        configurations[v_l].back_ptr = configurations[v_k].back_ptr + [v_k]
                        configurations[v_l].target_indices = temp_target_indices
                        heapq.heappush(self.open, (
                        configurations[v_l].cost + self.heuristic_configuration(v_l, tuple(temp_target_indices)), v_l))
        return "No path exists, or I am an idiot"

    def get_limited_neighbours(self, v_k):
        V_k = []
        options = []
        configurations = self.configurations
        for i in range(self.n_agents):
            vi_k = v_k[i]
            options_i = []
            if i in configurations[v_k].collisions:
                # ADD all the neighbours
                options_i.append(vi_k)
                for nbr in self.graph[vi_k]:
                    options_i.append(nbr)
            else:
                source = v_k[i]
                target_index = configurations[v_k].target_indices[i]
                policy = self.policies[i][target_index]
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
                configurations[option] = Config([0] * self.n_agents)
            V_k.append(options[0][0])
            return V_k
        for element in itertools.product(*options):
            if element not in configurations:
                configurations[element] = Config([0] * self.n_agents)
            V_k.append(element)
        return V_k

    def backprop(self, v_k, C_l):
        C_k = self.configurations[v_k].collisions
        if not C_l.issubset(C_k):
            C_k.update(C_l)
            # Technically we should check whether its not already in open
            # But that takes too much time and it will settle it self
            # if not any(v_k in configuration for configuration in open):
            target_indices = tuple(self.configurations[v_k].target_indices)
            heapq.heappush(self.open,
                           (self.configurations[v_k].cost + self.heuristic_configuration(v_k, target_indices), v_k))
            for v_m in self.configurations[v_k].back_set:
                self.backprop(v_m, self.configurations[v_k].collisions)

    def get_edge_weight(self, v_k, v_l):
        return sum(0 if k == l == m else 1 for k, l, m in zip(v_k, v_l, self.v_F))

    # Check for collisions
    # Credit to Hytak
    @lru_cache(maxsize=None)
    def phi(self, v_k):
        seen = set()
        double = list()
        for i, val in enumerate(v_k):
            if val in seen:
                double.append(val)
            else:
                seen.add(val)
        double = set(double)
        return [i for i, val in enumerate(v_k) if val in double]

    @lru_cache(maxsize=None)
    def heuristic_configuration(self, v_k, target_indices=None):
        cost = 0
        target_indices = self.configurations[v_k].target_indices if target_indices is None else target_indices
        for i in range(self.n_agents):
            target_index = target_indices[i]
            target = self.targets[i]
            cost += self.distances[i][target_index][v_k[i]]
            target_index += 1
            while target_index < len(target):
                cost += self.distances[i][target_index][target[target_index - 1]]
                target_index += 1
        return cost
