import random
import numpy as np


l = []
for i in range(10):
    l.append(float(i))

print(l)
l.remove(l[0])
print(l[0])


l = np.array(l)
print(l)
l += 1.0
print(l)
