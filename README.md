# Knapsack Solvers

## Description

This project contains implementations of optimisation algorithms in Python to solve the binary knapsack problem. It includes a generator class create knapsack instances from input data or at random, and functions to solve the instances, which return an optimal allocation and value pair. The algorithms available are:

* Greedy Algorithm
* Dynamic Programming
* $...$

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
