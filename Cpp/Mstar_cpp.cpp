#include <pybind11/stl.h>
#include <pybind11/pybind11.h>

#include <string>
#include <utility>

#include <vector>

namespace py = pybind11;

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

    m.doc() = "Car path utilities";
	m.def("phi", &phi);
}