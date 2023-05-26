#!/usr/bin/python

import inquirer
import os

from src.oid import FBC_CLASSES
from src.utils import flush_spacer

data_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "data")


def config_classes():
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


def data_location_validation(answers, current):
    if current == "Already Installed" and not os.path.isdir(data_dir):
        raise inquirer.errors.ValidationError(
            "", reason="Data folder not found: {}".format(data_dir)
        )

    return True


def main():
    # Check where data is located
    questions = [
        inquirer.List(
            "data_location",
            message="Training Assets",
            choices=["Download from AWS", "Already Installed"],
            validate=data_location_validation,
        ),
        inquirer.List(
            "download_url",
            message="Download URL",
            choices=["https://website.com/models/fbc-seg.zip"],
            ignore=lambda x: x["data_location"] == "Already Installed",
        ),
    ]

    answers = inquirer.prompt(questions)

    ## Exit if user cancelled
    if not answers:
        exit(0)

    # Check if we need to get a download URL
    if answers["download_url"] is not None:
        download = "\n# Download URL ( Private FBC S3 Bucket )\ndownload: {}\n".format(
            answers["download_url"]
        )
    else:
        download = ""

    # Create config file
    config = """# Absolute path to data folder
path: {}

# Relative path to training images from data folder
train: images/train

# Relative path to validation images from data folder
val: images/val

{}{}""".format(
        data_dir, config_classes(), download
    )

    # Write Config File
    with open("config.yaml", "w") as outfile:
        outfile.write(config)

    print("› Config file created: config.yaml\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(flush_spacer(100), end="\r", flush=True)
        print("Exited Application")
        exit(0)
