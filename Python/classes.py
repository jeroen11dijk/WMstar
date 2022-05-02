import heapq
import math
from collections import namedtuple
from dataclasses import dataclass, field
from typing import List, Set

Config_key = namedtuple('Config_key', 'coordinates waypoints')


@dataclass
class Config_value:
    back_ptr: List[any] = field(default_factory=list)
    back_set: Set[any] = field(default_factory=set)
    collisions: Set[any] = field(default_factory=set)
    cost: int = math.inf
    waiting: List[any] = field(default_factory=list)

    def __str__(self):
        return str([self.cost, self.collisions, self.back_set, self.back_ptr])

    def __repr__(self):
        return str([self.cost, self.collisions, self.back_set, self.back_ptr])


class FastContainsPriorityQueue:
    def __init__(self):
        self.pq = []
        self.cs = {}

    def __contains__(self, item) -> bool:
        return item in self.cs

    def enqueue(self, item):
        heapq.heappush(self.pq, item)
        if item in self.cs:
            self.cs[item] += 1
        else:
            self.cs[item] = 1

    def dequeue(self):
        item = heapq.heappop(self.pq)

        if item in self.cs:
            if self.cs[item] > 1:
                self.cs[item] -= 1
            else:
                del self.cs[item]

        return item

    def empty(self) -> bool:
        return len(self.pq) == 0
