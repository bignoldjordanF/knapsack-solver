from knapsack import KnapsackInstance, KnapsackAllocation

# References:
# [1] https://medium.com/@fabianterh/how-to-solve-the-knapsack-problem-with-dynamic-programming-eb88c706d3cf

def dynamic_programming_solver(instance: KnapsackInstance) -> KnapsackAllocation:
    dp: list = [
        [0 for _ in range(instance.capacity + 1)]
        for _ in range(len(instance.items) + 1)
    ]

    for i in range(1, len(instance.items) + 1):
        for j in range(1, instance.capacity + 1):
            item = instance.items[i - 1]

            value_without_item: int = dp[i - 1][j]
            knapsack_can_hold: bool = item.weight <= j

            if not knapsack_can_hold:
                dp[i][j] = value_without_item
                continue
            
            value_with_item: int = dp[i - 1][j - item.weight] + item.value
            dp[i][j] = max(value_with_item, value_without_item)

    best_value: int = dp[-1][-1]
    allocation: list = []
    i: int = len(instance.items)
    j: int = instance.capacity

    while i > 0 and j > 0:
        if dp[i][j] != dp[i - 1][j]:
            allocation.append(i - 1)
            j -= instance.items[i - 1].weight
        i -= 1

    return KnapsackAllocation(allocation, best_value)
