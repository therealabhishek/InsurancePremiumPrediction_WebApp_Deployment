from dataclasses import dataclass
from from_root import from_root
import os
#from insurancePrice.configuration.s3_operations import S3Operation
from insurancePrice.utils.main_utils import MainUtils
from insurancePrice.constants import *


@dataclass
class DataIngestionConfig:
    def __init__(self):
        self.UTILS = MainUtils()
        self.SCHEMA_CONFIG = self.UTILS.read_yaml_file(filename= SCHEMA_FILE_PATH)
        self.DB_NAME = DB_NAME
        self.COLLECTION_NAME = COLLECTION_NAME
        self.DATA_INGESTION_ARTIFACTS_DIR:str = os.path.join(from_root(), 
                                                             ARTIFACTS_DIR, 
                                                             DATA_INGESTION_ARTIFACTS_DIR)
        self.TRAIN_DATA_ARTIFACT_FILE_DIR:str = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR,
                                                             DATA_INGESTION_TRAIN_DIR)
        self.TEST_DATA_ARTIFACT_FILE_DIR:str = os.path.join(self.DATA_INGESTION_ARTIFACTS_DIR,
                                                            DATA_INGESTION_TEST_DIR)
        self.TRAIN_DATA_FILE_PATH:str = os.path.join(self.TRAIN_DATA_ARTIFACT_FILE_DIR,
                                                     DATA_INGESTION_TRAIN_FILE_NAME)
        self.TEST_DATA_FILE_PATH:str = os.path.join(self.TEST_DATA_ARTIFACT_FILE_DIR,
                                                    DATA_INGESTION_TEST_FILE_NAME)
        


@dataclass
class DataValidationConfig:
    def __init__(self):
        self.UTILS = MainUtils()
        self.SCHEMA_CONFIG = self.UTILS.read_yaml_file(filename= SCHEMA_FILE_PATH)
        self.DATA_INGESTION_ARTIFACTS_DIR:str = os.path.join(from_root(),
                                                             ARTIFACTS_DIR,
                                                             DATA_INGESTION_ARTIFACTS_DIR)
        self.DATA_VALIDATION_ARTIFACTS_DIR:str = os.path.join(from_root(),
                                                              ARTIFACTS_DIR,
                                                              DATA_VALIDATION_ARTRIFACTS_DIR)
        self.DATA_DRIFT_FILE_PATH:str = os.path.join(self.DATA_VALIDATION_ARTIFACTS_DIR,
                                                     DATA_DRIFT_FILE_NAME)