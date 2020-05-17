import heapq
import itertools

from Mstar_cpp import python_phi

from graph import dijkstra_predecessor_and_distance


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
        self.n_agents = len(v_I)
        self.graph = graph
        self.v_I = v_I
        self.v_W = v_W
        for i in range(self.n_agents):
            start = v_I[i]
            end = v_F[i]
            if len(self.v_W[i]) > 0:
                self.v_W[i].sort(key=lambda x: euclidian_distance(start, x) / euclidian_distance(end, x))
        self.v_F = v_F
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
                    predecessor, distance = dijkstra_predecessor_and_distance(graph, waypoint)
                    policy_i.append(predecessor)
                    distance_i.append(distance)
                    targets_i.append(waypoint)
            predecessor, distance = dijkstra_predecessor_and_distance(graph, v_F[i])
            policy_i.append(predecessor)
            distance_i.append(distance)
            targets_i.append(v_F[i])
            self.policies.append(policy_i)
            self.distances.append(distance_i)
            self.targets.append(targets_i)
        self.open = []
        self.configurations[(v_I, (0,) * self.n_agents)] = Config()
        self.configurations[(v_I, (0,) * self.n_agents)].cost = 0
        heapq.heappush(self.open,
                       (self.heuristic_configuration(v_I, tuple([0] * self.n_agents)), (v_I, (0,) * self.n_agents)))

    def solve(self):
        configurations = self.configurations
        while len(self.open) > 0:
            v_k, target_indices = heapq.heappop(self.open)[1]
            v_k_config = configurations[(v_k, target_indices)]
            if v_k == self.v_F and all(target_indices[i] + 1 == len(self.targets[i]) for i in range(self.n_agents)):
                v_k_config.back_ptr.append(self.v_F)
                res = []
                for i in range(self.n_agents):
                    res.append([list(config[i]) for config in v_k_config.back_ptr])
                return res, v_k_config.cost
            if len(python_phi(v_k, [(-1, -1)])) == 0:
                for v_l in self.get_limited_neighbours(v_k, target_indices):
                    v_l_target_indices = list(target_indices)
                    for i in range(self.n_agents):
                        if v_l[i] == self.targets[i][v_l_target_indices[i]] and v_l[i] != self.v_F[i]:
                            v_l_target_indices[i] += 1
                    v_l_target_indices = tuple(v_l_target_indices)
                    v_l_collisions = python_phi(v_l, v_k)
                    if (v_l, v_l_target_indices) not in configurations:
                        configurations[(v_l, v_l_target_indices)] = Config()
                    v_l_config = configurations[(v_l, v_l_target_indices)]
                    v_l_config.collisions.update(v_l_collisions)
                    v_l_config.back_set.append((v_k, target_indices))
                    self.backprop(v_k, target_indices, v_l_config.collisions)

                    f = self.get_edge_weight(v_k, v_l, v_l_target_indices)
                    new_cost_v_l = v_k_config.cost + f
                    old_cost_v_l = v_l_config.cost
                    if len(v_l_collisions) == 0 and new_cost_v_l < old_cost_v_l:
                        v_l_config.cost = v_k_config.cost + f
                        v_l_config.back_ptr = v_k_config.back_ptr + [v_k]
                        heuristic = self.heuristic_configuration(v_l, v_l_target_indices)
                        heapq.heappush(self.open, (v_l_config.cost + heuristic, (v_l, v_l_target_indices)))
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
                target_index = target_indices[i]
                policy = self.policies[i][target_index]
                successors = policy[v_k[i]]
                if len(successors) == 0:
                    options_i.append(vi_k)
                else:
                    for successor in successors:
                        options_i.append(successor)
            options.append(options_i)
        if len(options) == 1:
            V_k.append((options[0][0],))
            return V_k
        for element in itertools.product(*options):
            V_k.append(element)
        return V_k

    def backprop(self, v_k, target_indices, C_l):
        v_k_config = self.configurations[(v_k, target_indices)]
        if not C_l.issubset(v_k_config.collisions):
            v_k_config.collisions.update(C_l)
            # Technically we should check whether its not already in open
            # But that takes too much time and it will settle it self
            # if not any(v_k in configuration for configuration in open):
            heuristic = self.heuristic_configuration(v_k, target_indices)
            heapq.heappush(self.open, (v_k_config.cost + heuristic, (v_k, target_indices)))
            for v_m, v_m_target_indices in v_k_config.back_set:
                self.backprop(v_m, v_m_target_indices, v_k_config.collisions)

    def get_edge_weight(self, v_k, v_l, target_indices):
        cost = 0
        for i in range(self.n_agents):
            if not (v_k[i] == v_l[i] == self.targets[i][-1] and target_indices[i] == len(self.targets[i]) - 1):
                cost += 1
        return cost

    def heuristic_configuration(self, v_k, target_indices):
        cost = 0
        for i in range(self.n_agents):
            target_index = target_indices[i]
            target = self.targets[i]
            cost += self.distances[i][target_index][v_k[i]]
            target_index += 1
            while target_index < len(target):
                cost += self.distances[i][target_index][target[target_index - 1]]
                target_index += 1
        return cost


def euclidian_distance(a, b):
    return abs(a[0] - b[0]) + abs(a[1] - b[1])
