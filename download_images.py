import argparse
import boto3
import botocore
import enum
import os
import re
import sys
import tqdm

from concurrent import futures

image_dir = './data/images'

BUCKET_NAME = 'open-images-dataset'
REGEX = r'(test|train|validation)/([a-fA-F0-9]*)'

class MaskTypes(str, enum.Enum):
    test = 'test'
    train = 'train'
    validation = 'validation'

def check_and_homogenize_one_image(image):
  split, image_id = re.match(REGEX, image).groups()
  yield split, image_id

def check_and_homogenize_image_list(image_list):
  for line_number, image in enumerate(image_list):
    try:
      yield from check_and_homogenize_one_image(image)
    except (ValueError, AttributeError):
      raise ValueError(
          f'ERROR in line {line_number} of the image list. The following image '
          f'string is not recognized: "{image}".')

def read_image_list_file(image_list_file):
  with open(image_list_file, 'r') as f:
    for line in f:
      yield line.strip().replace('.jpg', '')

def download_one_image(bucket, split, image_id, download_folder):
  try:
    bucket.download_file(f'{split}/{image_id}.jpg', os.path.join(download_folder, f'{image_id}.jpg'))
  except botocore.exceptions.ClientError as exception:
    sys.exit(f'ERROR when downloading image `{split}/{image_id}`: {str(exception)}')

def main(args):
  bucket = boto3.resource('s3', config=botocore.config.Config(signature_version=botocore.UNSIGNED)).Bucket(BUCKET_NAME)

  mask_type = args['type']

  if mask_type == 'validation':
    mask_type = 'val'

  download_folder = os.path.join(image_dir, mask_type)

  if not os.path.exists(download_folder):
    os.makedirs(download_folder)

  try:
    image_list = list(check_and_homogenize_image_list(read_image_list_file('meta/{}-images.txt'.format(args['type']))))
  except ValueError as exception:
    sys.exit(exception)

  progress_bar = tqdm.tqdm(total=len(image_list), desc='Downloading images', leave=True)
  
  with futures.ThreadPoolExecutor(max_workers=5) as executor:
    all_futures = [
      executor.submit(download_one_image, bucket, split, image_id, download_folder) for (split, image_id) in image_list
    ]
    for future in futures.as_completed(all_futures):
      future.result()
      progress_bar.update(1)
  
  progress_bar.close()

if __name__ == '__main__':
  parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
  parser.add_argument('type', type=MaskTypes)
  
  main(vars(parser.parse_args()))
  