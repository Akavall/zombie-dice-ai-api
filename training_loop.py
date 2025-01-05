
import pandas as pd
from lightgbm import LGBMRegressor
from collections import Counter

from matches import one_match
from monte_carlo import make_game_features
from models import Greedy, MC_Model_A, MC_Model_B

def training_loop():
    pass

N_MATCHES = 1000
N_GAMES = 500

if __name__ == "__main__":

    mc_model_a = None
    mc_model_b = None

    all_features_a = pd.DataFrame()
    all_features_b = pd.DataFrame()

    greedy_ai_2 = Greedy(n_max_shots=2)

    for i in range(50):

        print(f"working on iteration: {i}")

        features_a = make_game_features(N_GAMES, mc_model_a, get_features_for_player="a")

        all_features_a = pd.concat([all_features_a, features_a], axis=0)

        print(f"all_features_a.shape: {all_features_a.shape}")

        model_a = LGBMRegressor()

        df = all_features_a.copy()

        y = df.pop("target")
        X = df

        model_a.fit(X, y)
        mc_model_a = MC_Model_A(model_a)

        match_result = [one_match(mc_model_a, greedy_ai_2) for _ in range(N_MATCHES)]
        print(f"Model A vs Gready 2: {Counter(match_result)}")

        features_b = make_game_features(N_GAMES, mc_model_b, get_features_for_player="b")

        all_features_b = pd.concat([all_features_b, features_b], axis=0)
        print(f"all_features_b.shape: {all_features_b.shape}")

        model_b = LGBMRegressor()

        df = all_features_b.copy()

        y = df.pop("target")
        X = df

        model_b.fit(X, y)
        mc_model_b = MC_Model_B(model_b)

        match_result = [one_match(greedy_ai_2, mc_model_b) for _ in range(N_MATCHES)]
        print(f"Gready 2 vs Model B: {Counter(match_result)}")

