import sys
from insurancePrice.configuration.mongo_operations import MongoDBOperation
from insurancePrice.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact, DataTransformationArtifact, ModelTrainerArtifact

from insurancePrice.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig, ModelTrainerConfig

from insurancePrice.components.data_ingestion import DataIngestion
from insurancePrice.components.data_validation import DataValidation
from insurancePrice.components.data_transformation import DataTransformation
from insurancePrice.components.model_trainer import ModelTrainer
from insurancePrice.logger import logging
from insurancePrice.exception import InsuranceException



class TrainPipeline:
    def __init__(self) -> None:
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.data_transformation_config = DataTransformationConfig()
        self.model_trainer_config = ModelTrainerConfig()
        self.mongo_op = MongoDBOperation()

    # This method is used to start data ingestion
    def start_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entered start_data_ingestion method of Trainpipeline class.")
        try:
            logging.info("Getting data from mongodb")
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config,
                mongo_op=self.mongo_op
            )
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Exited the start_data_ingestion method of TrainPipeline class.")
            return data_ingestion_artifact
        except Exception as e:
            raise InsuranceException(e,sys) from e
        

    # This method is used to start the data validation
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        logging.info("Entered the start_data_validation method of TrainPipeline class.")
        try:
            data_validation = DataValidation(data_ingestion_artifacts=data_ingestion_artifact,
                                             data_validation_config=self.data_validation_config,
                                             )
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Performed the data validation operation.")
            logging.info("Exited the start_data_validation method of TrainPipeline class.")
            return data_validation_artifact
        except Exception as e:
            raise InsuranceException(e,sys)
        

    # This method is used to start data transformation
    def start_data_transformation(self, data_ingestion_artifact: DataIngestionArtifact)-> DataTransformationArtifact:
        logging.info("Entered the start_data_transformation method of Trainpipeline class.")
        try:
            data_transformation = DataTransformation(data_ingestion_artifacts=data_ingestion_artifact,
                                                     data_transformation_config=self.data_transformation_config)
            data_transformation_artifact = (
                data_transformation.initiate_data_transformation()
            )
            logging.info("Exited the start_data_transformation method of Trainpipeline class.")
            return data_transformation_artifact
        except Exception as e:
            raise InsuranceException(e,sys)
        

        # This method is used to start the model trainer
    def start_model_trainer(
        self, data_transformation_artifact: DataTransformationArtifact
    ) -> ModelTrainerArtifact:
        try:
            model_trainer = ModelTrainer(
                data_transformation_artifact=data_transformation_artifact,
                model_trainer_config=self.model_trainer_config,
            )
            model_trainer_artifact = model_trainer.initiate_model_trainer()
            return model_trainer_artifact

        except Exception as e:
            raise InsuranceException(e, sys) from e
        
        

    def run_pipeline(self) -> None:
        logging.info("Entered run_pipeline method of TrainPipeline class")

        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)
            data_transformation_artifact = self.start_data_transformation(data_ingestion_artifact=data_ingestion_artifact)
            model_trainer_artifact = self.start_model_trainer(
                data_transformation_artifact=data_transformation_artifact
            )

            logging.info("Exited run_pipeline method of TrainPipeline class")

        except Exception as e:
            raise InsuranceException(e, sys) from e

