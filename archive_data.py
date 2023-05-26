#!/usr/bin/python

import os
import threading
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


def upload_to_s3(file):
    """Upload to AWS S3 bucket

    Args:
        filename (str): Name of file to upload
    """
    import boto3
    from boto3.s3.transfer import TransferConfig

    s3_client = boto3.client("s3")

    print("Uploading to AWS S3 ... ( this may take a while )\n")

    config = TransferConfig(
        multipart_threshold=1024 * 25,
        max_concurrency=10,
        multipart_chunksize=1024 * 25,
        use_threads=True,
    )

    s3_client.upload_file(
        file,
        AWS_S3_BUCKET,
        "model-oid-seg/data.zip",
        ExtraArgs={"ACL": "public-read", "ContentType": "application/zip"},
        Config=config,
        Callback=ProgressPercentage(file),
    )


def zip_folder(filename, target_dir):
    """Zip Data Folder

    Args:
        filename (str): Name of file to create
        target_dir (str): Folder to zip
    """
    import zipfile

    count = 0

    print("Compressing data folder ... ( this may take a while )\n")

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
    # Make sure data folder exists
    if not os.path.isdir(data_dir):
        print("Data folder not found: {}".format(data_dir))
        exit(0)

    # Make sure AWS credentials are present
    if check_credentials() is True:
        filename = "data.zip"
        zip_folder(filename, data_dir)
        upload_to_s3(os.path.realpath(filename))
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
