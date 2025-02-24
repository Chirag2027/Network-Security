# I will write all the generic code for my project
import yaml
import pandas as pd 
import os, sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import pickle
import numpy as np
# import dill

# Function to read yaml file
def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, "rb") as yaml_file:
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

# function to write the content in yaml file
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace:
            if os.path.exists(file_path):
                os.remove(file_path)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w") as file:
            yaml.dump(content, file)

    except Exception as e:
            raise NetworkSecurityException(e, sys)

# Functions for data transformation : to save the numpy array and to save the preprocessor object
def save_numpy_array_data(file_path: str, array: np.array):
    """
    Save numpy array data to file,
    file_path -> location of file to be saved
    array: np.array -> data to be saved
    """

    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, "wb") as file_obj:
            np.save(file_obj, array)

    except Exception as e:
        raise NetworkSecurityException(e, sys)

# Saving the pickle file 
def save_object(file_path: str, obj: object) -> None:
    try:
        logging.info("Entered into the save_object method of main.utils ")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "wb") as file_obj:
            pickle.dump(obj, file_obj)
        logging.info("Exited the save_object method of main.util")

    except Exception as e:
        raise NetworkSecurityException(e, sys)
