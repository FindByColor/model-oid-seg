![Find By Color Logo](https://findbycolor-github.s3.amazonaws.com/logo.png 'Find By Color Logo')

**[↤ BACK](../README.md)**

# Downloading Assets

> The following steps need to be done in order:

### Step 1. Download Masks

First, let's get the image masks we need for this Segmentation Model.

```bash
python get_masks.py train
python get_masks.py validation
python get_masks.py test
```

### Step 2. Convert Masks to Labels

In order for YOLOv8 to use masks for training, they need to be converted from PNG to YOLOv8 Labels.

```bash
python masks_to_labels.py train
python masks_to_labels.py validation
python masks_to_labels.py test
```

### Step 3. Determine Images to Download

Only some of the images supported segmentation, so we only need to download those using the masks for reference.

```bash
python get_download_list.py train
python get_download_list.py validation
python get_download_list.py test
```

### Step 4. Download Images

Now that we know which images we need, we can download them.

```bash
python download_images.py train
python download_images.py validation
python download_images.py test
```
