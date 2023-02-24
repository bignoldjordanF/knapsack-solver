from knapsack import KnapsackInstance, KnapsackAllocation


def __run_greedy(instance: KnapsackInstance, items: list) -> KnapsackAllocation:
    """
    Runs the greedy algorithm on a sorted list of items, and returns the
    best allocation and value found.
    """
    capacity: int = instance.capacity
    allocation: list = []
    value: int = 0
    iterator: int = 0
    # We iterate through candidate items until we have exhausted 
    # all of them, or we have exhausted the budget.
    while 0 < capacity and iterator < len(items):
        cand: tuple = items[iterator]
        # If the capacity can hold this item, then include it in the result.
        # Otherwise, we simply skip this item and try the next one.
        if cand[1].weight <= capacity:
            allocation.append(cand[0])
            value += cand[1].value
            capacity -= cand[1].weight
        iterator += 1
    
    return KnapsackAllocation(allocation, value)


def ratio_greedy_solver(instance: KnapsackInstance) -> KnapsackAllocation:
    """
    A very fast and relatively accurate approximation scheme for the knapsack
    problem which computes the value-weight ratio for each item, sorts by
    this ratio in descending order and greedily chooses the items with
    the highest ratio until the budget is exhausted.
    """
    items: list = [(pid, cand, cand.value/cand.weight) for pid, cand in enumerate(instance.items)]
    items: list = sorted(items, key=lambda t: t[2], reverse=True)

    return __run_greedy(instance, items)


def greedy_solver(instance: KnapsackInstance) -> KnapsackAllocation:
    """
    A very fast and relatively accurate approximation scheme for the knapsack
    problem which sorts by the value in descending order and greedily chooses
    the items with the highest values until the budget is exhausted.
    """
    items: list = [(pid, cand) for pid, cand in enumerate(instance.items)]
    items: list = sorted(items, key=lambda t: t[1].value, reverse=True)

    return __run_greedy(instance, items)
        
