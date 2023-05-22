import argparse
import enum

from datetime import datetime
from ultralytics import YOLO
from src.utils import flush_spacer

models = {
    'nano': 'yolov8n-seg.pt',
    'small': 'yolov8s-seg.pt',
    'medium': 'yolov8m-seg.pt',
    'large': 'yolov8l-seg.pt',
    'extralarge': 'yolov8x-seg.pt',
}

class ModelSizes(str, enum.Enum):
    nano = 'nano'
    small = 'small'
    medium = 'medium'
    large = 'large'
    extralarge = 'extralarge'

def main(arg):
    # Create Timer
    start_time = datetime.now()
    print('› Started: {}'.format(start_time.strftime("%Y-%m-%d %H:%M:%S")))

    # Get Model Size
    model_name = models[arg['size']]

    # Load a pretrained YOLO model (recommended for training)
    model = YOLO(model_name)

    # Train the model using the 'config.yaml' dataset for 100 epochs
    model.train(data='config.yaml', epochs=100, imgsz=640)

    # Evaluate the model's performance on the validation set
    model.val()

    # Perform object detection on an image using the newly trained model
    model('test-image.jpg')

    # Output Run Time
    end_time = datetime.now()
    time_elapsed = end_time - start_time
    print('› Completed: {}'.format(end_time.strftime("%Y-%m-%d %H:%M:%S")))
    print('› Total Time: {}'.format(time_elapsed.strftime("%H:%M:%S")))

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('size', type=ModelSizes)

    try:
        main(vars(parser.parse_args()))
    except KeyboardInterrupt:
        print(flush_spacer(100), end="\r", flush=True)
        print('› Exited Application\n')
        exit(0)
