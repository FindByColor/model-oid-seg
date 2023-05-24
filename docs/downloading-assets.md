![Find By Color Logo](https://findbycolor-github.s3.amazonaws.com/logo.png 'Find By Color Logo')

**[↤ BACK](../README.md)**

# Downloading Assets

> The following steps need to be done in order:

NOTE: You only need to complete this step if you are rebuilding the training assets. If they have already been created, and you have a link to the S3 archive, you are good to go on to the next steps.

This process will take a while, perhaps an entire day.

- [X] `2,711,388` segmentation mask PNGs are downloaded for `train` and `validation`
- [X] `2,711,388` masks are converted into YOLOv8 labels using binary contours
- [X] `1,514,164` masks are removed because we don't actually want to train with them `*`
- [X] `TBD` training images are downloaded that were used when creating the segmentation masks
- [X] `TBD` images and `TBD` labels are then packaged up into a zip file and sent off to an S3 bucket

`*` Google does not provide a way to download just the segmentation masks we care about.  We have to download them all as zip files and pick the ones we want using the file's naming convention. That's also how we figure out which image IDs we need to download later for training.

## Step 1. Download Masks

First, let's get the image masks we need for this Segmentation Model.

```bash
python get_masks.py train
python get_masks.py validation
```

## Step 2. Convert Masks to Labels

In order for YOLOv8 to use masks for training, they need to be converted from PNG to YOLOv8 Labels.

```bash
python masks_to_labels.py train
python masks_to_labels.py validation
```

## Step 3. Determine Images to Download

Only some of the images supported segmentation, so we only need to download those using the masks for reference.

```bash
python get_download_list.py train
python get_download_list.py validation
```

## Step 4. Download Images

Now that we know which images we need, we can download them.

```bash
python download_images.py train
python download_images.py validation
```
