#pragma once

#include <iostream>

class Coordinate {
public:
    int a;
    int b;

    Coordinate() {};

    Coordinate(int &a, int &b) : a(a), b(b) {};

    friend std::ostream &operator<<(std::ostream &os, const Coordinate &coordinate);

    friend bool operator==(const Coordinate &c1, const Coordinate &c2);

    friend bool operator!=(const Coordinate &c1, const Coordinate &c2);
};

struct coordinate_hash {
    size_t operator()(const Coordinate &coordinate) const {
        return (coordinate.a * 0x1f1f1f1f) ^ coordinate.b;
    }
};