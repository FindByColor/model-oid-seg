import argparse
import os

from src.config import OID_CLASSIFICATIONS, OID_LABELS, OID_REGEX


# Create progress bar for wget
def bar_progress(current, total, width=80):
    print(
        "{:.2f}%: {}/{}".format(current / total * 100, current, total),
        end="\r",
        flush=True,
    )


# Check that image contains a valid path
def check_image(image):
    import re

    split, image_id = re.match(OID_REGEX, image).groups()
    yield split, image_id


# Check the image list and make sure each is valid
def check_image_list(image_list):
    for line_number, image in enumerate(image_list):
        try:
            yield from check_image(image)
        except (ValueError, AttributeError):
            raise ValueError(
                f"ERROR in line {line_number} of the image list. The following image "
                f'string is not recognized: "{image}".'
            )


# Count files in a given directory
def count_files(base_dir, type):
    return len([f for f in os.listdir(os.path.join(base_dir, get_folder(type)))])


# Download image from S3 bucket
def download_image(bucket, split, image_id, download_folder):
    import botocore
    import sys

    try:
        bucket.download_file(
            f"{split}/{image_id}.jpg", os.path.join(download_folder, f"{image_id}.jpg")
        )
    except botocore.exceptions.ClientError as exception:
        sys.exit(f"ERROR when downloading image `{split}/{image_id}`: {str(exception)}")


# Helper function to clear terminal output
def flush_spacer(size=100):
    return "".join(map(lambda x: x * size, " "))


# Get index from OID class
def get_class(id):
    return OID_CLASSIFICATIONS.index(id)


# Get label from OID class
def get_label(id):
    return OID_LABELS[id]


# Get folder name by type
def get_folder(type):
    folder = type

    if type == "validation":
        folder = "val"

    return folder


# Range validation for confidence param
def range_confidence(min_value, max_value):
    def check_valid(arg: str):
        try:
            val = float(arg)
        except ValueError:
            raise argparse.ArgumentTypeError(f"must be a valid `float`")
        if val < min_value or val > max_value:
            raise argparse.ArgumentTypeError(
                f"must be within [{min_value}, {max_value}]"
            )
        return val

    return check_valid


# Read image list for download
def read_image_list(image_list_file):
    with open(image_list_file, "r") as f:
        for line in f:
            yield line.strip().replace(".jpg", "")
