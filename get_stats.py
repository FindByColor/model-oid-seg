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
import json

total = 0


def main(args):
    count = 0
    class_codes = []
    class_stats = {}
    csv_data = []

    if DEBUG is True:
        start_time = datetime.now()
        print("› Loading Masks ...", end="\r", flush=True)

    # Make meta folder if it is not already present
    os.makedirs(DIR_META, exist_ok=True)

    # Define folder name
    folder_name = get_folder(args["type"])

    # Define download folder path
    download_folder = os.path.join(DIR_MASKS, folder_name)

    for f in os.listdir(download_folder):
        if f.lower().endswith((".png")):
            count += 1

            # get data from file name
            uuid = f.replace(".png", "", 1)
            image_id = uuid.split("_", 1)[0]
            segment_id = uuid.rpartition("_")[-1]

            # generate class ID
            code = uuid.replace(image_id + "_", "")
            code = code.replace("_" + segment_id, "")

            if code[0] == "g":
                code = code.replace("g", "/g/", 1)

            elif code[0] == "m":
                code = code.replace("m", "/m/", 1)

            elif code[0] == "o" and code[1] == "i":
                code = code.replace("oi", "/oi/", 1)

            # get class ID from label
            label = get_oid_label(code)

            if label not in class_stats:
                class_codes.append(code)
                class_stats[label] = {
                    "code": code,
                    "label": label,
                    "count": 0,
                }

            class_stats[label]["count"] += 1

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

    # Sort Data
    class_codes.sort()
    json_sorted = dict(sorted(class_stats.items()))
    json_class_stats = json.dumps(json_sorted, indent=2)
    json_class_codes = json.dumps(class_codes, indent=2)

    # Add sorted data to CSV
    row_num = 0
    for row in json_sorted:
        json_sorted[row]["id"] = row_num
        csv_data.append(json_sorted[row])
        row_num += 1

    fields = ["id", "code", "label", "count"]

    with open(
        "{}/{}-stats.csv".format(DIR_META, args["type"]), "w", newline=""
    ) as outfile:
        writer = csv.DictWriter(outfile, fieldnames=fields)
        writer.writeheader()
        writer.writerows(csv_data)

    # Write Class Names Used
    with open("{}/{}-stats.json".format(DIR_META, args["type"]), "w") as outfile:
        outfile.write(json_class_stats)

    # Write Class Codes Used
    with open("{}/{}-codes.json".format(DIR_META, args["type"]), "w") as outfile:
        outfile.write(json_class_codes)


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
