#!/usr/bin/python

import argparse
import enum
import tensorboard
import torch

from clearml import Task
from datetime import datetime
from ultralytics import YOLO


class ModelSizes(str, enum.Enum):
    nano = "nano"
    small = "small"
    medium = "medium"
    large = "large"
    extralarge = "extralarge"


def main(arg):
    # Create Timer
    start_time = datetime.now()
    print("› Resuming: {}".format(start_time.strftime("%Y-%m-%d %H:%M:%S")))

    # Create Task for ClearML
    task = Task.init(
        project_name="Find By Color",
        task_name="Segmentation Model",
        continue_last_task=True,
    )

    if torch.cuda.is_available():
        device = "0"
    else:
        device = "cpu"

    # Define Args for both YOLO and ClearML
    args = dict(
        data="config.yaml",
        device=device,
        epochs=500,
        exist_ok=True,
        imgsz=640,
        name="fbc-seg-{}".format(arg["size"][0]),
        project="fbc-ml-models",
        resume=True,
        verbose=True,
    )

    # Connect Args to YOLO
    task.connect(args)

    # Load the last model from previous training session
    model = YOLO("fbc-ml-models/fbc-seg-{}/weights/last.pt".format(arg["size"][0]))

    # Restart training from last training point
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
        description="Resume YOLOv8 Training on Model and Push Updates to ClearML",
        epilog="Find By Color - OID Segmentation Model",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("size", type=ModelSizes)

    try:
        main(vars(parser.parse_args()))
    except KeyboardInterrupt:
        print("Exited Application")
        exit(0)
