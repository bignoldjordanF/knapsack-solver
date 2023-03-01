import random
from dataclasses import dataclass
from collections import namedtuple


KnapsackAllocation = namedtuple('allocation', ('knapsack', 'value'))
KnapsackAllocation.__doc__ = \
    """Stores allocations found for knapsack instances by optimisation algorithms"""


KnapsackItem = namedtuple('item', ('weight', 'value'))
KnapsackItem.__doc__ = \
    """Stores items as (weight, value) pairs in knapsack instances"""


@dataclass
class KnapsackInstance:
    """
    Stores a knapsack instance as a capacity integer and a list of
    KnapsackItem instances to be passed to optimisation functions.
    """
    capacity: int
    items: list

    def __str__(self):
        str_repr: str = f'knapsack capacity: {self.capacity}\n'
        for cidx, candidate in enumerate(self.items):
            str_repr += f'{cidx}: {candidate}\n'
        return str_repr[:-1] 
        
    def to_tuple(self):
        return f'({self.capacity}, {[i.weight for i in self.items]}, {[i.value for i in self.items]})'


class KnapsackGenerator:
    """
    Used to generate randomly or create KnapsackInstance objects through
    the generate() and create() methods respectively.
    """
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

    def generate(self) -> KnapsackInstance:
        """
        Generates a random KnapsackInstance pair (capacity, [KnapsackItem...])
        where the second argument is a list of KnapsackItem pairs (weight, value).
        The capacity, number of items, weights and values are randomly generated
        and bounded by the values passed at construction.
        """
        capacity: int = random.randint(self.min_capacity, self.max_capacity)
        num_items: int = random.randint(self.min_num_items, self.max_num_items)
        candidates: list = [KnapsackItem(
            random.randint(self.min_weight, self.max_weight),
            random.randint(self.min_value, self.max_value)
        ) for _ in range(num_items)]

        return KnapsackInstance(capacity, candidates)

    def create(self, capacity: int, weights: list, values: list):
        """
        Creates a KnapsackInstance pair (capacity, [KnapsackItem...]) where
        the second argument is a list of KnapsackItem pairs (weight, value).
        The knapsack instance values (capacity, [weight...], [values...])
        are passed into the function manually. No randomness is involved.
        """
        candidates: list = [KnapsackItem(
            weight,
            values[idx]
        ) for idx, weight in enumerate(weights)]
        
        return KnapsackInstance(capacity, candidates)
