import heapq
import itertools
import random

from Python.classes import Config_key, Config_value, FastContainsPriorityQueue
from Python.utils import dijkstra_predecessor_and_distance, phi, dynamic_tsp


class Mstar:
    def __init__(self, graph, v_I, v_W, v_F):
        self.n_agents: int = len(v_I)
        self.graph = graph
        self.starts = v_I
        self.waypoints = v_W
        self.goals = v_F
        self.policies = {}
        self.distances = {}
        self.tsp_cache = {}
        self.update_policies_distances_targets()
        self.configurations = {}
        self.open = FastContainsPriorityQueue()
        v_I_key = Config_key(v_I, v_W)
        self.configurations[v_I_key] = Config_value(cost=0, waiting=self.n_agents * [0])
        self.open.enqueue((self.heuristic_configuration(v_I_key), v_I_key))

    def solve(self):
        configurations = self.configurations
        # While there are configurations to expand we keep going until we find a solution
        while not self.open.empty():
            # Stores the coordinates of the agents and the target indices
            current = self.open.dequeue()[1]
            # Stores the configuration information about current
            current_config = configurations[current]
            # The check to see if we have reached the target while having visited all the waypoints
            if current.coordinates == self.goals and all(len(current.waypoints[i]) == 0 for i in range(self.n_agents)):
                # Return a nice format for the founded path
                current_config.back_ptr.append(self.goals)
                return [list(config) for config in current_config.back_ptr], current_config.cost
            # Get all the neighbours of current and loop over them
            for neighbour in self.get_limited_neighbours(current, current_config.collisions):
                # Create the target indices of the neighbour based on the target indices of current
                neighbour_waypoints = list(current.waypoints)
                for i in range(self.n_agents):
                    if neighbour[i] in neighbour_waypoints[i]:
                        new_waypoints = set(neighbour_waypoints[i])
                        new_waypoints.remove(neighbour[i])
                        neighbour_waypoints[i] = frozenset(new_waypoints)
                # Create a config key for neighbour and get a new configuration for it if it doesnt exist in
                # configurations and else you get the configuration from configurations
                neighbour = Config_key(neighbour, tuple(neighbour_waypoints))
                if neighbour not in configurations:
                    neighbour_config = Config_value(waiting=self.n_agents * [0])
                else:
                    neighbour_config = configurations[neighbour]
                # Check whether the neighbour is in a collision and update the collision set accordingly
                neighbour_in_collision, neighbour_collisions = phi(neighbour.coordinates, current.coordinates)
                neighbour_config.collisions.update(neighbour_collisions)
                # Add current to the back set of neighbour and backpropagate the collisions of neighbour
                neighbour_config.back_set.add(current)
                self.backprop(current, current_config, neighbour_config.collisions)
                # Get the edge cost and see if we found a cheaper path to neighbour
                f = self.get_edge_weight(current.coordinates, neighbour, current_config.waiting)
                new_cost_v_l = current_config.cost + f
                old_cost_v_l = neighbour_config.cost
                if not neighbour_in_collision and new_cost_v_l < old_cost_v_l:
                    # If this is a cheaper path to neighbour we update the configuration of neighbour
                    neighbour_config.cost = current_config.cost + f
                    neighbour_config.back_ptr = current_config.back_ptr + [current.coordinates]
                    # Waiting is used in the case where an agent suddenly moves away from the agent, in which case it
                    # has to add the cost for waiting on the target.
                    for i in range(self.n_agents):
                        if neighbour.coordinates[i] == current.coordinates[i]:
                            neighbour_config.waiting[i] = current_config.waiting[i] + 1
                        else:
                            neighbour_config.waiting[i] = 0
                    configurations[neighbour] = neighbour_config
                    heuristic = self.heuristic_configuration(neighbour)
                    self.open.enqueue((neighbour_config.cost + heuristic, neighbour))
        return "No path exists, or I am an idiot"

    def update_policies_distances_targets(self):
        for i in range(self.n_agents):
            for waypoint in self.waypoints[i]:
                predecessor, distance = dijkstra_predecessor_and_distance(self.graph, waypoint)
                self.distances[waypoint] = distance
                self.policies[waypoint] = predecessor
            predecessor, distance = dijkstra_predecessor_and_distance(self.graph, self.goals[i])
            self.distances[self.goals[i]] = distance
            self.policies[self.goals[i]] = predecessor

    def get_limited_neighbours(self, config_key, collisions):
        neighbours = []
        options = []
        # Loop over all agents and add the neighbours per agent
        # At the end we will do a cartesian product
        for i in range(self.n_agents):
            current = config_key.coordinates[i]
            waypoints = config_key.waypoints[i]
            options_agent = []
            if i in collisions:
                # Append its own location so it can wait and add all the successors if there are multiple
                # Otherwise we add all outgoing neighbours
                options_agent.append(current)
                for nbr in self.graph[current]:
                    options_agent.append(nbr)
            else:
                if len(waypoints) == 0:
                    if current == self.goals[i]:
                        options_agent.append(current)
                    else:
                        options_agent.append(random.choice(self.policies[self.goals[i]][current]))
                elif len(waypoints) == 1:
                    options_agent.append(random.choice(self.policies[list(waypoints)[0]][current]))
                else:
                    tsp = dynamic_tsp(waypoints, self.goals[i], self.distances, self.tsp_cache)
                    min_dist = float("inf")
                    target = current
                    for key in tsp:
                        dist = tsp[key] + self.distances[key][self.starts[i]]
                        if dist < min_dist:
                            min_dist = dist
                            target = key
                    options_agent.append(random.choice(self.policies[target][current]))
            options.append(options_agent)
        # In case there is only one agent
        if len(options) == 1:
            neighbours.append((options[0][0],))
            return neighbours
        # Cartesian product of options to get all combinations of neighbours
        for element in itertools.product(*options):
            neighbours.append(element)
        return neighbours

    def backprop(self, key, config, collisions):
        # If collisions has an item that isnt in config.collisions we need to back propogate that info
        if not collisions.issubset(config.collisions):
            config.collisions.update(collisions)
            # Add configuration back to open since the collision set updated
            if key not in self.open:
                heuristic = self.heuristic_configuration(key)
                self.open.enqueue((config.cost + heuristic, key))
            # Recursive call
            for previous in config.back_set:
                self.backprop(previous, self.configurations[previous], config.collisions)

    def get_edge_weight(self, prev_coordinates, key, waiting):
        cost = 0
        # Loop over agents and calculate individual costs which we will sum at the end
        for i in range(self.n_agents):
            # Check if we visited all waypoints
            visited_waypoints = len(key.waypoints[i]) == 0
            prev = prev_coordinates[i]
            current = key.coordinates[i]
            target = self.goals[i]
            # If we move away from the target we have a cost of 1 + the amount of turns we were waiting on the target
            if prev == target and current != target and visited_waypoints:
                cost += 1 + waiting[i]
            # If we are not waiting on the target we have a cost of 1
            elif not (prev == current == target and visited_waypoints):
                cost += 1
        return cost

    def heuristic_configuration(self, key):
        heuristic = 0
        # Loop over agents and calculate individual heuristic which we will sum at the end
        for i in range(self.n_agents):
            current = key.coordinates[i]
            waypoints = key.waypoints[i]
            goal = self.goals[i]
            if len(waypoints) == 0:
                heuristic += self.distances[goal][current]
            elif len(key.waypoints[i]) == 1:
                heuristic += self.distances[goal][list(waypoints)[0]]
                heuristic += self.distances[list(waypoints)[0]][current]
            else:
                tsp = dynamic_tsp(waypoints, goal, self.distances, self.tsp_cache)
                min_dist = float("inf")
                for coord in tsp:
                    dist = tsp[coord] + self.distances[coord][current]
                    min_dist = min(min_dist, dist)
                heuristic += min_dist
        return heuristic
