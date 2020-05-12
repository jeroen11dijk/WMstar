#include <pybind11/stl.h>
#include <pybind11/pybind11.h>
#include <queue>
#include <string>
#include <utility>
#include <iostream>
#include <vector>

#include "Coordinate.h"

using namespace std;
namespace py = pybind11;

class Config_key {
public:
	Coordinate coordinate;
	vector<int> targets;
	Config_key() {};
	Config_key(Coordinate coordinate, vector<int> targets) {
		this->coordinate = coordinate;
		this->targets = targets;
	}
	friend ostream& operator<<(ostream& os, const Config_key &config_key);
	friend bool operator== (const Config_key &ck1, const Config_key &ck2);
};

ostream& operator<<(ostream& os, const Config_key &config_key) {
	std::string targets = "[";
	for (int i = 0; i < config_key.targets.size(); ++i) {
		targets.append(to_string(config_key.targets.at(i)));
		if (i != config_key.targets.size() - 1) {
			targets.append(", ");
		}
		else {
			targets.append("]");
		}
	}
	return os << "Coordinate: " << config_key.coordinate << ". And targets: " << targets;
}

bool operator== (const Config_key &ck1, const Config_key &ck2)
{
	return (ck1.coordinate == ck2.coordinate && ck1.targets == ck2.targets);
}

class Queue_entry {
public:
	int cost;
	Config_key config_key;
	Queue_entry(int cost, Config_key config_key) {
		this->cost = cost;
		this->config_key = config_key;
	}
	friend ostream& operator<<(ostream& os, const Queue_entry &queue_entry);
	friend bool operator> (const Queue_entry &q1, const Queue_entry &q2);
	friend bool operator== (const Queue_entry &q1, const Queue_entry &q2);
};

ostream& operator<<(ostream& os, const Queue_entry &queue_entry) {
	return os << "[Cost: " << queue_entry.cost << ". And config_key: " << queue_entry.config_key << "]";
}

bool operator> (const Queue_entry &q1, const Queue_entry &q2)
{
	return q1.cost > q2.cost;
}

bool operator== (const Queue_entry &q1, const Queue_entry &q2)
{
	return (q1.cost == q2.cost && q1.config_key == q2.config_key);
}


struct coordinate_hash
{
	size_t operator() (const Coordinate &coordinate) const
	{
		return (coordinate.a * 0x1f1f1f1f) ^ coordinate.b;
	}
};

struct config_key_hash
{
	size_t operator() (const Config_key &config_key) const
	{
		return (config_key.coordinate.a * 0x1f1f1f1f) ^ config_key.coordinate.b;
	}
};

class Config_value {
public:
	int cost = INT_MAX;
	int heuristic = INT_MAX;
	set<int> collisions{};
	vector<pair<Coordinate, vector<int>>> back_set{};
	vector<Coordinate> back_ptr{};
};

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

void test_queue() {
	priority_queue<Queue_entry, vector<Queue_entry>, greater<Queue_entry>> open;
	vector<int> vect{ 0, 1, 2 };
	Coordinate c1 = Coordinate(0, 0);
	Coordinate c2 = Coordinate(0, 1);
	Coordinate c3 = Coordinate(1, 0);
	Coordinate c4 = Coordinate(1, 1);
	Queue_entry entry1 = Queue_entry(4, Config_key(c1, vect));
	Queue_entry entry2 = Queue_entry(3, Config_key(c2, vect));
	Queue_entry entry3 = Queue_entry(2, Config_key(c3, vect));
	Queue_entry entry4 = Queue_entry(1, Config_key(c4, vect));
	open.push(entry1);
	open.push(entry2);
	open.push(entry3);
	open.push(entry4);
	cout << c1 << endl;
	cout << c2 << endl;
	cout << c3 << endl;
	cout << c4 << endl;
	cout << (c1.a == 0) << endl;
	while (!open.empty()) {
		cout << open.top() << endl;
		open.pop();
	}
	cout << '\n';
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
	m.def("test_queue", &test_queue);

	py::class_<Config_value>(m, "Config")
		.def(py::init<>())
		.def_readwrite("cost", &Config_value::cost)
		.def_readwrite("heuristic", &Config_value::heuristic)
		.def_readwrite("collisions", &Config_value::collisions)
		.def_readwrite("back_set", &Config_value::back_set)
		.def_readwrite("back_ptr", &Config_value::back_ptr);
}