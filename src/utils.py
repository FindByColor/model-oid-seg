import os

def count_files(base_dir, type):
    if type == 'validation':
        type = 'val'

    return len([f for f in os.listdir(os.path.join(base_dir, type))])

def flush_spacer(size=100):
    return ''.join(map(lambda x: x*size, ' '))