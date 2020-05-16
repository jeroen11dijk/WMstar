#include "python.h"

using namespace std;

set<int> python_phi(vector<pair<int, int>> & v_l, vector<pair<int, int>> & v_k) {
	set<pair<int, int>> seen{};
	set<pair<int, int>> collisions{};
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