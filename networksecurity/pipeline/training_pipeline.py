# In this pipeline, I'll initiate all the steps of the components folder. 
# I'll initiate data ingestion, validation, transformation, model trainer
# Code is similar to main.py 

import os, sys 
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.model_trainer import ModelTrainer

from networksecurity.entity.config_entity import(
    TrainingPipelineConfig, 
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig, 
    ModelTrainerConfig
)

from networksecurity.entity.artifact_entity import(
    DataIngestionArtifact,
    DataValidationArtifact,
    DataTransformationArtifact,
    ModelTrainerArtifact
)

# Now I want to run all the config files 
class TrainingPipeline:
    def __init__(self):
        self.training_pipeline_config = TrainingPipelineConfig()

    def start_data_ingestion(self):
        try:
            self.data_ingestion_config = DataIngestionConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Start Data Ingestion")

            data_ingestion = DataIngestion(self.data_ingestion_config)
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info(f"Data Ingestion completed and Artifact: {data_ingestion_artifact}")

            return data_ingestion_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_validation(self, data_ingestion_artifact:DataIngestionArtifact):
        try:
            data_validation_config = DataValidationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Start Data Validation")
            data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Data Validation completed")
            return data_validation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_data_transformation(self, data_validation_artifact:DataValidationArtifact):
        try:
            data_transformation_config = DataTransformationConfig(training_pipeline_config=self.training_pipeline_config)
            logging.info("Data Transformation Started")
            data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
            data_transformation_artifact = data_transformation.initiate_data_transformation()
            logging.info("Data Transformation completed")
            return data_transformation_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def start_model_trainer(self, data_transformation_artifact:DataTransformationArtifact) -> ModelTrainerArtifact:
        try:
            self.model_trainer_config: ModelTrainerConfig = ModelTrainerConfig(training_pipeline_config=self.training_pipeline_config)
            model_trainer = ModelTrainer(model_trainer_config=self.model_trainer_config, data_transformation_artifact=data_transformation_artifact)
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            logging.info("Model Trainer Artifact Created Successfully")
            return model_trainer_artifact
    
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    # Run One by One Sequentially
    def run_pipeline(self):
        try:
            data_ingestion_artifact = self.start_data_ingestion()
            
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            
            data_transformation_artifact = self.start_data_transformation(data_validation_artifact=data_validation_artifact)
            
            model_trainer_artifact = self.start_model_trainer(data_transformation_artifact=data_transformation_artifact)

            return model_trainer_artifact

        except Exception as e:
            raise NetworkSecurityException(e, sys)
