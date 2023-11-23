import os
from insurancePrice.logger import logging
import sys
from pandas import DataFrame
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from insurancePrice.entity.config_entity import DataTransformationConfig
from insurancePrice.entity.artifact_entity import DataIngestionArtifact, DataTransformationArtifact
from insurancePrice.exception import InsuranceException

class DataTransformation:
    def __init__(
            self,
            data_ingestion_artifacts: DataIngestionArtifact,
            data_transformation_config: DataTransformationConfig):
        
        self.data_ingestion_artifacts = data_ingestion_artifacts
        self.data_transformation_config = data_transformation_config
        
        # reading train and test csv
        self.train_set = pd.read_csv(self.data_ingestion_artifacts.train_data_file_path)
        self.test_set = pd.read_csv(self.data_ingestion_artifacts.test_data_file_path)

    # this method is used to get the transformer object
    def get_data_transformer_object(self)->object:
        """
        Method Name :   get_data_transformer_object

        Description :   This method gives preprocessor object. 
        
        Output      :   Preprocessor Object.
        """
        logging.info("Entered the get_data_transformer_object method of Data Ingestion Class.")

        try:
            # Getting the required columns from the config file:
            numerical_columns = self.data_transformation_config.SCHEMA_CONFIG["numerical_columns"]
            onehot_columns = self.data_transformation_config.SCHEMA_CONFIG["categorical_columns"]
            logging.info("Got numerical and categorical columns from Schema Config.")

            # Creating transformer objects:
            numeric_transformer = StandardScaler()
            oh_transformer = OneHotEncoder(handle_unknown="ignore")
            logging.info("Initialized Standard Scaler and OneHotEncoder.")

            # Using the transformer objects in columns transformer
            preprocessor = ColumnTransformer(
                [
                    ("OneHotEncoder", oh_transformer, onehot_columns),
                    ("StandardScaler",numeric_transformer, numerical_columns)
                ]
            )

            logging.info("Created preprocessor object from ColumnTransformer")
            logging.info("Exited get_data_transformer_object method of Data Transformation class.")
            return preprocessor

        except Exception as e:
            raise InsuranceException(e,sys) from e
        

    
    # This method is used to initialize data transformation
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        """
        Method Name :   initiate_data_transformation

        Description :   This method initiates data transformation. 
        
        Output      :   Data Transformation Artifacts.
        """
        try:
            # creating directory for data transformation artifacts
            os.makedirs(self.data_transformation_config.DATA_TRANSFORMATION_ARTIFACTS_DIR, exist_ok=True)
            logging.info("Created Data Transformation artifacts directory")

            # Getting preprocessor object
            preprocessor = self.get_data_transformer_object()
            logging.info("Got the preprocessor object.")

            target_column_name = self.data_transformation_config.SCHEMA_CONFIG["target_column"]
            
            # Getting the input features and target feature of Training Dataset.
            input_feature_train_df = self.train_set.drop(columns=[target_column_name], axis=1)

            target_feature_train_df = self.train_set[target_column_name]
            logging.info("Got train features and target column.")

            # Getting the input features and target feature of Test Dataset.
            input_feature_test_df = self.test_set.drop(columns=[target_column_name], axis=1)

            target_feature_test_df = self.test_set[target_column_name]
            logging.info("Got test features and target column.")

            # Applying the preprocessor object on the train test datasets.
            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)
            logging.info("Used preprocessor object to fit and transform train and transform test features.")

            #Concatenating the input feature train array and the target feature of train array
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            logging.info("Created train array.")

            #Creating directory for transformed train dataset array and saving the dataset
            os.makedirs(self.data_transformation_config.TRANSFORMED_TRAIN_DATA_DIR, exist_ok=True)

            transformed_train_file = self.data_transformation_config.UTILS.save_numpy_array_data(
                self.data_transformation_config.TRANSFORMED_TRAIN_FILE_PATH, train_arr
            )

            logging.info("Saved train array to transformed train file path.")

            #Concatenating the input feature test array and the target feature of test array
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]
            logging.info("Created test array.")

            #Creating directory for transformed train dataset array and saving the dataset
            os.makedirs(self.data_transformation_config.TRANSFORMED_TEST_DATA_DIR, exist_ok=True)

            transformed_test_file = self.data_transformation_config.UTILS.save_numpy_array_data(
                self.data_transformation_config.TRANSFORMED_TEST_FILE_PATH, test_arr
            )

            logging.info("Saved test array to transformed test file path.")

            #saving preprocessor object to data transformation artifacts dir
            preprocessor_obj_file = self.data_transformation_config.UTILS.save_object(
                self.data_transformation_config.PREPROCESSOR_FILE_PATH, preprocessor
            )

            logging.info("Saved the preprocessor object in DataTransformation artifacts directory.")
            logging.info("Exited initiate_data_transformation method of Data_Transformation class")

            # saving data transformation artifacts:
            data_transformation_artifacts = DataTransformationArtifact(
                transformed_object_file_path=preprocessor_obj_file,
                transformed_train_file_path=transformed_train_file,
                transformed_test_file_path=transformed_test_file
            )

            return data_transformation_artifacts
        except Exception as e:
            raise InsuranceException(e,sys)
