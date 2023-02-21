from knapsack import Knapsack


def greedy_solver(knapsack: Knapsack):
    capacity: int = knapsack.capacity
    candidates: list = [(pid, cand) for pid, cand in enumerate(knapsack.candidates)]
    candidates = sorted(candidates, key=lambda t: t[1][1], reverse=True)
    
    allocation: list = []
    value: int = 0
    iterator: int = 0
    while 0 < capacity and iterator < len(candidates):
        cand: tuple = candidates[iterator]
        if cand[1][0] <= capacity:
            allocation.append(cand[0])
            value += cand[1][1]
            capacity -= cand[1][0]
        iterator += 1
    
    return allocation, value
        
