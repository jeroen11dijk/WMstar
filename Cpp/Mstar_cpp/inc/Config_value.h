#ifndef MSTAR_CPP_CONFIG_VALUE_H
#define MSTAR_CPP_CONFIG_VALUE_H

class Config_value {
public:
    int cost = INT_MAX;
    std::unordered_set<int> collisions{};
    std::unordered_set<Config_key, config_key_hash> back_set{};
    std::vector<std::vector<Coordinate>> back_ptr{};
};

#endif //MSTAR_CPP_CONFIG_VALUE_H