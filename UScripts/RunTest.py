import unreal
import tensorflow as tf
import argparse
from tensorflow import keras
from UClassTEst import *
from NeuralNet import *

@unreal.uclass()
class GamePlay(unreal.GameplayStatics):
    pass


parser = argparse.ArgumentParser(description='Test2')
parser.add_argument('carnum', type=float, help="Number of cars")
args = parser.parse_args()

tag = "learn" + str(int(args.carnum))

for actor in class_test.actors:
    if actor.actor_has_tag(tag):
        class_test.actor[int(args.carnum)] = actor
        class_test.brain[int(args.carnum)] = car_nn()
