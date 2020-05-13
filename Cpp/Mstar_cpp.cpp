#include <pybind11/stl.h>
#include <pybind11/pybind11.h>
#include <queue>
#include <string>
#include <utility>
#include <iostream>
#include <vector>
#include <numeric>

#include "classes/Config_key.h"
#include "classes/Config_value.h"
#include "classes/Coordinate.h"
#include "classes/Queue_entry.h"

using namespace std;
namespace py = pybind11;

class CompareTuple
{
public:
	bool operator()(tuple<int, int, Coordinate> t1, tuple<int, int, Coordinate> t2) {
		if (get<0>(t1) == get<0>(t2)) {
			return get<1>(t1) > get<1>(t2);
		}
		else {
			return get<0>(t1) > get<0>(t2);
		}
	}
};

set<int> phi(vector<Coordinate> v_k) {
	unordered_set<Coordinate, coordinate_hash> seen{};
	unordered_set<Coordinate, coordinate_hash> collisions{};
	set<int> res{};
	for (Coordinate val : v_k) {
		if (seen.count(val)) {
			collisions.insert(val);
		}
		else {
			seen.insert(val);
		}
	}
	for (int i = 0; i != v_k.size(); i++) {
		if (collisions.count(v_k[i])) {
			res.insert(i);
		}
	}
	return res;
}

pair<unordered_map<Coordinate, vector<Coordinate>, coordinate_hash>, unordered_map<Coordinate, int, coordinate_hash>> dijkstra_predecessor_and_distance(unordered_map<Coordinate, vector<Coordinate>, coordinate_hash> graph, Coordinate source) {
	unordered_map<Coordinate, int, coordinate_hash> distances;
	unordered_map<Coordinate, vector<Coordinate>, coordinate_hash> pred = { {source, vector<Coordinate>{}} };
	unordered_map<Coordinate, int, coordinate_hash> seen = { {source, 0} };
	int c = 1;
	priority_queue<tuple<int, int, Coordinate>, vector<tuple<int, int, Coordinate>>, CompareTuple> fringe;
	fringe.push(make_tuple(0, c, source));
	while (!fringe.empty()) {
		tuple<int, int, Coordinate> current = fringe.top();
		fringe.pop();
		int distance = get<0>(current);
		Coordinate node = get<2>(current);
		if (distances.count(node)) {
			continue;
		}
		distances[node] = distance;
		vector<Coordinate> neighbours = graph[node];
		for (Coordinate neighbour : neighbours) {
			int neighbour_distance = distance + 1;
			if (!seen.count(neighbour) || neighbour_distance < seen[neighbour]) {
				seen[neighbour] = neighbour_distance;
				c++;
				fringe.push(make_tuple(neighbour_distance, c, neighbour));
				pred[neighbour] = vector<Coordinate>{ node };
			}
			else if (neighbour_distance == seen[neighbour]) {
				pred[neighbour].push_back(node);
			}
		}
	}
	return make_pair(pred, distances);
}

unordered_map<Coordinate, vector<Coordinate>, coordinate_hash> create_graph(vector<vector<int>> grid) {
	unordered_map<Coordinate, vector<Coordinate>, coordinate_hash> graph;
	for (int i = 0; i != grid.size(); i++) {
		for (int j = 0; j != grid[0].size(); j++) {
			if (grid[i][j] == 0) {
				Coordinate current = Coordinate(j, i);
				vector<Coordinate> neighbours;
				if (i != 0 && grid[i - 1][j] == 0) {
					neighbours.push_back(Coordinate(j, i - 1));
				}
				if (j != 0 && grid[i][j - 1] == 0) {
					neighbours.push_back(Coordinate(j - 1, i));
				}
				if (i != grid.size() - 1 && grid[i + 1][j] == 0) {
					neighbours.push_back(Coordinate(j, i + 1));
				}
				if (j != grid[0].size() - 1 && grid[i][j + 1] == 0) {
					neighbours.push_back(Coordinate(j + 1, i));
				}
				graph[current] = neighbours;
			}
		}
	}
	return graph;
}

// Credit: https://stackoverflow.com/a/17050528
vector<vector<Coordinate>> cart_product(const vector<vector<Coordinate>>& v) {
	vector<vector<Coordinate>> s = { {} };
	for (const auto& u : v) {
		vector<vector<Coordinate>> r;
		for (const auto& x : s) {
			for (const auto y : u) {
				r.push_back(x);
				r.back().push_back(y);
			}
		}
		s = move(r);
	}
	return s;
}

