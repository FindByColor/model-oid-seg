def get_training_data():
    """Download data from AWS S3 bucket"""
    import boto3
    import shutil
    import os

    from pathlib import Path
    from zipfile import ZipFile

    cwd = os.path.dirname(os.path.realpath(__file__))

    try:
        data_dir = Path(yaml["path"])
    except:
        data_dir = os.path.join(cwd, "data")

    # Delete download folder if it already exists
    if os.path.exists(data_dir):
        print(
            "WARNING: Data directory already exists.\n\nManually delete the following directory before trying again:\n{}\n".format(
                data_dir
            )
        )
        exit(0)

    debug_missing = False
    temp_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), ".temp")

    # Make required directories
    os.makedirs(temp_dir, exist_ok=True)

    s3 = boto3.resource("s3")

    # Get validation data
    try:
        print("Downloading validation images ( all files ) ...")
        s3.meta.client.download_file(
            "fbc-ml-dataset",
            "model-oid-seg/validation-images.zip",
            "{}/validation-images.zip".format(temp_dir),
        )
    except:
        if debug_missing is True:
            print("Missing: model-oid-seg/validation-labels.zip")

    try:
        print("Downloading validation labels ( all files ) ...")
        s3.meta.client.download_file(
            "fbc-ml-dataset",
            "model-oid-seg/validation-labels.zip",
            "{}/validation-labels.zip".format(temp_dir),
        )
    except:
        if debug_missing is True:
            print("Missing: model-oid-seg/validation-labels.zip")

    # Get training data
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
        # Get training images
        try:
            print(
                "Downloading training images ( files that start with '{}' ) ...".format(
                    an
                )
            )
            s3.meta.client.download_file(
                "fbc-ml-dataset",
                "model-oid-seg/train-images-{an}.zip",
                "{temp_dir}/train-images-{an}.zip",
            ).format(an=an, temp_dir=temp_dir)
        except:
            if debug_missing is True:
                print("Missing: model-oid-seg/train-images-{}.zip".format(an))

        # Get training labels
        try:
            print(
                "Downloading training labels ( files that start with '{}' ) ...".format(
                    an
                )
            )
            s3.meta.client.download_file(
                "fbc-ml-dataset",
                "model-oid-seg/train-labels-{an}.zip",
                "{temp_dir}/train-labels-{an}.zip",
            ).format(an=an, temp_dir=temp_dir)
        except:
            if debug_missing is True:
                print("Missing: model-oid-seg/train-images-{}.zip".format(an))

    # Extract zip files
    for zip in os.listdir(temp_dir):
        if zip.lower().endswith((".zip")):
            print("Unzipping File: {} ...".format(zip))
            with ZipFile(os.path.join(temp_dir, zip), "r") as zObject:
                zObject.extractall(path=cwd)

            zObject.close()

            # Do some cleanup
            os.remove(os.path.join(temp_dir, zip))

    # Delete temp folder we created
    if os.path.exists(temp_dir):
        try:
            shutil.rmtree(temp_dir)
        except OSError as e:
            print("Error: %s - %s." % (e.filename, e.strerror))


if __name__ == "__main__":
    get_training_data()
