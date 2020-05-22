#include "../inc/Queue_entry.h"

std::ostream &operator<<(std::ostream &os, const Queue_entry &queue_entry) {
    return os << "[Cost: " << queue_entry.cost << ". And config_key: " << queue_entry.config_key << "]";
}

bool operator>(const Queue_entry &q1, const Queue_entry &q2) {
    return q1.cost > q2.cost;
}

bool operator<(const Queue_entry &q1, const Queue_entry &q2) {
    return q1.cost < q2.cost;
}

bool operator==(const Queue_entry &q1, const Queue_entry &q2) {
    return (q1.cost == q2.cost && q1.config_key == q2.config_key);
}
