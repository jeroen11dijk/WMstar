#include <utility>
#include <limits>

#ifndef MSTAR_CPP_CONFIG_VALUE_H
#define MSTAR_CPP_CONFIG_VALUE_H

class Config_value {
public:
    std::unordered_set<Config_key, config_key_hash> back_set{};
    std::vector<std::vector<Coordinate>> back_ptr{};
    std::unordered_set<int> collisions{};
    float cost = std::numeric_limits<float>::infinity();
    std::vector<int> waiting;

    Config_value() = default;

    explicit Config_value(std::vector<int> waiting) : waiting(std::move(waiting)) {};
};

#endif //MSTAR_CPP_CONFIG_VALUE_H