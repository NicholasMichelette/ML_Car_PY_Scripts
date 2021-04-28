from UClassTEst import *
import numpy as np
import random
from NeuralNet import *

filepath = "J:/Documents/UScripts/UScripts/UScripts/data/"
iter_char = 'g'
mutation_rate = 0.05
crossover_rate = 0.225
mutation_change = 1.0


def record(filename):
    bestcar = 0
    total_fitness = 0
    for i in range(len(class_test.brain)):
        total_fitness += class_test.fitness[i]
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            bestcar = i
    afn = filepath + filename + "avg.txt"
    bfn = filepath + filename + "best.txt"
    avg_fit = str(total_fitness/len(class_test.brain)) + "\n"
    f = open(afn, "a+")
    f.write(avg_fit)
    f.close()

    f2 = open(bfn, "a+")
    f2.write(str(class_test.fitness[bestcar]) + "\n")
    f2.close()

def mutate(weights):
    new_weights = weights
    for l in range(len(new_weights)):
        for w in range(len(new_weights[l])):
            if random.uniform(0, 1) > 1 - mutation_rate:
                new_weights[l][w] += random.uniform(-mutation_change, mutation_change)
    return new_weights

def crossover(parent1, parent2): #parents are the weights
    w1 = parent1.copy()
    w2 = parent2.copy()
    new_w1 = w1.copy()
    new_w2 = w2.copy()

    gene = random.randint(0, len(w1) - 1)
    gene2 = random.randint(0, len(w1[gene]) - 1)

    new_w1[gene] = w2[gene]
    new_w2[gene] = w1[gene]

    return np.asarray([new_w1,new_w2])


def mutate_individual(weights):
    new_weights = weights.copy()
    for l in range(len(new_weights)):
        for w in range(len(new_weights[l])):
            if type(new_weights[l][w]) == np.ndarray:
                for r in range(len(new_weights[l][w])):
                    if random.uniform(0, 1) > 1 - mutation_rate:
                        new_weights[l][w][r] += random.uniform(-mutation_change, mutation_change)
            else:
                if random.uniform(0, 1) > 1 - mutation_rate:
                    new_weights[l][w] += random.uniform(-mutation_change, mutation_change)

    return new_weights

def crossover_random(parent1, parent2): #parents are the weights
    w1 = parent1.copy()
    w2 = parent2.copy()
    new_w1 = w1.copy()
    new_w2 = w2.copy()

    for l in range(len(w1)):
        for w in range(len(w1[l])):
            if type(w1[l][w]) == np.ndarray:
                for r in range(len(w1[l][w])):
                    if random.uniform(0, 1) > 1 - crossover_rate:
                        new_w1[l][w][r] = w2[l][w][r]
                        new_w2[l][w][r] = w1[l][w][r]
            else:
                if random.uniform(0, 1) > 1 - crossover_rate:
                        new_w1[l][w] = w2[l][w]
                        new_w2[l][w] = w1[l][w]

    return np.asarray([new_w1,new_w2])


