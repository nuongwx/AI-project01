import random

POPULATION_SIZE = 100
MAX_GENERATION = 100
MUTATION_RATE = 0.01

class GeneticAlgorithm:

    population = []
    capacity = 0
    number_of_classes = 0
    weights = []
    values = []
    class_label = []

    def __init__(self, case):
        self.capacity = case["capacity"]
        self.number_of_classes = case["number_of_classes"]
        self.weights = case["weights"]
        self.values = case["values"]
        self.class_label = case["class_label"]
        
    def generate_individual(self):
        individual = []
        for i in range(len(self.weights)):
            individual.append(random.randint(0, 1))
        return individual    

    def generate_population(self):
        for i in range(POPULATION_SIZE):
            self.population.append(self.generate_individual())
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
        #at least one item from each class
        if len(set([self.class_label[i] for i in range(len(individual)) if individual[i] == 1])) < self.number_of_classes:
            return 0
        return value
            

    #40% of fitest popoulation, Individuals will mate to produce offspring
    def selection_parent(self):
        self.population.sort(key=self.fitness, reverse=True)
        return self.population[:int(0.4 * POPULATION_SIZE)]
    
    def crossover(self, parent1, parent2):
        child = []
        for i in range(len(parent1)):
            prob = random.random()
            #If prob < 0.5, parent1 gene will be selected, else parent2 gene will be selected
            if prob < 0.5:
                child.append(parent1[i])
            else:
                child.append(parent2[i])
        return child

    def mutate(self, individual):
        #flip 1 gene randomly
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
        #generate initial population
        self.generate_population()
        new_generation = []
        #run genetic algorithm creating MAX_GENERATION new generation
        for i in range(MAX_GENERATION):
            #select parent
            parent_list = self.selection_parent()
            for i in range(POPULATION_SIZE):
                parent = random.sample(parent_list, 2)
                child = self.crossover(parent[0], parent[1])
                new_generation.append(child)
            #mutate new generation
            new_generation = self.mutationMethod(new_generation)
            #extend new generation to population and get POPULATION_SIZE best individuals
            self.population.extend(new_generation)
            self.population.sort(key=self.fitness, reverse=True)
            self.population = self.population[:POPULATION_SIZE]
        self.population.sort(key=self.fitness, reverse=True)
        return self.population[0], self.fitness(self.population[0])

def input(file_name):
    capacity = 0
    number_of_classes = 0
    weights = []
    values = []
    class_label = []

    # Open the file
    f = open(file_name, "r")
    lines = f.readlines()
    capacity = int(lines[0])
    number_of_classes = int(lines[1])
    weights = [int(i) for i in lines[2].split(',')]
    values = [int(i) for i in lines[3].split(',')]
    class_label = [int(i) for i in lines[4].split(',')]
    f.close()
    return {
        "capacity": capacity,
        "number_of_classes": number_of_classes,
        "weights": weights,
        "values": values,
        "class_label": class_label
    }

case = input("./test_case/input_1.txt")
ga = GeneticAlgorithm(case)
print(ga.run())
