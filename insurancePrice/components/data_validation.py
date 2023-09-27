import json
import os,sys
import pandas as pd
from pandas import DataFrame
from evidently.model_profile import Profile
from evidently.model_profile.sections import DataDriftProfileSection
from typing import Tuple,Union
from insurancePrice.logger import logging
from insurancePrice.exception import InsuranceException
from insurancePrice.entity.config_entity import DataValidationConfig
from insurancePrice.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact


class DataValidation:
    def __init__(self,
                 data_ingestion_artifacts = DataIngestionArtifact,
                 data_validation_config = DataValidationConfig
                 ):
            self.data_ingestion_artifacts = data_ingestion_artifacts
            self.data_validation_config = data_validation_config


    # This method is used to validate schema columns
    def validate_schema_columns(self, df: DataFrame) -> bool:

        """
        Method Name :   validate_schema_columns

        Description :   This method validates schema columns of dataframe. 
        
        Output      :   True or False 
        """
        try:
            # Checking the len of dataframe columns and schema file columns
            if len(df.columns) == len(
                self.data_validation_config.SCHEMA_CONFIG["columns"]
            ):
                validation_status = True
            else:
                validation_status = False
            return validation_status
        
        except Exception as e:
             raise InsuranceException(e,sys) from e
        

    # this method is used to validate the numerical columns:
    def do_numerical_columns_exist(self, df:DataFrame) -> bool:
          
          """
          Method Name :   is_numerical_column_exists

          Description :   This method validates whether a numerical column exists in the dataframe or not. 
        
          Output      :   True or False 
          
          """
          try:

            # check the length of the dataframe columns and length of columns mentioned in schema file
            validation_status = False

                # checking numeircal schema columns with dataframe columns
            for column in self.data_validation_config.SCHEMA_CONFIG["numerical_columns"]:
                if column not in df.columns:
                    logging.info(f"{column} column is not present in the dataframe.")
                else:
                    validation_status = True
            return validation_status
          
          except Exception as e:
                raise InsuranceException(e,sys)
          

    def do_categorical_columns_exist(self, df:DataFrame) -> bool:
          
          """
          Method Name :   is_numerical_column_exists

          Description :   This method validates whether a numerical column exists in the dataframe or not. 
        
          Output      :   True or False 
          
          """
          try:

            # check the length of the dataframe columns and length of columns mentioned in schema file
            validation_status = False

                # checking numeircal schema columns with dataframe columns
            for column in self.data_validation_config.SCHEMA_CONFIG["categorical_columns"]:
                if column not in df.columns:
                    logging.info(f"{column} column is not present in the dataframe.")
                else:
                    validation_status = True
            return validation_status
          
          except Exception as e:
                raise InsuranceException(e,sys)
          
    

    def validate_dataset_schema_columns(self) -> Tuple[bool, bool]:
         
        """
        Method Name :   validate_dataset_schema_columns

        Description :   This method validates schema for train dataframe and test dataframe. 
        
        Output      :   True or False 
        """
        logging.info("Entered validate_dataset_schema_columns method of DataValidation class")
        try:
            logging.info("Validating dataset schema columns.")
              
            # validating schema columns for train dataset
            train_schema_status = self.validate_schema_columns(self.train_set)
            logging.info("Validated dataset schema columns on the train set.")

            # validating schema columns for test dataset
            test_schema_status = self.validate_schema_columns(self.test_set)
            logging.info("Validated dataset schema columns on the test set.")
            logging.info("Validated dataset schema columns.")
            return train_schema_status, test_schema_status
         
        except Exception as e:
              raise InsuranceException(e,sys)
        

    def validate_if_numerical_column_exists(self) -> Tuple[bool, bool]:

        """
        Method Name :   validate_is_numerical_column_exists

        Description :   This method validates whether numerical columns exists for train dataframe and test dataframe or not. 
        
        Output      :   True or False 
        """
        logging.info("Entered validate_dataset_schema_for_numerical_datatype method of Data_Validation class")
        try:
            logging.info("Validating dataset schema for numerical datatype")

            # Validating numerical columns with Train dataframe
            train_num_datatype_status = self.do_numerical_columns_exist(self.train_set)
            logging.info("Validated dataset schema for numerical datatype for train set")

            # Validating numerical columns with Test dataframe
            test_num_datatype_status = self.do_numerical_columns_exist(self.test_set)
            logging.info("Validated dataset schema for numerical datatype for test set")
            logging.info("Exited validate_dataset_schema_for_numerical_datatype method of Data_Validation class")
            return train_num_datatype_status, test_num_datatype_status

        except Exception as e:
            raise InsuranceException(e, sys)
        


    def validate_if_categorical_column_exists(self) -> Tuple[bool, bool]:

        """
        Method Name :   validate_is_categorical_column_exists

        Description :   This method validates whether categorical columns exists for train dataframe and test dataframe or not. 
        
        Output      :   True or False 
        """
        logging.info("Entered validate_dataset_schema_for_numerical_datatype method of Data_Validation class")
        try:
            logging.info("Validating dataset schema for numerical datatype")

            # Validating categorical columns with Train dataframe
            train_cat_datatype_status = self.do_categorical_columns_exist(self.train_set)
            logging.info("Validated dataset schema for numerical datatype for train set")

            # Validating categorical columns with Test dataframe
            test_cat_datatype_status = self.do_categorical_columns_exist(self.test_set)
            logging.info("Validated dataset schema for numerical datatype for test set")
            logging.info("Exited validate_dataset_schema_for_numerical_datatype method of Data_Validation class")
            return train_cat_datatype_status, test_cat_datatype_status

        except Exception as e:
            raise InsuranceException(e, sys)
        



    def detect_dataset_drift(self, reference: DataFrame, production: DataFrame, get_ratio: bool = False) -> Union[bool, float]:

        """
        Method Name :   detect_dataset_drift

        Description :   This method detects whether data drift is present or not. 
        
        Output      :   Report in json format and drift status True or False 
        """
        try:
            data_drift_profile = Profile(sections=[DataDriftProfileSection()])
            data_drift_profile.calculate(reference, production)

            # Getting data drift report in json format
            report = data_drift_profile.json()
            json_report = json.loads(report)

            # Saving the json report in artifacts directory
            data_drift_file_path = self.data_validation_config.DATA_DRIFT_FILE_PATH
            self.data_validation_config.UTILS.write_json_to_yaml_file(json_report, data_drift_file_path)
            n_features = json_report["data_drift"]["data"]["metrics"]["n_features"]
            n_drifted_features = json_report["data_drift"]["data"]["metrics"]["n_drifted_features"]

            if get_ratio:
                return n_drifted_features / n_features  # Calculating the drift ratio
            else:
                return json_report["data_drift"]["data"]["metrics"]["dataset_drift"]

        except Exception as e:
            raise InsuranceException(e, sys) from e     



    def initiate_data_validation(self) -> DataValidationArtifact:

        """
        Method Name :   initiate_data_validation

        Description :   This method initiates data validation. 
        
        Output      :   Data validation artifacts 
        """
        logging.info("Entered initiate_data_validation method of Data_Validation class")
        try:

            # Reading the Train and Test data from Data Ingestion Artifacts folder
            self.train_set = pd.read_csv(self.data_ingestion_artifacts.train_data_file_path)
            self.test_set = pd.read_csv(self.data_ingestion_artifacts.test_data_file_path)
            logging.info("Initiated data validation for the dataset")

            # Creating the Data Validation Artifacts directory
            os.makedirs(self.data_validation_config.DATA_VALIDATION_ARTIFACTS_DIR, exist_ok=True)
            logging.info(f"Created Artifatcs directory for {os.path.basename(self.data_validation_config.DATA_VALIDATION_ARTIFACTS_DIR)}")

            # Checking the dataset drift
            drift = self.detect_dataset_drift(self.train_set, self.test_set)
            (schema_train_col_status,schema_test_col_status) = self.validate_dataset_schema_columns()

            logging.info(f"Schema train cols status is {schema_train_col_status} and schema test cols status is {schema_test_col_status}")
            logging.info("Validated dataset schema columns")

            (schema_train_cat_cols_status,schema_test_cat_cols_status) = self.validate_if_categorical_column_exists()
            logging.info(f"Schema train cat cols status is {schema_train_cat_cols_status} and schema test cat cols status is {schema_test_cat_cols_status}")
            logging.info("Validated dataset schema for catergorical datatype")
            
            (schema_train_num_cols_status,schema_test_num_cols_status,) = self.validate_if_numerical_column_exists()
            logging.info(f"Schema train numerical cols status is {schema_train_num_cols_status} and schema test numerical cols status is {schema_test_num_cols_status}")
            logging.info("Validated dataset schema for numerical datatype")

            # Checking dfist status, initially the status is None
            drift_status = None
            if (
                schema_train_cat_cols_status is True
                and schema_test_cat_cols_status is True
                and schema_train_num_cols_status is True
                and schema_test_num_cols_status is True
                and schema_train_col_status is True
                and schema_test_col_status is True
                and drift is False
            ):
                logging.info("Dataset schema validation completed")
                drift_status == True
            else:
                drift_status == False

            # Saving data validation artifacts
            data_validation_artifacts = DataValidationArtifact(
                data_drift_file_path=self.data_validation_config.DATA_DRIFT_FILE_PATH,
                validation_status=drift_status,
            )

            return data_validation_artifacts

        except Exception as e:
            raise InsuranceException(e, sys) from e   
        
