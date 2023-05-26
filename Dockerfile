FROM python:3.9

LABEL maintainer "Peter Schmalfeldt peter@findbycolor.com"
LABEL version="1.0"
LABEL description="Model OID Segmentation"
LABEL vendor="Find By Color"

# Set Working Directory
WORKDIR /fbc

# Copy Required Files
COPY archive_data.py archive_data.py
COPY create_config.py create_config.py
COPY download_images.py download_images.py
COPY get_download_list.py get_download_list.py
COPY get_masks.py get_masks.py
COPY get_stats.py get_stats.py
COPY masks_to_labels.py masks_to_labels.py
COPY predict.py predict.py
COPY requirements-dev.txt requirements-dev.txt
COPY requirements.txt requirements.txt
COPY resume.py resume.py
COPY test-image.jpg test-image.jpg
COPY train.py train.py
COPY validate.py validate.py

# Copy Required Folders
COPY src/ src/

# Update Packages
RUN apt-get update && apt-get install -y build-essential curl software-properties-common git libgl1 && rm -rf /var/lib/apt/lists/*

# Install Python Dependencies
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt
RUN pip3 install -r requirements-dev.txt
