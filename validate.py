#!/usr/bin/python

import argparse
import enum
import os

from datetime import datetime
from ultralytics import YOLO

# Set CUDA Allocation to 512MB
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"

# Run script from current working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

models = {
    "nano": "yolov8n-seg.pt",
    "small": "yolov8s-seg.pt",
    "medium": "yolov8m-seg.pt",
    "large": "yolov8l-seg.pt",
    "extralarge": "yolov8x-seg.pt",
}


class ModelSizes(str, enum.Enum):
    nano = "nano"
    small = "small"
    medium = "medium"
    large = "large"
    extralarge = "extralarge"


def main(arg):
    # Create Timer
    start_time = datetime.now()
    print("› Starting Validation: {}".format(start_time.strftime("%Y-%m-%d %H:%M:%S")))

    # Load the last model from previous training session
    model = YOLO("fbc-ml-models/fbc-seg-{}/weights/last.pt".format(arg["size"][0]))

    # Evaluate the model's performance on the validation set
    model.val()

    # Output Run Time
    end_time = datetime.now()
    time_elapsed = end_time - start_time
    print("› Completed: {}".format(end_time.strftime("%Y-%m-%d %H:%M:%S")))
    print("› Total Time: {}".format(time_elapsed))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Validate YOLOv8 Model",
        epilog="Find By Color - OID Segmentation Model",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("size", type=ModelSizes)

    try:
        main(vars(parser.parse_args()))
    except KeyboardInterrupt:
        print("Exited Application")
        exit(0)
