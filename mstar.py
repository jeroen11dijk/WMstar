import heapq
import itertools
import math
from copy import copy
from functools import lru_cache

import networkx as nx


class Config:
    def __init__(self):
        self.cost = float('inf')
        self.heuristic = float('inf')
        self.collisions = set()
        self.back_set = []
        self.back_ptr = []

    def __str__(self):
        return str([self.cost, self.collisions, self.back_set, self.back_ptr])

    def __repr__(self):
        return str([self.cost, self.collisions, self.back_set, self.back_ptr])


class Mstar:
    def __init__(self, graph, v_I, v_W, v_F):
        self.graph = graph
        self.v_I = v_I
        self.v_W = v_W
        self.v_F = v_F
        self.n_agents = len(v_I)
        self.configurations = {}
        self.policies = []
        self.distances = []
        self.targets = []
        for i in range(self.n_agents):
            policy_i = []
            distance_i = []
            targets_i = []
            for waypoint in v_W[i]:
                if waypoint in graph:
                    predecessor, distance = nx.dijkstra_predecessor_and_distance(graph, waypoint)
                    policy_i.append(predecessor)
                    distance_i.append(distance)
                    targets_i.append(waypoint)
            predecessor, distance = nx.dijkstra_predecessor_and_distance(graph, v_F[i])
            policy_i.append(predecessor)
            distance_i.append(distance)
            targets_i.append(v_F[i])
            self.policies.append(policy_i)
            self.distances.append(distance_i)
            self.targets.append(targets_i)
        self.open = []
        self.configurations[(v_I, (0,) * self.n_agents)] = Config()
        self.configurations[(v_I, (0,) * self.n_agents)].cost = 0
        heapq.heappush(self.open, (self.heuristic_configuration(v_I, tuple([0] * self.n_agents)), (v_I, (0,) * self.n_agents)))

    def solve(self):
        configurations = self.configurations
        while len(self.open) > 0:
            v_k, target_indices = heapq.heappop(self.open)[1]
            if v_k == self.v_F and all(target_indices[i] + 1 == len(self.targets[i]) for i in range(len(self.v_F))):
                configurations[(v_k, target_indices)].back_ptr.append(self.v_F)
                res = []
                for i in range(self.n_agents):
                    res.append([list(config[i]) for config in configurations[(v_k, target_indices)].back_ptr])
                return res, configurations[(v_k, target_indices)].cost
            if len(self.phi(v_k)) == 0:
                V_k = self.get_limited_neighbours(v_k, target_indices)
                for v_l in V_k:
                    v_l_target_indices = list(target_indices)
                    for i in range(self.n_agents):
                        if v_l[i] == self.targets[i][v_l_target_indices[i]] and v_l[i] != self.v_F[i]:
                            v_l_target_indices[i] += 1
                    v_l_target_indices = tuple(v_l_target_indices)
                    v_l_collisions = self.phi(v_l)
                    if (v_l, v_l_target_indices) not in configurations:
                        configurations[(v_l, v_l_target_indices)] = Config()
                    configurations[(v_l, v_l_target_indices)].collisions.update(v_l_collisions)
                    configurations[(v_l, v_l_target_indices)].back_set.append((v_k, target_indices))
                    self.backprop(v_k, target_indices, configurations[(v_l, v_l_target_indices)].collisions)

                    f = self.get_edge_weight(v_k, v_l, v_l_target_indices)
                    new_cost_v_l = configurations[(v_k, target_indices)].cost + f
                    old_cost_v_l = configurations[(v_l, v_l_target_indices)].cost
                    if len(v_l_collisions) == 0 and new_cost_v_l < old_cost_v_l:
                        configurations[(v_l, v_l_target_indices)].cost = configurations[(v_k, target_indices)].cost + f
                        configurations[(v_l, v_l_target_indices)].back_ptr = configurations[(v_k, target_indices)].back_ptr + [v_k]
                        heuristic = self.heuristic_configuration(v_l, v_l_target_indices)
                        heapq.heappush(self.open, (configurations[(v_l, v_l_target_indices)].cost + heuristic, (v_l, v_l_target_indices)))
        return "No path exists, or I am an idiot"

    def get_limited_neighbours(self, v_k, target_indices):
        V_k = []
        options = []
        configurations = self.configurations
        for i in range(self.n_agents):
            vi_k = v_k[i]
            options_i = []
            if i in configurations[(v_k, target_indices)].collisions:
                # ADD all the neighbours
                options_i.append(vi_k)
                for nbr in self.graph[vi_k]:
                    options_i.append(nbr)
            else:
                source = v_k[i]
                target_index = target_indices[i]
                policy = self.policies[i][target_index]
                successors = policy[v_k[i]]
                if len(successors) == 0:
                    options_i.append(source)
                else:
                    for successor in successors:
                        options_i.append(successor)
            options.append(options_i)
        if len(options) == 1:
            V_k.append(options[0][0])
            return V_k
        for element in itertools.product(*options):
            V_k.append(element)
        return V_k

    def backprop(self, v_k, target_indices, C_l):
        C_k = self.configurations[(v_k, target_indices)].collisions
        if not C_l.issubset(C_k):
            C_k.update(C_l)
            # Technically we should check whether its not already in open
            # But that takes too much time and it will settle it self
            # if not any(v_k in configuration for configuration in open):
            heapq.heappush(self.open,
                           (self.configurations[(v_k, target_indices)].cost + self.heuristic_configuration(v_k, target_indices), (v_k, target_indices)))
            for v_m, v_m_target_indices in self.configurations[(v_k, target_indices)].back_set:
                self.backprop(v_m, v_m_target_indices, self.configurations[(v_k, target_indices)].collisions)

    @lru_cache(maxsize=None)
    def get_edge_weight(self, v_k, v_l, target_indices):
        cost = 0
        for i in range(self.n_agents):
            if v_k[i] == v_l[i] == self.v_F[i] and target_indices[i] == len(self.targets[i]) - 1:
                cost += 0
            else:
                cost += 1
        return cost

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
