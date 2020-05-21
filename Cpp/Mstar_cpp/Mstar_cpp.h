#pragma once
#include <queue>
#include <string>
#include <utility>
#include <iostream>
#include <vector>
#include <numeric>
#include <tuple>
#include <unordered_map>
#include <unordered_set>
#include <set>

#include "classes/Config_key.h"
#include "classes/Config_value.h"
#include "classes/Coordinate.h"
#include "classes/Timer.h"
#include "classes/Queue_entry.h"

class Mstar_cpp {
public:
	int n_agents;
	std::unordered_map<Coordinate, std::vector<Coordinate>, coordinate_hash> graph;
	std::vector<Coordinate> v_I, v_F;
	std::vector<std::vector<Coordinate>> v_W;
	std::unordered_map<Config_key, Config_value, config_key_hash> configurations;
	std::vector<std::vector<std::unordered_map<Coordinate, std::vector<Coordinate>, coordinate_hash>>> policies;
	std::vector<std::vector<std::unordered_map<Coordinate, int, coordinate_hash>>> distances;
	std::vector<std::vector<Coordinate>> targets;
	std::priority_queue<Queue_entry, std::vector<Queue_entry>, std::greater<Queue_entry>> open;

	timer time = timer();
	float backprop_time1 = 0.0f;
	float backprop_time2 = 0.0f;

	Mstar_cpp(std::vector<std::vector<int>> & grid, std::vector<std::pair<int, int>> & v_I_a, std::vector<std::vector<std::pair<int, int>>> & v_W_a, std::vector<std::pair<int, int>> & v_F_a);
	std::pair<std::vector<std::vector<std::pair<int, int>>>, int> solve();
	int get_edge_weight(Config_key & v_k, Config_key & v_l);
	void backprop(Config_key & v_k, std::unordered_set<int> & C_l);
	std::vector<std::vector<Coordinate>> get_limited_neighbours(Config_key & v_k);
	int heuristic_configuration(Config_key & v_k);
};