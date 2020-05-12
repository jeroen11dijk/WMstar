#include <pybind11/stl.h>
#include <pybind11/pybind11.h>

#include <string>
#include <utility>

#include <vector>

namespace py = pybind11;

typedef std::pair<int, int> coordinate;

struct pair_hash
{
	template <class T1, class T2>
	std::size_t operator() (const std::pair<T1, T2> &pair) const
	{
		return (pair.first * 0x1f1f1f1f) ^ pair.second;
	}
};

class Config {
public:
	int cost = INT_MAX;
	int heuristic = INT_MAX;
	std::set<int> collisions{};
	std::vector<std::pair<std::pair<int, int>, std::vector<int>>> back_set{};
	std::vector<std::pair<int, int>> back_ptr{};
};

std::unordered_map<coordinate, std::vector<coordinate>, pair_hash> create_graph(std::vector<std::vector<int>> grid) {
	std::unordered_map<std::pair<int, int>, std::vector<coordinate>, pair_hash> graph;
	for (int i = 0; i != grid.size(); i++) {
		for (int j = 0; j != grid[0].size(); j++) {
			if (grid[i][j] == 0) {
				coordinate current = std::make_pair(j, i);
				std::vector<coordinate> neighbours;
				if (i != 0 && grid[i - 1][j] == 0) {
					neighbours.push_back(std::make_pair(j, i - 1));
				}
				if (j != 0 && grid[i][j - 1] == 0) {
					neighbours.push_back(std::make_pair(j - 1, i));
				}
				if (i != grid.size() - 1 && grid[i + 1][j] == 0) {
					neighbours.push_back(std::make_pair(j, i + 1));
				}
				if (j != grid[0].size() - 1 && grid[i][j + 1] == 0) {
					neighbours.push_back(std::make_pair(j + 1, i));
				}
				graph[current] = neighbours;
			}
		}
	}
	return graph;
}

std::set<int> phi(std::vector<std::pair<int, int>> v_k) {
	std::set<std::pair<int, int>> seen{};
	std::set<std::pair<int, int>> collisions{};
	std::set<int> res{};
	for (std::pair<int, int> val : v_k) {
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

	py::class_<Config>(m, "Config")
		.def(py::init<>())
		.def_readwrite("cost", &Config::cost)
		.def_readwrite("heuristic", &Config::heuristic)
		.def_readwrite("collisions", &Config::collisions)
		.def_readwrite("back_set", &Config::back_set)
		.def_readwrite("back_ptr", &Config::back_ptr);
}