#ifndef MSTAR_CPP_UTILS_H
#define MSTAR_CPP_UTILS_H

#include <vector>
#include <unordered_map>
#include <unordered_set>
#include <set>
#include "Coordinate.h"

int euclidian_distance(Coordinate a, Coordinate b);

bool isSubset(std::unordered_set<int> &a, std::unordered_set<int> &b);

std::set<int> phi(std::vector<Coordinate> &v_l, const std::vector<Coordinate> &v_k = std::vector<Coordinate>{});

std::vector<std::vector<Coordinate>> cart_product(const std::vector<std::vector<Coordinate>> &v);

#endif //MSTAR_CPP_UTILS_H
