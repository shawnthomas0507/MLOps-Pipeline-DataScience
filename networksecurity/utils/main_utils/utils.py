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
