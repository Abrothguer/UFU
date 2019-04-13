from random import randint
from math import ceil


def fitness(state):
    conflict = 0
    for queen_1 in range(len(state)):
        for queen_2 in range(queen_1 + 1, len(state)):

            # Same row
            if state[queen_1] == state[queen_2]:
                conflict += 1

            # Diagonal
            difference = queen_2 - queen_1
            if (state[queen_1] == state[queen_2] - difference or
                    state[queen_1] == state[queen_2] + difference):
                conflict += 1
    return conflict


def generate_population(pop_size, board_size):

    population = []
    for _ in range(pop_size):
        population.append([randint(0, board_size - 1) for _ in range(board_size)])
    return population


def reproduce(indv_1, indv_2, fixed_crossover=-1):

    if fixed_crossover != -1:
        split_index = randint(0, len(indv_1) - 1)
    else:
        split_index = fixed_crossover

    child_1 = indv_1[0:split_index] + indv_2[split_index:]
    child_2 = indv_2[0:split_index] + indv_1[split_index:]

    return (child_1, child_2)


def mutate(indv, mutation_chance=10):

    chance = randint(1, mutation_chance)
    if chance == 1:
        # print(f"mutating {indv}\n")
        row = randint(0, len(indv) - 1)
        column = randint(0, len(indv) - 1)
        indv[row] = column
    return indv


def genetic_solving(population, max_gens=None, crossover=-1, mutation_chance=10):

    population = [(fitness(indv), indv) for indv in population]
    print(f"Original population: \n")
    for fit, indv in population:
        print(f"fitness = {fit}, indv = {indv} ")

    limit = 0

    while limit != max_gens:

        # Ordenar por melhores
        population.sort()
        if population[0][0] == 0:
            return (population[0][1], limit)

        print(f"\nRaking:")
        for fit, indv in population:
            print(f"Fitness = {fit}, Indv = {indv} ")

        children_pop = []
        for index in range(ceil(len(population) / 2)):

            parent_1 = population[index]
            parent_2 = population[randint(0, round(len(population) - 1))]
            children = reproduce(parent_1[1], parent_2[1], crossover)

            # print(f"children of {parent_1} and {parent_2}")
            # print(f" = {children[0]} and {children[1]}\n")

            children_pop += [mutate(child, mutation_chance) for child in children]

        population = [(fitness(indv), indv) for indv in children_pop]
        limit += 1
        # input()

    return None


def main():

    try:
        board_size = int(input("Tamanho do tabuleiro (Default: 4): "))
    except:
        board_size = 4
    try:
        pop_size = int(input("Tamanho da populacao (Default: 10): "))
    except:
        pop_size = 10
    try:
        gen_limit = int(input("Nro maximo de geracoes (Default: 1000): "))
    except:
        gen_limit = 1000
    try:
        crossover = int(input("Ponto de crossover (Default: Aleatorio): "))
        crossover = crossover if crossover >= 0 and crossover < board_size - 1 else 4
    except:
        crossover = -1
    try:
        mutation_chance = int(input("Chance de mutacao (Default: 10 - significando 1 em 10): "))
    except:
        mutation_chance = 10

    population = generate_population(pop_size, board_size)
    resolution = genetic_solving(population, gen_limit, crossover, mutation_chance)

    if resolution is None:
        print(f"Nenhuma solucao encontrada ao longo de {gen_limit} geracoes")
    else:
        print(f"\nSolucao encontrada em {resolution[1]} geracoes")
        print(f"Individuo : {resolution[0]}")


if __name__ == "__main__":
    main()
