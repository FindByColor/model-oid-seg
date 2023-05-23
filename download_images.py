#!/usr/bin/python

import argparse
import boto3
import botocore
import os
import shutil
import sys
import tqdm

from concurrent import futures
from src.config import DIR_DATA, DIR_IMAGES, DIR_META, OID_BUCKET_NAME
from src.mask_types import MaskTypes
from src.utils import (
    check_image_list,
    download_image,
    flush_spacer,
    get_folder,
    read_image_list,
)


def main(args):
    # Make required directories if they do not exist
    os.makedirs(DIR_DATA, exist_ok=True)
    os.makedirs(DIR_IMAGES, exist_ok=True)

    # Define AWS S3 bucket
    bucket = boto3.resource(
        "s3", config=botocore.config.Config(signature_version=botocore.UNSIGNED)
    ).Bucket(OID_BUCKET_NAME)

    # Define folder name
    folder_name = get_folder(args["type"])

    # Define download folder path
    download_folder = os.path.join(DIR_IMAGES, folder_name)

    # Delete download folder if it already exists
    if os.path.exists(download_folder):
        try:
            shutil.rmtree(download_folder)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    # Create download folder
    os.makedirs(download_folder, exist_ok=True)

    # Fetch image list for downloading
    try:
        image_list = list(
            check_image_list(read_image_list("{}/{}-images.txt".format(DIR_META, args["type"])))
        )
    except ValueError as exception:
        sys.exit(exception)

    # Setup progress bar for download indicators
    progress_bar = tqdm.tqdm(
        total=len(image_list), desc="Downloading images", leave=True
    )

    # Start downloading
    with futures.ThreadPoolExecutor(max_workers=5) as executor:
        all_futures = [
            executor.submit(download_image, bucket, split, image_id, download_folder)
            for (split, image_id) in image_list
        ]
        for future in futures.as_completed(all_futures):
            future.result()
            progress_bar.update(1)

    # Close progress bar since we're done downloading
    progress_bar.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Download Images from Open Images Dataset",
        epilog="Find By Color - OID Segmentation Model",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("type", type=MaskTypes)

    try:
        main(vars(parser.parse_args()))
    except KeyboardInterrupt:
        print(flush_spacer(100), end="\r", flush=True)
        print("Exited Application")
        exit(0)
