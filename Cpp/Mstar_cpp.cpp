#include <pybind11/stl.h>
#include <pybind11/pybind11.h>
#include <queue>
#include <string>
#include <utility>
#include <iostream>
#include <vector>

#include "classes/Config_key.h"
#include "classes/Config_value.h"
#include "classes/Coordinate.h"
#include "classes/Queue_entry.h"

using namespace std;
namespace py = pybind11;

class Mstar {
public:
	int n_agent;
	unordered_map<Coordinate, vector<Coordinate>, coordinate_hash> graph;
	vector<Coordinate> V_I, v_F;
	vector<vector<Coordinate>> v_W;
	unordered_map<Config_key, Config_value, config_key_hash> configurations;
	vector<vector<unordered_map<Coordinate, vector<Coordinate>, coordinate_hash>>> policies;
	vector<vector<unordered_map<Coordinate, int, coordinate_hash>>> distances;
	vector<vector<Coordinate>> targets;
	priority_queue<Queue_entry, vector<Queue_entry>, greater<Queue_entry>> open;
};

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

PYBIND11_MODULE(Mstar_cpp, m) {

	m.doc() = "Mstar in Cpp";
	m.def("phi", &phi);
	m.def("create_graph", &create_graph);

	py::class_<Config_value>(m, "Config")
		.def(py::init<>())
		.def_readwrite("cost", &Config_value::cost)
		.def_readwrite("heuristic", &Config_value::heuristic)
		.def_readwrite("collisions", &Config_value::collisions)
		.def_readwrite("back_set", &Config_value::back_set)
		.def_readwrite("back_ptr", &Config_value::back_ptr);
}