import random2
pool = []
population = [[0] + random2.sample(range(1, 10), 9),
              [0] + random2.sample(range(1, 10), 9),
              [0] + random2.sample(range(1, 10), 9)]

fitness = []


def calculateDistance(route):
    total_cost = 0
    for i in range(1, len(route)):
        total_cost += abs(route[i] - route[i - 1])
    return total_cost


def mutate(seq):
    idx = range(len(seq))
    i1, i2 = random2.sample(idx, 2)
    seq[i1], seq[i2] = seq[i2], seq[i1]


recordDistance = float('inf')
best_ever = []
d = 0

while d < recordDistance:
    for i in range(10):
        for generation in population:
            d = calculateDistance(generation)
            if d < recordDistance:
                recordDistance = d
                best_ever = generation
            fitness = np.append(fitness, 1 / d)

        best_fit = population.index(best_ever)

        total = sum(fitness)
        fitness = np.array(fitness) / total

        for i in range(10):
            mutate(population[best_fit])
        print(population[best_fit], fitness[best_fit], calculateDistance(population[best_fit]))