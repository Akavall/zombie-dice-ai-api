from lightgbm import LGBMRegressor
import pandas as pd


if __name__ == "__main__":

    model = LGBMRegressor()

    df = pd.read_csv("./traing_data/training_data_b_10000.csv")

    y = df.pop("target")
    X = df

    model.fit(X, y)

    # model.save_model("model_1.lgb")

    model.booster_.save_model('./models/model_b_10000.txt')

    # sample_test = {'will_move': [1, 0],
    #                 'player_a_total_score': [6, 6],
    #                 'player_b_total_score': [6, 6],
    #                  'player_a_current_score': [5, 5],
    #                 'player_a_times_shot': [2, 2],
    #                 'player_a_n_green_walks': [0, 0],
    #                 'player_a_n_yellow_walks': [0, 0],
    #                 'player_a_n_red_walks': [0, 0],
    #                 'green_dice_left': [3, 3],
    #                 'yellow_dice_left': [3, 3],
    #                'red_dice_left': [2, 2]
    #                }
    
    # # test_df = pd.DataFrame(data=sample_test.values(), columns=sample_test.keys())
    # test_df = pd.DataFrame(sample_test)

    # result_if_move = model.predict(test_df)

    # print(f"result_if_move: {result_if_move}")
