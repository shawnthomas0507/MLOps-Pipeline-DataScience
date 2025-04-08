from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from scipy.stats import ks_2samp 
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
import pandas as pd 
import os 
import sys 
import yaml 
import numpy as np 
import pickle
import dill
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score


def read_yaml(file_path: str) -> dict:
    try:
        with open(file_path,"rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e,sys)


def write_yaml(file_path: str,content:object,replace:bool=False)-> None:

    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
        with open(file_path,'w') as file:
            yaml.dump(content,file)
    except Exception as e:
            raise NetworkSecurityException(e,sys) 



def save_numpy_array_data(file_path: str,array: np.array):
    try:
        dir_path=os.path.dirname(file_path)
        os.makedirs(dir_path,exist_ok=True)
        with open(file_path,"wb") as file_obj:
            np.save(file_obj,array)
    
    except Exception as e:
            raise NetworkSecurityException(e,sys) 





def save_object(file_path:str,obj:object) -> None:
     try:
          logging.info("entered save object")
          dir_path=os.path.dirname(file_path)
          os.makedirs(dir_path,exist_ok=True)
          with open(file_path,"wb") as file_obj:
               pickle.dump(obj,file_obj)
     
     except Exception as e:
            raise NetworkSecurityException(e,sys) 





def load_object(file_path: str)->object:
     try:
          if not os.path.exists(file_path):
               raise Exception("not there chief")
          with open(file_path,"rb") as file_obj:
               return pickle.load(file_obj)
          
     except Exception as e:
            raise NetworkSecurityException(e,sys) 
     


def load_numpy_array_data(file_path:str)->np.array:
     
     try:
          if not os.path.exists(file_path):
               raise Exception("not there chief")
          with open(file_path,"rb") as file_obj:
               return np.load(file_obj)
          
     except Exception as e:
            raise NetworkSecurityException(e,sys) 
     


def evaluate_models(X_train,y_train,X_test,y_test,models:dict,param:dict)-> dict:
    try:
        report={}
        for i in range(len(list(models))):
             model=list(models.values())[i]
             para=param[list(models.keys())[i]]

             gs=GridSearchCV(
                 estimator=model,
                 param_grid=para,
                 cv=3,
             )
             gs.fit(X_train,y_train)
             model.set_params(**gs.best_params_)
             model.fit(X_train,y_train)

             y_train_pred=model.predict(X_train)
             y_test_pred=model.predict(X_test)

             train_model_score=r2_score(y_train,y_train_pred)
             test_model_score=r2_score(y_test,y_test_pred)
             report[list(models.keys())[i]]=test_model_score
        return report
    except Exception as e:
        raise NetworkSecurityException(e,sys)