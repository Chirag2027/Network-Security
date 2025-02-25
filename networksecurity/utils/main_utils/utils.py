# I will write all the generic code for my project
import yaml
import pandas as pd 
import os, sys
from networksecurity.logging.logger import logging
from networksecurity.exception.exception import NetworkSecurityException
import pickle
import numpy as np
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import r2_score, accuracy_score
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

# Read/Load the pkl file
def load_object(file_path: str) -> object:
    try:
        if not os.path.exists(file_path):
            raise Exception(f"The file: {file_path} does not exists")
        with open (file_path, 'rb') as file_obj:
            print(file_obj)
            return pickle.load(file_obj)

        
    except Exception as e:
            raise NetworkSecurityException(e, sys)

# Function for : Load the numpy array
def load_numpy_array_data(file_path: str) -> np.array:
    """
    load numpy array data from file
    file_path: str location of file to load
    return: np.array data loaded
    """
    try:
        with open(file_path, "rb") as file_obj:
            return np.load(file_obj)
    except Exception as e:
        raise NetworkSecurityException(e, sys)

# Function for Model evaluation
def evaluate_models(x_train, y_train, x_test, y_test, models):
    try:
        report = {}

        # for i in range(len(list(models))):
        #     model = list(models.values())[i]
        #     para = param[model]

        for model_name, model in models.items():
            model.fit(x_train, y_train)  # Train the model

            y_train_pred = model.predict(x_train)
            y_test_pred = model.predict(x_test)

            train_model_score = accuracy_score(y_train, y_train_pred)  # Classification accuracy
            test_model_score = accuracy_score(y_test, y_test_pred)

            report[model_name] = test_model_score  # Store test accuracy in the report
        
        return report

    except Exception as e:
        raise NetworkSecurityException(e, sys)

