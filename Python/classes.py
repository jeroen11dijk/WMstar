from dataclasses import dataclass, field
from typing import List, Set
from collections import namedtuple

Config_key = namedtuple('Config_key', 'coordinates target_indices')

@dataclass
class Config_value:
    back_ptr: List[any] = field(default_factory=list)
    back_set: List[any] = field(default_factory=list)
    collisions: Set[any] = field(default_factory=set)
    cost: int = float('inf')

    def __str__(self):
        return str([self.cost, self.collisions, self.back_set, self.back_ptr])

    def __repr__(self):
        return str([self.cost, self.collisions, self.back_set, self.back_ptr])
