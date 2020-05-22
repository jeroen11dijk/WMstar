class Config_value {
public:
    int cost = INT_MAX;
    std::unordered_set<int> collisions{};
    std::unordered_set<Config_key, config_key_hash> back_set{};
    std::vector<std::vector<Coordinate>> back_ptr{};
};