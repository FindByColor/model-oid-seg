import os
import argparse
import enum

from datetime import datetime
from src.utils import count_files, flush_spacer

debug = True
input_dir = './data/masks'
total = 0
batch = 100

class MaskTypes(str, enum.Enum):
    test = 'test'
    train = 'train'
    validation = 'validation'

def main(args):
    count = 0
    ids = []

    if debug is True:
        start_time = datetime.now()
        print('› Loading Masks ...', end="\r", flush=True)

    mask_type = args['type']

    if mask_type == 'validation':
        mask_type = 'val'

    list_file = 'meta/{}-images.txt'.format(args['type'])
    if os.path.isfile(list_file):
        os.remove(list_file)

    mask_folder = os.path.join(input_dir, mask_type)
    with open(list_file, 'a') as list:
        for f in os.listdir(mask_folder):
            if f.lower().endswith(('.png')):
                count += 1

                # get data from file name
                uuid = f.replace('.png', '', 1)
                image_id = uuid.split('_', 1)[0]

                # check if this uuid was already detected
                if image_id not in ids:
                    ids.append(image_id)
                    list.write('{}/{}\n'.format(args['type'], image_id))

                if debug is True:
                    time_elapsed = datetime.now() - start_time
                    percent = (count / total) * 100
                    print('› {:.2f}%: {}/{} ({}) {}'.format(percent, count, total, time_elapsed.strftime("%H:%M:%S"), flush_spacer(25)), end="\r", flush=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('type', type=MaskTypes)

    try:
        args = vars(parser.parse_args())
        total = count_files(input_dir, args['type'])
        main(args)
    except KeyboardInterrupt:
        print(flush_spacer(100), end="\r", flush=True)
        print('Exited Application')
        exit(0)
