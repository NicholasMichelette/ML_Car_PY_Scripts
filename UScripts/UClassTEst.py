import unreal


@unreal.uclass()
class GamePlay(unreal.GameplayStatics):
    pass

class class_test:
    actor = None
    brain = None
    actors = None
    fitness = None
    best_fitness = None
    best_fitness2 = None
    best_weights = None
    best_weights2 = None


class q_learn:
    actor = None
    q_values = None
    curr_throt = None
    curr_steer = None
    last_state = None
    last_action = None
    max_dist = None
    epoch = None
    calls = None
    last_fitness = None

