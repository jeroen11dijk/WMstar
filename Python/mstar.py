import heapq
import itertools

from Python.classes import Config_key, Config_value
from Python.utils import dijkstra_predecessor_and_distance, tsp_dynamic, phi


class Mstar:
    def __init__(self, graph, v_I, v_W, v_F, ordered=False, inflated=False):
        self.n_agents: int = len(v_I)
        self.graph = graph
        self.v_I = v_I
        self.v_W = v_W
        self.v_F = v_F
        self.policies = []
        self.distances = []
        self.targets = []
        self.inflated = inflated
        self.update_policies_distances_targets()
        self.v_W = []
        for i in range(self.n_agents):
            start = v_I[i]
            end = v_F[i]
            if len(v_W[i]) > 1:
                if not ordered:
                    self.v_W.append(tsp_dynamic(start, end, v_W[i], self.distances[i]))
                else:
                    self.v_W.append(v_W[i])
                self.targets.append(self.v_W[i] + [self.v_F[i]])
            elif (len(v_W[i])) == 1:
                self.v_W.append(v_W[i])
                self.targets.append(self.v_W[i] + [self.v_F[i]])
            else:
                self.v_W.append(v_W[i])
                self.targets.append([self.v_F[i]])
        self.configurations = {}
        self.open = []
        v_I_target_indices = [0] * self.n_agents
        for i in range(self.n_agents):
            if v_I[i] == self.targets[i][0] and \
                    v_I_target_indices[i] < len(self.targets[i]) - 1:
                v_I_target_indices[i] += 1
        v_I_key = Config_key(v_I, tuple(v_I_target_indices))
        self.configurations[v_I_key] = Config_value(cost=0, waiting=self.n_agents * [0])
        heapq.heappush(self.open, (self.heuristic_configuration(v_I_key), v_I_key))

    def solve(self):
        configurations = self.configurations
        # While there are configurations to expand we keep going until we find a solution
        while len(self.open) > 0:
            # Stores the coordinates of the agents and the target indices
            current = heapq.heappop(self.open)[1]
            # Stores the configuration information about current
            current_config = configurations[current]
            # The check to see if we have reached the target while having visited all the waypoints
            if current.coordinates == self.v_F and all(
                    current.target_indices[i] + 1 == len(self.targets[i]) for i in range(self.n_agents)):
                # Return a nice format for the founded path
                current_config.back_ptr.append(self.v_F)
                res = []
                for i in range(self.n_agents):
                    res.append([list(config[i]) for config in current_config.back_ptr])
                return res, current_config.cost + self.n_agents
            # Get all the neighbours of current and loop over them
            neighbours = self.get_limited_neighbours(current, current_config.collisions)
            for neighbour_coordinates in neighbours:
                # Create the target indices of the neighbour based on the target indices of current
                neighbour_target_indices = list(current.target_indices)
                for i in range(self.n_agents):
                    if neighbour_coordinates[i] == self.targets[i][neighbour_target_indices[i]] and \
                            neighbour_target_indices[i] < len(self.targets[i]) - 1:
                        neighbour_target_indices[i] += 1
                # Create a config key for neighbour and get a new configuration for it if it doesnt exist in
                # configurations and else you get the configuration from configurations
                neighbour = Config_key(neighbour_coordinates, tuple(neighbour_target_indices))
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
                        if neighbour_coordinates[i] == current.coordinates[i]:
                            neighbour_config.waiting[i] = current_config.waiting[i] + 1
                        else:
                            neighbour_config.waiting[i] = 0
                    configurations[neighbour] = neighbour_config
                    heuristic = self.heuristic_configuration(neighbour)
                    heapq.heappush(self.open, (neighbour_config.cost + heuristic, neighbour))
        return "No path exists, or I am an idiot"

    def update_policies_distances_targets(self):
        self.policies = []
        self.distances = []
        # Loop over all agents and append to policies and distances so the index can be used to retrieve per agent
        for i in range(self.n_agents):
            policy_i = {}
            distance_i = {}
            # Add the predecessor and distance policy of the waypoints
            for waypoint in self.v_W[i]:
                if waypoint in self.graph:
                    predecessor, distance = dijkstra_predecessor_and_distance(self.graph, waypoint)
                    policy_i[waypoint] = predecessor
                    distance_i[waypoint] = distance
            # Add the predecessor and distance policy of the target
            predecessor, distance = dijkstra_predecessor_and_distance(self.graph, self.v_F[i])
            policy_i[self.v_F[i]] = predecessor
            distance_i[self.v_F[i]] = distance
            self.policies.append(policy_i)
            self.distances.append(distance_i)

    def get_limited_neighbours(self, key, collisions):
        neighbours = []
        options = []
        # Loop over all agents and add the neighbours per agent
        # At the end we will do a cartesian product
        for i in range(self.n_agents):
            coordinates_i = key.coordinates[i]
            options_i = []
            target_index = key.target_indices[i]
            target = self.targets[i][target_index]
            policy = self.policies[i][target]
            successors = policy[key.coordinates[i]]
            # See if this agent will run in a collision
            if i in collisions:
                # Append its own location so it can wait and add all the successors if there are multiple
                # Otherwise we add all outgoing neighbours
                options_i.append(coordinates_i)
                if len(successors) > 1:
                    for successor in successors:
                        options_i.append(successor)
                else:
                    for nbr in self.graph[coordinates_i]:
                        options_i.append(nbr)
            else:
                # Either append the only successor or the first one
                if len(successors) == 0:
                    options_i.append(coordinates_i)
                else:
                    options_i.append(successors[0])
            options.append(options_i)
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
            heuristic = self.heuristic_configuration(key)
            heapq.heappush(self.open, (config.cost + heuristic, key))
            # Recursive call
            for previous in config.back_set:
                self.backprop(previous, self.configurations[previous], config.collisions)

    def get_edge_weight(self, prev_coordinates, key, waiting):
        cost = 0
        # Loop over agents and calculate individual costs which we will sum at the end
        for i in range(self.n_agents):
            # Check if we visited all waypoints
            visited_waypoints = key.target_indices[i] == len(self.targets[i]) - 1
            prev = prev_coordinates[i]
            current = key.coordinates[i]
            target = self.targets[i][-1]
            # If we move away from the target we have a cost of 1 + the amount of turns we were waiting on the target
            if prev == target and current != target and visited_waypoints:
                cost += 1 + waiting[i]
            # If we are not waiting on the target we have a cost of 1
            elif not (prev == current == target and visited_waypoints):
                cost += 1
        return cost

    def heuristic_configuration(self, key):
        cost = 0
        # Loop over agents and calculate individual heuristic which we will sum at the end
        for i in range(self.n_agents):
            # Add the cost from the agent location to its next waypoint
            target_index = key.target_indices[i]
            targets = self.targets[i]
            cost += self.distances[i][targets[target_index]][key.coordinates[i]]
            # Add the cost from the next waypoint to the next until you reach the target
            target_index += 1
            while target_index < len(targets):
                cost += self.distances[i][targets[target_index]][targets[target_index - 1]]
                target_index += 1
        # Multiply the cost with 1.1 in case we run the inflated heuristic version
        if self.inflated:
            return 1.1 * cost
        else:
            return cost
