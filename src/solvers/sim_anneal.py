from knapsack import KnapsackInstance, KnapsackAllocation
from dataclasses import dataclass
import numpy as np
import random


# Ignore Exp Overflow
np.seterr(over='ignore')

# TODO: This doesn't work very well, and it isn't very fast.
# A better neighbourhood is probably in order, and a better
# tuning of the parameters.


@dataclass
class SAKnapsack:
    instance: KnapsackInstance
    allocation: list  # e.g. [1, 0, 0, 1, 0]
    value: int
    weight: int

    def __str__(self):
        return str(self.allocation) + f', (weight {self.weight}), (value {self.value})'

    def neighbour(self):
        """
        Generates a neighbour by randomly flipping a single bit and adding
        adding or subtracting the corresponding weight and value from
        the total. Allocations exceeding the weight capacity are given
        a negative valuation, such that the default allocation (all
        zeroes) is better.
        """
        _allocation: list = self.allocation[:]
        _value: int = self.value
        _weight: int = self.weight

        ridx: int = random.randint(0, len(_allocation) - 1)
        _allocation[ridx] = int(not _allocation[ridx])

        pos_neg: int = 1 if _allocation[ridx] else -1
        _value = abs(_value) + (pos_neg * self.instance.items[ridx].value)
        _weight += pos_neg * self.instance.items[ridx].weight

        if _weight > self.instance.capacity:
            _value = -_value

        return SAKnapsack(self.instance, _allocation, _value, _weight)


def __simulated_annealing_solver(
        instance: KnapsackInstance,
        initial_temperature: float,
        temperature_length: int,
        cooling_ratio: float,
        num_non_improve: int
):
    # Track the current temperature and the number of 
    # non-improved solutions:
    current_temperature: float = INITIAL_TEMPERATURE
    count_num_non_improve: int = 0

    # Track the current allocation and best allocation
    # found so far:
    current_allocation: SAKnapsack = SAKnapsack(
        instance,
        [0] * len(instance.items),
        0,
        0
    )
    best_allocation: SAKnapsack = current_allocation

    # As long as we have improved within the deadline:
    while count_num_non_improve < num_non_improve:
        for _ in range(temperature_length):
            # Generate a neighbour and compare values:
            neighbour_allocation: SAKnapsack = current_allocation.neighbour()
            delta_value: int = neighbour_allocation.value - current_allocation.value

            # A better allocation instantly becomes the current allocation:
            if delta_value >= 0:
                current_allocation = neighbour_allocation
                count_num_non_improve += 1
                # Update best_allocation if it is the best:
                if current_allocation.value > best_allocation.value:
                    best_allocation = current_allocation
                    # We have improved, so reset the count:
                    count_num_non_improve = 0
            
            # Otherwise, accept a worse allocation with some probability:
            else:
                q = random.uniform(0, 1)
                p = np.exp(-delta_value / current_temperature)
                if q < p:
                    current_allocation = neighbour_allocation
                count_num_non_improve += 1
        
        # After temperature_length iterations, update the temperature:
        current_temperature *= cooling_ratio

    result = [idx for idx, val in enumerate(best_allocation.allocation) if val]
    return KnapsackAllocation(result, best_allocation.value)


INITIAL_TEMPERATURE: float = 10.0
TEMPERATURE_LENGTH: int = 1
COOLING_RATIO = 0.999
NUM_NON_IMPROVE = 100000


def simulated_annealing_solver(instance: KnapsackInstance):
    return __simulated_annealing_solver(
        instance,
        INITIAL_TEMPERATURE,
        TEMPERATURE_LENGTH,
        COOLING_RATIO,
        NUM_NON_IMPROVE
    )
