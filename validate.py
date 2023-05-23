#!/usr/bin/python

from datetime import datetime
from ultralytics import YOLO


def main():
    # Create Timer
    start_time = datetime.now()
    print("› Starting Validation: {}".format(start_time.strftime("%Y-%m-%d %H:%M:%S")))

    # Load the last model from previous training session
    model = YOLO("runs/segment/train/weights/last.pt")

    # Evaluate the model's performance on the validation set
    model.val()

    # Output Run Time
    end_time = datetime.now()
    time_elapsed = end_time - start_time
    print("› Completed: {}".format(end_time.strftime("%Y-%m-%d %H:%M:%S")))
    print("› Total Time: {}".format(time_elapsed))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Exited Application")
        exit(0)
