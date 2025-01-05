import os
from collections import Counter
import random as rn
import numpy as np
import pandas as pd
import lightgbm

# import torch

from zombie_dice import Player, init_game_state, init_player_state
from monte_carlo import reformat_game_state_a, reformat_game_state_b
from models import RandomAI, Greedy, MC_Model_A, MC_Model_B



# class RandomAI:

#     def should_continue(self, player=None, game_state=None):
#         return rn.choice([False, True])


# class Greedy:

#     def __init__(self, n_max_shots):
#         self.n_max_shots = n_max_shots

#     def should_continue(self, player=None, game_state=None):
#         if player.player_state.times_shot >= self.n_max_shots:
#             return False
#         else:
#             return True

# class RL_Simple:

#     def __init__(self, model_path):
#         self.model = load_model(model_path)

#     def should_continue(self, player=None, game_state=None):

#         state, _, _ = get_features(player, game_state)

#         prediction = self.model.predict(np.expand_dims(state, axis=0))

#         return np.argmax(prediction[0])

# class MC_Model_A:

#     def __init__(self, model_path):

#         self.model = lightgbm.Booster(model_file=model_path)

#     def should_continue(self, player=None, game_state=None):

#         features_not_move, feature_names = reformat_game_state_a(game_state, will_move=0)
#         features_move, feature_names = reformat_game_state_a(game_state, will_move=1)

#         df = pd.DataFrame(data=[features_not_move, features_move], columns=feature_names)

#         prediction = self.model.predict(df)

#         return prediction.argmax()


# class MC_Model_B:

#     def __init__(self, model_path):

#         self.model = lightgbm.Booster(model_file=model_path)

#     def should_continue(self, player=None, game_state=None):

#         features_not_move, feature_names = reformat_game_state_b(game_state, will_move=0)
#         features_move, feature_names = reformat_game_state_b(game_state, will_move=1)

#         df = pd.DataFrame(data=[features_not_move, features_move], columns=feature_names)

#         prediction = self.model.predict(df)

#         return prediction.argmin()


def one_match(ai_a, ai_b):

    player_a = Player(init_player_state(), "a", False, 0)
    player_b = Player(init_player_state(), "b", False, 0)
    game_state = init_game_state([player_a, player_b], "my_game")

    while game_state.game_over is False:

        while(ai_a.should_continue(player_a, game_state) and not player_a.player_state.is_dead):
            player_a.take_turn(game_state.zombie_deck)

        game_state.end_turn()
        player_a.player_state.reset()

        while(ai_b.should_continue(player_b, game_state) and not player_b.player_state.is_dead):
            player_b.take_turn(game_state.zombie_deck)

        game_state.end_turn()
        player_b.player_state.reset()

        game_state.end_round()

    return game_state.winner.id


if __name__ == "__main__":

    random_ai = RandomAI()
    greedy_ai_1 = Greedy(n_max_shots=1)
    greedy_ai_2 = Greedy(n_max_shots=2)

    # rl_simple_ai_a = RL_Simple("experimental_model.h5")
    # rl_simple_ai_b = RL_Simple("my_model_1000_4_layer_eps_06_4.h5")
    # rl_simple_ai_a = RL_Simple("experimental_model_method_0_model4.h5")

    
    # best model
    # rl_simple_ai_b = RL_Simple("new_best_model.h5")
    # rl_simple_ai_b = RL_Simple("exprimental_model_method_1_model_4.h5")

    # it looks like 1000 is slightly better than 5000

    model_a_inner = lightgbm.Booster(model_file='./models/model_8.txt')
    model_b_inner = lightgbm.Booster(model_file="./models/model_b_10000.txt")

    mc_model = MC_Model_A(model_a_inner)
    model_b = MC_Model_B(model_b_inner)

    n_matches = 1000

    match_result = [one_match(mc_model, model_b) for _ in range(n_matches)]
    print(f"Model A vs Model B: {Counter(match_result)}")

    # match_result = [one_match(random_ai, model_b) for _ in range(n_matches)]
    # print(f"MC Model vs Random: {Counter(match_result)}")


    # match_result = [one_match(mc_model, random_ai) for _ in range(n_matches)]
    # print(f"MC Model vs Random: {Counter(match_result)}")

    # match_result = [one_match(mc_model, greedy_ai_1) for _ in range(n_matches)]
    # print(f"MC Model vs Greedy (max 1 shot): {Counter(match_result)}")

    # match_result = [one_match(mc_model, greedy_ai_2) for _ in range(n_matches)]
    # print(f"MC Model vs Greedy (max 2 shots): {Counter(match_result)}")