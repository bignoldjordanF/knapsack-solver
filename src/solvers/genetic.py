from knapsack import KnapsackInstance, KnapsackAllocation
import random

# TODO: This is a fairly rough initial approach, and it
# hasn't been tested thoroughly, so use with caution.
# However, the initial tests showed very good
# approximations of the optimal solutions for
# small and medium sized instances.

# TODO: Add documentation to the functions.

def __create_population(instance: KnapsackInstance, population_size: int):
    """
    Creates an initial population of population_size chromosomes
    in the form e.g. [0, 1, 0, 0, 1, 1, 1], where each index is
    a binary gene representing one item. A one gene means that
    the corresponding item is currently in the knapsack.
    """
    population: list = []
    for _ in range(population_size):
        chromosome: list = [random.randint(0, 1) for _ in range(len(instance.items))]
        population.append(chromosome)
    return population


def __fitness(instance: KnapsackInstance, chromosome: list):
    total_weight: int = 0
    total_value: int = 0

    for i in range(len(chromosome)):
        if chromosome[i]:
            total_weight += instance.items[i].weight
            total_value += instance.items[i].value
    
    # We want to heavily discourage invalid chromosomes
    # because they are not fit for survival.
    if total_weight > instance.capacity:
        return -total_value

    return total_value


def __selection(instance: KnapsackInstance, population: list):
    tournament_size: int = 2
    selected_parents: list = []
    for _ in range(2):
        tournament: list = random.sample(population, tournament_size)
        best_chromosome: list = max(tournament, key=lambda chromosome: __fitness(instance, chromosome))
        selected_parents.append(best_chromosome)
    return tuple(selected_parents)


def __crossover(crossover_rate: float, parent_a: list, parent_b: list):
    if random.random() > crossover_rate:
        return parent_a, parent_b

    crossover_point: int = random.randint(1, len(parent_a) - 1)
    child_a: list = parent_a[:crossover_point] + parent_b[crossover_point:]
    child_b: list = parent_b[:crossover_point] + parent_a[crossover_point:]

    return child_a, child_b


def __mutation(mutation_rate: float, chromosome: list):
    if random.random() > mutation_rate:
        return chromosome

    mutation_point: int = random.randint(0, len(chromosome) - 1)
    chromosome[mutation_point] = 1 - chromosome[mutation_point]
    return chromosome


def __genetic_algorithm_solver(
    instance: KnapsackInstance,
    population_size: int,
    mutation_rate: int,
    crossover_rate: int,
    num_generations: int
):
    
    # Initial population
    population: list = __create_population(instance, population_size)

    # Generate offspring num_generations times
    for _ in range(num_generations):
        offspring: list = []
        best_chromosome: list = []
        
        # The offspring population must be of population_size
        while len(offspring) < len(population):
            
            # Select two parents based on fitness values
            parent_a, parent_b = __selection(instance, population)
            child_a, child_b = __crossover(crossover_rate, parent_a, parent_b)

            child_a = __mutation(mutation_rate, child_a)
            child_b = __mutation(mutation_rate, child_b)

            offspring.append(child_a)
            offspring.append(child_b)
        
        population = offspring
    
    best_chromosome: list = max(population, key=lambda chromosome: __fitness(instance, chromosome))
    best_fitness: int = __fitness(instance, best_chromosome)

    allocation: list = [idx for idx, gene in enumerate(best_chromosome) if gene]
    return KnapsackAllocation(allocation, best_fitness)


POPULATION_SIZE = 100
MUTATION_RATE = 0.3
CROSSOVER_RATE = 0.8
NUM_GENERATIONS = 250


def genetic_algorithm_solver(instance: KnapsackInstance):
    return __genetic_algorithm_solver(
        instance,
        POPULATION_SIZE,
        MUTATION_RATE,
        CROSSOVER_RATE,
        NUM_GENERATIONS
    )
