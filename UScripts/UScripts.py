import unreal
import argparse
import shelve
from UClassTEst import *



parser = argparse.ArgumentParser(description='Test')
parser.add_argument('d1', type=float, help="Forward Vector")
parser.add_argument('d2', type=float, help="Forward-Right Vector")
parser.add_argument('d3', type=float, help="Forward-Left Vector")
parser.add_argument('d4', type=float, help="Right Vector")
parser.add_argument('d5', type=float, help="Left Vector")
parser.add_argument('speed', type=float, help="speed")
parser.add_argument('max_dist', type=float, help="Maximum distance a raycast can be.")
parser.add_argument('fitness', type=float, help="The fitness of the car")
parser.add_argument('carnum', type=float, help="Number of car")
args = parser.parse_args()

#setting up the values for nn input NOT NORMALIZED
speed = args.speed/3.6 # convert to m/s from km/h
d1 = args.d1/100 # convert to m from cm
d2 = args.d2/100 # convert to m from cm
d3 = args.d3/100 # convert to m from cm
d4 = args.d4/100 # convert to m from cm
d5 = args.d5/100 # convert to m from cm

#setting up the values for nn input NORMALIZED
#speed = args.speed/100 # max km/hr is around 90
#d1 = args.d1/args.max_dist # convert to percentage of max line trace distance
if args.d1 == 0:
    d1 = args.max_dist
#d2 = args.d2/args.max_dist # convert to percentage of max line trace distance
if args.d2 == 0:
    d2 = args.max_dist
#d3 = args.d3/args.max_dist # convert to percentage of max line trace distance
if args.d3 == 0:
    d3 = args.max_dist
#d4 = args.d4/args.max_dist # convert to percentage of max line trace distance
if args.d4 == 0:
    d4 = args.max_dist
#d5 = args.d5/args.max_dist # convert to percentage of max line trace distance
if args.d5 == 0:
    d5 = args.max_dist

out = class_test.brain[int(args.carnum)].predict(d1 = d1, d2 = d2, d3 = d3, d4 = d4, d5 = d5, speed = speed)[0]

print((out[0].item() - 0.5) * 2)
print((out[1].item() - 0.5) * 2)
print(class_test.actor[int(args.carnum)])
class_test.actor[int(args.carnum)].vehicle_movement.set_throttle_input((out[0].item() - 0.5) * 2)
class_test.actor[int(args.carnum)].vehicle_movement.set_steering_input((out[1].item() - 0.5) * 2)
#class_test.actor.vehicle_movement.set_handbrake_input(True)

