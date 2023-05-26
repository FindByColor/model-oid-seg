#!/usr/bin/python

import argparse
import enum
import tensorboard

from clearml import Task
from datetime import datetime
from src.utils import flush_spacer
from ultralytics import YOLO

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
    print("› Started: {}".format(start_time.strftime("%Y-%m-%d %H:%M:%S")))

    # Create Task for ClearML
    task = Task.init(project_name="Find By Color", task_name="Segmentation Model")

    # Get Model Size
    model_name = models[arg["size"]]

    # Load a pretrained YOLO model (recommended for training)
    model = YOLO(model_name)

    # Define Args for both YOLO and ClearML
    args = dict(data="config.yaml", epochs=100, imgsz=640)

    # Connect Args to YOLO
    task.connect(args)

    # Train the model using the 'config.yaml' dataset for 100 epochs
    model.train(**args)

    # Close ClearML Task
    task.close()

    # Output Run Time
    end_time = datetime.now()
    time_elapsed = end_time - start_time
    print("› Completed: {}".format(end_time.strftime("%Y-%m-%d %H:%M:%S")))
    print("› Total Time: {}".format(time_elapsed))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run YOLOv8 Training on Model and Push Updates to ClearML",
        epilog="Find By Color - OID Segmentation Model",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("size", type=ModelSizes)

    try:
        main(vars(parser.parse_args()))
    except KeyboardInterrupt:
        print(flush_spacer(100), end="\r", flush=True)
        print("Exited Application")
        exit(0)
