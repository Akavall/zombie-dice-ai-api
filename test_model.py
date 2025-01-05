import lightgbm
import pandas as pd 

if __name__ == "__main__":

    model = lightgbm.Booster(model_file='./models/model_7.txt')

    sample_test = {'will_move': [0, 1],
                    'player_a_total_score': [9, 9],
                    'player_b_total_score': [12, 12],
                     'player_a_current_score': [3, 3],
                    'player_a_times_shot': [1, 1],
                    'player_a_n_green_walks': [0, 0],
                    'player_a_n_yellow_walks': [0, 0],
                    'player_a_n_red_walks': [0, 0],
                    'green_dice_left': [3, 3],
                    'yellow_dice_left': [3, 3],
                   'red_dice_left': [2, 2]
                   }

    # test_df = pd.DataFrame(data=sample_test.values(), columns=sample_test.keys())
    test_df = pd.DataFrame(sample_test)

    result_if_move = model.predict(test_df)

    print(f"result_if_move: {result_if_move}")