class Mstar_cpp {
public:
	int n_agents;
	unordered_map<Coordinate, vector<Coordinate>, coordinate_hash> graph;
	vector<Coordinate> v_I, v_F;
	vector<vector<Coordinate>> v_W;
	unordered_map<Config_key, Config_value, config_key_hash> configurations;
	vector<vector<unordered_map<Coordinate, vector<Coordinate>, coordinate_hash>>> policies;
	vector<vector<unordered_map<Coordinate, int, coordinate_hash>>> distances;
	vector<vector<Coordinate>> targets;
	priority_queue<Queue_entry, vector<Queue_entry>, greater<Queue_entry>> open;

	Mstar_cpp(vector<vector<int>> grid, vector<pair<int, int>> v_I, vector<vector<pair<int, int>>> v_W, vector<pair<int, int>> v_F) {
		this->n_agents = v_I.size();
		this->graph = create_graph(grid);
		for (pair<int, int> start : v_I) {
			this->v_I.push_back(Coordinate(start.first, start.second));
		}
		// TODO Sort v_W
		for (vector<pair<int, int>> waypoints : v_W) {
			vector<Coordinate> waypoints_i;
			for (pair<int, int> waypoint : waypoints) {
				if (waypoint.first != -1 && waypoint.second != -1) {
					waypoints_i.push_back(Coordinate(waypoint.first, waypoint.second));
				}
			}
			this->v_W.push_back(waypoints_i);
		}
		for (pair<int, int> goal : v_F) {
			this->v_F.push_back(Coordinate(goal.first, goal.second));
		}
		for (int i = 0; i != this->n_agents; i++) {
			vector<unordered_map<Coordinate, vector<Coordinate>, coordinate_hash>> policy_i;
			vector<unordered_map<Coordinate, int, coordinate_hash>> distance_i;
			vector<Coordinate> targets_i;
			for (Coordinate const& waypoint : this->v_W[i]) {
				if (this->graph.count(waypoint)) {
					pair<unordered_map<Coordinate, vector<Coordinate>, coordinate_hash>, unordered_map<Coordinate, int, coordinate_hash>> dijkstra = dijkstra_predecessor_and_distance(graph, waypoint);
					policy_i.push_back(dijkstra.first);
					distance_i.push_back(dijkstra.second);
					targets_i.push_back(waypoint);
				}
			}
			pair<unordered_map<Coordinate, vector<Coordinate>, coordinate_hash>, unordered_map<Coordinate, int, coordinate_hash>> dijkstra = dijkstra_predecessor_and_distance(graph, this->v_F[i]);
			policy_i.push_back(dijkstra.first);
			distance_i.push_back(dijkstra.second);
			targets_i.push_back(this->v_F[i]);
			this->policies.push_back(policy_i);
			this->distances.push_back(distance_i);
			this->targets.push_back(targets_i);
		}
		Config_key v_I_key = Config_key(this->v_I, vector<int>(this->n_agents, 0));
		configurations[v_I_key] = Config_value();
		configurations[v_I_key].cost = 0;
		open.push(Queue_entry(heuristic_configuration(v_I_key), v_I_key));
	}

	pair<vector<vector<pair<int, int>>>, int> solve() {
		while (!open.empty()) {
			Config_key v_k = open.top().config_key;
			open.pop();
			// TODO check for waypoints
			if (v_k.coordinates == v_F) {
				bool visited_waypoints = true;
				for (int i = 0; i != n_agents; i++) {
					if (v_k.targets[i] != targets[i].size() - 1) {
						visited_waypoints = false;
						break;
					}
				}
				if (visited_waypoints) {
					configurations[v_k].back_ptr.push_back(v_F);
					vector<vector<pair<int, int>>> res;
					for (int i = 0; i != n_agents; i++) {
						bool visited_waypoints = true;
						vector<pair<int, int>> res_i;
						for (auto config : configurations[v_k].back_ptr) {
							res_i.push_back(make_pair(config[i].a, config[i].b));
						}
						res.push_back(res_i);
					}
					return make_pair(res, configurations[v_k].cost);
				}
			}
			if (phi(v_k.coordinates).size() == 0) {
				for (vector<Coordinate> v_l : get_limited_neighbours(v_k)) {
					vector<int> v_l_target_indices = v_k.targets;
					for (int i = 0; i != n_agents; i++) {
						if (v_l[i] == targets[i][v_l_target_indices[i]] && v_l[i] != v_F[i]) {
							v_l_target_indices[i]++;
						}
					}
					set<int> v_l_collisions = phi(v_l);
					Config_key v_l_key = Config_key(v_l, v_l_target_indices);
					if (!configurations.count(v_l_key)) {
						configurations[v_l_key] = Config_value();
					}
					configurations[v_l_key].collisions.insert(v_l_collisions.begin(), v_l_collisions.end());
					configurations[v_l_key].back_set.push_back(v_k);
					backprop(v_k, configurations[v_l_key].collisions);
					int f = get_edge_weight(v_k, v_l_key);
					int new_cost_v_l = configurations[v_k].cost + f;
					int old_cost_v_l = configurations[v_l_key].cost;
					if (v_l_collisions.size() == 0 && new_cost_v_l < old_cost_v_l) {
						configurations[v_l_key].cost = new_cost_v_l;
						configurations[v_l_key].back_ptr = configurations[v_k].back_ptr;
						configurations[v_l_key].back_ptr.push_back(v_k.coordinates);
						int heuristic = heuristic_configuration(v_l_key);
						open.push(Queue_entry(configurations[v_l_key].cost + heuristic, v_l_key));
					}
				}
			}
		}
		cout << "No path exists, or I am an idiot";
	}

