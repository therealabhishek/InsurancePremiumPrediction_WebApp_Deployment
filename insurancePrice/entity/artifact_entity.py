from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_data_file_path: str
    test_data_file_path: str


@dataclass
class DataValidationArtifact:
    data_drift_file_path: str
    validation_status: bool