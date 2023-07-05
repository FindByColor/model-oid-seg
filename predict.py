#!/usr/bin/python

import argparse
import enum
import os
import pathlib
import torch

from datetime import datetime
from ultralytics import YOLO
from src.utils import range_confidence


class ModelSizes(str, enum.Enum):
    nano = "nano"
    small = "small"
    medium = "medium"
    large = "large"
    extralarge = "extralarge"


def main(arg):
    # Make sure image exists before processing
    if not os.path.exists(arg["image"].resolve()):
        return print("❌ Unable to locate file: {}".format(arg["image"].resolve()))

    # Create Timer
    start_time = datetime.now()
    print("› Starting Prediction: {}".format(start_time.strftime("%Y-%m-%d %H:%M:%S")))

    # Fetch code size from args
    code = arg["size"][0]

    # Fix code used for naming
    if code == "e":
        code = "x"

    if torch.cuda.is_available():
        device = "0"
    else:
        device = "cpu"

    # Load the last model from previous training session
    model = YOLO("fbc-ml-models/fbc-seg-{}/weights/last.pt".format(code))

    with open(
        "fbc-ml-models/fbc-seg-{}/results.csv".format(code),
        "r",
        encoding="utf-8",
        errors="ignore",
    ) as scraped:
        final_line = scraped.readlines()[-1]
        last_epoch = int(final_line.split(",")[0]) + 1

    # Define Args for both YOLO and ClearML
    args = dict(
        device=device,
        exist_ok=True,
        imgsz=640,
        name="fbc-seg-{}-e{}".format(code, last_epoch),
        project="predictions",
        verbose=True,
        save=True,
        save_txt=True,  # Save masks as .txt file
        save_conf=True,  # save results with confidence scores
        save_crop=True,  # save cropped images with results
        retina_masks=True,
        conf=arg["confidence"],
    )

    # Perform object detection on an image using the newly trained model
    model.predict(arg["image"].resolve(), **args)

    # Output Run Time
    end_time = datetime.now()
    time_elapsed = end_time - start_time
    print("› Completed: {}".format(end_time.strftime("%Y-%m-%d %H:%M:%S")))
    print("› Total Time: {}".format(time_elapsed))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run YOLOv8 Model Predictions",
        epilog="Find By Color - OID Segmentation Model",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("size", type=ModelSizes)
    parser.add_argument(
        "-i",
        "--image",
        type=pathlib.Path,
        metavar="\b",
        default="samples",
        help="Absolute Image Path",
    )
    parser.add_argument(
        "-c",
        "--confidence",
        type=range_confidence(0, 1),
        metavar="\b",
        default=0.01,
        help="Prediction Confidence [0-1]",
    )

    try:
        main(vars(parser.parse_args()))
    except KeyboardInterrupt:
        print("Exited Application")
        exit(0)
