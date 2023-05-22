import cv2
import os

from classifications import get_class
from datetime import datetime

from src.utils import count_files, flush_spacer

import argparse
import os
import enum

class MaskTypes(str, enum.Enum):
    test = 'test'
    train = 'train'
    validation = 'validation'

debug = True
input_dir = './data/masks'
output_dir = './data/labels'
total = 0

def main(args):
    count = 0

    if debug is True:
        start_time = datetime.now()
        print('› Loading Masks ...', end="\r", flush=True)

    mask_type = args['type']

    if mask_type == 'validation':
        mask_type = 'val'

    mask_folder = os.path.join(input_dir, mask_type)
    label_folder = os.path.join(output_dir, mask_type)

    for f in os.listdir(mask_folder):
        if f.lower().endswith(('.png')):
            count += 1

            # build absolute path
            image_path = os.path.join(mask_folder, f)

            # get data from file name
            uuid = f.replace('.png', '', 1)
            image_id = uuid.split('_', 1)[0]
            segment_id = uuid.rpartition('_')[-1]

            # generate class ID
            class_label = uuid.replace(image_id + '_', '')
            class_label = class_label.replace('_' + segment_id, '')

            if class_label[0] == 'g':
                class_label = class_label.replace('g', '/g/', 1)

            elif class_label[0] == 'm':
                class_label = class_label.replace('m', '/m/', 1)

            elif class_label[0] == 'o' and class_label[1] == 'i':
                class_label = class_label.replace('oi', '/oi/', 1)

            # get class ID from label
            class_id = get_class(class_label)

            # load the binary mask and get its contours
            mask = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
            _, mask = cv2.threshold(mask, 1, 255, cv2.THRESH_BINARY)

            H, W = mask.shape
            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            # convert the contours to polygons
            polygons = []
            for cnt in contours:
                if cv2.contourArea(cnt) > 200:
                    polygon = []
                    for point in cnt:
                        x, y = point[0]
                        polygon.append(x / W)
                        polygon.append(y / H)
                    polygons.append(polygon)

            # print the polygons
            with open('{}.txt'.format(os.path.join(label_folder, image_id)), 'a') as label:
                for polygon in polygons:
                    for p_, p in enumerate(polygon):
                        if p_ == len(polygon) - 1:
                            label.write('{}\n'.format(p))
                        elif p_ == 0:
                            # Lookup Class Name from File Path and map to Numeric Value
                            label.write('{} {} '.format(class_id, p))
                        else:
                            label.write('{} '.format(p))
                label.close()

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
        print('Exited Application\n')
        exit(0)
