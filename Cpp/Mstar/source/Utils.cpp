#include <algorithm>
#include "../inc/Utils.h"

bool isSubset(std::unordered_set<int> &a, std::unordered_set<int> &b) {
    if (a.size() > b.size()) {
        return false;
    }
    if (a.size() == 0) {
        return true;
    }
    for (auto &index : a) {
        if (!b.count(index)) {
            return false;
        }
    }
    return true;
}

std::set<int> phi(std::vector<Coordinate> &v_l, const std::vector<Coordinate> &v_k) {
    std::unordered_set<Coordinate, coordinate_hash> seen{};
    std::unordered_set<Coordinate, coordinate_hash> collisions{};
    std::set<int> res{};
    for (int i = 0; i != v_l.size(); i++) {
        if (seen.count(v_l[i])) {
            collisions.insert(v_l[i]);
        } else {
            seen.insert(v_l[i]);
        }
        if (std::count(v_k.begin(), v_k.end(), v_l[i])) {
            auto it = find(v_k.begin(), v_k.end(), v_l[i]);
            int v_k_index = distance(v_k.begin(), it);
            if (v_k[i] == v_l[v_k_index] && i != v_k_index) {
                res.insert(i);
            }
        }
    }
    for (int i = 0; i != v_l.size(); i++) {
        if (collisions.count(v_l[i])) {
            res.insert(i);
        }
    }
    return res;
}

// Credit: https://stackoverflow.com/a/17050528
std::vector<std::vector<Coordinate>> cart_product(const std::vector<std::vector<Coordinate>> &v) {
    std::vector<std::vector<Coordinate>> s = {{}};
    for (const auto &u : v) {
        std::vector<std::vector<Coordinate>> r;
        for (const auto &x : s) {
            for (const auto &y : u) {
                r.push_back(x);
                r.back().push_back(y);
            }
        }
        s = move(r);
    }
    return s;
}
