#pragma once
#include <iostream>
#include "Config_key.h"
#include "Coordinate.h"

using namespace std;

class Queue_entry {
public:
	int cost;
	Config_key config_key;
	Queue_entry(int cost, Config_key config_key) : cost(cost), config_key(config_key) {};
	friend ostream& operator<<(ostream& os, const Queue_entry &queue_entry);
	friend bool operator> (const Queue_entry &q1, const Queue_entry &q2);
	friend bool operator== (const Queue_entry &q1, const Queue_entry &q2);
};

ostream& operator<<(ostream& os, const Queue_entry &queue_entry) {
	return os << "[Cost: " << queue_entry.cost << ". And config_key: " << queue_entry.config_key << "]";
}

bool operator> (const Queue_entry &q1, const Queue_entry &q2)
{
	return q1.cost > q2.cost;
}

bool operator== (const Queue_entry &q1, const Queue_entry &q2)
{
	return (q1.cost == q2.cost && q1.config_key == q2.config_key);
}
