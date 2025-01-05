import os
from collections import Counter
import random as rn
import numpy as np
import pandas as pd
import lightgbm

# import torch

from zombie_dice import Player, init_game_state, init_player_state
from monte_carlo import reformat_game_state_a, reformat_game_state_b


class RandomAI:

    def should_continue(self, player=None, game_state=None):
        return rn.choice([False, True])


class Greedy:

    def __init__(self, n_max_shots):
        self.n_max_shots = n_max_shots

    def should_continue(self, player=None, game_state=None):
        if player.player_state.times_shot >= self.n_max_shots:
            return False
        else:
            return True


# Current Shotguns Rule
# 0 Always keep rolling.
# 1
# If we must roll 3 red dice, stop at 1 brain.
# If (rf = 2 and yf = 1) or yc > gc, stop at 2 brains.
# If (rf = 2 and gf = 1) or gc > yc, stop at 3 brains.
# If we must roll 3 green dice, roll again.
# If gf = 2, roll again.
# 2
# With gf = 3, stop at 2 brains.
# Otherwise, stop at 1 brain

class Cook_Taylor_Model:

    def should_continue(self, player=None, game_state=None):

        dice_names = Counter(d.name for d in game_state.zombie_deck.dice)

        walks = {"red": player.player_state.red_walks,
                 "yellow": player.player_state.yellow_walks,
                 "green": player.player_state.green_walks,
                 }

        if player.player_state.times_shot == 0:
            return True
        
        elif player.player_state.times_shot == 1:

            if walks["red"] == 3:
                return player.player_state.current_score < 1
            elif (walks["red"] == sum(walks.values())) and (dice_names["red"] == len(dice_names.values())):
                return player.player_state.current_score < 1
            elif walks["red"] == 2 and walks["yellow"] == 1:
                return player.player_state.current_score < 2
            elif walks["red"] == 2 and walks["green"] == 1:
                return player.player_state.current_score < 3 
            elif walks["green"] >= 2:
                return True
            elif (walks["green"] == sum(walks.values())) and (dice_names["green"] == len(dice_names.values())):
                return True

            # Missing key cases :( 

        elif player.player_state.times_shot == 2:
            if walks["green"] == 3:
                return player.player_state.current_score < 2
            else:
                return player.player_state.current_score < 1


# class RL_Simple:

#     def __init__(self, model_path):
#         self.model = load_model(model_path)

#     def should_continue(self, player=None, game_state=None):

#         state, _, _ = get_features(player, game_state)

#         prediction = self.model.predict(np.expand_dims(state, axis=0))

#         return np.argmax(prediction[0])

class MC_Model_A:

    def __init__(self, model):

        self.model = model

    def should_continue(self, player=None, game_state=None):

        features_not_move, feature_names = reformat_game_state_a(game_state, will_move=0)
        features_move, feature_names = reformat_game_state_a(game_state, will_move=1)

        df = pd.DataFrame(data=[features_not_move, features_move], columns=feature_names)

        prediction = self.model.predict(df)

        return int(prediction.argmax())


class MC_Model_B:

    def __init__(self, model):

        self.model = model 

    def load_model(self, model_path):
        self.model = lightgbm.Booster(model_file=model_path)

    def should_continue(self, player=None, game_state=None):

        features_not_move, feature_names = reformat_game_state_b(game_state, will_move=0)
        features_move, feature_names = reformat_game_state_b(game_state, will_move=1)

        df = pd.DataFrame(data=[features_not_move, features_move], columns=feature_names)

        prediction = self.model.predict(df)

        return int(prediction.argmin())