from UClassTEst import *
import argparse
import unreal

@unreal.uclass()
class GamePlay(unreal.GameplayStatics):
    pass



parser = argparse.ArgumentParser(description='Test2')
parser.add_argument('numcars', type=float, help="Number of cars")
args = parser.parse_args()

class_test.actors = GamePlay().get_all_actors_with_tag(unreal.EditorLevelLibrary.get_game_world(), 'learn')
class_test.actor = [None] * int(args.numcars) 
class_test.brain = [None] * int(args.numcars)
class_test.fitness = [None] * int(args.numcars)
class_test.best_fitness = 0
class_test.best_fitness2 = 0
class_test.best_weights = []
class_test.best_weights2 = []