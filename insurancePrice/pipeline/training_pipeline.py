import sys
from insurancePrice.configuration.mongo_operations import MongoDBOperation
from insurancePrice.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact

from insurancePrice.entity.config_entity import DataIngestionConfig, DataValidationConfig

from insurancePrice.components.data_ingestion import DataIngestion
from insurancePrice.components.data_validation import DataValidation
from insurancePrice.logger import logging
from insurancePrice.exception import InsuranceException



class TrainPipeline:
    def __init__(self) -> None:
        self.data_ingestion_config = DataIngestionConfig()
        self.data_validation_config = DataValidationConfig()
        self.mongo_op = MongoDBOperation()


    def start_data_ingestion(self) -> DataIngestionArtifact:
        logging.info("Entered start_data_ingestion method of Trainpipeline class.")
        try:
            logging.info("Getting data from mongodb")
            data_ingestion = DataIngestion(
                data_ingestion_config=self.data_ingestion_config,
                mongo_op=self.mongo_op
            )
            data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
            logging.info("Exited the start_data_ingestion method of TrainPipeline class")
            return data_ingestion_artifact
        except Exception as e:
            raise InsuranceException(e,sys) from e
        

         # This method is used to start the data validation
    def start_data_validation(self, data_ingestion_artifact: DataIngestionArtifact) -> DataValidationArtifact:
        logging.info("Entered the start_data_validation method of TrainPipeline class")
        try:
            data_validation = DataValidation(data_ingestion_artifacts=data_ingestion_artifact,
                                             data_validation_config=self.data_validation_config,
                                             )
            data_validation_artifact = data_validation.initiate_data_validation()
            logging.info("Performed the data validation operation")
            logging.info("Exited the start_data_validation method of TrainPipeline class")
            return data_validation_artifact
        except Exception as e:
            raise InsuranceException(e,sys)
        
        

    def run_pipeline(self) -> None:
        logging.info("Entered run_pipeline method of TrainPipeline class")

        try:
            data_ingestion_artifact = self.start_data_ingestion()
            data_validation_artifact = self.start_data_validation(data_ingestion_artifact=data_ingestion_artifact)

            logging.info("Exited run_pipeline method of TrainPipeline class")

        except Exception as e:
            raise InsuranceException(e, sys) from e