#basic select top two, cross, mutate 
def algo1():
    record(iter_char + "algo1")
    bestcar = 0
    bestcar2 = 1
    for i in range(len(class_test.brain)):
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            bestcar = i

    for i in range(len(class_test.brain)):
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            if bestcar2 != bestcar:
                bestcar = i

    best_weights = class_test.brain[bestcar].model.get_weights().copy()
    best_weights2 = class_test.brain[bestcar].model.get_weights().copy()
    if class_test.fitness[bestcar] > class_test.best_fitness:
        print("using best of current gen")
        class_test.best_fitness = class_test.fitness[bestcar]
        class_test.best_weights = best_weights
        if class_test.fitness[bestcar2] > class_test.best_fitness2:
            class_test.best_fitness2 = class_test.fitness[bestcar2]
            class_test.best_weights2 = best_weights2
        else:
            best_weights2 = class_test.best_weights2.copy()
    else:
        print("using previous gen")
        if len(class_test.best_weights) > 0:
            best_weights = class_test.best_weights.copy()
            best_weights2 = class_test.best_weights2.copy()


    for i in range(len(class_test.brain)//2):
        tomutate = best_weights.copy()
        tomutate2 = best_weights2.copy()
        crossed = crossover(tomutate, tomutate2)

        class_test.brain[i * 2].model.set_weights(mutate(crossed[0]))
        class_test.brain[i * 2 + 1].model.set_weights(mutate(crossed[1]))
        class_test.fitness[i * 2] = 0
        class_test.fitness[i * 2 + 1] = 0


#select 2 based on probabilities, cross them, mutate them
#   did end up learning to turn right, but lost the ability
def algo2():
    record(iter_char + "algo2")
    total_fitness = 0
    for i in range(len(class_test.brain)):
        total_fitness += class_test.fitness[i]

    p1 = random.uniform(0, total_fitness)
    p2 = random.uniform(0, total_fitness)
    totalfit = 0
    parent1 = 0
    parent2 = 0
    for i in range(len(class_test.brain)):
        totalfit += class_test.fitness[i]
        if p1 > totalfit:
            parent1 = i
        if p2 > totalfit:
            parent2 = i

    best_weights = class_test.brain[parent1].model.get_weights().copy()
    best_weights2 = class_test.brain[parent2].model.get_weights().copy()

    for i in range(len(class_test.brain)//2):
        tomutate = best_weights.copy()
        tomutate2 = best_weights2.copy()
        crossed = crossover(tomutate, tomutate2)

        class_test.brain[i * 2].model.set_weights(mutate(crossed[0]))
        class_test.brain[i * 2 + 1].model.set_weights(mutate(crossed[1]))
        class_test.fitness[i * 2] = 0
        class_test.fitness[i * 2 + 1] = 0

    class_test.brain[len(class_test.brain) - 1] = car_nn()
    class_test.fitness[len(class_test.brain) - 1] = 0


#select weights randomly to change based on fitness for probability, then mutate
def algo3():
    record(iter_char + "algo3")
    total_fitness = 0
    fit_chance = []
    weights = []
    for i in range(len(class_test.brain)):
        total_fitness += class_test.fitness[i]
        fit_chance.append(total_fitness)
        weights.append(class_test.brain[i].model.get_weights().copy())

    for i in range(len(class_test.brain)):
        basew = class_test.brain[0].model.get_weights().copy()
        for weightl in range(len(basew)):
            for weight in range(len(basew[weightl])):
                rn = random.uniform(0, total_fitness)
                cn = 0
                for c in range(len(fit_chance)):
                    if rn > fit_chance[c]:
                        cn = c
                basew[weightl][weight] = weights[cn][weightl][weight]
        class_test.brain[i].model.set_weights(mutate(basew))


    class_test.brain[len(class_test.brain) - 1] = car_nn()
    class_test.fitness[len(class_test.brain) - 1] = 0


#cross best car with each car, then mutate
def algo4():
    record(iter_char + "algo4")
    bestcar = 0
    for i in range(len(class_test.brain)):
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            bestcar = i


    best_weights = class_test.brain[bestcar].model.get_weights().copy()
    if class_test.fitness[bestcar] > class_test.best_fitness:
        print("using best of current gen")
        class_test.best_fitness = class_test.fitness[bestcar]
        class_test.best_weights = best_weights
    else:
        print("using previous gen")
        if len(class_test.best_weights) > 0:
            best_weights = class_test.best_weights.copy()


    for i in range(len(class_test.brain)):
        tomutate = best_weights.copy()
        tomutate2 = class_test.brain[i].model.get_weights().copy()
        crossed = crossover(tomutate, tomutate2)

        class_test.brain[i].model.set_weights(mutate(crossed[random.randint(0, 1)]))
        class_test.fitness[i] = 0

    class_test.brain[len(class_test.brain) - 1] = car_nn()
    class_test.fitness[len(class_test.brain) - 1] = 0


#algo4 but saves uses previous weights if current gen does not produce a new best
def algo5():
    record(iter_char + "algo5")
    bestcar = 0
    allw = []
    for i in range(len(class_test.brain)):
        allw.append(class_test.brain[i].model.get_weights().copy())
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            bestcar = i


    best_weights = class_test.brain[bestcar].model.get_weights().copy()
    if class_test.fitness[bestcar] > class_test.best_fitness:
        print("using best of current gen")
        class_test.best_fitness = class_test.fitness[bestcar]
        class_test.best_weights = best_weights
        class_test.best_weights2 = allw.copy()
    else:
        print("using previous gen")
        if len(class_test.best_weights) > 0:
            best_weights = class_test.best_weights.copy()


    for i in range(len(class_test.brain)):
        tomutate = best_weights.copy()
        tomutate2 = class_test.best_weights2.copy()[i]
        crossed = crossover(tomutate, tomutate2)

        class_test.brain[i].model.set_weights(mutate(crossed[1]))
        class_test.fitness[i] = 0

    class_test.brain[len(class_test.brain) - 1] = car_nn()
    class_test.fitness[len(class_test.brain) - 1] = 0


def algo6():
    record(iter_char + "algo6")
    bestcar = 0
    allw = []
    for i in range(len(class_test.brain)):
        allw.append(class_test.brain[i].model.get_weights().copy())
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            bestcar = i


    best_weights = class_test.brain[bestcar].model.get_weights().copy()
    if class_test.fitness[bestcar] > class_test.best_fitness:
        print("using best of current gen")
        class_test.best_fitness = class_test.fitness[bestcar]
        class_test.best_weights = best_weights
        class_test.best_weights2 = allw.copy()
    else:
        print("using previous gen")
        if len(class_test.best_weights) > 0:
            best_weights = class_test.best_weights.copy()


    for i in range(len(class_test.brain)):
        tomutate = best_weights.copy()
        tomutate2 = class_test.best_weights2.copy()[i]
        crossed = crossover_random(tomutate, tomutate2)

        class_test.brain[i].model.set_weights(mutate_individual(crossed[1]))
        class_test.fitness[i] = 0

    class_test.brain[len(class_test.brain) - 1] = car_nn()
    class_test.fitness[len(class_test.brain) - 1] = 0


# select 2 randomly based on probality derived from fitness, random crossover, individual mutation
# does not save the best
# learned to turn right by gen 9, immediatly forgot
def algo7():
    record(iter_char + "algo7")
    total_fitness = 0
    for i in range(len(class_test.brain)):
        total_fitness += class_test.fitness[i]

    p1 = random.uniform(0, total_fitness)
    p2 = random.uniform(0, total_fitness)
    totalfit = 0
    parent1 = 0
    parent2 = 0
    for i in range(len(class_test.brain)):
        totalfit += class_test.fitness[i]
        if p1 > totalfit:
            parent1 = i
        if p2 > totalfit:
            parent2 = i

    best_weights = class_test.brain[parent1].model.get_weights().copy()
    best_weights2 = class_test.brain[parent2].model.get_weights().copy()

    for i in range(len(class_test.brain)//2):
        tomutate = best_weights.copy()
        tomutate2 = best_weights2.copy()
        crossed = crossover_random(tomutate, tomutate2)

        class_test.brain[i * 2].model.set_weights(mutate(crossed[0]))
        class_test.brain[i * 2 + 1].model.set_weights(mutate(crossed[1]))
        class_test.fitness[i * 2] = 0
        class_test.fitness[i * 2 + 1] = 0

    class_test.brain[len(class_test.brain) - 1] = car_nn()
    class_test.fitness[len(class_test.brain) - 1] = 0


def algo8():
    record(iter_char + "algo8")
    bestcar = 0
    bestcar2 = 1
    for i in range(len(class_test.brain)):
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            bestcar = i

    for i in range(len(class_test.brain)):
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            if bestcar2 != bestcar:
                bestcar = i

    best_weights = class_test.brain[bestcar].model.get_weights().copy()
    best_weights2 = class_test.brain[bestcar].model.get_weights().copy()
    if class_test.fitness[bestcar] > class_test.best_fitness:
        print("using best of current gen")
        class_test.best_fitness = class_test.fitness[bestcar]
        class_test.best_weights = best_weights
        if class_test.fitness[bestcar2] > class_test.best_fitness2:
            class_test.best_fitness2 = class_test.fitness[bestcar2]
            class_test.best_weights2 = best_weights2
        else:
            best_weights2 = class_test.best_weights2.copy()
    else:
        print("using previous gen")
        if len(class_test.best_weights) > 0:
            best_weights = class_test.best_weights.copy()
            best_weights2 = class_test.best_weights2.copy()


    for i in range(len(class_test.brain)//2):
        tomutate = best_weights.copy()
        tomutate2 = best_weights2.copy()
        crossed = crossover_random(tomutate, tomutate2)

        class_test.brain[i * 2].model.set_weights(mutate_individual(crossed[0]))
        class_test.brain[i * 2 + 1].model.set_weights(mutate_individual(crossed[1]))
        class_test.fitness[i * 2] = 0
        class_test.fitness[i * 2 + 1] = 0

    class_test.brain[len(class_test.brain) - 1] = car_nn()
    class_test.fitness[len(class_test.brain) - 1] = 0


def algo9():
    record(iter_char + "algo9")
    total_fitness = 0
    bestcar = 0
    fit_chance = []
    weights = []
    for i in range(len(class_test.brain)):
        total_fitness += class_test.fitness[i]
        fit_chance.append(total_fitness)
        weights.append(class_test.brain[i].model.get_weights().copy())
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            bestcar = i

    if class_test.fitness[bestcar] < class_test.best_fitness:
        total_fitness += class_test.best_fitness
        fit_chance.append(total_fitness)
        weights.append(class_test.best_weights.copy())
    else:
        class_test.best_fitness = class_test.fitness[bestcar]
        class_test.best_weights = class_test.brain[bestcar].model.get_weights().copy()

    for i in range(len(class_test.brain)):
        basew = class_test.brain[0].model.get_weights().copy()
        for weightl in range(len(basew)):
            for weight in range(len(basew[weightl])):
                rn = random.uniform(0, total_fitness)
                cn = 0
                for c in range(len(fit_chance)):
                    if rn > fit_chance[c]:
                        cn = c
                basew[weightl][weight] = weights[cn][weightl][weight]
        class_test.brain[i].model.set_weights(mutate(basew))


    class_test.brain[len(class_test.brain) - 1] = car_nn()
    class_test.fitness[len(class_test.brain) - 1] = 0


def algo10():
    record(iter_char + "algo10")
    total_fitness = 0
    bestcar = 0
    bestcar2 = 1
    fit_chance = []
    weights = []
    for i in range(len(class_test.brain)):
        total_fitness += class_test.fitness[i]
        fit_chance.append(total_fitness)
        weights.append(class_test.brain[i].model.get_weights().copy())
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            bestcar = i

    for i in range(len(class_test.brain)):
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            if i != bestcar:
                bestcar2 = i

    if class_test.fitness[bestcar] < class_test.best_fitness:
        if class_test.fitness[bestcar] < class_test.best_fitness2 or class_test.fitness[bestcar2] < class_test.best_fitness2:
            total_fitness += class_test.best_fitness2
            fit_chance.append(total_fitness)
            weights.append(class_test.best_weights2.copy())
        total_fitness += class_test.best_fitness
        fit_chance.append(total_fitness)
        weights.append(class_test.best_weights.copy())
        
    else:
        class_test.best_fitness = class_test.fitness[bestcar]
        class_test.best_weights = class_test.brain[bestcar].model.get_weights().copy()
        if class_test.fitness[bestcar2] > class_test.best_fitness2:
            class_test.best_fitness2 = class_test.fitness[bestcar2]
            class_test.best_weights2 = class_test.brain[bestcar2].model.get_weights().copy()

    for i in range(len(class_test.brain)):
        basew = class_test.brain[0].model.get_weights().copy()
        for weightl in range(len(basew)):
            for weight in range(len(basew[weightl])):
                rn = random.uniform(0, total_fitness)
                cn = 0
                for c in range(len(fit_chance)):
                    if rn > fit_chance[c]:
                        cn = c
                basew[weightl][weight] = weights[cn][weightl][weight]
        class_test.brain[i].model.set_weights(mutate_individual(basew))


    class_test.brain[len(class_test.brain) - 1] = car_nn()
    class_test.fitness[len(class_test.brain) - 1] = 0


def algo11():
    record(iter_char + "algo11")
    total_fitness = 0
    bestcar = 0
    bestcar2 = 1
    fit_chance = []
    weights = []
    for i in range(len(class_test.brain)):
        total_fitness += class_test.fitness[i]
        fit_chance.append(total_fitness)
        weights.append(class_test.brain[i].model.get_weights().copy())
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            bestcar = i

    for i in range(len(class_test.brain)):
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            if i != bestcar:
                bestcar2 = i

    if class_test.fitness[bestcar] < class_test.best_fitness:
        if class_test.fitness[bestcar] < class_test.best_fitness2 or class_test.fitness[bestcar2] < class_test.best_fitness2:
            total_fitness += class_test.best_fitness2
            fit_chance.append(total_fitness)
            weights.append(class_test.best_weights2.copy())
        total_fitness += class_test.best_fitness
        fit_chance.append(total_fitness)
        weights.append(class_test.best_weights.copy())
        
    else:
        class_test.best_fitness = class_test.fitness[bestcar]
        class_test.best_weights = class_test.brain[bestcar].model.get_weights().copy()
        if class_test.fitness[bestcar2] > class_test.best_fitness2:
            class_test.best_fitness2 = class_test.fitness[bestcar2]
            class_test.best_weights2 = class_test.brain[bestcar2].model.get_weights().copy()

    for i in range(len(class_test.brain)):
        basew = class_test.brain[0].model.get_weights().copy()
        for weightl in range(len(basew)):
            for weight in range(len(basew[weightl])):
                rn = random.uniform(0, total_fitness)
                cn = 0
                for c in range(len(fit_chance)):
                    if rn > fit_chance[c]:
                        cn = c
                basew[weightl][weight] = weights[cn][weightl][weight]
        class_test.brain[i].model.set_weights(mutate(basew))


    class_test.brain[len(class_test.brain) - 1] = car_nn()
    class_test.fitness[len(class_test.brain) - 1] = 0


def algo12():
    record(iter_char + "algo12")
    total_fitness = 0
    bestcar = 0
    bestcar2 = 1
    fit_chance = []
    weights = []
    for i in range(len(class_test.brain)):
        total_fitness += class_test.fitness[i]
        fit_chance.append(total_fitness)
        weights.append(class_test.brain[i].model.get_weights().copy())
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            bestcar = i

    for i in range(len(class_test.brain)):
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            if i != bestcar:
                bestcar2 = i

    if class_test.fitness[bestcar] < class_test.best_fitness:
        if class_test.fitness[bestcar] < class_test.best_fitness2 or class_test.fitness[bestcar2] < class_test.best_fitness2:
            total_fitness += class_test.best_fitness2
            fit_chance.append(total_fitness)
            weights.append(class_test.best_weights2.copy())
        total_fitness += class_test.best_fitness
        fit_chance.append(total_fitness)
        weights.append(class_test.best_weights.copy())
        
    else:
        class_test.best_fitness = class_test.fitness[bestcar]
        class_test.best_weights = class_test.brain[bestcar].model.get_weights().copy()
        f = open(filepath + "/models/best" + str(int(class_test.fitness[bestcar])) + ".keras", "w+")
        f.write(str(class_test.best_weights))
        f.close()
        if class_test.fitness[bestcar2] > class_test.best_fitness2:
            class_test.best_fitness2 = class_test.fitness[bestcar2]
            class_test.best_weights2 = class_test.brain[bestcar2].model.get_weights().copy()

    for i in range(len(class_test.brain)):
        basew = class_test.brain[0].model.get_weights().copy()
        for weightl in range(len(basew)):
            for weight in range(len(basew[weightl])):
                rn = random.uniform(0, total_fitness)
                cn = 0
                for c in range(len(fit_chance)):
                    if rn > fit_chance[c]:
                        cn = c
                basew[weightl][weight] = weights[cn][weightl][weight]
        class_test.brain[i].model.set_weights(mutate(basew))


    class_test.brain[len(class_test.brain) - 1] = car_nn()
    class_test.fitness[len(class_test.brain) - 1] = 0
    class_test.brain[0].model.set_weights(class_test.best_weights.copy())
    class_test.fitness[0] = class_test.best_fitness
    class_test.brain[1].model.set_weights(class_test.best_weights2.copy())
    class_test.fitness[1] = class_test.best_fitness2


def algo13():
    record(iter_char + "algo13")
    total_fitness = 0
    bestcar = 0
    bestcar2 = 1
    fit_chance = []
    weights = []
    for i in range(len(class_test.brain)):
        total_fitness += class_test.fitness[i]
        fit_chance.append(total_fitness)
        weights.append(class_test.brain[i].model.get_weights().copy())
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            bestcar = i

    for i in range(len(class_test.brain)):
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            if i != bestcar:
                bestcar2 = i

    if class_test.fitness[bestcar] < class_test.best_fitness:
        if class_test.fitness[bestcar] < class_test.best_fitness2 or class_test.fitness[bestcar2] < class_test.best_fitness2:
            total_fitness += class_test.best_fitness2
            fit_chance.append(total_fitness)
            weights.append(class_test.best_weights2.copy())
        total_fitness += class_test.best_fitness
        fit_chance.append(total_fitness)
        weights.append(class_test.best_weights.copy())
        
    else:
        class_test.best_fitness = class_test.fitness[bestcar]
        class_test.best_weights = class_test.brain[bestcar].model.get_weights().copy()
        f = open(filepath + "/models/besta" + str(int(class_test.fitness[bestcar])) + ".keras", "w+")
        f.write(str(class_test.best_weights))
        f.close()
        if class_test.fitness[bestcar2] > class_test.best_fitness2:
            class_test.best_fitness2 = class_test.fitness[bestcar2]
            class_test.best_weights2 = class_test.brain[bestcar2].model.get_weights().copy()

    for i in range(len(class_test.brain)):
        basew = class_test.brain[0].model.get_weights().copy()
        for weightl in range(len(basew)):
            for weight in range(len(basew[weightl])):
                rn = random.uniform(0, total_fitness)
                cn = 0
                for c in range(len(fit_chance)):
                    if rn > fit_chance[c]:
                        cn = c
                basew[weightl][weight] = weights[cn][weightl][weight]
        class_test.brain[i].model.set_weights(mutate_individual(basew))


    class_test.brain[len(class_test.brain) - 1] = car_nn()
    class_test.fitness[len(class_test.brain) - 1] = 0
    class_test.brain[0].model.set_weights(class_test.best_weights.copy())
    class_test.fitness[0] = class_test.best_fitness
    class_test.brain[1].model.set_weights(class_test.best_weights2.copy())
    class_test.fitness[1] = class_test.best_fitness2


def algo14():
    record(iter_char + "algo14")
    bestcar = 0
    bestcar2 = 1
    for i in range(len(class_test.brain)):
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            bestcar = i

    for i in range(len(class_test.brain)):
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            if bestcar2 != bestcar:
                bestcar = i

    best_weights = class_test.brain[bestcar].model.get_weights().copy()
    best_weights2 = class_test.brain[bestcar].model.get_weights().copy()
    if class_test.fitness[bestcar] > class_test.best_fitness:
        print("using best of current gen")
        class_test.best_fitness = class_test.fitness[bestcar]
        class_test.best_weights = best_weights
        if class_test.fitness[bestcar2] > class_test.best_fitness2:
            class_test.best_fitness2 = class_test.fitness[bestcar2]
            class_test.best_weights2 = best_weights2
        else:
            best_weights2 = class_test.best_weights2.copy()
    else:
        print("using previous gen")
        if len(class_test.best_weights) > 0:
            best_weights = class_test.best_weights.copy()
            best_weights2 = class_test.best_weights2.copy()


    for i in range(len(class_test.brain)//2):
        tomutate = best_weights.copy()
        tomutate2 = best_weights2.copy()
        crossed = crossover(tomutate, tomutate2)

        class_test.brain[i * 2].model.set_weights(mutate(crossed[0]))
        class_test.brain[i * 2 + 1].model.set_weights(mutate(crossed[1]))
        class_test.fitness[i * 2] = 0
        class_test.fitness[i * 2 + 1] = 0


    class_test.brain[len(class_test.brain) - 1] = car_nn()
    class_test.fitness[len(class_test.brain) - 1] = 0
    class_test.brain[0].model.set_weights(class_test.best_weights.copy())
    class_test.fitness[0] = class_test.best_fitness
    class_test.brain[1].model.set_weights(class_test.best_weights2.copy())
    class_test.fitness[1] = class_test.best_fitness2


def algo15():
    record(iter_char + "algo15")
    total_fitness = 0
    bestcar = 0
    bestcar2 = 1
    for i in range(len(class_test.brain)):
        total_fitness += class_test.fitness[i]
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            bestcar = i

    for i in range(len(class_test.brain)):
        if class_test.fitness[i] > class_test.fitness[bestcar]:
            if i != bestcar:
                bestcar2 = i


    if class_test.fitness[bestcar] > class_test.best_fitness:
        class_test.best_fitness = class_test.fitness[bestcar]
        class_test.best_weights = class_test.brain[bestcar].model.get_weights().copy()
        if class_test.fitness[bestcar2] > class_test.best_fitness2:
            class_test.best_fitness2 = class_test.fitness[bestcar2]
            class_test.best_weights2 = class_test.brain[bestcar2].model.get_weights().copy()

        f = open(filepath + "/models/best" + str(int(class_test.fitness[bestcar])) + ".w", "w+")
        f.write(str(class_test.best_weights))
        f.close()
    else:
        if class_test.fitness[bestcar] > class_test.best_fitness2:
            class_test.best_fitness2 = class_test.fitness[bestcar]
            class_test.best_weights2 = class_test.brain[bestcar].model.get_weights().copy()


    p1 = random.uniform(0, total_fitness)
    p2 = random.uniform(0, total_fitness)
    totalfit = 0
    parent1 = 0
    parent2 = 0
    for i in range(len(class_test.brain)):
        totalfit += class_test.fitness[i]
        if p1 > totalfit:
            parent1 = i
        if p2 > totalfit:
            parent2 = i

    best_weights = class_test.brain[parent1].model.get_weights().copy()
    best_weights2 = class_test.brain[parent2].model.get_weights().copy()

    for i in range(len(class_test.brain)//2):
        tomutate = best_weights.copy()
        tomutate2 = best_weights2.copy()
        crossed = crossover_random(tomutate, tomutate2)

        class_test.brain[i * 2].model.set_weights(mutate(crossed[0]))
        class_test.brain[i * 2 + 1].model.set_weights(mutate(crossed[1]))
        class_test.fitness[i * 2] = 0
        class_test.fitness[i * 2 + 1] = 0

    class_test.brain[len(class_test.brain) - 1] = car_nn()
    class_test.fitness[len(class_test.brain) - 1] = 0
    class_test.brain[0].model.set_weights(class_test.best_weights.copy())
    class_test.fitness[0] = class_test.best_fitness
    class_test.brain[1].model.set_weights(class_test.best_weights2.copy())
    class_test.fitness[1] = class_test.best_fitness2


algo15()