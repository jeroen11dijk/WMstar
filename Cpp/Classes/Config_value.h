class Config_value {
public:
	int cost = INT_MAX;
	unordered_set<int> collisions{};
	unordered_set<Config_key, config_key_hash> back_set{};
	vector<vector<Coordinate>> back_ptr{};
};