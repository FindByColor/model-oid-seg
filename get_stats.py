import os

from classifications import get_class, get_label
from datetime import datetime

from src.utils import count_files, flush_spacer

import argparse
import os
import enum
import json

class MaskTypes(str, enum.Enum):
    test = 'test'
    train = 'train'
    validation = 'validation'

debug = True
input_dir = './data/masks'
total = 0

def countFiles(args):
    mask_type = args['type']

    if mask_type == 'validation':
        mask_type = 'val'

    mask_folder = os.path.join(input_dir, mask_type)
    return len([f for f in os.listdir(mask_folder)])

def main(args):
    count = 0
    class_codes = []
    class_stats = {}

    if debug is True:
        start_time = datetime.now()
        print('› Loading Masks ...', end="\r", flush=True)

    mask_type = args['type']

    if mask_type == 'validation':
        mask_type = 'val'

    mask_folder = os.path.join(input_dir, mask_type)

    for f in os.listdir(mask_folder):
        if f.lower().endswith(('.png')):
            count += 1

            # get data from file name
            uuid = f.replace('.png', '', 1)
            image_id = uuid.split('_', 1)[0]
            segment_id = uuid.rpartition('_')[-1]

            # generate class ID
            code = uuid.replace(image_id + '_', '')
            code = code.replace('_' + segment_id, '')

            if code[0] == 'g':
                code = code.replace('g', '/g/', 1)

            elif code[0] == 'm':
                code = code.replace('m', '/m/', 1)

            elif code[0] == 'o' and code[1] == 'i':
                code = code.replace('oi', '/oi/', 1)

            # get class ID from label
            id = get_class(code)
            label = get_label(code)

            if label not in class_stats:
                class_codes.append(code)
                class_stats[label] = 0

            class_stats[label] += 1

            if debug is True:
                time_elapsed = datetime.now() - start_time
                percent = (count / total) * 100
                print('› {:.2f}%: {}/{} ({}) {}'.format(percent, count, total, time_elapsed.strftime("%H:%M:%S"), flush_spacer(25)), end="\r", flush=True)

    # Serializing json
    class_codes.sort()
    json_class_stats = json.dumps(dict(sorted(class_stats.items())), indent=4)
    json_class_codes = json.dumps(class_codes, indent=4)

    # Write Class Names Used
    with open('meta/{}-stats.json'.format(args['type']), 'w') as outfile:
        outfile.write(json_class_stats)

    # Write Class Codes Used
    with open('meta/{}-codes.json'.format(args['type']), 'w') as outfile:
        outfile.write(json_class_codes)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('type', type=MaskTypes)

    try:
        args = vars(parser.parse_args())
        total = count_files(input_dir, args['type'])
        main(args)
    except KeyboardInterrupt:
        print(flush_spacer(100), end="\r", flush=True)
        print('Exited Application\n')
        exit(0)
