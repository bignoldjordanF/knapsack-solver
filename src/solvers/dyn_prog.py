from knapsack import Knapsack, Allocation


def dynamic_programming_solver(knapsack: Knapsack) -> Allocation:
    dp: list = [
        [0 for _ in range(knapsack.capacity + 1)]
        for _ in range(len(knapsack.candidates) + 1)
    ]

    for i in range(1, len(knapsack.candidates) + 1):
        for j in range(1, knapsack.capacity + 1):
            candidate = knapsack.candidates[i - 1]

            value_without_item: int = dp[i - 1][j]
            knapsack_can_hold: bool = candidate.weight <= j

            if not knapsack_can_hold:
                dp[i][j] = value_without_item
                continue
            
            value_with_item: int = dp[i - 1][j - candidate.weight] + candidate.value
            dp[i][j] = max(value_with_item, value_without_item)

    best_value: int = dp[-1][-1]
    allocation: list = []
    i: int = len(knapsack.candidates)
    j: int = knapsack.capacity

    while i > 0 and j > 0:
        if dp[i][j] != dp[i - 1][j]:
            allocation.append(i - 1)
            j -= knapsack.candidates[i - 1].weight
        i -= 1

    return Allocation(allocation, best_value)
