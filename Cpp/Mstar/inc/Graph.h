#ifndef MSTAR_CPP_GRAPH_H
#define MSTAR_CPP_GRAPH_H

#include <vector>
#include <unordered_map>
#include "Coordinate.h"

class CompareTuple {
public:
    bool operator()(std::tuple<int, int, Coordinate> &t1, std::tuple<int, int, Coordinate> &t2);
};

std::unordered_map<Coordinate, std::vector<Coordinate>, coordinate_hash>
create_graph(std::vector<std::vector<int>> &grid);

std::pair<std::unordered_map<Coordinate, std::vector<Coordinate>, coordinate_hash>, std::unordered_map<Coordinate, int, coordinate_hash>>
dijkstra_predecessor_and_distance(std::unordered_map<Coordinate, std::vector<Coordinate>, coordinate_hash> &graph,
                                  Coordinate source);

std::vector<Coordinate> tsp_greedy(Coordinate &start, Coordinate &end, std::vector<Coordinate> &waypoints,
                                   std::vector<std::unordered_map<Coordinate, int, coordinate_hash>> &distances);

std::vector<Coordinate> tsp_dynamic(Coordinate &start, Coordinate &end, std::vector<Coordinate> &waypoints,
                                    std::vector<std::unordered_map<Coordinate, int, coordinate_hash>> &distances);

std::vector<int> held_karp(std::vector<std::vector<int>> matrix);

std::vector<std::vector<int>> combinations(std::vector<int> src, int r);

#endif //MSTAR_CPP_GRAPH_H
