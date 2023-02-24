from knapsack import KnapsackInstance, KnapsackAllocation

# References:
# [1] https://medium.com/@fabianterh/how-to-solve-the-knapsack-problem-with-dynamic-programming-eb88c706d3cf

def dynamic_programming_solver(instance: KnapsackInstance) -> KnapsackAllocation:
    """
    We build a dynamic programming matrix that holds the maximum value achievable
    at any (i, j) pair, where i means we only have access to the first i items, 
    i.e., {1, 2, ..., i}, and j means we only have j budget available. The base
    cases are simple: dp[0][j] = 0 for all j because there are no items to choose
    from, and dp[i][0] = 0 for all i, assuming all values are positive, because
    we have no budget. Each successive case can then use previous solutions.
    """

    # The dynamic programming matrix is initialised with zeros, thus the
    # base cases are already filled.
    dp: list = [
        [0 for _ in range(instance.capacity + 1)]
        for _ in range(len(instance.items) + 1)
    ]

    # We iterate through every possible item subset with every possible
    # integer budget {1, 2, ..., budget}.
    for i in range(1, len(instance.items) + 1):
        for j in range(1, instance.capacity + 1):
            item = instance.items[i - 1]

            # At each (i, j) pair, we decide either to exclude or include
            # the item i:
            value_without_item: int = dp[i - 1][j]
            knapsack_can_hold: bool = item.weight <= j

            # If the capacity cannot include i, naturally exclude it.
            if not knapsack_can_hold:
                dp[i][j] = value_without_item
                continue
            
            # Otherwise, our value is the current item value, plus the
            # maximum value achievable with the remaining items
            # {1, 2, ..., i - 1} and the remaining budget j - i.weight.
            # Elegantly, our matrix will have already computed this value.
            value_with_item: int = dp[i - 1][j - item.weight] + item.value
            dp[i][j] = max(value_with_item, value_without_item)

    # The best value is stored at the very end of the matrix. We can
    # find the optimal allocation that gives this value by backtracking.
    best_value: int = dp[-1][-1]
    allocation: list = []
    i: int = len(instance.items)
    j: int = instance.capacity

    # We add item indexes where the maximum value possible changes,
    # because it must be the case that that item was included.
    while i > 0 and j > 0:
        if dp[i][j] != dp[i - 1][j]:
            allocation.append(i - 1)
            j -= instance.items[i - 1].weight
        i -= 1

    return KnapsackAllocation(allocation, best_value)
