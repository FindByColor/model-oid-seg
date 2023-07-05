#!/usr/bin/python

import argparse
import enum
import os
import tensorboard
import torch

from clearml import Task
from datetime import datetime
from ultralytics import YOLO

# Set CUDA Allocation to 512MB
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"

# Increase Training Speed
os.environ["OMP_NUM_THREADS"] = "1"

# Run script from current working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))


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

    # Fetch code size from args
    code = arg["size"][0]

    # Fix code used for naming
    if code == "e":
        code = "x"

    # Create Task for ClearML
    task = Task.init(
        project_name="Find By Color",
        task_name="Segmentation Model",
        tags=["fbc-seg-{}".format(code)],
        continue_last_task=True,
        auto_connect_streams={"stdout": False, "stderr": False, "logging": False},
        auto_connect_frameworks={"pytorch": False, "matplotlib": False},
    )

    if torch.cuda.is_available():
        device = "0"
    else:
        device = "cpu"

    # Define Args for both YOLO and ClearML
    args = dict(
        batch=-1,
        cache="disk",
        data="config.yaml",
        device=device,
        epochs=10000,
        exist_ok=True,
        imgsz=1024,
        mask_ratio=1,
        name="fbc-seg-{}".format(code),
        patience=50,
        project="fbc-ml-models",
        resume=True,
        save_period=10,
        verbose=False,
        retina_masks=True,
        workers=16,
    )

    # Connect Args to YOLO
    task.connect(args)

    # Load the last model from previous training session
    model = YOLO("fbc-ml-models/fbc-seg-{}/weights/last.pt".format(code))

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
