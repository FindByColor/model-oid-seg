#!/usr/bin/python

import inquirer
import os

from src.oid import FBC_CLASSES
from src.utils import flush_spacer

data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")
file_name = "config.yaml"


def generate_classes():
    output = []
    id = 0
    for code in FBC_CLASSES:
        output.append("  {}: {}".format(id, FBC_CLASSES[code]))
        id += 1

    return """# Number of classes
nc: {}

# Classes
names:
{}
""".format(
        len(output), "\n".join(output)
    )


def generate_download(answers):
    # Check if we need to get a download URL
    if answers["download_url"] is not None:
        download = "\n# Download from URL\ndownload: {}\n".format(
            answers["download_url"]
        )
    elif answers["data_location"] == "Download from AWS":
        download = """
# Download from FBC S3 Bucket
download: |
  import boto3
  import os

  from pathlib import Path
  from zipfile import ZipFile

  dir = Path(yaml["path"])

  s3 = boto3.resource("s3")
  s3.meta.client.download_file("fbc-ml-dataset", "model-oid-seg/data.zip", "data.zip")

  with ZipFile("data.zip", "r") as zObject:
      zObject.extractall(path=dir)

  zObject.close()
  os.remove(save_path)
"""
    else:
        download = ""

    return download


def data_location_validation(answers, current):
    credentials = os.path.expanduser("~/.aws/credentials")

    if current == "Already Installed" and not os.path.isdir(data_dir):
        raise inquirer.errors.ValidationError(
            "", reason="Data folder not found: {}".format(data_dir)
        )
    elif current == "Download from AWS" and not os.path.isfile(credentials):
        raise inquirer.errors.ValidationError(
            "", reason="AWS not configured. Run `python aws_setup.py`"
        )

    return True


def autocomplete_fn(_text, state):
    urls = ["https://fbc-ml-dataset.s3.amazonaws.com/model-oid-seg/data.zip"]
    return urls[state % len(urls)]


def main():
    # Check where data is located
    questions = [
        inquirer.List(
            "data_location",
            message="Training Assets",
            choices=["Download from AWS", "Download from URL", "Already Installed"],
            validate=data_location_validation,
        ),
        inquirer.Text(
            "download_url",
            message="Download URL ( TAB to autocomplete )",
            autocomplete=autocomplete_fn,
            validate=lambda _, x: x.startswith("https://"),
            ignore=lambda x: x["data_location"] == "Already Installed"
            or x["data_location"] == "Download from AWS",
        ),
    ]

    answers = inquirer.prompt(questions)

    ## Exit if user cancelled
    if not answers:
        exit(0)

    # Create config file
    config = """# Absolute path to data folder
path: {}

# Relative path to training images from data folder
train: images/train

# Relative path to validation images from data folder
val: images/val

{}{}""".format(
        data_dir, generate_classes(), generate_download(answers)
    )

    # Write Config File
    with open(file_name, "w") as outfile:
        outfile.write(config)

    print("› Config file created: {}\n".format(file_name))


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(flush_spacer(100), end="\r", flush=True)
        print("Exited Application")
        exit(0)
