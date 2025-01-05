
import lightgbm
import pandas as pd 

if __name__ == "__main__":

    model = lightgbm.Booster(model_file='./models/model_b_10000.txt')

    sample_test = {'will_move': [0, 1],
                    'player_a_total_score': [9, 9],
                    'player_b_total_score': [9, 9],
                     'player_b_current_score': [1, 1],
                    'player_b_times_shot': [0, 0],
                    'player_b_n_green_walks': [2, 2],
                    'player_b_n_yellow_walks': [0, 0],
                    'player_b_n_red_walks': [0, 0],
                    'green_dice_left': [3, 3],
                    'yellow_dice_left': [3, 3],
                   'red_dice_left': [2, 2]
                   }

    # test_df = pd.DataFrame(data=sample_test.values(), columns=sample_test.keys())
    test_df = pd.DataFrame(sample_test)

    result_if_move = model.predict(test_df)

    print(f"result_if_move: {result_if_move}")