import random
import numpy as np


l = []
for i in range(10):
    l.append(float(i))


l = np.array(l)
print(l)
l += 1.0
print(l)

def mutate(weights):
    print("IN MUTATE")
    new_weights = weights
    for l in range(len(new_weights)):
        print(new_weights[l])
        for w in range(len(new_weights[l])):
            if type(new_weights[l][w]) == list:
                for a in range(len(new_weights[l][w])):
                    if random.uniform(0, 1) > 1 - mutation_rate:
                        new_weights[l][w][a] += random.uniform(-mutation_change, mutation_change)
            else:
                if random.uniform(0, 1) > 1 - mutation_rate:
                        new_weights[l][w] += random.uniform(-mutation_change, mutation_change)
    return new_weights