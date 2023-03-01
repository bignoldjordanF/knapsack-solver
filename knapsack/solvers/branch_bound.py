from knapsack import KnapsackInstance, KnapsackAllocation
from dataclasses import dataclass
from collections import deque

# References:
# [0] https://www.geeksforgeeks.org/implementation-of-0-1-knapsack-using-branch-and-bound/?ref=lbp
# [1] https://stackoverflow.com/questions/43965835/knapsack-branch-and-bound-wrong-result

@dataclass
class KnapsackNode:
    level: int  # The level of the node in the decision tree [i.e., the item index]
    value: int  # The total value on this path in the decision tree
    bound: int  # The upper bound of maximum profit in the subtree of this node
    weight: int  # The total weight on this path in the decision tree
    allocation: list  # The allocation (knapsack) found by this path in the decision tree


def __bound(node: KnapsackNode, n_items: int, capacity: int, items: list):
    """
    We relax the strict binary constraint on the decision variables such
    that items may be partially included in the knapsack. This problem,
    known as the fractional knapsack problem, can be solved in linear
    time by a greedy algorithm. This algorithm is utilitised below to 
    identify an upper bound on the maximum value achievable at this node. 
    """
    
    # Invalid Node
    if node.weight >= capacity:
        return 0
    
    # We are finding the upper bound based on the remaining elements
    # given the actual [binary constraint] value we have achieved so far.
    value_bound: int = node.value
    level: int = node.level + 1
    weight: int = node.weight

    # Add remaining items in the order they are passed into the function
    # until the capacity is exhausted, or we run out of items.
    while level < n_items and weight + items[level][1].weight <= capacity:
        weight += items[level][1].weight
        value_bound += items[level][1].value
        level += 1
    
    # If the capacity is exhausted, we add as much of the last item as 
    # possible to the bound to give the upper bound.
    if level < n_items:
        value_bound += (capacity - weight) * \
            items[level][1].value / items[level][1].weight
    
    return value_bound


def branch_and_bound_solver(knapsack: KnapsackInstance) -> KnapsackAllocation:
    """
    We start with a root knapsack node, and then generate child nodes which
    do or do not contain each successive item in a sorted list. We expand
    promising nodes, i.e., nodes which have an upper bound, as defined by
    a constraint relaxation, that is higher than the current best value.
    These promising nodes eventually lead to the returned optimal solution.
    """

    # The items are sorted by their value-weight ratio for the bound algorithm,
    # which uses a greedy approach:
    items: list = [(pid, cand) for pid, cand in enumerate(knapsack.items)]
    items: list = sorted(items, key=lambda i: i[1].value/i[1].weight, reverse=True)

    # Make a queue to traverse the decision tree:
    queue: deque = deque()
    queue.append(KnapsackNode(-1, 0, 0, 0, []))  # Root Node

    max_value: int = 0
    max_allocation: list = []

    # Each knapsack node has a level attribute, which considers all
    # items in the item subset {1, ..., level}.
    while queue:
        curr: KnapsackNode = queue.popleft()
        child: KnapsackNode = KnapsackNode(0, 0, 0, 0, [])

        # If curr is the root node, then the child is
        # at level zero:
        if curr.level == -1:
            child.level = 0
        
        # If the current level (item subset) considers all items,
        # then there is nothing more to be done:
        if curr.level == len(items) - 1:
            continue

        # Our first possible child considers the solution with the
        # current item (level) included:
        child.level = curr.level + 1
        child.weight = curr.weight + items[child.level][1].weight
        child.value = curr.value + items[child.level][1].value
        child.allocation = curr.allocation[:] + [items[child.level][0]]

        # If our child node is valid and has the largest value so far,
        # update the max_value and max_allocation values.
        if child.weight <= knapsack.capacity and child.value > max_value:
            max_value = child.value
            max_allocation = child.allocation

        # The upper bound tells us the optimal solution given the child
        # node provided we can partially include the remaining items
        # {level + 1, ..., n}.
        child.bound = __bound(child, len(items), knapsack.capacity, items)
        
        # If the child bound is larger than the max_value, then there
        # is still 'potential', so add it to the queue.
        if child.bound > max_value:
            queue.append(child)

        # We repeat the process for a child node that does not include
        # the current item (level). We do not try to update the 
        # max_value or max_allocation variables.

        child = KnapsackNode(0, 0, 0, 0, [])
        child.level = curr.level + 1
        child.weight = curr.weight
        child.value = curr.value
        child.allocation = curr.allocation[:]
        child.bound = __bound(child, len(items), knapsack.capacity, items)

        if child.bound > max_value:
            queue.append(child)
    
    return KnapsackAllocation(max_allocation, max_value)

