#!/usr/bin/python

import argparse
import os
import shutil
import wget

from src.config import DIR_MASKS, OID_DOWNLOADS
from src.mask_types import MaskTypes
from src.utils import bar_progress, get_folder, flush_spacer
from zipfile import ZipFile


def main(args):
    # Define folder name
    folder_name = get_folder(args["type"])

    # Create masks folder if not present
    os.makedirs(DIR_MASKS, exist_ok=True)

    # Define download folder path
    download_folder = os.path.join(DIR_MASKS, folder_name)

    # Delete download folder if it already exists
    if os.path.exists(download_folder):
        try:
            print("Deleting Existing Masks ... ( this may take a while )")
            shutil.rmtree(download_folder)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))

    # Create download folder
    os.makedirs(download_folder)

    # Let user know we are about to download a half a million files
    print("Downloading Segmentation Masks ... ( this will take a long time )")

    # Loop through available downloads
    for zip in OID_DOWNLOADS:
        # Update URL for requested type
        url = zip.replace("TYPE", args["type"])

        # Create save path for file
        name = url.rpartition("/")[-1]
        save_path = os.path.join(download_folder, name)

        # Show status of downloads
        print("\nDownloading: {}".format(name))
        wget.download(url, save_path, bar=bar_progress)

        # Start unzipping the file
        print(flush_spacer(100), end="\r", flush=True)
        print("Unzipping: {}".format(name))
        with ZipFile(save_path, "r") as zObject:
            zObject.extractall(path=download_folder)

        # Close zip file
        zObject.close()

        # Do some cleanup
        print("Removing: {}".format(name))
        os.remove(save_path)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Get Segmentation Masks from Open Images Dataset",
        epilog="Find By Color - OID Segmentation Model",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("type", type=MaskTypes, help="Image Type: [train|validation]")

    try:
        main(vars(parser.parse_args()))
    except KeyboardInterrupt:
        print(flush_spacer(100), end="\r", flush=True)
        print("Exited Application")
        exit(0)
