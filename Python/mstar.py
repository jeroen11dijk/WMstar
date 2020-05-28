import heapq
import itertools
import math
from collections import namedtuple
from dataclasses import dataclass, field
from typing import List, Set

from Cpp.Mstar_pybind import python_phi

from Python.utils import dijkstra_predecessor_and_distance, tsp_dynamic

Config_key = namedtuple('Config_key', 'coordinates target_indices')


@dataclass
class Config_value:
    back_ptr: List[any] = field(default_factory=list)
    back_set: Set[any] = field(default_factory=set)
    collisions: Set[any] = field(default_factory=set)
    cost: int = math.inf
    waiting: List[any] = field(default_factory=list)

    def __str__(self):
        return str([self.cost, self.collisions, self.back_set, self.back_ptr])

    def __repr__(self):
        return str([self.cost, self.collisions, self.back_set, self.back_ptr])


class Mstar:
    def __init__(self, graph, v_I, v_W, v_F, inflated=False):
        self.n_agents = len(v_I)
        self.graph = graph
        self.v_I = v_I
        self.v_W = v_W
        self.v_F = v_F
        self.inflated = inflated
        self.update_policies_distances_targets(graph)
        self.v_W = []
        for i in range(self.n_agents):
            start = v_I[i]
            end = v_F[i]
            if len(v_W[i]) > 1:
                self.v_W.append(tsp_dynamic(start, end, v_W[i], self.distances[i]))
            else:
                self.v_W.append(v_W[i])
        self.update_policies_distances_targets(graph)
        self.configurations = {}
        self.open = []
        v_I_key = Config_key(v_I, (0,) * self.n_agents)
        self.configurations[v_I_key] = Config_value(cost=0, waiting=self.n_agents * [0])
        heapq.heappush(self.open, (self.heuristic_configuration(v_I_key), v_I_key))

    def solve(self):
        configurations = self.configurations
        while len(self.open) > 0:
            current = heapq.heappop(self.open)[1]
            current_config = configurations[current]
            print(current_config.collisions)
            if current.coordinates == self.v_F and all(
                    current.target_indices[i] + 1 == len(self.targets[i]) for i in range(self.n_agents)):
                current_config.back_ptr.append(self.v_F)
                res = []
                for i in range(self.n_agents):
                    res.append([list(config[i]) for config in current_config.back_ptr])
                return res, current_config.cost + self.n_agents
            neighbours = self.get_limited_neighbours(current, current_config.collisions)
            for neighbour_coordinates in neighbours:
                neighbour_target_indices = list(current.target_indices)
                for i in range(self.n_agents):
                    if neighbour_coordinates[i] == self.targets[i][neighbour_target_indices[i]] and \
                            neighbour_coordinates[i] != self.v_F[i]:
                        neighbour_target_indices[i] += 1
                neighbour = Config_key(neighbour_coordinates, tuple(neighbour_target_indices))
                neighbour_collisions = python_phi(neighbour.coordinates, current.coordinates)
                if neighbour not in configurations:
                    neighbour_config = Config_value(waiting=self.n_agents * [0])
                else:
                    neighbour_config = configurations[neighbour]
                neighbour_config.collisions.update(neighbour_collisions)
                neighbour_config.back_set.add(current)
                self.backprop(current, current_config, neighbour_config.collisions)
                f = self.get_edge_weight(current.coordinates, neighbour, current_config.waiting)
                new_cost_v_l = current_config.cost + f
                old_cost_v_l = neighbour_config.cost
                if len(neighbour_collisions) == 0 and new_cost_v_l < old_cost_v_l:
                    neighbour_config.cost = current_config.cost + f
                    neighbour_config.back_ptr = current_config.back_ptr + [current.coordinates]
                    for i in range(self.n_agents):
                        if neighbour_coordinates[i] == current.coordinates[i]:
                            neighbour_config.waiting[i] = current_config.waiting[i] + 1
                        else:
                            neighbour_config.waiting[i] = 0
                    configurations[neighbour] = neighbour_config
                    heuristic = self.heuristic_configuration(neighbour)
                    heapq.heappush(self.open, (neighbour_config.cost + heuristic, neighbour))
        return "No path exists, or I am an idiot"

    def update_policies_distances_targets(self, graph):
        self.policies = []
        self.distances = []
        self.targets = []
        for i in range(self.n_agents):
            policy_i = []
            distance_i = []
            targets_i = []
            for waypoint in self.v_W[i]:
                if waypoint in graph:
                    predecessor, distance = dijkstra_predecessor_and_distance(graph, waypoint)
                    policy_i.append(predecessor)
                    distance_i.append(distance)
                    targets_i.append(waypoint)
            predecessor, distance = dijkstra_predecessor_and_distance(graph, self.v_F[i])
            policy_i.append(predecessor)
            distance_i.append(distance)
            targets_i.append(self.v_F[i])
            self.policies.append(policy_i)
            self.distances.append(distance_i)
            self.targets.append(targets_i)

    def get_limited_neighbours(self, key, collisions):
        neighbours = []
        options = []
        for i in range(self.n_agents):
            coordinates_i = key.coordinates[i]
            options_i = []
            if i in collisions:
                # ADD all the neighbours
                target_index = key.target_indices[i]
                policy = self.policies[i][target_index]
                successors = policy[key.coordinates[i]]
                options_i.append(coordinates_i)
                if len(successors) > 1:
                    for successor in successors:
                        options_i.append(successor)
                else:
                    for nbr in self.graph[coordinates_i]:
                        options_i.append(nbr)
            else:
                target_index = key.target_indices[i]
                policy = self.policies[i][target_index]
                successors = policy[key.coordinates[i]]
                if len(successors) == 0:
                    options_i.append(coordinates_i)
                else:
                    options_i.append(successors[0])
            options.append(options_i)
        if len(options) == 1:
            neighbours.append((options[0][0],))
            return neighbours
        for element in itertools.product(*options):
            neighbours.append(element)
        return neighbours

    def backprop(self, key, config, collisions):
        if not collisions.issubset(config.collisions):
            config.collisions.update(collisions)
            # Technically we should check whether its not already in open
            # But that takes too much time and it will settle it self
            # if not any(v_k in configuration for configuration in open):
            heuristic = self.heuristic_configuration(key)
            heapq.heappush(self.open, (config.cost + heuristic, key))
            for previous in config.back_set:
                self.backprop(previous, self.configurations[previous], config.collisions)

    def get_edge_weight(self, prev_coordinates, key, waiting):
        cost = 0
        for i in range(self.n_agents):
            visited_waypoints = key.target_indices[i] == len(self.targets[i]) - 1
            prev = prev_coordinates[i]
            current = key.coordinates[i]
            target = self.targets[i][-1]
            if prev == target and current != target and visited_waypoints:
                cost += 1 + waiting[i]
            elif not (prev == current == target and visited_waypoints):
                cost += 1
        return cost

    def heuristic_configuration(self, key):
        cost = 0
        for i in range(self.n_agents):
            target_index = key.target_indices[i]
            target = self.targets[i]
            cost += self.distances[i][target_index][key.coordinates[i]]
            target_index += 1
            while target_index < len(target):
                cost += self.distances[i][target_index][target[target_index - 1]]
                target_index += 1
        if self.inflated:
            return 1.1 * cost
        else:
            return cost
