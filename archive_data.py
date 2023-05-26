#!/usr/bin/python

import os
import sys
import zipfile

from datetime import datetime
from src.config import DEBUG, DIR_IMAGES
from src.utils import count_files, flush_spacer

data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
start_time = datetime.now()
total = 0


def zip_folder(filename, target_dir):
    count = 0

    with zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED) as zip_obj:
        root_len = len(target_dir) + 1
        for base, dirs, files in os.walk(target_dir):
            for file in files:
                if file.lower().endswith((".cache")):
                    continue
                fn = os.path.join(base, file)
                zip_obj.write(fn, fn[root_len:])

                if DEBUG is True:
                    count += 1
                    time_elapsed = datetime.now() - start_time
                    percent = (count / total) * 100
                    print(
                        "› {:.2f}%: {}/{} ({}) {}".format(
                            percent, count, total, time_elapsed, flush_spacer(25)
                        ),
                        end="\r",
                        flush=True,
                    )


def main():
    if not os.path.isdir(data_dir):
        print("Data folder not found: {}".format(data_dir))
        sys.exit()

    print("Compressing data folder ... ( this may take a while )\n")

    zip_folder("data.zip", data_dir)

    print("Config file created: data.zip\n")
    sys.exit()


if __name__ == "__main__":
    try:
        total = count_files(DIR_IMAGES, "train")
        total += count_files(DIR_IMAGES, "validation")
        total = total * 2
        main()
    except KeyboardInterrupt:
        print(flush_spacer(100), end="\r", flush=True)
        print("Exited Application")
        exit(0)
