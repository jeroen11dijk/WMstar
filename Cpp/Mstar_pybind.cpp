#include <pybind11/stl.h>
#include <pybind11/pybind11.h>
#include <vector>
#include "Mstar/Mstar.h"


using namespace std;
namespace py = pybind11;

int main() {
    vector<vector<int>> grid{{0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0},
                             {1, 1, 1, 0, 1, 1, 1},
                             {1, 1, 1, 0, 1, 1, 1},
                             {1, 1, 1, 0, 1, 1, 1},
                             {0, 0, 0, 0, 0, 0, 0},
                             {0, 0, 0, 0, 0, 0, 0}};
    vector<pair<int, int>> v_I_a{std::make_pair(1, 0), std::make_pair(6, 1), std::make_pair(0, 6),
                                 std::make_pair(5, 6)};
    std::vector<std::vector<std::pair<int, int>>> v_W_a{{std::make_pair(-1, -1)},
                                                        {std::make_pair(-1, -1)},
                                                        {std::make_pair(-1, -1)},
                                                        {std::make_pair(-1, -1)}};
    vector<pair<int, int>> v_F_a{std::make_pair(1, 5), std::make_pair(3, 6), std::make_pair(5, 0),
                                 std::make_pair(3, 0)};
    Mstar lol = Mstar(grid, v_I_a, v_W_a, v_F_a);
    std::vector<std::vector<std::pair<int, int>>> res = lol.solve().first;
    for (const auto& agent : res) {
        cout << "[";
        for (const auto& loc : agent) {
            cout << "(" << loc.first << ", " << loc.second << "), ";
        }
        cout << "]" << endl;
    }
    return 0;
}


struct pair_hash
{
	size_t operator() (const pair<int, int> &pair) const
	{
		return (pair.first * 0x1f1f1f1f) ^ pair.second;
	}
};

set<int> python_phi(vector<pair<int, int>> & v_l, vector<pair<int, int>> & v_k) {
	unordered_set<pair<int, int>, pair_hash> seen{};
	unordered_set<pair<int, int>, pair_hash> collisions{};
	set<int> res{};
	for (int i = 0; i != v_l.size(); i++) {
		if (seen.count(v_l[i])) {
			collisions.insert(v_l[i]);
		}
		else {
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

PYBIND11_MODULE(Mstar_cpp, m) {

	m.doc() = "Mstar in Cpp";
	m.def("python_phi", &python_phi);
}