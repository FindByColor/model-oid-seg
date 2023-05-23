#!/usr/bin/python

from clearml import Task
from datetime import datetime
from ultralytics import YOLO


def main():
    # Create Timer
    start_time = datetime.now()
    print("› Resuming: {}".format(start_time.strftime("%Y-%m-%d %H:%M:%S")))

    # Create Task for ClearML
    task = Task.init(project_name="Find By Color", task_name="Segmentation Model")

    # Load the last model from previous training session
    model = YOLO("./runs/segment/train/weights/last.pt")

    # Restart training from lasy training point
    model.train(resume=True)

    # Close ClearML Task
    task.close()

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
