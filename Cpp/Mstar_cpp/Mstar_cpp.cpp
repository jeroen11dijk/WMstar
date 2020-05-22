#include <algorithm>
#include "Mstar_cpp.h"
#include "inc/Graph.h"
#include "inc/Utils.h"

using namespace std;

Mstar_cpp::Mstar_cpp(vector<vector<int>> &grid, vector<pair<int, int>> &v_I_a, vector<vector<pair<int, int>>> &v_W_a,
                     vector<pair<int, int>> &v_F_a) {
    n_agents = v_I_a.size();
    graph = create_graph(grid);
    for (pair<int, int> &start : v_I_a) {
        v_I.emplace_back(start.first, start.second);
    }
    for (pair<int, int> &goal : v_F_a) {
        v_F.emplace_back(goal.first, goal.second);
    }
    for (const vector<pair<int, int>> &waypoints : v_W_a) {
        vector<Coordinate> waypoints_i;
        for (pair<int, int> waypoint : waypoints) {
            if (waypoint.first != -1 && waypoint.second != -1) {
                waypoints_i.emplace_back(waypoint.first, waypoint.second);
            }
        }
        v_W.push_back(waypoints_i);
    }
    for (int i = 0; i != n_agents; i++) {
        Coordinate start = v_I[i];
        Coordinate end = v_F[i];
        if (v_W[i].size() > 1) {
            sort(v_W[i].begin(), v_W[i].end(),
                 [start, end](const Coordinate &a, const Coordinate &b) -> bool {
                     float a_ratio = float(euclidian_distance(a, start)) / float(euclidian_distance(a, end));
                     float b_ratio = float(euclidian_distance(b, start)) / float(euclidian_distance(b, end));
                     return a_ratio < b_ratio;
                 });
        }
    }
    for (int i = 0; i != n_agents; i++) {
        vector<unordered_map<Coordinate, vector<Coordinate>, coordinate_hash>> policy_i;
        vector<unordered_map<Coordinate, int, coordinate_hash>> distance_i;
        vector<Coordinate> targets_i;
        for (Coordinate const &waypoint : v_W[i]) {
            if (graph.count(waypoint)) {
                pair<unordered_map<Coordinate, vector<Coordinate>, coordinate_hash>, unordered_map<Coordinate, int, coordinate_hash>> dijkstra = dijkstra_predecessor_and_distance(
                        graph, waypoint);
                policy_i.push_back(dijkstra.first);
                distance_i.push_back(dijkstra.second);
                targets_i.push_back(waypoint);
            }
        }
        pair<unordered_map<Coordinate, vector<Coordinate>, coordinate_hash>, unordered_map<Coordinate, int, coordinate_hash>> dijkstra = dijkstra_predecessor_and_distance(
                graph, v_F[i]);
        policy_i.push_back(dijkstra.first);
        distance_i.push_back(dijkstra.second);
        targets_i.push_back(v_F[i]);
        policies.push_back(policy_i);
        distances.push_back(distance_i);
        targets.push_back(targets_i);
    }
    Config_key v_I_key = Config_key(v_I, vector<int>(n_agents, 0));
    configurations[v_I_key] = Config_value();
    configurations[v_I_key].cost = 0;
    open.push(Queue_entry(heuristic_configuration(v_I_key), v_I_key));
}

