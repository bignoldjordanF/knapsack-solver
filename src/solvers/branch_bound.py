from knapsack import KnapsackInstance, KnapsackAllocation
from collections import deque
from dataclasses import dataclass


@dataclass
class KnapsackNode:
    level: int
    value: int
    bound: int
    weight: int


def bound(u, n, capacity, candidates):
    if u.weight >= capacity:
        return 0
    
    profit_bound: int = u.value
    j: int = u.level + 1
    totweight: int = u.weight

    while j < n and totweight + candidates[j][1].weight <= capacity:
        totweight += candidates[j][1].weight
        profit_bound += candidates[j][1].value
        j += 1

    if j < n:
        profit_bound += (capacity - totweight) * candidates[j][1].value / candidates[j][1].weight
    
    return profit_bound


def branch_and_bound_solver(knapsack: KnapsackInstance) -> KnapsackAllocation:
    candidates: list = [(pid, cand) for pid, cand in enumerate(knapsack.candidates)]
    items: list = sorted(candidates, key=lambda t: t[1].value/t[1].weight, reverse=True)
    total_items = len(candidates)
    weight = knapsack.capacity

    Q: deque = deque()
    u: KnapsackNode = KnapsackNode(-1, 0, 0, 0)
    Q.append(u)

    maxProfit: int = 0
    while Q:
        u = Q.popleft()
        v = KnapsackNode(0, 0, 0, 0)
        if u.level == -1:
            v.level = 0

        if u.level == total_items - 1:
            continue

        v.level = u.level + 1
        v.weight = u.weight + items[v.level][1].weight
        v.value = u.value + items[v.level][1].value
        if (v.weight <= weight and v.value > maxProfit):
            maxProfit = v.value

        v.bound = bound(v, total_items, weight, items)
        if (v.bound > maxProfit):
            Q.append(v)

        v = KnapsackNode(0, 0, 0, 0)                                  # Added line
        v.level = u.level + 1                       # Added line
        v.weight = u.weight
        v.value = u.value
        v.bound = bound(v, total_items, weight, items)
        if (v.bound > maxProfit):
            # print(items[v.level])
            Q.append(v)
        
    return maxProfit
