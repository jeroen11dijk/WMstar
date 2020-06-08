import heapq
import itertools
from queue import Queue
from typing import Dict, Tuple
from Cpp.Mstar_pybind import python_phi

from Python.classes import Config_key, Config_value
from Python.utils import dijkstra_predecessor_and_distance, dynamic_tsp


class Mstar:
    def __init__(self, graph, v_I, v_W, v_F, inflated=False):
        self.n_agents = len(v_I)
        self.graph = graph
        self.v_I = v_I
        self.v_W = v_W
        self.v_F = v_F
        self.policies = []
        self.distances = []
        self.targets = []
        self.inflated = inflated
        self.update_policies_distances_targets(graph)
        self.configurations = dict()
        self.open = []
        self.shared_cache = dict()
        v_I_key = Config_key(coordinates=v_I, visited_waypoints=(frozenset(), ) * self.n_agents)
        self.configurations[v_I_key] = Config_value(cost=0, waiting=self.n_agents * [0])
        heapq.heappush(self.open, (self.heuristic_configuration(v_I_key), v_I_key))

    def solve(self):
        configurations = self.configurations
        while len(self.open) > 0:
            current = heapq.heappop(self.open)[1]
            print(current.coordinates, [len(waypoints) for waypoints in current.visited_waypoints])
            current_config = configurations[current]
            if current.coordinates == self.v_F and all(
                    len(current.visited_waypoints[i]) == len(self.v_W[i]) for i in range(self.n_agents)):
                current_config.back_ptr.append(self.v_F)
                res = []
                for i in range(self.n_agents):
                    res.append([list(config[i]) for config in current_config.back_ptr])
                return res, current_config.cost + self.n_agents
            neighbours = self.get_limited_neighbours(current, current_config.collisions)
            for neighbour_coordinates in neighbours:
                neighbour_visited_waypoints = list(current.visited_waypoints)
                for i in range(self.n_agents):
                    if neighbour_coordinates[i] in self.v_W[i]:
                        normalset = set(neighbour_visited_waypoints[i])
                        normalset.add(neighbour_coordinates[i])
                        neighbour_visited_waypoints[i] = frozenset(normalset)
                neighbour = Config_key(neighbour_coordinates, tuple(neighbour_visited_waypoints))
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
        for i in range(self.n_agents):
            policy_i = {}
            distance_i = {}
            for waypoint in self.v_W[i]:
                if waypoint in graph:
                    predecessor, distance = dijkstra_predecessor_and_distance(graph, waypoint)
                    policy_i[waypoint] = predecessor
                    distance_i[waypoint] = distance
            predecessor, distance = dijkstra_predecessor_and_distance(graph, self.v_F[i])
            policy_i[self.v_F[i]] = predecessor
            distance_i[self.v_F[i]] = distance
            self.policies.append(policy_i)
            self.distances.append(distance_i)

    def get_limited_neighbours(self, key, collisions):
        neighbours = []
        options = []
        for i in range(self.n_agents):
            position = key.coordinates[i]
            distances = self.distances[i]
            policies = self.policies[i]
            waypoints = self.v_W[i]
            target = self.v_F[i]
            options_i = []
            if len(key.visited_waypoints[i]) != len(waypoints):
                to_visit = self.v_W[i] - key.visited_waypoints[i]
                path_lengths = dynamic_tsp(to_visit, target, distances)
                waypoint = min(path_lengths.items(), key=lambda wp: path_lengths[wp[0]] + distances[wp[0]][position])[0]
                successors = policies[waypoint][position]
            else:
                successors = policies[target][position]
            if i in collisions:
                options_i.append(position)
                if len(successors) > 1:
                    for successor in successors:
                        options_i.append(successor)
                else:
                    for nbr in self.graph[position]:
                        options_i.append(nbr)
            else:
                if len(successors) == 0:
                    options_i.append(position)
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
            visited_waypoints = len(key.visited_waypoints[i]) == len(self.v_W[i])
            prev = prev_coordinates[i]
            current = key.coordinates[i]
            target = self.v_F[i]
            if prev == target and current != target and visited_waypoints:
                cost += 1 + waiting[i]
            elif not (prev == current == target and visited_waypoints):
                cost += 1
        return cost

    def heuristic_configuration(self, key):
        cost = 0
        for i in range(self.n_agents):
            position = key.coordinates[i]
            distances = self.distances[i]
            target = self.v_F[i]
            waypoints = self.v_W[i]
            if len(key.visited_waypoints[i]) != len(waypoints):
                to_visit = self.v_W[i] - key.visited_waypoints[i]
                path_lengths = dynamic_tsp(to_visit, target, distances)
                cost += min(path_lengths[wp] + distances[wp][position] for wp in to_visit)
            else:
                cost += distances[target][position]
        if self.inflated:
            return 1.1 * cost
        else:
            return cost
