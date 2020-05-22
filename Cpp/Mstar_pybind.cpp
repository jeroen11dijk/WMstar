#include <pybind11/stl.h>
#include <pybind11/pybind11.h>
#include <vector>
#include "Mstar/Mstar.h"


using namespace std;
namespace py = pybind11;

struct pair_hash {
    size_t operator()(const pair<int, int> &pair) const {
        return (pair.first * 0x1f1f1f1f) ^ pair.second;
    }
};

set<int> python_phi(vector<pair<int, int>> &v_l, vector<pair<int, int>> &v_k) {
    unordered_set<pair<int, int>, pair_hash> seen{};
    unordered_set<pair<int, int>, pair_hash> collisions{};
    set<int> res{};
    for (int i = 0; i != v_l.size(); i++) {
        if (seen.count(v_l[i])) {
            collisions.insert(v_l[i]);
        } else {
            seen.insert(v_l[i]);
        }
        if (count(v_k.begin(), v_k.end(), v_l[i])) {
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

PYBIND11_MODULE(Mstar_pybind, m) {

    m.doc() = "Mstar in Cpp";
    m.def("python_phi", &python_phi);

    py::class_<Mstar>(m, "Mstar")
            .def(py::init<vector<vector<int>>, vector<pair<int, int>>, vector<vector<pair<int, int>>>, vector<pair<int, int>>>())
            .def("solve", &Mstar::solve);
}