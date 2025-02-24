# Final Output After Data Transformation : .npy files and .pkl files
import os
import sys
import pandas as pd 
import numpy as np
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN
from networksecurity.constant.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact, DataValidationArtifact
)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# for saving the .npy file and .pkl file
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact, 
    data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact: DataValidationArtifact = data_validation_artifact
            self.data_transformation_config: DataTransformationConfig = data_transformation_config

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Function for reading train & test data
    @staticmethod
    def read_data(file_path) -> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Function for knn imputer
    def get_data_transformer_object(cls) -> Pipeline:
        """
        It initialises a KNNImputer object with the parameters specified in the training_pipeline.py file
        and returns a Pipeline object with the KNNImputer object as the first step.

        Args:
          cls: DataTransformation

        Returns:
          A Pipeline object
        """

        logging.info("Entered get_data_transformer_object method of DataTransformation class")
        try:
            imputer: KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info(f"Initialize KNNImputer with {DATA_TRANSFORMATION_IMPUTER_PARAMS}")

            # Creating a pipeline with the KNNImputer object as the first step  
            processor:Pipeline = Pipeline([("imputer", imputer)])
            return processor

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Initiate data transformation
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Entered initiate_data_transformation method of DataTransformation class")

        try:
            logging.info("Starting data transformation")
            # Read train & test data
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)

            # removing target col. 
            # training df
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)   # I/P
            target_feature_train_df = train_df[TARGET_COLUMN]                         # D/P
            target_feature_train_df = target_feature_train_df.replace(-1, 0)

            # testing df
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)   # I/P
            target_feature_test_df = test_df[TARGET_COLUMN]                         # D/P
            target_feature_test_df = target_feature_test_df.replace(-1, 0)

            # Implementing KNN Imputer for missing values
            preprocessor = self.get_data_transformer_object()
            # for train data
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)# array as O/P

            # for test data
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)  # array as O/P

            # combining transformed input features with target feature
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

            # saving numpy array & pkl file
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array=train_arr, )
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array=test_arr, )
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object, )

            # preparing our artifacts -> O/P which will be returned after Data Transformation stage
            data_transformation_artifact = DataTransformationArtifact(
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
            )

            return data_transformation_artifact




        except Exception as e:
            raise NetworkSecurityException(e, sys)
