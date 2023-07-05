#!/usr/bin/python

import argparse
import enum
import os
import torch

from datetime import datetime
from ultralytics import YOLO

# Set CUDA Allocation to 512MB
os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:512"

# Run script from current working directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))


class ModelSizes(str, enum.Enum):
    nano = "nano"
    small = "small"
    medium = "medium"
    large = "large"
    extralarge = "extralarge"


debug = False
epoch = 0
last_epoch = 0
last_run = None


def main(arg):
    global epoch
    global last_epoch
    global last_run

    # Fetch code size from args
    code = arg["size"][0]

    # Fix code used for naming
    if code == "e":
        code = "x"

    # Make sure file exists
    if os.path.isfile("fbc-ml-models/fbc-seg-{}/results.csv".format(code)):
        with open(
            "fbc-ml-models/fbc-seg-{}/results.csv".format(code),
            "r",
            encoding="utf-8",
            errors="ignore",
        ) as scraped:
            final_line = scraped.readlines()[-1]
            epoch = int(final_line.split(",")[0]) + 1

            if epoch > last_epoch:
                last_epoch = epoch

                if epoch % 10 == 0:
                    current_time = datetime.now()

                    if last_run is not None and debug is True:
                        time_elapsed = current_time - last_run
                        last_run = current_time
                        print("› Next Run ETA: {}".format(time_elapsed))

                    if not os.path.exists(
                        "predictions/fbc-seg-{}-e{}".format(code, last_epoch)
                    ):
                        if debug is True:
                            print(
                                "› Generating Samples from Epoch #{} {}".format(
                                    epoch, current_time.strftime("%Y-%m-%d %H:%M:%S")
                                )
                            )
                        # Run Predictions
                        predict(vars(parser.parse_args()))


def predict(arg):
    global epoch

    # Create Timer
    if debug is True:
        start_time = datetime.now()
        print(
            "› Starting Predictions: {}".format(
                start_time.strftime("%Y-%m-%d %H:%M:%S")
            )
        )

    # Create Timer
    if torch.cuda.is_available():
        device = "0"
    else:
        device = "cpu"

    # Load the last model from previous training session
    model = YOLO("fbc-ml-models/fbc-seg-{}/weights/last.pt".format(code))

    # Define Args for both YOLO and ClearML
    args = dict(
        device=device,
        exist_ok=True,
        imgsz=640,
        name="fbc-seg-{}-e{}".format(code, last_epoch),
        project="predictions",
        verbose=True,
        save=True,
        save_txt=False,  # Save masks as .txt file
        save_conf=False,  # save results with confidence scores
        save_crop=False,  # save cropped images with results
        retina_masks=True,
        conf=0.01,
    )

    # Perform object detection on an image using the newly trained model
    model.predict("samples", **args)

    # Output Run Time
    if debug is True:
        end_time = datetime.now()
        time_elapsed = end_time - start_time
        print("\n› Completed: {}".format(end_time.strftime("%Y-%m-%d %H:%M:%S")))
        print("› Total Time: {}\n".format(time_elapsed))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run YOLOv8 Model Predictions",
        epilog="Find By Color - OID Segmentation Model",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("size", type=ModelSizes)

    try:
        if debug is True:
            start_time = datetime.now()
            print(
                "› Starting Test Sample Generation: {}".format(
                    start_time.strftime("%Y-%m-%d %H:%M:%S")
                )
            )
            print("› Process will run every 5 Epochs\n")

        main(vars(parser.parse_args()))

    except KeyboardInterrupt:
        if debug is True:
            print("Exited Application")
        exit(0)
