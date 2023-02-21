import random
from dataclasses import dataclass
from collections import namedtuple

Candidate = namedtuple('candidate', ('weight', 'value'))

@dataclass
class Knapsack:
    capacity: int
    candidates: list

    def __str__(self):
        str_repr: str = f'knapsack capacity: {self.capacity}\n'
        for cidx, candidate in enumerate(self.candidates):
            str_repr += f'{cidx}: {candidate}\n'
        return str_repr[:-1]


class KnapsackGenerator:
    def __init__(
        self,
        min_capacity: int=5,
        max_capacity: int=10,
        min_num_items: int=1,
        max_num_items: int=10,
        min_weight: int=1,
        max_weight: int=10,
        min_value: int=1,
        max_value: int=10
    ):
        self.min_capacity = max(1, min_capacity)
        self.max_capacity = max(min_capacity, max_capacity)

        self.min_num_items = max(1, min_num_items)
        self.max_num_items = max(min_num_items, max_num_items)

        self.min_weight = max(1, min_weight)
        self.max_weight = max(min_weight, max_weight)

        self.min_value = max(1, min_value)
        self.max_value = max(min_value, max_value)

    def generate(self) -> Knapsack:
        capacity: int = random.randint(self.min_capacity, self.max_capacity)
        num_items: int = random.randint(self.min_num_items, self.max_num_items)
        candidates: list = [Candidate(
            random.randint(self.min_weight, self.max_weight),
            random.randint(self.min_value, self.max_value)
        ) for _ in range(num_items)]

        return Knapsack(capacity, candidates)

    def create(self, capacity: int, weights: list, values: list):
        candidates: list = [Candidate(
            weight,
            values[idx]
        ) for idx, weight in enumerate(weights)]
        
        return Knapsack(capacity, candidates)
