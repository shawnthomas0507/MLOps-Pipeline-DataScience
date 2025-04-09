import os 
import sys 
import json 
from dotenv import load_dotenv
import certifi
import pandas as pd 
import numpy as np 
import pymongo
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from flask import Flask
from networksecurity.pipeline.training_pipeline import TrainingPipeline

load_dotenv()


MONGO_DB_URL=os.getenv("MONGO_DB_URL")
ca=certifi.where()


app=Flask(__name__)



@app.route('/train')
def train():
    try:
        training_pipeline=TrainingPipeline()
        training_pipeline.run_pipeline()
        return "running"
    except Exception as e:
        raise NetworkSecurityException(e,sys)
    

if __name__=="__main__":
    app.run(host="0.0.0.0",port=8080,debug=True)






