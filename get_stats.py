#!/usr/bin/python

import csv
import os

from datetime import datetime

from src.config import DEBUG, DIR_MASKS, DIR_META
from src.mask_types import MaskTypes
from src.oid import get_oid_label
from src.utils import count_files, flush_spacer, get_folder

import argparse
import os

total = 0


def main(args):
    class_stats = {}
    csv_data = []
    unique_images = []

    masks = 0
    percent = 0
    time_elapsed = 0

    if DEBUG is True:
        start_time = datetime.now()
        print(
            "› Starting Validation: {}".format(start_time.strftime("%Y-%m-%d %H:%M:%S"))
        )
        print("› Loading Masks ...", end="\r", flush=True)

    # Make meta folder if it is not already present
    os.makedirs(DIR_META, exist_ok=True)

    # Define folder name
    folder_name = get_folder(args["type"])

    # Define download folder path
    download_folder = os.path.join(DIR_MASKS, folder_name)

    for f in os.listdir(download_folder):
        if f.lower().endswith((".png")):
            masks += 1

            # Get data from file name
            uuid = f.replace(".png", "", 1)
            image_id = uuid.split("_", 1)[0]
            segment_id = uuid.rpartition("_")[-1]

            # Generate class ID
            code = uuid.replace(image_id + "_", "")
            code = code.replace("_" + segment_id, "")

            if code[0] == "g":
                code = code.replace("g", "/g/", 1)

            elif code[0] == "m":
                code = code.replace("m", "/m/", 1)

            elif code[0] == "o" and code[1] == "i":
                code = code.replace("oi", "/oi/", 1)

            # Get class ID from label
            label = get_oid_label(code)

            # Create class stats
            if label not in class_stats:
                class_stats[label] = {
                    "code": code,
                    "label": label,
                    "masks": 0,
                    "images": 0,
                }

            # Update mask count
            class_stats[label]["masks"] += 1

            # Add image to unique images
            if image_id not in unique_images:
                unique_images.append(image_id)
                class_stats[label]["images"] += 1

            if DEBUG is True:
                time_elapsed = datetime.now() - start_time
                percent = (masks / total) * 100
                print(
                    "› {:.2f}%: {}/{} ({}) {}".format(
                        percent, masks, total, time_elapsed, flush_spacer(25)
                    ),
                    end="\r",
                    flush=True,
                )

    # Sort Data
    sorted_data = dict(sorted(class_stats.items()))

    # Add sorted data to CSV
    row_num = 0
    for row in sorted_data:
        sorted_data[row]["id"] = row_num
        csv_data.append(sorted_data[row])
        row_num += 1

    # Define CSV Fields
    fields = ["id", "code", "label", "masks", "images"]

    # Write CSV
    with open(
        "{}/{}-stats.csv".format(DIR_META, args["type"]), "w", newline=""
    ) as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(csv_data)

    if DEBUG is True:
        print("› Completed: {}".format(datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        print(
            "› {:.2f}%: {}/{} ({}) {}".format(
                percent, masks, total, time_elapsed, flush_spacer(25)
            )
        )


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate Statistics for Classname Usage",
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
