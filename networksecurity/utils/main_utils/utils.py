# I will write all the generic code for my project
import yaml
import pandas as pd 
import os, sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import pickle
# import dill

# Function to read yaml file
def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

