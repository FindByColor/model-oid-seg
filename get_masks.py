import argparse
import os
import enum
import wget
from zipfile import ZipFile

from src.utils import flush_spacer

output_dir = './data/masks'

DOWNLOADS = [
   'https://storage.googleapis.com/openimages/v5/TYPE-masks/TYPE-masks-0.zip',
   'https://storage.googleapis.com/openimages/v5/TYPE-masks/TYPE-masks-1.zip',
   'https://storage.googleapis.com/openimages/v5/TYPE-masks/TYPE-masks-2.zip',
   'https://storage.googleapis.com/openimages/v5/TYPE-masks/TYPE-masks-3.zip',
   'https://storage.googleapis.com/openimages/v5/TYPE-masks/TYPE-masks-4.zip',
   'https://storage.googleapis.com/openimages/v5/TYPE-masks/TYPE-masks-5.zip',
   'https://storage.googleapis.com/openimages/v5/TYPE-masks/TYPE-masks-6.zip',
   'https://storage.googleapis.com/openimages/v5/TYPE-masks/TYPE-masks-7.zip',
   'https://storage.googleapis.com/openimages/v5/TYPE-masks/TYPE-masks-8.zip',
   'https://storage.googleapis.com/openimages/v5/TYPE-masks/TYPE-masks-9.zip',
   'https://storage.googleapis.com/openimages/v5/TYPE-masks/TYPE-masks-a.zip',
   'https://storage.googleapis.com/openimages/v5/TYPE-masks/TYPE-masks-b.zip',
   'https://storage.googleapis.com/openimages/v5/TYPE-masks/TYPE-masks-c.zip',
   'https://storage.googleapis.com/openimages/v5/TYPE-masks/TYPE-masks-d.zip',
   'https://storage.googleapis.com/openimages/v5/TYPE-masks/TYPE-masks-e.zip',
   'https://storage.googleapis.com/openimages/v5/TYPE-masks/TYPE-masks-f.zip',
]

class MaskTypes(str, enum.Enum):
    test = 'test'
    train = 'train'
    validation = 'validation'

#create this bar_progress method which is invoked automatically from wget
def bar_progress(current, total, width=80):
    print('{:.2f}%: {}/{}'.format(current / total * 100, current, total), end="\r", flush=True)

def main(args):
    for zip in DOWNLOADS:
        mask_type = args['type']

        if mask_type == 'validation':
            mask_type = 'val'

        url = zip.replace('TYPE', args['type'])
        name = url.rpartition('/')[-1]
        save_folder = os.path.join(output_dir, mask_type)
        save_path = os.path.join(save_folder, name)
        
        print('\nDownloading: {}'.format(name))
        wget.download(url, save_path, bar=bar_progress)

        print(flush_spacer(100), end="\r", flush=True)
        print('Unzipping: {}'.format(name))
        
        with ZipFile(save_path, 'r') as zObject:
            zObject.extractall(path=save_folder)

        zObject.close()

        print('Removing: {}'.format(name))
        os.remove(save_path)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('type', type=MaskTypes)

    try:
        main(vars(parser.parse_args()))
    except KeyboardInterrupt:
        print(flush_spacer(100), end="\r", flush=True)
        print('Exited Application\n')
        exit(0)