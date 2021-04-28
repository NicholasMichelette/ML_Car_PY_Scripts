from UClassTEst import *
import argparse


parser = argparse.ArgumentParser(description='A collision has happened')
parser.add_argument('carnum', type=int, help="Number of cars")
parser.add_argument('fitness', type=float, help="Number of cars")
args = parser.parse_args()

class_test.fitness[args.carnum] = args.fitness