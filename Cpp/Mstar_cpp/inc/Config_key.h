#pragma once

#include <iostream>
#include <vector>
#include "Coordinate.h"

class Config_key {
public:
    std::vector<Coordinate> coordinates;
    std::vector<int> targets;

    Config_key() {};

    Config_key(std::vector<Coordinate> &coordinates, const std::vector<int> &targets) : coordinates(coordinates),
                                                                                        targets(targets) {};

    friend std::ostream &operator<<(std::ostream &os, const Config_key &config_key);

    friend bool operator==(const Config_key &ck1, const Config_key &ck2);
};

struct config_key_hash {
    size_t operator()(const Config_key &config_key) const {
        std::size_t hash = 0;
        for (auto i = config_key.coordinates.begin(); i != config_key.coordinates.end(); ++i) {
            hash += (i->a * 0x1f1f1f1f) ^ i->b;
        }
        int sum = 0;
        for (auto &target : config_key.targets) {
            sum += target;
        }
        std::hash<int> hasher;
        hash += hasher(sum);
        return hash;
    }
};
