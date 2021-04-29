import matplotlib.pyplot as plt
import matplotlib.colors as clr
import random

datapath = "data/"

def one_algo():
    f = open(datapath + "halgo15avg.txt", "r")
    f2 = open(datapath + "halgo15best.txt", "r")
    l = f.read().split('\n')
    l.remove('')
    l2 = f2.read().split('\n')
    l2.remove('')
    generations = []

    for i in range (len(l)):
        generations.append(i)
        l[i] = float(l[i])
        l2[i] = float(l2[i])

    plt.plot(generations, l, "b--")
    plt.plot(generations, l2, "r")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.show()

    f.close()
    f2.close()


def all_algo(numalgos):
    generations = []
    avgs = []
    bests = []
    for i in range(numalgos):
        f = open(datapath + "algo" + str(i + 1) + "avg.txt", "r")
        f1 = open(datapath + "algo" + str(i + 1) + "best.txt", "r")

        l = f.read().split('\n')
        l.remove('')
        avgs.append(l)

        l2 = f1.read().split('\n')
        l2.remove('')
        bests.append(l2)

        f.close()
        f1.close()


    for i in range (len(avgs[0])):
        generations.append(i)
        for j in range(numalgos):
            avgs[j][i] = float(avgs[j][i])
            bests[j][i] = float(bests[j][i])
            
    for i in range(numalgos):
        r = random.random()
        g = random.random()
        b = random.random()
        color = (r, g, b)
        l = "algo" + str(i + 1)
        plt.plot(generations, avgs[i], "--", c=color, label=l + " avg")
        plt.plot(generations, bests[i], c=color, label=l + " best")

    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.legend(bbox_to_anchor =(1, 1), loc='upper left')
    plt.show()


def qv_algo():
    f = open(datapath + "qv3.txt", "r")
    l = f.read().split('\n')
    l.remove('')
    generations = []

    for i in range (len(l)):
        generations.append(i)
        l[i] = float(l[i])

    plt.plot(generations, l, "b--")
    plt.xlabel("Generation")
    plt.ylabel("Fitness")
    plt.show()

    f.close()
    f2.close()
#all_algo(12)
#qv_algo()
one_algo()