	int get_edge_weight(Config_key v_k, Config_key v_l) {
		int cost = 0;
		for (int i = 0; i != n_agents; i++) {
			if (!(v_k.coordinates[i] == v_l.coordinates[i] && v_k.coordinates[i] == v_F[i] && v_l.targets[i] == targets[i].size() - 1)) {
				cost++;
			}
		}
		return cost;
	}

	void backprop(Config_key v_k, set<int> C_l) {
		Config_value* v_k_config = &configurations[v_k];
		if (includes(C_l.begin(), C_l.end(), v_k_config->collisions.begin(), v_k_config->collisions.end())) {
			v_k_config->collisions.insert(C_l.begin(), C_l.end());
			int heuristic = heuristic_configuration(v_k);
			open.push(Queue_entry(v_k_config->cost + heuristic, v_k));
			for (Config_key v_m : v_k_config->back_set) {
				backprop(v_m, v_k_config->collisions);
			}
		}
	}

	vector<vector<Coordinate>> get_limited_neighbours(Config_key v_k) {
		vector<vector<Coordinate>> options;
		for (int i = 0; i != n_agents; i++) {
			Coordinate source = v_k.coordinates[i];
			vector<Coordinate> options_i;
			if (configurations[v_k].collisions.count(i)) {
				// Add all the neighbours
				options_i.push_back(source);
				for (auto nbr : graph[source]) {
					options_i.push_back(nbr);
				}
			}
			else {
				int target_index = v_k.targets[i];
				vector<Coordinate> successors = policies[i][target_index][source];
				if (successors.size() == 0) {
					options_i.push_back(source);
				}
				else {
					for (auto successor : successors) {
						options_i.push_back(successor);
					}
				}
			}
			options.push_back(options_i);
		}
		if (options.size() == 1) {
			return options;
		}
		else {
			return cart_product(options);
		}
	}

	int heuristic_configuration(Config_key v_k) {
		int cost = 0;
		for (int i = 0; i != this->n_agents; i++) {
			int target_index = v_k.targets[i];
			vector<Coordinate> targets = this->targets[i];
			cost += this->distances[i][target_index][v_k.coordinates[i]];
			target_index++;
			while (target_index < targets.size()) {
				cost += this->distances[i][target_index][targets[target_index - 1]];
				target_index++;
			}
		}
		return cost;
	}
};


PYBIND11_MODULE(Mstar_cpp, m) {

	m.doc() = "Mstar in Cpp";
	m.def("phi", &phi);
	m.def("create_graph", &create_graph);

	py::class_<Mstar_cpp>(m, "Mstar_cpp")
		.def(py::init<vector<vector<int>>, vector<pair<int, int>>, vector<vector<pair<int, int>>>, vector<pair<int, int>>>())
		.def("solve", &Mstar_cpp::solve)
		.def_readwrite("n_agents", &Mstar_cpp::n_agents)
		.def_readwrite("graph", &Mstar_cpp::graph)
		.def_readwrite("v_I", &Mstar_cpp::v_I)
		.def_readwrite("v_W", &Mstar_cpp::v_W)
		.def_readwrite("v_F", &Mstar_cpp::v_F)
		.def_readwrite("configurations", &Mstar_cpp::configurations)
		.def_readwrite("policies", &Mstar_cpp::policies)
		.def_readwrite("distances", &Mstar_cpp::distances)
		.def_readwrite("targets", &Mstar_cpp::targets)
		.def_readwrite("open", &Mstar_cpp::open);
}