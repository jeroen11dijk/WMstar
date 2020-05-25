#include <algorithm>
#include "Mstar.h"
#include "inc/Graph.h"
#include "inc/Utils.h"

Mstar::Mstar(std::vector<std::vector<int>> &grid, std::vector<std::pair<int, int>> &v_I_a,
             std::vector<std::vector<std::pair<int, int>>> &v_W_a,
             std::vector<std::pair<int, int>> &v_F_a) {
    n_agents = v_I_a.size();
    graph = create_graph(grid);
    for (std::pair<int, int> &start : v_I_a) {
        v_I.emplace_back(start.first, start.second);
    }
    for (std::pair<int, int> &goal : v_F_a) {
        v_F.emplace_back(goal.first, goal.second);
    }
    for (const std::vector<std::pair<int, int>> &waypoints : v_W_a) {
        std::vector<Coordinate> waypoints_i;
        for (std::pair<int, int> waypoint : waypoints) {
            if (waypoint.first != -1 && waypoint.second != -1) {
                waypoints_i.emplace_back(waypoint.first, waypoint.second);
            }
        }
        v_W.push_back(waypoints_i);
    }
    update_policies_distances_targets();
    bool unordered = true;
    if (unordered) {
        for (int i = 0; i != n_agents; i++) {
            v_W[i] = tsp_dynamic(v_I[i], v_F[i], v_W[i], distances[i]);
        }
        update_policies_distances_targets();
    }
    Config_key v_I_key = Config_key(v_I, std::vector<int>(n_agents, 0));
    configurations[v_I_key] = Config_value(std::vector<int>(n_agents, 0));
    configurations[v_I_key].cost = 0;
    open.push(Queue_entry(heuristic_configuration(v_I_key), v_I_key));
}

void Mstar::update_policies_distances_targets() {
    policies = {};
    distances = {};
    targets = {};
    for (int i = 0; i != n_agents; i++) {
        std::vector<std::unordered_map<Coordinate, std::vector<Coordinate>, coordinate_hash>> policy_i;
        std::vector<std::unordered_map<Coordinate, int, coordinate_hash>> distance_i;
        std::vector<Coordinate> targets_i;
        for (Coordinate const &waypoint : v_W[i]) {
            if (graph.count(waypoint)) {
                std::pair<std::unordered_map<Coordinate, std::vector<Coordinate>, coordinate_hash>, std::unordered_map<Coordinate, int, coordinate_hash>> dijkstra = dijkstra_predecessor_and_distance(
                        graph, waypoint);
                policy_i.push_back(dijkstra.first);
                distance_i.push_back(dijkstra.second);
                targets_i.push_back(waypoint);
            }
        }
        std::pair<std::unordered_map<Coordinate, std::vector<Coordinate>, coordinate_hash>, std::unordered_map<Coordinate, int, coordinate_hash>> dijkstra = dijkstra_predecessor_and_distance(
                graph, v_F[i]);
        policy_i.push_back(dijkstra.first);
        distance_i.push_back(dijkstra.second);
        targets_i.push_back(v_F[i]);
        policies.push_back(policy_i);
        distances.push_back(distance_i);
        targets.push_back(targets_i);
    }
}

