class Config_value {
public:
	int cost = INT_MAX;
	int heuristic = INT_MAX;
	set<int> collisions{};
	vector<pair<Coordinate, vector<int>>> back_set{};
	vector<Coordinate> back_ptr{};
};