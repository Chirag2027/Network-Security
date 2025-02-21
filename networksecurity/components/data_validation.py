from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
from scipy.stats import ks_2samp            # To check whether there is a data drift or not
import pandas as pd 
import os, sys

# Read the schema from data_schema folder{schema.yaml}, and compare that schema with the data coming for training
# I am just checking the validity of data
from networksecurity.constant.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):

        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        



