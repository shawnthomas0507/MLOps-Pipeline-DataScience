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


load_dotenv()


MONGO_DB_URL=os.getenv("MONGO_DB_URL")
ca=certifi.where()



class NetworkDataExtract():
    def __init__(self):
        try:
            pass 
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    


    def csv_to_json(self,file_path):
        try:
            data=pd.read_csv(file_path) 
            data.reset_index(drop=True,inplace=True)
            data = pd.read_csv(file_path)
            records = data.to_dict(orient='records')
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    

    def insert_data_tomongo(self,records,database,collection):

        try:
            self.database=database
            self.collection=collection
            self.records=records
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            self.database=self.mongo_client[self.database]
            self.collection=self.database[self.collection]
            self.collection.insert_many(self.records)
            print(self.collection.count_documents({}))

            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        


if __name__=="__main__":
    FILE_PATH="Network_Data\Phishing_Legitimate_full.csv"
    DATABASE="SHAWNDB"
    Collection="NetworkData"
    networkobj=NetworkDataExtract()
    records=networkobj.csv_to_json(file_path=FILE_PATH)
    print(records)
    num_of_records=networkobj.insert_data_tomongo(records,DATABASE,Collection)
    print(num_of_records)
