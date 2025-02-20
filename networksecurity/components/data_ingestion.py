from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Call the config file for data ingestion config
from networksecurity.entity.config_entity import DataIngestionConfig
import os
import sys 
import pymongo
import pandas as pd 
import numpy as np 
from typing import List
from sklearn.model_selection import train_test_split

# To get the Output Data Ingestion Artifact(train_path, test_path) after Data Ingestion Componet
from networksecurity.entity.artifact_entity import DataIngestionArtifact

# Read data from MongoDB 
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

# Start reading data from MONGO_DB_URL
class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try:
            # Initialize the entire data ingestion config from DataIngestionConfig class
            self.data_ingestion_config = data_ingestion_config

        except Exception as e: 
            raise NetworkSecurityException(e, sys)

    # exporting the data as a DF from mongodb collection, and Reading it also
    # This function connects to MongoDB, retrieves data from a collection, and converts it into a Pandas DataFrame.
    def export_collection_as_dataframe(self):
        try:
            database_name = self.data_ingestion_config.database_name 
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, serverSelectionTimeoutMS=60000)
            collection = self.mongo_client[database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            # Whenever we read any data from mongodb, by default a column is added there ->> _id
            if "_id" in df.columns.to_list():
                df = df.drop(columns=["_id"], axis=1)

            df.replace({"na": np.nan}, inplace=True)

            return df

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Store the Data in feature_store_file_path {raw data ko as csv store krna}
    def export_data_into_feature_store(self, dataframe:pd.DataFrame):
        try:
            # Export the data into feature store
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # creating the folder
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)
            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Split the Data
    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        try:
            # Split the data into training and testing sets
            train_set, test_set, = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio)

            logging.info("Performed train test split on DF")

            logging.info("Exited split_data_as_train_test method of DataIngestion class")

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)

            logging.info("Exporting train & test file path")

            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)

            logging.info("Exported train & test file path")

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Initiating data ingestion
    def initiate_data_ingestion(self):
        try:
            # Get the DataFrame
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)

            # Get the O/P after Data Ingestion component as train_path, test_path
            dataingestionartifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path, test_file_path=self.data_ingestion_config.testing_file_path)
            return dataingestionartifact   # Final O/P of Data Ingestion component

        except Exception as e:
            raise NetworkSecurityException(e, sys)

