#include <queue>
#include <algorithm>
#include <set>
#include <numeric>
#include <cmath>
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

bool sort_pair(const std::pair<int, Coordinate> &a, std::pair<int, Coordinate> &b) {
    return a.first < b.first;
}

std::vector<Coordinate> tsp_greedy(Coordinate &start, Coordinate &end, std::vector<Coordinate> &waypoints,
                                   std::vector<std::unordered_map<Coordinate, int, coordinate_hash>> &distances) {
    std::unordered_map<Coordinate, std::vector<std::pair<int, Coordinate>>, coordinate_hash> graph;
    Coordinate dummy = Coordinate(-1, -1);
    graph[start] = {std::make_pair(distances.back()[start], end), std::make_pair(0, dummy)};
    graph[end] = {std::make_pair(distances.back()[start], start), std::make_pair(0, dummy)};
    graph[dummy] = {std::make_pair(0, start), std::make_pair(0, end)};
    for (int i = 0; i != waypoints.size(); i++) {
        Coordinate current = waypoints[i];
        graph[current] = {};
        for (Coordinate other : waypoints) {
            graph[current].emplace_back(std::make_pair(distances[i][other], other));
        }
        graph[current].emplace_back(std::make_pair(distances[i][start], start));
        graph[current].emplace_back(std::make_pair(distances[i][end], end));
        std::sort(graph[current].begin(), graph[current].end(), sort_pair);
        // Add this way point to start and end
        graph[start].emplace_back(std::make_pair(distances[i][start], current));
        graph[end].emplace_back(std::make_pair(distances[i][end], current));
    }
    std::sort(graph[start].begin(), graph[start].end(), sort_pair);
    std::sort(graph[end].begin(), graph[end].end(), sort_pair);
    int n_nodes = waypoints.size() + 3;
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
    visited.erase(visited.begin(), visited.begin() + 3);
    return visited;
}

std::vector<Coordinate> tsp_dynamic(Coordinate &start, Coordinate &end, std::vector<Coordinate> &waypoints,
                                    std::vector<std::unordered_map<Coordinate, int, coordinate_hash>> &distances) {
    std::vector<std::vector<int>> matrix;
    Coordinate dummy = Coordinate(-1, -1);
    std::vector<Coordinate> nodes = {start, dummy, end};
    nodes.insert(nodes.end(), waypoints.begin(), waypoints.end());
    matrix.push_back({0, 0, distances.back()[start]});
    matrix.push_back({0, 0, 0});
    matrix.push_back({distances.back()[start], 0, 0});
    for (int i = 0; i != waypoints.size(); i++) {
        matrix[0].push_back(distances[i][start]);
        matrix[1].push_back(INT_MAX);
        matrix[2].push_back(distances[i][end]);
        std::vector<int> current_row = {distances[i][start], INT_MAX, distances[i][end]};
        for (Coordinate other : waypoints) {
            current_row.push_back(distances[i][other]);
        }
        matrix.push_back(current_row);
    }
    std::vector<int> indices = held_karp(matrix);
    std::vector<Coordinate> res;
    res.reserve(indices.size());
    for (int index : indices) {
        res.emplace_back(nodes[index]);
    }
    return std::vector<Coordinate>(res.begin() + 1, res.end() - 2);
}

struct pairhash {
public:
    template<typename T, typename U>
    std::size_t operator()(const std::pair<T, U> &x) const {
        return std::hash<T>()(x.first) ^ std::hash<U>()(x.second);
    }
};

std::vector<int> held_karp(std::vector<std::vector<int>> matrix) {
    int n = matrix.size();
    std::unordered_map<std::pair<int, int>, std::pair<int, int>, pairhash> C;
    for (int k = 1; k != n; k++) {
        C[std::make_pair(1 << k, k)] = std::make_pair(matrix[0][k], 0);
    }
    for (int subset_size = 2; subset_size != n; subset_size++) {
        std::vector<int> range(n - 1);
        std::iota(std::begin(range), std::end(range), 1);
        for (const std::vector<int>& subset : combinations(range, subset_size)) {
            int bits = 0;
            for (int bit : subset) {
                bits |= 1 << bit;
            }
            for (int k : subset) {
                int prev = bits & ~(1 << k);
                std::vector<std::pair<int, int>> res;
                for (int m : subset) {
                    if (m == 0 || k == 0) {
                        continue;
                    }
                    if (C[std::make_pair(prev, m)].first + matrix[m][k] > 0) {
                        res.emplace_back(std::make_pair(C[std::make_pair(prev, m)].first + matrix[m][k], m));
                    } else {
                        res.emplace_back(std::make_pair(INT_MAX, m));
                    }
                }
                sort(res.begin(), res.end());
                C[std::make_pair(bits, k)] = res[0];
            }
        }
    }
    int bits = int(pow(2, n)) - 2;
    std::vector<std::pair<int, int>> res;
    for (int k = 1; k != n; k++) {
        if (C[std::make_pair(bits, k)].first + matrix[k][0] > 0) {
            res.emplace_back(C[std::make_pair(bits, k)].first + matrix[k][0], k);
        } else {
            res.emplace_back(INT_MAX, k);
        }
    }
    sort(res.begin(), res.end());
    int parent = res[0].second;
    std::vector<int> path;
    for (int i = 0; i != n - 1; i++) {
        path.emplace_back(parent);
        int new_bits = bits & ~(1 << parent);
        parent = C[std::make_pair(bits, parent)].second;
        bits = new_bits;
    }
    path.emplace_back(0);
    std::reverse(path.begin(), path.end());
    return path;
}

std::vector<std::vector<int>> combinations(std::vector<int> src, int r) {
    std::vector<std::vector<int>> cs;
    if (r == 1) {
        for (auto i = 0; i < src.size(); i++) {
            std::vector<int> c;
            c.push_back(src[i]);
            cs.push_back(c);
        }
        return cs;
    }
    int *places = (int *) malloc(sizeof(int) * r);
    for (auto i = 0; i < r; i++) places[i] = i;
    while (true) {
        // push_back another combination
        std::vector<int> c;
        c.reserve(r);
        for (auto i = 0; i < r; i++) {
            c.push_back(src[places[i]]);
        }
        cs.push_back(c);
        // update places
        for (auto i = 0; i < r - 1; i++) {
            places[i]++;
            if (places[i + 1] == places[i]) {
                places[i] = i;
                if (i == r - 2) places[r - 1]++;
                continue;
            }
            break;
        }
        if (places[r - 1] == src.size()) break;
    }
    free(places);
    return cs;
}
