from dataclasses import dataclass

@dataclass
class DataIngestionArtifact:
    train_data_file_path: str
    test_data_file_path: str


@dataclass
class DataValidationArtifact:
    data_drift_file_path: str
    validation_status: bool


@dataclass
class DataTransformationArtifact:
    transformed_object_file_path: str
    transformed_train_file_path: str
    transformed_test_file_path: str


@dataclass
class ModelTrainerArtifact:
    trained_model_file_path: str


@dataclass
class ModelEvaluationArtifact:
    is_model_accepted: bool
    trained_model_path: str
    changed_accuracy: float


@dataclass
class ModelPusherArtifact:
    bucket_name: str
    s3_model_path: str