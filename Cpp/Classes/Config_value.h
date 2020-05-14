class Config_value {
public:
	int cost = INT_MAX;
	int heuristic = INT_MAX;
	set<int> collisions{};
	vector<Config_key> back_set{};
	vector<vector<Coordinate>> back_ptr{};
};