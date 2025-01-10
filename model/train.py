import os

from lightgbm import LGBMRegressor
import pandas as pd

from dotenv import load_dotenv

load_dotenv() 


if __name__ == "__main__":

    model = LGBMRegressor()

    TRAINING_DATA_PATH_LOCAL = os.getenv("TRAINING_DATA_PATH_LOCAL")

    df = pd.read_csv(TRAINING_DATA_PATH_LOCAL)

    y = df.pop("target")
    X = df

    model.fit(X, y)

    MODEL_PATH_LOCAL = os.getenv("MODEL_PATH_LOCAL")

    model.booster_.save_model(MODEL_PATH_LOCAL)
