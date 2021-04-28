import argparse
import unreal
import threading
from UClassTEst import *


#parser = argparse.ArgumentParser(description='Test')
#parser.add_argument('d1', type=float, help="Forward Vector")
#parser.add_argument('d2', type=float, help="Forward-Right Vector")
#parser.add_argument('d3', type=float, help="Forward-Left Vector")
#parser.add_argument('d4', type=float, help="Right Vector")
#parser.add_argument('d5', type=float, help="Left Vector")
#parser.add_argument('speed', type=float, help="speed")
#parser.add_argument('carnum', type=float, help="Number of car")
parser = argparse.ArgumentParser(description='Test2')
parser.add_argument('max_dist', type=float, help="Maximum distance a raycast can be.")
parser.add_argument('vars', type=str, nargs="*")
args = parser.parse_args()
args = parser.parse_args()

def do_movement(carnum, d1, d2, d3, d4, d5, speed):
    out = class_test.brain[carnum].predict(d1 = d1, d2 = d2, d3 = d3, d4 = d4, d5 = d5, speed = speed)[0]
    class_test.actor[carnum].vehicle_movement.set_throttle_input((out[0].item() - 0.5) * 2)
    class_test.actor[carnum].vehicle_movement.set_steering_input((out[1].item() - 0.5) * 2)

processes = []
for a in args.vars:
    inputs = a.split(',')
    carnum = int(inputs[0])
    d1 = float(inputs[1])/100 # convert to m from cm
    d2 = float(inputs[2])/100 # convert to m from cm
    d3 = float(inputs[3])/100 # convert to m from cm
    d4 = float(inputs[4])/100 # convert to m from cm
    d5 = float(inputs[5])/100 # convert to m from cm
    speed = float(inputs[6])/3.6 # convert to m/s from km/h
    if d1 == 0:
        d1 = args.max_dist
    if d2 == 0:
        d2 = args.max_dist
    if d3 == 0:
        d3 = args.max_dist
    if d4 == 0:
        d4 = args.max_dist
    if d5 == 0:
        d5 = args.max_dist

    #class_test.brain[carnum].model.make_predict_function()
    #p = threading.Thread(target=do_movement, args=(carnum, d1, d2, d3, d4, d5, speed,))
    #processes.append(p)
    #p.start()
    out = class_test.brain[carnum].predict(d1 = d1, d2 = d2, d3 = d3, d4 = d4, d5 = d5, speed = speed)[0]
    #class_test.actor[carnum].vehicle_movement.set_throttle_input((out[0].item() - 0.5) * 2)
    class_test.actor[carnum].vehicle_movement.set_throttle_input((out[0].item()))
    class_test.actor[carnum].vehicle_movement.set_steering_input((out[1].item() - 0.5) * 2)
    if out[2].item() > 0.5:
        class_test.actor[carnum].vehicle_movement.set_handbrake_input(True)
    else:
        class_test.actor[carnum].vehicle_movement.set_handbrake_input(False)


for process in processes:
    process.join()

