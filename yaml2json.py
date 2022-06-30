import os
from sys import argv
import json
import imagesize
import yaml

"""
Converts COCO dataset annotations from yaml-yolo to MSCOCO-JSON format and 
prints them to stdout.

This script returns image_ids in string integer format.

Usage: 
json-parser.py dataset.yaml train > dataset.json
                            val
                            test

"""


if __name__ == '__main__':
    yaml_file = argv[1]
    split_name = argv[2]

    # Load yaml into a dict and fetch the paths of the target split
    with open(yaml_file) as f:
        dataset_yaml = yaml.load(f, Loader=yaml.FullLoader)
        class_names = dataset_yaml.get('names') 
        split_path = dataset_yaml.get(split_name)   


    ## Header
    print('\n{')


    ## Body

    # Print category stuff
    print('"categories": ['),
    for id, name in enumerate(class_names):
        print(',' if id !=0 else '', end='')
        print('\t{"id": %s, "name": "%s"}' % (id, name), end='')
    print('\n],'),

    # Print image stuff
    print('"images": ['),
    for idx_file, img_name in enumerate(os.listdir(split_path)):
        img_path = split_path + img_name
        image_id = img_path.split('/')[-1].split('.')[0]
        width, height = imagesize.get(img_path)

        # If not first row, print a comma
        if not(idx_file ==0): 
            print(',')


        # This will explode within yoloR evaluation
        #try:
        #    image_id = int(image_id)
        #except Exception:
        #    pass

        # Print to stdout 
        res = {
            'id':       image_id, 
            'height':   height, 
            'width':    width, 
            'license':  None, 
            'coco_url': None, 
        }
        print('\t' + json.dumps(res), end='')
    print('\n],')


    # Annotation stuff
    print('"annotations": [')
    overall_id = 0
    first_time = True
    # Fetch each image in the specified split
    for idx_file, img_name in enumerate(os.listdir(split_path)):

        # Get the image and label paths for said image
        img_path = split_path + img_name
        label_path = img_path.replace('images', 'labels').split('.')[0] + '.txt'
        image_id = img_path.split('/')[-1].split('.')[0]
        width, height = imagesize.get(img_path)

        # Scan the label for that image and do yolo2coco formatting
        # Take each line (one line per detection) and split it by whitespaces
        with open(label_path, 'r') as file:            
            for idx_line, line in enumerate(file):
                sline = line.split()
                x = float(sline[1]) * width
                y = float(sline[2]) * height
                w = float(sline[3]) * width
                h = float(sline[4]) * height
                x = x - w/2
                y = y - h/2

                # If not first row, print a comma
                if not first_time: 
                    print(',')
                first_time = False

                # Print to stdout 
                res = {
                    'id':            overall_id,
                    'image_id':      image_id, 
                    'category_id':   int(sline[0]), 
                    'bbox':          [int(i) for i in [x,y,w,h]], 
                    'area':          int(w * h), 
                    'iscrowd':       0,
                    'supercategory': None,
                }
                print('\t' + json.dumps(res), end='')
                overall_id += 1
            

    ## Tail of the json file
    print('\n]}\n')
