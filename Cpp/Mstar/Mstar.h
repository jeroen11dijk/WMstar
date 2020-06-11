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

#include "inc/Config_key.h"
#include "inc/Config_value.h"
#include "inc/Coordinate.h"
#include "inc/Timer.h"
#include "inc/Queue_entry.h"

class Mstar {
public:
	int n_agents;
	bool inflated;
	std::unordered_map<Coordinate, std::vector<Coordinate>, coordinate_hash> graph;
	std::vector<Coordinate> v_I, v_F;
	std::vector<std::vector<Coordinate>> v_W;
	std::unordered_map<Config_key, Config_value, config_key_hash> configurations;
	std::vector<std::unordered_map<Coordinate, std::unordered_map<Coordinate, std::vector<Coordinate>, coordinate_hash>, coordinate_hash>> policies;
	std::vector<std::unordered_map<Coordinate, std::unordered_map<Coordinate, int, coordinate_hash>, coordinate_hash>> distances;
	std::vector<std::vector<Coordinate>> targets;
	std::priority_queue<Queue_entry, std::vector<Queue_entry>, std::greater<>> open;

	Mstar(std::vector<std::vector<int>>& grid, std::vector<std::pair<int, int>>& v_I_a, std::vector<std::vector<std::pair<int, int>>>& v_W_a, std::vector<std::pair<int, int>>& v_F_a, const bool &unordered);
    void update_policies_distances_targets();
    std::pair<std::vector<std::vector<std::pair<int, int>>>, int> solve();
	int get_edge_weight(std::vector<Coordinate> &prev_coordinates, Config_key & key, std::vector<int> &waiting);
	void backprop(Config_key &key, Config_value &value, std::unordered_set<int> &collisions);
	std::vector<std::vector<Coordinate>> get_limited_neighbours(Config_key &v_k, std::unordered_set<int> &collisions);
	float heuristic_configuration(Config_key & v_k);
};