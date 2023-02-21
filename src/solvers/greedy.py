from knapsack import Knapsack, Allocation


def greedy_solver(knapsack: Knapsack) -> Allocation:
    capacity: int = knapsack.capacity
    candidates: list = [(pid, cand, cand.value/cand.weight) for pid, cand in enumerate(knapsack.candidates)]
    candidates: list = sorted(candidates, key=lambda t: t[2], reverse=True)

    allocation: list = []
    value: int = 0
    iterator: int = 0
    while 0 < capacity and iterator < len(candidates):
        cand: tuple = candidates[iterator]
        if cand[1].weight <= capacity:
            allocation.append(cand[0])
            value += cand[1].value
            capacity -= cand[1].weight
        iterator += 1
    
    return Allocation(allocation, value)


def simple_greedy_solver(knapsack: Knapsack) -> Allocation:
    capacity: int = knapsack.capacity
    candidates: list = [(pid, cand) for pid, cand in enumerate(knapsack.candidates)]
    candidates: list = sorted(candidates, key=lambda t: t[1].value, reverse=True)
    
    allocation: list = []
    value: int = 0
    iterator: int = 0
    while 0 < capacity and iterator < len(candidates):
        cand: tuple = candidates[iterator]
        if cand[1].weight <= capacity:
            allocation.append(cand[0])
            value += cand[1].value
            capacity -= cand[1].weight
        iterator += 1
    
    return Allocation(allocation, value)
        
