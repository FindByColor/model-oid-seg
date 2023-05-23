#!/usr/bin/python

import os
import argparse

from datetime import datetime
from src.config import DEBUG, DIR_MASKS, DIR_META
from src.mask_types import MaskTypes
from src.utils import count_files, get_folder, flush_spacer

batch = 100


def main(args):
    # Setup Progress Tracking
    count = 0
    total = 0

    # Store IDs
    ids = []

    if DEBUG is True:
        start_time = datetime.now()
        print("› Loading Masks ...", end="\r", flush=True)

    # Define mask folder name
    mask_folder = get_folder(args["type"])

    # Make meta folder if it is not already present
    os.makedirs(DIR_META, exist_ok=True)

    # Define list file name
    list_file = "{}/{}-images.txt".format(DIR_META, args["type"])

    # Delete list file if it already exists
    if os.path.isfile(list_file):
        os.remove(list_file)

    mask_folder = os.path.join(DIR_MASKS, mask_folder)
    with open(list_file, "a") as list:
        for f in os.listdir(mask_folder):
            if f.lower().endswith((".png")):
                count += 1

                # get data from file name
                uuid = f.replace(".png", "", 1)
                image_id = uuid.split("_", 1)[0]

                # check if this uuid was already detected
                if image_id not in ids:
                    ids.append(image_id)
                    list.write("{}/{}\n".format(args["type"], image_id))

                if DEBUG is True:
                    time_elapsed = datetime.now() - start_time
                    percent = (count / total) * 100
                    print(
                        "› {:.2f}%: {}/{} ({}) {}".format(
                            percent, count, total, time_elapsed, flush_spacer(25)
                        ),
                        end="\r",
                        flush=True,
                    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate list of Images to Download from Open Images Dataset",
        epilog="Find By Color - OID Segmentation Model",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("type", type=MaskTypes)

    try:
        args = vars(parser.parse_args())
        total = count_files(DIR_MASKS, args["type"])
        main(args)
    except KeyboardInterrupt:
        print(flush_spacer(100), end="\r", flush=True)
        print("Exited Application")
        exit(0)