std::pair<std::vector<std::vector<std::pair<int, int>>>, int> Mstar::solve() {
    while (!open.empty()) {
        Config_key v_k = open.top().config_key;
        std::cout << v_k << std::endl;
        Config_value &v_k_config = configurations[v_k];
        open.pop();
        if (v_k.coordinates == v_F) {
            bool visited_waypoints = true;
            for (int i = 0; i != n_agents; i++) {
                if (v_k.targets[i] != targets[i].size() - 1) {
                    visited_waypoints = false;
                    break;
                }
            }
            if (visited_waypoints) {
                v_k_config.back_ptr.push_back(v_F);
                std::vector<std::vector<std::pair<int, int>>> res;
                for (int i = 0; i != n_agents; i++) {
                    std::vector<std::pair<int, int>> res_i;
                    for (auto &config : v_k_config.back_ptr) {
                        res_i.emplace_back(config[i].a, config[i].b);
                    }
                    res.push_back(res_i);
                }
                return make_pair(res, v_k_config.cost + n_agents);
            }
        }
        for (std::vector<Coordinate> &v_l : get_limited_neighbours(v_k, v_k_config.collisions)) {
            std::vector<int> v_l_target_indices = v_k.targets;
            for (int i = 0; i != n_agents; i++) {
                if (v_l[i] == targets[i][v_l_target_indices[i]] && v_l[i] != v_F[i]) {
                    v_l_target_indices[i]++;
                }
            }
            std::set<int> v_l_collisions = phi(v_l, v_k.coordinates);
            Config_key v_l_key = Config_key(v_l, v_l_target_indices);
            Config_value v_l_config;
            if (!configurations.count(v_l_key)) {
                v_l_config = Config_value(std::vector<int>(n_agents, 0));
            } else {
                v_l_config = configurations[v_l_key];
            }
            v_l_config.collisions.insert(v_l_collisions.begin(), v_l_collisions.end());
            v_l_config.back_set.insert(v_k);
            backprop(v_k, v_k_config, v_l_config.collisions);
            int f = get_edge_weight(v_k.coordinates, v_l_key, v_k_config.waiting);
            int new_cost_v_l = v_k_config.cost + f;
            int old_cost_v_l = v_l_config.cost;
            if (v_l_collisions.empty() && new_cost_v_l < old_cost_v_l) {
                v_l_config.cost = new_cost_v_l;
                v_l_config.back_ptr = v_k_config.back_ptr;
                v_l_config.back_ptr.push_back(v_k.coordinates);
                for (int i = 0; i != n_agents; i++) {
                    if (v_l_key.coordinates[i] == v_k.coordinates[i]) {
                        v_l_config.waiting[i] = v_k_config.waiting[i] + 1;
                    } else{
                        v_l_config.waiting[i] = 0;
                    }
                }
                configurations[v_l_key] = v_l_config;
                int heuristic = heuristic_configuration(v_l_key);
                open.push(Queue_entry(v_l_config.cost + heuristic, v_l_key));
            }
        }
    }
    std::cout << "No path exists, or I am an idiot";
}

int Mstar::get_edge_weight(std::vector<Coordinate> &prev_coordinates, Config_key &key, std::vector<int> &waiting) {
    int cost = 0;
    for (int i = 0; i != n_agents; i++) {
        bool visited_waypoints = key.targets[i] == targets[i].size() - 1;
        Coordinate prev = prev_coordinates[i];
        Coordinate current = key.coordinates[i];
        Coordinate target = targets[i].back();
        if (prev == target && current != target && visited_waypoints) {
            cost += 1 + waiting[i];
        } else if(!(prev == current && current == target && visited_waypoints)) {
            cost += 1;
        }
    }
    return cost;
}

void Mstar::backprop(Config_key &key, Config_value &value, std::unordered_set<int> &collisions) {
    bool subset = isSubset(collisions, value.collisions);
    if (!subset) {
        value.collisions.insert(collisions.begin(), collisions.end());
        int heuristic = heuristic_configuration(key);

        open.push(Queue_entry(value.cost + heuristic, key));
        for (Config_key v_m : value.back_set) {
            backprop(v_m, configurations[v_m], value.collisions);
        }
    }
}

std::vector<std::vector<Coordinate>> Mstar::get_limited_neighbours(Config_key &v_k, std::unordered_set<int> &collisions) {
    std::vector<std::vector<Coordinate>> options;
    for (int i = 0; i != n_agents; i++) {
        Coordinate source = v_k.coordinates[i];
        std::vector<Coordinate> options_i;
        if (collisions.count(i)) {
            // Add all the neighbours
            options_i.push_back(source);
            int target_index = v_k.targets[i];
            std::vector<Coordinate> successors = policies[i][target_index][source];
            if (successors.size() > 1) {
                for (auto &successor : successors) {
                    options_i.push_back(successor);
                }
            } else {
                for (auto &nbr : graph[source]) {
                    options_i.push_back(nbr);
                }
            }
        } else {
            int target_index = v_k.targets[i];
            std::vector<Coordinate> successors = policies[i][target_index][source];
            if (successors.empty()) {
                options_i.push_back(source);
            } else {
                options_i.push_back(successors[0]);
            }
        }
        options.push_back(options_i);
    }
    std::vector<std::vector<Coordinate>> res;
    if (options.size() == 1) {
        res = options;
    } else {
        res = cart_product(options);
    }
    return res;
}

int Mstar::heuristic_configuration(Config_key &v_k) {
    int cost = 0;
    for (int i = 0; i != n_agents; i++) {
        int target_index = v_k.targets[i];
        std::vector<Coordinate> targets_i = targets[i];
        cost += distances[i][target_index][v_k.coordinates[i]];
        target_index++;
        while (target_index < targets_i.size()) {
            cost += distances[i][target_index][targets_i[target_index - 1]];
            target_index++;
        }
    }
    return cost;
}