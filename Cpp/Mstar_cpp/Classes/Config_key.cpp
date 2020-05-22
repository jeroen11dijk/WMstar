#include "Config_key.h"
#include <string>
#include <sstream>

std::ostream &operator<<(std::ostream &os, const Config_key &config_key) {
    std::string coordinates = "[";
    std::string targets = "[";
    for (int i = 0; i < config_key.targets.size(); ++i) {
        Coordinate coordinate = config_key.coordinates[i];
        coordinates.append("(" + std::to_string(coordinate.a) + ", " + std::to_string(coordinate.b) + ")");
        targets.append(std::to_string(config_key.targets[i]));
        if (i != config_key.targets.size() - 1) {
            coordinates.append(", ");
            targets.append(", ");
        } else {
            coordinates.append("]");
            targets.append("]");
        }
    }
    return os << "Coordinate: " << coordinates << ". And targets: " << targets;
}

bool operator==(const Config_key &ck1, const Config_key &ck2) {
    return (ck1.coordinates == ck2.coordinates && ck1.targets == ck2.targets);
}
