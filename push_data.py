import os
import sys
import json

# To call all the environment variables
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

# The certifi library in Python provides a bundle of trusted CA certificates for verifying SSL/TLS connections. It is commonly used when making secure HTTPS requests, especially when working with requests, urllib3, or MongoDB connections.
import certifi
# The function certifi.where() returns the path to the CA (Certificate Authority) bundle that certifi provides. This bundle is used to verify SSL/TLS certificates when making secure connections. It ensures that your program uses a trusted, up-to-date CA bundle, preventing SSL errors when connecting to secure servers.
ca = certifi.where()

import pandas as pd 
import numpy as np
import pymongo
from pymongo import MongoClient
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException

# ETL Pipeline
class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Read all the data and convert it into json file
    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            # Dropping the index column
            data.reset_index(drop=True, inplace=True)
            # Convert the data into json format, List of json array
            records = list(json.loads(data.T.to_json()).values())
            return records

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Load Data into MongoDB
    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database
            self.collection = collection
            self.records = records
            # mongo_client to connect to mongodb, pymongo is the library used to connect to mongodb
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)

            # Assign to the mongo_client, that what DB we are using
            self.database = self.mongo_client[self.database]
            # Assign to the database, that what collection we are using
            self.collection = self.database[self.collection]
            # To insert
            self.collection.insert_many(self.records)

            return(len(self.records))

        except Exception as e:
            raise NetworkSecurityException(e, sys)

if __name__ == "__main__":
    FILE_PATH = "Network_Data\phisingData.csv"
    DATABASE = "CHIRAGAI"
    COLLECTION = "NetworkData"

    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records = networkobj.insert_data_mongodb(records, DATABASE, COLLECTION)
    print(no_of_records)
    