pair<vector<vector<pair<int, int>>>, int> Mstar_cpp::solve() {
    while (!open.empty()) {
        Config_key v_k = open.top().config_key;
        cout << v_k << endl;
        Config_value v_k_config = configurations[v_k];
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
                vector<vector<pair<int, int>>> res;
                for (int i = 0; i != n_agents; i++) {
                    vector<pair<int, int>> res_i;
                    for (auto &config : v_k_config.back_ptr) {
                        res_i.emplace_back(config[i].a, config[i].b);
                    }
                    res.push_back(res_i);
                }
                cout << "backprop1 took: " << backprop_time1
                     << ". Which is hopefully the title of your sextape and was called: " << endl;
                cout << "backprop2 took: " << backprop_time2
                     << ". Which is hopefully the title of your sextape and was called: " << endl;
                return make_pair(res, v_k_config.cost);
            }
        }
        for (vector<Coordinate> &v_l : get_limited_neighbours(v_k)) {
            vector<int> v_l_target_indices = v_k.targets;
            for (int i = 0; i != n_agents; i++) {
                if (v_l[i] == targets[i][v_l_target_indices[i]] && v_l[i] != v_F[i]) {
                    v_l_target_indices[i]++;
                }
            }
            set<int> v_l_collisions = phi(v_l, v_k.coordinates);
            Config_key v_l_key = Config_key(v_l, v_l_target_indices);
            Config_value v_l_config;
            if (!configurations.count(v_l_key)) {
                v_l_config = Config_value();
            } else {
                v_l_config = configurations[v_l_key];
            }
            v_l_config.collisions.insert(v_l_collisions.begin(), v_l_collisions.end());
            v_l_config.back_set.insert(v_k);
            backprop(v_k, v_l_config.collisions);
            int f = get_edge_weight(v_k, v_l_key);
            int new_cost_v_l = v_k_config.cost + f;
            int old_cost_v_l = v_l_config.cost;
            if (v_l_collisions.empty() && new_cost_v_l < old_cost_v_l) {
                v_l_config.cost = new_cost_v_l;
                v_l_config.back_ptr = v_k_config.back_ptr;
                v_l_config.back_ptr.push_back(v_k.coordinates);
                configurations[v_l_key] = v_l_config;
                int heuristic = heuristic_configuration(v_l_key);
                open.push(Queue_entry(v_l_config.cost + heuristic, v_l_key));
            }
        }
    }
    cout << "No path exists, or I am an idiot";
}

int Mstar_cpp::get_edge_weight(Config_key &v_k, Config_key &v_l) {
    int cost = 0;
    for (int i = 0; i != n_agents; i++) {
        if (!(v_k.coordinates[i] == v_l.coordinates[i] && v_k.coordinates[i] == v_F[i] &&
              v_l.targets[i] == targets[i].size() - 1)) {
            cost++;
        }
    }
    return cost;
}

void Mstar_cpp::backprop(Config_key &v_k, unordered_set<int> &C_l) {
    time.start();
    Config_value &current_config = configurations[v_k];
    bool subset = isSubset(C_l, current_config.collisions);
    time.stop();
    backprop_time1 += float(time.elapsed());
    time.start();
    if (!subset) {
        current_config.collisions.insert(C_l.begin(), C_l.end());
        int heuristic = heuristic_configuration(v_k);

        open.push(Queue_entry(current_config.cost + heuristic, v_k));
        for (Config_key v_m : current_config.back_set) {
            backprop(v_m, current_config.collisions);
        }
    }
    time.stop();
    backprop_time2 += float(time.elapsed());
}

vector<vector<Coordinate>> Mstar_cpp::get_limited_neighbours(Config_key &v_k) {
    vector<vector<Coordinate>> options;
    for (int i = 0; i != n_agents; i++) {
        Coordinate source = v_k.coordinates[i];
        vector<Coordinate> options_i;
        if (configurations[v_k].collisions.count(i)) {
            // Add all the neighbours
            options_i.push_back(source);
            int target_index = v_k.targets[i];
            vector<Coordinate> successors = policies[i][target_index][source];
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
            vector<Coordinate> successors = policies[i][target_index][source];
            if (successors.empty()) {
                options_i.push_back(source);
            } else {
                options_i.push_back(successors[0]);
            }
        }
        options.push_back(options_i);
    }
    if (options.size() == 1) {
        return options;
    } else {
        return cart_product(options);
    }
}

int Mstar_cpp::heuristic_configuration(Config_key &v_k) {
    int cost = 0;
    for (int i = 0; i != n_agents; i++) {
        int target_index = v_k.targets[i];
        vector<Coordinate> targets_i = targets[i];
        cost += distances[i][target_index][v_k.coordinates[i]];
        target_index++;
        while (target_index < targets_i.size()) {
            cost += distances[i][target_index][targets_i[target_index - 1]];
            target_index++;
        }
    }
    return cost;
}