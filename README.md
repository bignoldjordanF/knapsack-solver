# Knapsack Solver

## Description

This project contains implementations of optimisation algorithms in Python to solve the binary knapsack problem. It includes a generator class create knapsack instances from input data or at random, and functions to solve the instances, which return an optimal allocation and value pair. The algorithms available are:

* Dynamic Programming (Exact)
* Branch & Bound (Exact)
* Greedy & Ratio Greedy (Approximation)
* Simulated Annealing (Approximation)
* Genetic Algorithm (Approximation)

## Example Use

Before using the solvers, we wrap our problems in ```KnapsackInstance``` objects, using the ```KnapsackGenerator``` class. We can randomly generate instances or pass our own instance (capacity, weights and values):

```python

from knapsack import *

# You can pass minimum and maximum randomness bounds
# for each of capacity, num_items, weight and values.
generator: KnapsackGenerator = KnapsackGenerator()

# We can use generate() for a random instance:
instance: KnapsackInstance = generator.generate()

# We can use create() for a custom instance:
instance: KnapsackInstance = generator.create(
  80,  # Capacity
  [40, 25, 45, 60],  # Weights/Sizes
  [6, 5, 2, 8]  # Values
)

```

The solvers can be used by importing them from `solvers` and passing our created `KnapsackInstance`. They return a named tuple `KnapsackAllocation`, which has attributes `allocation` and `value`.

```python

# ...

from knapsack.solvers import *

allocation: KnapsackAllocation = genetic_algorithm_solver(instance)
print(allocation.knapsack)  # e.g. [0, 1]
print(allocation.value)  # e.g. 11

```

A file containing examples for generating a problem instance and using the solving algorithms can be found at ```example.py```.

## Available Solvers
All of the solvers take a single `KnapsackInstance` object. They can all be imported at once, or individually:

* `from knapsack.solvers import dynamic_programming_solver`
* `from knapsack.solvers import branch_and_bound_solver`
* `from knapsack.solvers import greedy_solver`
* `from knapsack.solvers import ratio_greedy_solver`
* `from knapsack.solvers import simulated_annealing_solver`
* `from knapsack.solvers import genetic_algorithm_solver`

## Binary Knapsack Problem

In the binary knapsack problem, we are typically given a set of items and a knapsack with a weight capacity. Each item has some value and some weight. We must compute the largest sum of values the knapsack can hold without exceeding the weight capacity. A typical problem instance may be expressed more formally as follows:

* $\text{A maximum knapsack capacity }W\text{, where } W\in{\mathbb{Z}}.$
* $\text{A set of candidate items }N=\lbrace{}1,2,...,n\rbrace{}\text{, where }n\text{ is the number of candidate items, and thus }n\in{\mathbb{Z}}.$
* $\text{A weight function }w\text{ defining the weight for each item such that }w_i:i\mapsto{\mathbb{R}}\space\forall{i\in{N}}.$
* $\text{A value function }v\text{ defining the value for each item such that }v_i:i\mapsto{\mathbb{R}}\space\forall{i\in{N}}.$

By creating a binary decision variable $x_i\space\forall{i\in{N}}$, we can express the binary knapsack problem as an integer linear program:

* $\text{Max. }\sum_{i\in{N}}{x_i\cdot{}v_i}$
* $\text{Subject to constraints:}$
  * $\sum_{i\in{N}}{x_i\cdot{}w_i}\le{W}$
  * $x_i\in\lbrace{0, 1}\rbrace{}\space\forall{i\in{N}}$

In words, a binary decision variable $x_i=1$ if and only if item $i$ is included in the knapsack. We want to maximise an objective function which sums the values of all the items who are included in the knapsack, subject to the constraint that the summed weights of those included items do not exceed the knapsack capacity. 
