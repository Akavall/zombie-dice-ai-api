
import os

import lightgbm as lgb
import boto3

from dotenv import load_dotenv

load_dotenv() 

RUN_ENV = os.getenv("RUN_ENV")


def load_model():
    if RUN_ENV == "local":
        # Load the model from the local file system
        MODEL_PATH_LOCAL = os.getenv("MODEL_PATH_LOCAL")
        print(f"Loading model from local path: {MODEL_PATH_LOCAL}")
        booster = lgb.Booster(model_file=MODEL_PATH_LOCAL)
    elif RUN_ENV == "production":
        # Load the model from S3
        MODEL_PATH_S3 = os.getenv("MODEL_PATH_S3")
        PATH_TO_MODEL = os.getenv("PATH_TO_MODEL")
        print(f"Loading model from S3 path: {MODEL_PATH_S3}")
        s3 = boto3.client("s3")
        bucket_name, s3_key = parse_s3_path(MODEL_PATH_S3)
        s3.download_file(bucket_name, s3_key, PATH_TO_MODEL)
        booster = lgb.Booster(model_file=PATH_TO_MODEL)
    else:
        raise ValueError(f"Unknown RUN_ENV: {RUN_ENV}")
    return booster

def parse_s3_path(s3_path):
    if not s3_path.startswith("s3://"):
        raise ValueError("Invalid S3 path")
    path_parts = s3_path[5:].split("/", 1)
    return path_parts[0], path_parts[1]