#pragma once
#include <iostream>

using namespace std;

class Coordinate {
public:
	int a;
	int b;
	Coordinate() {};
	Coordinate(int a, int b) : a(a), b(b) {};
	friend ostream& operator<<(ostream& os, const Coordinate &coordinate);
	friend bool operator== (const Coordinate &c1, const Coordinate &c2);
};

ostream& operator<<(ostream& os, const Coordinate &coordinate) {
	return os << "(" << coordinate.a << ", " << coordinate.b << ")";
}

bool operator== (const Coordinate &c1, const Coordinate &c2)
{
	return (c1.a == c1.a && c1.b == c1.b);
}

struct coordinate_hash
{
	size_t operator() (const Coordinate &coordinate) const
	{
		return (coordinate.a * 0x1f1f1f1f) ^ coordinate.b;
	}
};