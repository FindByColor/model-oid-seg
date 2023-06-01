#!/usr/bin/python

import argparse
import enum
import tensorboard
import torch

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

    if torch.cuda.is_available():
        device = "0"
    else:
        device = "cpu"

    # Get Model Size
    model_name = models[arg["size"]]

    # Load a pretrained YOLO model (recommended for training)
    model = YOLO(model_name)

    # Define Args for both YOLO and ClearML
    args = dict(
        data="config.yaml",
        device=device,
        epochs=1000,
        exist_ok=True,
        imgsz=640,
        name="fbc-seg-{}".format(arg["size"][0]),
        patience=50,
        project="fbc-ml-models",
        resume=False,
        save_period=10,
        verbose=True,
    )

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
