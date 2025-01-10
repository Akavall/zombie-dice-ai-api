
import random as rn
from copy import deepcopy
import time
from collections import Counter
import pandas as pd

from zombie_dice.zombie_dice import init_game_state, Player, init_player_state


def simulate_game(game_state, mc_model_a=None, mc_model_b=None, get_features_for_player="a"):

    player_a = game_state.players[0]
    player_b = game_state.players[1]

    # game_state = init_game_state(players, "my_game")

    game_and_player_states = []

    # if mc_model_a is not None:
    #     import ipdb
    #     ipdb.set_trace()

    while game_state.game_over is False:

        # time.sleep(3)

        if game_state.player_turn == 0: # 0 means player "a"
            player_a_to_move = True
        else:
            player_a_to_move = False

        while player_a_to_move:

            # player_a.player_state.is_dead = False
            # player_a.player_state.times_shot = 0

            # game_and_player_states.append(
            #     (deepcopy(game_state),
            #     deepcopy(player_a),
            #     deepcopy(player_b)))

            if mc_model_a is None:
                will_move = rn.randint(0, 1)
            else:
                will_move = mc_model_a.should_continue(player=None, game_state=game_state)

            if get_features_for_player == "a":
                game_and_player_states.append((deepcopy(game_state), will_move))

            if will_move == 1:

                # game_and_player_states.append((deepcopy(game_state), will_move))

                player_a.take_turn(game_state.zombie_deck) 

                # print(f"deck size: {len(game_state.zombie_deck.dices)}")
                if player_a.player_state.is_dead == True:
                    player_a_to_move = False
            else:
                player_a_to_move = False

        game_state.end_turn()

        player_a.player_state.reset()
        player_a_to_move = False

            # print(f"Player A score: {game_state.players[0].total_score}")
            # print(f"Player B score: {game_state.players[1].total_score}")
            
        player_b_to_move = True

        while player_b_to_move:

            # player_b.player_state.is_dead = False
            # player_b.player_state.times_shot = 0

            if mc_model_b is None:
                will_move = rn.randint(0, 1)
            else:
                will_move = mc_model_b.should_continue(player=None, game_state=game_state)

            if get_features_for_player == "b":

                game_and_player_states.append((deepcopy(game_state), will_move))

            if will_move == 1:

                player_b.take_turn(game_state.zombie_deck) 
                # print(f"deck size: {len(game_state.zombie_deck.dices)}")
                if player_b.player_state.is_dead == True:
                    player_b_to_move = False
            else:
                player_b_to_move = False

        game_state.end_turn()
        player_b.player_state.reset()
        player_b_to_move = False

        game_state.end_round()

        # print(f"Player A score: {game_state.players[0].total_score}")
        # print(f"Player B score: {game_state.players[1].total_score}")

        # print("round ended")

    return game_and_player_states, game_state.winner


def reformat_game_state_a(game_state, will_move):

    player_a = game_state.players[0]
    player_b = game_state.players[1]

    features = []
    features_names = []

    features.append(will_move)
    features_names.append("will_move")

    features.append(player_a.total_score)
    features_names.append("player_a_total_score")

    features.append(player_b.total_score)
    features_names.append("player_b_total_score")

    features.append(player_a.player_state.current_score)
    features_names.append("player_a_current_score")

    features.append(player_a.player_state.times_shot)
    features_names.append("player_a_times_shot")

    features.append(player_a.player_state.n_green_walks)
    features_names.append("player_a_n_green_walks")

    features.append(player_a.player_state.n_yellow_walks)
    features_names.append("player_a_n_yellow_walks")

    features.append(player_a.player_state.n_red_walks)
    features_names.append("player_a_n_red_walks")

    zombie_deck = game_state.zombie_deck

    dice_names = Counter(d.name for d in zombie_deck.dices)

    features.append(dice_names.get("green", 0))
    features_names.append("green_dice_left")

    features.append(dice_names.get("yellow", 0))
    features_names.append("yellow_dice_left")

    features.append(dice_names.get("red", 0))
    features_names.append("red_dice_left")

    return features, features_names


def reformat_game_state_b(game_state, will_move):

    player_a = game_state.players[0]
    player_b = game_state.players[1]

    features = []
    features_names = []

    features.append(will_move)
    features_names.append("will_move")

    features.append(player_a.total_score)
    features_names.append("player_a_total_score")

    features.append(player_b.total_score)
    features_names.append("player_b_total_score")

    features.append(player_b.player_state.current_score)
    features_names.append("player_b_current_score")

    features.append(player_b.player_state.times_shot)
    features_names.append("player_b_times_shot")

    features.append(player_b.player_state.n_green_walks)
    features_names.append("player_b_n_green_walks")

    features.append(player_b.player_state.n_yellow_walks)
    features_names.append("player_b_n_yellow_walks")

    features.append(player_b.player_state.n_red_walks)
    features_names.append("player_b_n_red_walks")

    zombie_deck = game_state.zombie_deck

    dice_names = Counter(d.name for d in zombie_deck.dices)

    features.append(dice_names.get("green", 0))
    features_names.append("green_dice_left")

    features.append(dice_names.get("yellow", 0))
    features_names.append("yellow_dice_left")

    features.append(dice_names.get("red", 0))
    features_names.append("red_dice_left")

    return features, features_names


def reformat_state_batch(game_states, get_features_for_player="a"):

    reformatted_states = [] 
    for game_state, will_move in game_states:
        if get_features_for_player == "a":
            reformatted_state, feature_names = reformat_game_state_a(game_state, will_move)
        elif get_features_for_player == "b":
            reformatted_state, feature_names = reformat_game_state_b(game_state, will_move)
        reformatted_states.append(reformatted_state)

    return reformatted_states, feature_names


def make_game_features(n_games, mc_model=None, get_features_for_player="a"):

    reformatted_states_list = []
    winners = []

    winner_mapper = {"a": 1, "b": -1}

    for i in range(n_games):

        # print(f"Working on Game: {i}")

        player_a = Player(init_player_state(), "a", False, 0)
        player_b = Player(init_player_state(), "b", False, 0)

        players = [player_a, player_b]

        game_state = init_game_state(players, "my_game")

        if get_features_for_player == "a":

            game_states_and_move, winner = simulate_game(game_state, mc_model, None, get_features_for_player)

        elif get_features_for_player == "b":

            game_states_and_move, winner = simulate_game(game_state, None, mc_model, get_features_for_player)
    

        reformatted_states, feature_names = reformat_state_batch(game_states_and_move, get_features_for_player)
        reformatted_states_list.extend(reformatted_states)
        winners.extend([winner_mapper[winner.id]] * len(game_states_and_move))

    df = pd.DataFrame(data=reformatted_states_list, columns=feature_names)
    df["target"] = winners

    return df


if __name__ == "__main__":

    # player_a = Player(init_player_state(), "a", False, 0)
    # player_b = Player(init_player_state(), "b", False, 0)

    # players = [player_a, player_b]

    # game_state = init_game_state(players, "my_game")

    # states, winner = simulate_game(game_state)

    # print(f"winner is: {winner.id}")

    N_GAMES=25000
    PLAYER="b"

    df = make_game_features(n_games=N_GAMES, mc_model=None, get_features_for_player=PLAYER)

    # df = X
    # df["target"] = y

    df.to_csv(f"./model/training_data/training_data_{PLAYER}_{N_GAMES}.csv", index=False)

    # Next step is to train a lot of X and y
    # save them and test the model