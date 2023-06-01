#!/usr/bin/python

import argparse
import enum
import os
import schedule
import time
import torch

from datetime import datetime
from ultralytics import YOLO


class ModelSizes(str, enum.Enum):
    nano = "nano"
    small = "small"
    medium = "medium"
    large = "large"
    extralarge = "extralarge"


epoch = 0
last_epoch = 0
last_run = None
no_change_count = 0


def check_epoch(arg):
    global epoch
    global last_epoch
    global last_run
    global no_change_count

    with open(
        "fbc-ml-models/fbc-seg-{}/results.csv".format(arg["size"][0]),
        "r",
        encoding="utf-8",
        errors="ignore",
    ) as scraped:
        final_line = scraped.readlines()[-1]
        epoch = int(final_line.split(",")[0]) + 1

        if epoch > last_epoch:
            last_epoch = epoch
            no_change_count = 0

            if epoch % 10 == 0:
                current_time = datetime.now()

                if last_run is not None:
                    time_elapsed = current_time - last_run
                    print("› Next Run ETA: {}".format(time_elapsed))

                last_run = current_time

                if not os.path.exists(
                    "predictions/fbc-seg-{}-e{}".format(arg["size"][0], last_epoch)
                ):
                    print(
                        "› Generating Samples from Epoch #{} {}".format(
                            epoch, current_time.strftime("%Y-%m-%d %H:%M:%S")
                        )
                    )
                    # Run Predictions
                    predict(vars(parser.parse_args()))
        else:
            no_change_count += 1

    # Check how long it has been since the last change ( 120 minutes: 5 min * 24 runs = 120 )
    if no_change_count >= 24:
        # Exit Application
        schedule.clear()
        print("Exiting Application as no change has been detected in 120 minutes")
        exit(0)


def predict(arg):
    global epoch

    # Create Timer
    start_time = datetime.now()
    print("› Starting Predictions: {}".format(start_time.strftime("%Y-%m-%d %H:%M:%S")))

    # Create Timer
    if torch.cuda.is_available():
        device = "0"
    else:
        device = "cpu"

    # Load the last model from previous training session
    model = YOLO("fbc-ml-models/fbc-seg-{}/weights/last.pt".format(arg["size"][0]))

    # Define Args for both YOLO and ClearML
    args = dict(
        device=device,
        exist_ok=True,
        imgsz=640,
        name="fbc-seg-{}-e{}".format(arg["size"][0], last_epoch),
        project="predictions",
        verbose=False,
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
    end_time = datetime.now()
    time_elapsed = end_time - start_time
    print("\n› Completed: {}".format(end_time.strftime("%Y-%m-%d %H:%M:%S")))
    print("› Total Time: {}\n".format(time_elapsed))


def main():
    check_epoch(vars(parser.parse_args()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Run YOLOv8 Model Predictions",
        epilog="Find By Color - OID Segmentation Model",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("size", type=ModelSizes)

    try:
        start_time = datetime.now()
        print(
            "› Starting Test Sample Generation: {}".format(
                start_time.strftime("%Y-%m-%d %H:%M:%S")
            )
        )
        print("› Process will run every 5 Epochs\n")

        schedule.every(10).minutes.do(main)
        while True:
            schedule.run_pending()
            time.sleep(60)

    except KeyboardInterrupt:
        schedule.clear()
        print("Exited Application")
        exit(0)
