#!/usr/bin/python

import argparse
import os
import pathlib

from datetime import datetime
from ultralytics import YOLO
from src.utils import range_confidence


def main(args):
    # Make sure image exists before processing
    if not os.path.exists(args["image"].resolve()):
        return print("❌ Unable to locate file: {}".format(args["image"].resolve()))

    # Create Timer
    start_time = datetime.now()
    print("› Starting Prediction: {}".format(start_time.strftime("%Y-%m-%d %H:%M:%S")))

    # Load the last model from previous training session
    model = YOLO(
        "runs/segment/train/weights/last.pt"
    )

    # Perform object detection on an image using the newly trained model
    model.predict(
        args["image"].resolve(), save=True, retina_masks=True, conf=args["confidence"]
    )

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
    parser.add_argument(
        "-i",
        "--image",
        type=pathlib.Path,
        metavar="\b",
        default="test-image.jpg",
        help="Absolute Image Path",
    )
    parser.add_argument(
        "-c",
        "--confidence",
        type=range_confidence(0, 1),
        metavar="\b",
        default=0.25,
        help="Prediction Confidence [0-1]",
    )

    try:
        main(vars(parser.parse_args()))
    except KeyboardInterrupt:
        print("Exited Application")
        exit(0)
