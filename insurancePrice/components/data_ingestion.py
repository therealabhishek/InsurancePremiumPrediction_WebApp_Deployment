import sys
import os
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from typing import Tuple
from insurancePrice.logger import logging
from insurancePrice.exception import InsuranceException
from insurancePrice.configuration.mongo_operations import MongoDBOperation
from insurancePrice.entity.config_entity import DataIngestionConfig
from insurancePrice.entity.artifact_entity import DataIngestionArtifact
from insurancePrice.constants import TEST_SIZE



class DataIngestion:
    def __init__(self,
                 data_ingestion_config: DataIngestionConfig,
                 mongo_op: MongoDBOperation):
        
        self.data_ingestion_config = data_ingestion_config
        self.mongo_op = mongo_op
        
    # This method will fetch data from mongodb
    def get_data_from_mongodb(self) -> DataFrame:
        """
        Method Name :   get_data_from_mongodb

        Description :   This method fetches data from MongoDB database. 
        
        Output      :   DataFrame
        
        """
        logging.info("Entered get_data_from_mongodb method of Data Ingestion class.")
        try:
            logging.info("Getting dataframe from mongodb")

            # Getting collection from mongodb database
            df = self.mongo_op.get_collection_as_dataframe(
                self.data_ingestion_config.DB_NAME,
                self.data_ingestion_config.COLLECTION_NAME
            )
            logging.info("Got dataframe from mongodb.")
            logging.info("Exited get_data_from_mongodb method of DataIngestion class.")
            return df
        except Exception as e:
            raise InsuranceException(e, sys) from e
        

    # This method will split the data into train and test sets:
    def split_data_as_train_test(self, df : DataFrame) -> Tuple[DataFrame, DataFrame]:

        """
        Method Name :  split_data_as_train_test

        Description :  This method splits the dataframe into train set and test set based on split ratio.
        
        Output      :  Train DataFrame and Test DataFrame 
        """
        logging.info("Entered split_data_as_train_test method of Data_Ingestion class.")

        try:
            # Creating data_ingestion artifacts dir:
            os.makedirs(self.data_ingestion_config.DATA_INGESTION_ARTIFACTS_DIR, exist_ok= True)

            # Splitting data into train and test:
            train_set, test_set = train_test_split(df, test_size=TEST_SIZE)
            logging.info("Performed train test split on the dataframe.")

            # Creating dir to store train data under data_ingestion_artifact dir:
            os.makedirs(self.data_ingestion_config.TRAIN_DATA_ARTIFACT_FILE_DIR, exist_ok=True)
            logging.info("Created train data directory.")

            # Creating dir to store test data under data_ingestion_artifact dir:
            os.makedirs(self.data_ingestion_config.TEST_DATA_ARTIFACT_FILE_DIR, exist_ok=True)
            logging.info("Created test data directory.")

            # Saving train data to train dir:
            train_set.to_csv(self.data_ingestion_config.TRAIN_DATA_FILE_PATH, index = False, header = True)

            # Saving test data to test dir:
            test_set.to_csv(self.data_ingestion_config.TEST_DATA_FILE_PATH, index = False, header = True)

            logging.info("Converted Train and Test Dataframe to csv")
            logging.info("Saved train and test files in Data Ingestion Artifacts dir.")

            return train_set, test_set
        
        except Exception as e:
            raise InsuranceException(e,sys) from e
        

    # This method initiates data ingestion:
    def initiate_data_ingestion(self) -> DataIngestionArtifact:
        """
        Method Name :   initiate_data_ingestion

        Description :   This method initiates data ingestion.
        
        Output      :   Data ingestion artifact
        """
        try:
            #Getting data from mongodb:
            df = self.get_data_from_mongodb()

            #Dropping na:
            df = df.dropna()
            logging.info("Got Data from mongodb.")

            #Splitting data into train and test:
            self.split_data_as_train_test(df)
            logging.info("Exited initiate_data_ingestion method of Data_ingestion class.")

            # saving the data ingestion artifacts:
            data_ingestion_artifacts = DataIngestionArtifact(
                train_data_file_path=self.data_ingestion_config.TRAIN_DATA_FILE_PATH,
                test_data_file_path=self.data_ingestion_config.TEST_DATA_FILE_PATH
            )
            
            return data_ingestion_artifacts


        except Exception as e:
            raise InsuranceException(e,sys) from e