import numpy as np
import argparse
import math
from UClassTEst import *


parser = argparse.ArgumentParser(description='Test')
parser.add_argument('d1', type=float, help="Forward Vector")
parser.add_argument('d2', type=float, help="Forward-Right Vector")
parser.add_argument('d3', type=float, help="Forward-Left Vector")
parser.add_argument('d4', type=float, help="Right Vector")
parser.add_argument('d5', type=float, help="Left Vector")
parser.add_argument('speed', type=float, help="speed")
parser.add_argument('reward', type=float, help="reward")
parser.add_argument('fitness', type=float, help="reward")

args = parser.parse_args()


epsilon = 0.8 # percentage of time that a random action is not taken
discount_factor = 0.9
learning_rate = 0.9

STATES = 5
actions = ['t_up', 't_down', 's_right', 's_left']
increment = 0.1

def get_action(v1, v2, v3, v4, v5, speed, epsilon):
    if np.random.random() < epsilon:
        return np.argmax(q_learn.q_values[v1, v2, v3, v4, v5, speed])
    else:
        return np.random.randint(len(actions))

def do_action(action_index):
    if actions[action_index] == 't_up' and q_learn.current_throttle < 1.0:
        q_learn.current_throttle += increment
    elif actions[action_index] == 't_down' and q_learn.current_throttle > -1.0:
        q_learn.current_throttle -= increment
    elif actions[action_index] == 's_right' and q_learn.current_steering < 1.0:
        q_learn.current_steering += increment
    elif actions[action_index] == 's_left' and q_learn.current_steering > -1.0:
        q_learn.current_steering -= increment


state_inc = q_learn.max_dist/(STATES - 1)
vectors = []
speed_state = 0
action_index = 0

for i in range(5):
    vectors.append(0)

for i in range(STATES):
    if args.d1 >= ((i/2)** 2) * state_inc:
        vectors[0] = i
for i in range(STATES):
    if args.d2 >= ((i/2)** 2) * state_inc:
        vectors[1] = i
for i in range(STATES):
    if args.d3 >= ((i/2)** 2) * state_inc:
        vectors[2] = i
for i in range(STATES):
    if args.d4 >= ((i/2)** 2) * state_inc:
        vectors[3] = i
for i in range(STATES):
    if args.d5 >= ((i/2)** 2) * state_inc:
        vectors[4] = i
        
for i in range(STATES):
    if args.speed >= (i ** 1.35) * 10:
        speed_state = i

# giving reward for previous action
fit_diff = args.fitness - q_learn.last_fitness
q_learn.last_fitness = args.fitness
old_q = q_learn.q_values[int(q_learn.last_state[0]), int(q_learn.last_state[1]), int(q_learn.last_state[2]), int(q_learn.last_state[3]), int(q_learn.last_state[4]), int(q_learn.last_state[5]), q_learn.last_action]
temporal_diff = (args.reward + fit_diff + q_learn.current_throttle/200) + (discount_factor * np.max(q_learn.q_values[int(q_learn.last_state[0]), int(q_learn.last_state[1]), int(q_learn.last_state[2]), int(q_learn.last_state[3]), int(q_learn.last_state[4]), int(q_learn.last_state[5])])) - old_q
new_q = old_q + (learning_rate * temporal_diff)
q_learn.q_values[int(q_learn.last_state[0]), int(q_learn.last_state[1]), int(q_learn.last_state[2]), int(q_learn.last_state[3]), int(q_learn.last_state[4]), int(q_learn.last_state[5]), q_learn.last_action] = new_q

if args.reward <= -99.0: #this means the car crashed
    if q_learn.epoch % 5000 == 0:
        f = open("J:/Documents/UScripts/UScripts/UScripts/data/ql/gena/qv" + str(q_learn.epoch) + ".qv", "w+")
        f.write(str(q_learn.q_values))
        f.close()
    q_learn.epoch += 1

# doing next action
action_index = get_action(vectors[0], vectors[1], vectors[2], vectors[3], vectors[4], speed_state, epsilon)
do_action(action_index)
q_learn.last_state = [vectors[0], vectors[1], vectors[2], vectors[3], vectors[4], speed_state]
q_learn.last_action = action_index
q_learn.actor.vehicle_movement.set_throttle_input(q_learn.current_throttle)
q_learn.actor.vehicle_movement.set_steering_input(q_learn.current_steering)
q_learn.calls += 1



      