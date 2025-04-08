import os 
import sys 
import numpy as np 
import pandas as pd 

TARGET_COLUMN="CLASS_LABEL"
PIPELINE_NAME: str="NetworkSecurity"
ARTIFACT_DIR: str="Artifacts"
FILE_NAME: str="NetworkData.csv"

TRAIN_FILE_NAME: str="train.csv"
TEST_FILE_NAME: str="test.csv"

DATA_INGESTION_COLLECTION_NAME: str="NetworkData"
DATA_INGESTION_DATABASE_NAME: str="SHAWNDB"
DATA_INGESTION_DIR_NAME: str="data_ingestion"
DATA_INGESTION_FEATURE_STORE_DIR: str="feature_store"
DATA_INGESTION_INGESTED_DIR: str="ingested"
DATA_INGESTED_TRAIN_TEST_SPLIT_RATIO: float= 0.2




DATA_VALIDATION_DIR_NAME: str="data validation"
DATA_VALIDATION_VALID_DIR: str="validated"
DATA_VALIDATION_INVALID_DIR: str="invalid"
DATA_VALIDATION_DRIFT_REPORT_DIR:str="drift_report"
DATA_VALIDATION_DRIFT_REPORT_FILE_NAME: str="report.yaml"


SCHEMA_FILE_PATH=os.path.join("Network_Data","data_schema","schema.yaml")



DATA_TRANSFORMATION_DIR_NAME: str="data transformation"
PREPROCESSING_OBJECT_FILE_NAME: str="preprocessing.pkl"
PREPROCESSING_FOLDER:str="preprocessing"


DATA_TRANSFORMATION_IMPUTER_PARAMS: dict={
    "missing_values":np.nan,
    "n_neighbors": 3,
    "weights": "uniform"
}





MODEL_TRAINER_DIR_NAME="model_trainer"
MODEL_TRAINER_MODEL_DIR="trained_model"
MODEL_FILE_NAME="model.pkl"
MODEL_TRAINER_EXPECTED_SCORE=0.6
MODEL_TRAIANER_OVER_UNDER_THRESHOLD=0.05



SAVED_MODEL_DIR=os.path.join("saved_models")
