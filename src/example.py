from knapsack import *
from solvers.greedy import greedy_solver, ratio_greedy_solver
from solvers.dyn_prog import dynamic_programming_solver
from solvers.branch_bound import branch_and_bound_solver
from solvers.sim_anneal import simulated_annealing_solver


generator: KnapsackGenerator = KnapsackGenerator(
    min_capacity=500000,
    max_capacity=1000000,
    min_num_items=5,
    max_num_items=25,
    min_weight=1000,
    max_weight=500000,
    min_value=1,
    max_value=10
)
knapsack: KnapsackInstance = generator.generate()

print()
print('KNAPSACK INSTANCE')
print('-' * 17)
print(knapsack)

print()
print('LINEAR APPROXIMATIONS')
print('-' * 21)
print(f'Greedy: {greedy_solver(knapsack)}')
print(f'Ratio Greedy: {ratio_greedy_solver(knapsack)}')

print()
print('META-HEURISTICS')
print('-' * 15)
print(f'Simulated Annealing: {simulated_annealing_solver(knapsack)}')

print()
print('EXACT ALGORITHMS')
print('-' * 16)
print(f'Dynamic Programming: {dynamic_programming_solver(knapsack)}')
print(f'Branch & Bound: {branch_and_bound_solver(knapsack)}')

print()
