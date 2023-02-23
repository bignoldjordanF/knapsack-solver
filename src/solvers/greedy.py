from knapsack import KnapsackInstance, KnapsackAllocation


def __run_greedy(instance: KnapsackInstance, items: list) -> KnapsackAllocation:
    capacity: int = instance.capacity
    allocation: list = []
    value: int = 0
    iterator: int = 0
    while 0 < capacity and iterator < len(items):
        cand: tuple = items[iterator]
        if cand[1].weight <= capacity:
            allocation.append(cand[0])
            value += cand[1].value
            capacity -= cand[1].weight
        iterator += 1
    
    return KnapsackAllocation(allocation, value)


def ratio_greedy_solver(instance: KnapsackInstance) -> KnapsackAllocation:
    items: list = [(pid, cand, cand.value/cand.weight) for pid, cand in enumerate(instance.items)]
    items: list = sorted(items, key=lambda t: t[2], reverse=True)

    return __run_greedy(instance, items)


def greedy_solver(instance: KnapsackInstance) -> KnapsackAllocation:
    items: list = [(pid, cand) for pid, cand in enumerate(instance.items)]
    items: list = sorted(items, key=lambda t: t[1].value, reverse=True)

    return __run_greedy(instance, items)
        
