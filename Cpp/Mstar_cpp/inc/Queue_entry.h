#ifndef MSTAR_CPP_QUEUE_ENTRY_H
#define MSTAR_CPP_QUEUE_ENTRY_H

#include <iostream>
#include "Config_key.h"
#include "Coordinate.h"

class Queue_entry {
public:
    int cost;
    Config_key config_key;

    Queue_entry(int cost, Config_key config_key) : cost(cost), config_key(config_key) {};

    friend std::ostream &operator<<(std::ostream &os, const Queue_entry &queue_entry);

    friend bool operator>(const Queue_entry &q1, const Queue_entry &q2);

    friend bool operator<(const Queue_entry &q1, const Queue_entry &q2);

    friend bool operator==(const Queue_entry &q1, const Queue_entry &q2);
};

#endif //MSTAR_CPP_QUEUE_ENTRY_H