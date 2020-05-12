#pragma once
#include <iostream>
#include "Coordinate.h"

using namespace std;

class Config_key {
public:
	Coordinate coordinate;
	vector<int> targets;
	Config_key() {};
	Config_key(Coordinate coordinate, vector<int> targets) : coordinate(coordinate), targets(targets) {};
	friend ostream& operator<<(ostream& os, const Config_key &config_key);
	friend bool operator== (const Config_key &ck1, const Config_key &ck2);
};

ostream& operator<<(ostream& os, const Config_key &config_key) {
	std::string targets = "[";
	for (int i = 0; i < config_key.targets.size(); ++i) {
		targets.append(to_string(config_key.targets.at(i)));
		if (i != config_key.targets.size() - 1) {
			targets.append(", ");
		}
		else {
			targets.append("]");
		}
	}
	return os << "Coordinate: " << config_key.coordinate << ". And targets: " << targets;
}

bool operator== (const Config_key &ck1, const Config_key &ck2)
{
	return (ck1.coordinate == ck2.coordinate && ck1.targets == ck2.targets);
}

struct config_key_hash
{
	size_t operator() (const Config_key &config_key) const
	{
		return (config_key.coordinate.a * 0x1f1f1f1f) ^ config_key.coordinate.b;
	}
};
