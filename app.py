from insurancePrice.logger import logging
import sys
from insurancePrice.exception import InsuranceException
from insurancePrice.pipeline.training_pipeline import TrainPipeline


if __name__ == '__main__':
    obj = TrainPipeline()
    obj.run_pipeline()