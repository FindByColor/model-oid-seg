#!/usr/bin/python

import os
import threading
import shutil
import sys

from datetime import datetime
from src.config import AWS_S3_BUCKET, DEBUG, DIR_IMAGES
from src.utils import count_files, flush_spacer

data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
start_time = datetime.now()
total = 0


class ProgressPercentage(object):
    def __init__(self, filename):
        self._filename = filename
        self._size = float(os.path.getsize(filename))
        self._seen_so_far = 0
        self._lock = threading.Lock()

    def __call__(self, bytes_amount):
        # To simplify we'll assume this is hooked up
        # to a single filename.
        with self._lock:
            self._seen_so_far += bytes_amount
            percentage = (self._seen_so_far / self._size) * 100
            sys.stdout.write(
                "\r%s  %s / %s  (%.2f%%)"
                % (self._filename, self._seen_so_far, self._size, percentage)
            )
            sys.stdout.flush()


def check_credentials():
    """Check if AWS credentials are present

    Returns:
        Boolean: Whether or not AWS credentials are present
    """
    credentials = os.path.expanduser("~/.aws/credentials")

    if os.path.isfile(credentials):
        return True
    else:
        return False


def upload_to_s3(file, key):
    """Upload to AWS S3 bucket

    Args:
        filename (str): Name of file to upload
        key (str): Path for bucket
    """
    import boto3
    from boto3.s3.transfer import TransferConfig

    s3_client = boto3.client("s3")

    print("\nUploading to AWS S3 ...")

    config = TransferConfig(
        multipart_threshold=1024 * 25,
        max_concurrency=10,
        multipart_chunksize=1024 * 25,
        use_threads=True,
    )

    s3_client.upload_file(
        file,
        AWS_S3_BUCKET,
        key,
        ExtraArgs={"ContentType": "application/zip"},
        Config=config,
        Callback=ProgressPercentage(file),
    )


def archive_training(an):
    """Zip Training Assets

    Args:
        an (str): Alphanumeric character to zip
    """

    # Make meta folder if it is not already present
    os.makedirs(".archive", exist_ok=True)

    print("\n\nTraining Images ( files that start with: '{an}' ) ...".format(an=an))

    os.system(
        "zip -rX .archive/train-images-{an}.zip data/images/train/{an}* 2>&1 | pv -lep -s $(ls -Rl1 data/images/train/{an}* | egrep -c '^[-/]') > /dev/null".format(
            an=an
        )
    )
    upload_to_s3(
        os.path.realpath(".archive/train-images-{an}.zip".format(an=an)),
        "model-oid-seg/train-images-{an}.zip".format(an=an),
    )

    print("\n\nTraining Labels ( files that start with '{an}' ) ...".format(an=an))

    os.system(
        "zip -rX .archive/train-labels-{an}.zip data/labels/train/{an}* 2>&1 | pv -lep -s $(ls -Rl1 data/labels/train/{an}* | egrep -c '^[-/]') > /dev/null".format(
            an=an
        )
    )
    upload_to_s3(
        os.path.realpath(".archive/train-labels-{an}.zip".format(an=an)),
        "model-oid-seg/train-labels-{an}.zip".format(an=an),
    )


def archive_validation():
    """Zip Validation Assets"""

    # Make meta folder if it is not already present
    os.makedirs(".archive", exist_ok=True)

    print("\n\nValidation Images ( all files ) ...")

    os.system(
        "zip -rX .archive/validation-images.zip data/images/val/* 2>&1 | pv -lep -s $(ls -Rl1 data/images/val/* | egrep -c '^[-/]') > /dev/null"
    )
    upload_to_s3(
        os.path.realpath(".archive/validation-images.zip"),
        "model-oid-seg/validation-images.zip",
    )

    print("\n\nValidation Labels ( all files ) ...")

    os.system(
        "zip -rX .archive/validation-labels.zip data/labels/val/* 2>&1 | pv -lep -s $(ls -Rl1 data/labels/val/* | egrep -c '^[-/]') > /dev/null"
    )
    upload_to_s3(
        os.path.realpath(".archive/validation-labels.zip"),
        "model-oid-seg/validation-labels.zip",
    )


def main():
    # Make sure data folder exists
    if not os.path.isdir(data_dir):
        print("Data folder not found: {}".format(data_dir))
        exit(0)

    # Make sure AWS credentials are present
    if check_credentials() is True:
        # Zip validation data
        archive_validation()

        # Zip training data by alphanumeric first character
        codes = [
            "0",
            "1",
            "2",
            "3",
            "4",
            "5",
            "6",
            "7",
            "8",
            "9",
            "a",
            "b",
            "c",
            "d",
            "e",
            "f",
        ]
        for an in codes:
            archive_training(an)

        # Delete temp folder we created
        if os.path.exists(os.path.realpath(".archive")):
            try:
                shutil.rmtree(os.path.realpath(".archive"))
            except OSError as e:
                print("Error: %s - %s." % (e.filename, e.strerror))
    else:
        print("AWS credentials not found: ~/.aws/credentials")
        print("Run `python aws_setup.py` to setup AWS credentials")


if __name__ == "__main__":
    try:
        # Get counts for images ( then double it for masks )
        total = count_files(DIR_IMAGES, "train")
        total += count_files(DIR_IMAGES, "validation")
        total = total * 2
        main()
    except KeyboardInterrupt:
        print(flush_spacer(100), end="\r", flush=True)
        print("Exited Application")
        exit(0)
