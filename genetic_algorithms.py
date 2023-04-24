import random

POPULATION_MULTIPLIER = 5
MAX_GENERATION = 100
MUTATION_RATE = 0.1


class GeneticAlgorithm:
    def __init__(self, case):
        self.capacity = case["capacity"]
        self.number_of_classes = case["number_of_classes"]
        self.weights = case["weights"]
        self.values = case["values"]
        self.class_label = case["labels"]
        self.population_size = self.weights.__len__() * POPULATION_MULTIPLIER * self.number_of_classes  # fmt: skip

    def generate_population(self):
        # a decent initial population, with minimum² 1 item from each class
        self.population = [[0] * self.weights.__len__()] * self.population_size
        temp = [[float("inf")] * 2] * self.number_of_classes
        for i in range(self.number_of_classes):
            for j in range(self.weights.__len__()):
                if self.class_label[j] == i + 1 and temp[i][0] > self.weights[j]:
                    temp[i] = [self.weights[j], j]
        for i in range(self.number_of_classes):
            self.population[0][temp[i][1]] = 1

        return

    def fitness(self, individual):
        weight = 0
        value = 0
        for i in range(len(individual)):
            if individual[i] == 1:
                weight += self.weights[i]
                value += self.values[i]
        if weight > self.capacity:
            return 0
        # at least one item from each class
        if len(set([self.class_label[i] for i in range(len(individual)) if individual[i]])) != self.number_of_classes:
            return 0
        return value

    # 40% of fitest popoulation, Individuals will mate to produce offspring
    def selection_parent(self):
        self.population.sort(key=self.fitness, reverse=True)
        return self.population[: int(0.4 * self.population_size)]

    def crossover(self, parent1, parent2):
        child = []
        for i in range(len(parent1)):
            prob = random.random()
            # If prob < 0.5, parent1 gene will be selected, else parent2 gene will be selected
            if prob < 0.5:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        return child

    def mutate(self, individual):
        # flip 1 gene randomly
        pos = random.randint(0, len(individual) - 1)
        individual[pos] = 1 - individual[pos]
        return individual

    def mutationMethod(self, population):
        for i in range(len(population)):
            prob = random.randint(0, 100) / 100
            if prob < MUTATION_RATE:
                population[i] = self.mutate(population[i])
        return population

    def run(self):
        # generate initial population
        self.generate_population()
        new_generation = []
        # run genetic algorithm creating MAX_GENERATION new generation
        for i in range(MAX_GENERATION):
            # print(i, self.fitness(self.population[0]))
            # select parent
            parent_list = self.selection_parent()
            for i in range(self.population_size):
                parent = random.sample(parent_list, 2)
                child = self.crossover(parent[0], parent[1])
                new_generation.append(child)
            # mutate new generation
            new_generation = self.mutationMethod(new_generation)
            # extend new generation to population and get self.population_size best individuals
            self.population.extend(new_generation)
            self.population.sort(key=self.fitness, reverse=True)
            self.population = self.population[: self.population_size]
            # the whole population is "pretty much" homogeneous, stop?
            if self.fitness(self.population[0]) == self.fitness(self.population[-1]):
                break

        self.population.sort(key=self.fitness, reverse=True)
        return self.fitness(self.population[0]), self.population[0]


def run(case):
    ga = GeneticAlgorithm(case)
    return ga.run()
