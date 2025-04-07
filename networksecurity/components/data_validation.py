from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from scipy.stats import ks_2samp 
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
import pandas as pd 
import os 
import sys 
from networksecurity.utils.main_utils.utils import read_yaml,write_yaml

class DataValidation:
    def __init__(self,data_ingestion_artifact:DataIngestionArtifact,data_validation_config:DataValidationConfig):

        try:
            self.data_ingestion_artifact=data_ingestion_artifact
            self.data_validation_config=data_validation_config
            self.schema_config=read_yaml(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e,sys)

    def vaidate_num_columns(self,dataframe: pd.DataFrame)->bool:
        try:
            number_of_columns=len(self.schema_config['columns']) 
            if len(dataframe.columns)==number_of_columns:
                return True 
            return False 
        except Exception as e:
            raise NetworkSecurityException(e,sys) 
        
    def check_if_numerical(self,dataframe:pd.DataFrame):
        try:
            columns=self.schema_config['numerical_columns']
            for i in columns:
                if i not in dataframe.columns:
                    return False 
                return True
        except Exception as e:
            raise NetworkSecurityException(e,sys) 
        
    def detect_dataset_drift(self,base_df,current_df,threshold=0.05) -> bool:

        try:
            status=True
            report={}
            for column in base_df.columns:
                d1=base_df[column]
                d2=current_df[column]
                is_sample_dist=ks_2samp(d1,d2)
                if threshold<=is_sample_dist.pvalue:
                    is_found=False
                else:
                    is_found=True
                    status=False 
                report.update({column:{
                    "p_value":float(is_sample_dist.pvalue),
                    "drift_status":is_found
                }})
            
            drift_report_file_path=self.data_validation_config.drift_report_path
            dir_name=os.path.dirname(drift_report_file_path)
            os.makedirs(dir_name,exist_ok=True)
            write_yaml(file_path=drift_report_file_path,content=report)


        except Exception as e:
            raise NetworkSecurityException(e,sys) 

    
    
    def initiate_data_validation(self)->DataValidationArtifact:

        try:
            train_file_path=self.data_ingestion_artifact.trained_file_path
            test_file_path=self.data_ingestion_artifact.test_file_path


            trained_dataframe=pd.read_csv(train_file_path)
            test_dataframe=pd.read_csv(test_file_path)

            status=self.vaidate_num_columns(dataframe=trained_dataframe)
            if not status:
                error_messages=f"train df does not contain all columns"

            status=self.vaidate_num_columns(dataframe=test_dataframe)
            if not status:
                error_messages=f"test df does not contain all columns"
            
            status=self.check_if_numerical(dataframe=trained_dataframe)
            if not status:
                error_messages=f"train df does not contain all numerical columns"

            status=self.check_if_numerical(dataframe=test_dataframe)
            if not status:
                error_messages=f"test df does not contain all numerical columns"
            
            
            status=self.detect_dataset_drift(base_df=trained_dataframe,current_df=test_dataframe)

            dir_path=os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path,exist_ok=True)

            trained_dataframe.to_csv(self.data_validation_config.valid_train_file_path,index=False,header=True)

            trained_dataframe.to_csv(self.data_validation_config.valid_test_file_path,index=False,header=True)

            data_validation_artifact=DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_ingestion_artifact.trained_file_path,
                valid_test_file_path=self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_path
            )
            return data_validation_artifact





        except Exception as e:
            raise NetworkSecurityException(e,sys)

        





