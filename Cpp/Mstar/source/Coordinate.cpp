#include "../inc/Coordinate.h"

std::ostream &operator<<(std::ostream &os, const Coordinate &coordinate) {
    return os << "(" << coordinate.a << ", " << coordinate.b << ")";
}

bool operator==(const Coordinate &c1, const Coordinate &c2) {
    return (c1.a == c2.a && c1.b == c2.b);
}

bool operator!=(const Coordinate &c1, const Coordinate &c2) {
    return (c1.a != c2.a || c1.b != c2.b);
}