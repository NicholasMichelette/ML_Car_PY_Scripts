from UClassTEst import *
import argparse
import unreal
import numpy as np

@unreal.uclass()
class GamePlay(unreal.GameplayStatics):
    pass



parser = argparse.ArgumentParser(description='Test2')
parser.add_argument('max_dist', type=float, help="Maximum distance for vector")
args = parser.parse_args()

q_learn.actor = GamePlay().get_all_actors_with_tag(unreal.EditorLevelLibrary.get_game_world(), 'learn')[0]
#                           one STATES per lines trace,             | speed      actions
q_learn.q_values = np.zeros((5, 5, 5, 5, 4))
q_learn.last_state = np.zeros(4)
q_learn.last_action = 0
q_learn.current_throttle = 0
q_learn.current_steering = 0
q_learn.max_dist = args.max_dist
q_learn.epoch = 0
q_learn.calls = 0
q_learn.last_fitness = 0
q_learn.state_list = []

