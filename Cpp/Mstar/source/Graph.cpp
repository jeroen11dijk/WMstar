#include <queue>
#include <algorithm>
#include "../inc/Graph.h"

bool CompareTuple::operator()(std::tuple<int, int, Coordinate> &t1, std::tuple<int, int, Coordinate> &t2) {
    if (std::get<0>(t1) == std::get<0>(t2)) {
        return std::get<1>(t1) > std::get<1>(t2);
    } else {
        return std::get<0>(t1) > std::get<0>(t2);
    }
}

std::unordered_map<Coordinate, std::vector<Coordinate>, coordinate_hash>
create_graph(std::vector<std::vector<int>> &grid) {
    std::unordered_map<Coordinate, std::vector<Coordinate>, coordinate_hash> graph;
    for (int i = 0; i != grid.size(); i++) {
        for (int j = 0; j != grid[0].size(); j++) {
            if (grid[i][j] == 0) {
                Coordinate current = Coordinate(j, i);
                std::vector<Coordinate> neighbours;
                if (i != 0 && grid[i - 1][j] == 0) {
                    int up = i - 1;
                    neighbours.emplace_back(j, up);
                }
                if (j != 0 && grid[i][j - 1] == 0) {
                    int left = j - 1;
                    neighbours.emplace_back(left, i);
                }
                if (i != grid.size() - 1 && grid[i + 1][j] == 0) {
                    int down = i + 1;
                    neighbours.emplace_back(j, down);
                }
                if (j != grid[0].size() - 1 && grid[i][j + 1] == 0) {
                    int right = j + 1;
                    neighbours.emplace_back(right, i);
                }
                graph[current] = neighbours;
            }
        }
    }
    return graph;
}

std::pair<std::unordered_map<Coordinate, std::vector<Coordinate>, coordinate_hash>, std::unordered_map<Coordinate, int, coordinate_hash>>
dijkstra_predecessor_and_distance(std::unordered_map<Coordinate, std::vector<Coordinate>, coordinate_hash> &graph,
                                  Coordinate source) {
    std::unordered_map<Coordinate, int, coordinate_hash> distances;
    std::unordered_map<Coordinate, std::vector<Coordinate>, coordinate_hash> pred = {{source, std::vector<Coordinate>{}}};
    std::unordered_map<Coordinate, int, coordinate_hash> seen = {{source, 0}};
    int c = 1;
    std::priority_queue<std::tuple<int, int, Coordinate>, std::vector<std::tuple<int, int, Coordinate>>, CompareTuple> fringe;
    fringe.push(std::make_tuple(0, c, source));
    while (!fringe.empty()) {
        std::tuple<int, int, Coordinate> current = fringe.top();
        fringe.pop();
        int distance = std::get<0>(current);
        Coordinate node = std::get<2>(current);
        if (distances.count(node)) {
            continue;
        }
        distances[node] = distance;
        std::vector<Coordinate> neighbours = graph[node];
        for (Coordinate &neighbour : neighbours) {
            int neighbour_distance = distance + 1;
            if (!seen.count(neighbour) || neighbour_distance < seen[neighbour]) {
                seen[neighbour] = neighbour_distance;
                c++;
                fringe.push(std::make_tuple(neighbour_distance, c, neighbour));
                pred[neighbour] = std::vector<Coordinate>{node};
            } else if (neighbour_distance == seen[neighbour]) {
                pred[neighbour].push_back(node);
            }
        }
    }
    return make_pair(pred, distances);
}

bool sort_pair(const std::pair<int, Coordinate> & a, std::pair<int, Coordinate> & b) {
    return a.first < b.first;
}

std::vector<Coordinate> tsp_greedy(Coordinate &start, Coordinate &end, std::vector<Coordinate> &waypoints,
                                   std::vector<std::unordered_map<Coordinate, int, coordinate_hash>> &distances) {
    std::unordered_map<Coordinate, std::vector<std::pair<int, Coordinate>>, coordinate_hash> graph;
    std::vector<Coordinate> nodes;
    nodes.emplace_back(start);
    nodes.emplace_back(end);
    nodes.insert(nodes.end(), waypoints.begin(), waypoints.end());
    for (int i = 0; i != nodes.size(); i++) {
        Coordinate current = nodes[i];
        graph[current] = {};
        if (current == start || current == end) {
            graph[current].emplace_back(std::make_pair(0, Coordinate(-1, -1)));
        }
        for (Coordinate other : nodes) {
            graph[current].emplace_back(std::make_pair(distances[i][other], other));
        }
        graph[current].emplace_back(std::make_pair(distances[i][start], start));
        graph[current].emplace_back(std::make_pair(distances[-1][current], end));
        std::sort(graph[current].begin(), graph[current].end(), sort_pair);
    }
    int n_nodes = nodes.size() + 1;
    std::vector<Coordinate> visited = {end};
    Coordinate current = end;
    while (visited.size() < n_nodes) {
        int index = 0;
        while (std::count(visited.begin(), visited.end(), graph[current][index].second)) {
            if (start == end && start == graph[current][index].second &&
                std::count(visited.begin(), visited.end(), start) < 2) {
                break;
            }
            index++;
        }
        Coordinate next = graph[current][index].second;
        visited.emplace_back(next);
        current = next;
    }
    std::cout << "Path" << std::endl;
    for (auto loc : visited) {
        std::cout << loc << std::endl;
    }
    return visited;
}