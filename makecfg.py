import os
import argparse

"""
This script automates these steps to fix yolo nets cfgs for custom detection
https://github.com/AlexeyAB/darknet#how-to-train-to-detect-your-custom-objects

Modded from https://github.com/xaerincl/cfg_yolo to make it more ME-readable 
"""


def calcular(classes, num_images):
    """ Compute the numeric stuff we need, mostly 1st paragraph """ 
    filters = int((int(classes)+5)*3)
    max_batches = max(classes*2000, 6000, num_images)
    steps = [int(max_batches*ii) for ii in [0.8, 0.9]]
    return filters, max_batches, steps


def exact_filter_line(file_content):
    """ Get the exact line of the last filter line before each yolo layer """

    # Scan the file for the [yolo] and filter= lines
    yolo_lines = [i for i,line in enumerate(file_content) if '[yolo]' in line]
    filter_lines = [i for i,line in enumerate(file_content) if 'filters' in line]

    # Get only the filter lines prior to yolo layers
    exact_filter_list = []
    for i in yolo_lines:
        it = filter(lambda number: number < i, filter_lines)
        filtered_numbers = list(it)
        exact_filter_list.append(filtered_numbers[-1])

    return exact_filter_list



def main(inputcfg, classes, training, num_images, width, height, batch, subdivisions, no_flip, no_random):
    """ Do the shit. """

    # Load the file to a list
    file_content = []
    with open(inputcfg, 'r') as file_object:
        for line in file_object:
            file_content.append(line)

    # Compute the numeric stuff and 
    filters, max_batches, steps = calcular(classes, num_images)   
    lines_filter_before_yolo = exact_filter_line(file_content)
    training = training
    hue_line = False

    assert height % 32 == 0 
    assert width % 32 == 0 

    # Actually modify the file
    file_out = inputcfg.split('.')[0] + '_custom.cfg'
    with open(file_out, 'w') as file_object:
        for idx,line in enumerate(file_content):


            # AlexeyAB described changes
            if 'batch=' in line and 'batch_' not in line and '_batch' not in line:
                file_object.write(f'batch={batch if training else 1}'+'\n')

            elif 'subdivisions=' in line:
                file_object.write('#' if not training else '')
                file_object.write(f'subdivisions={subdivisions}'+'\n')

            elif 'max_batche=s' in line:
                file_object.write(f'max_batches = {max_batches}'+'\n')

            elif 'steps=' in line and 'policy' not in line:
                file_object.write(f'steps={steps[0]},{steps[1]}'+'\n')

            elif 'width=' in line:
                file_object.write(f'width={width}'+'\n')

            elif 'height=' in line:
                file_object.write(f'height={height}'+'\n')

            elif 'classes=' in line:
                file_object.write(f'classes={classes}'+'\n')
                
            elif idx in lines_filter_before_yolo:
                file_object.write(f'filters={filters}'+'\n')

            # Extra config
            elif 'hue=' in line and no_flip:
                file_object.write('hue=.1'+'\n')
                file_object.write('flip=0')
            elif 'random=' in line and no_random:
                file_object.write('random=0'+'\n')
            else:
                file_object.write(line)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='''Create YOLO cfg''')
    parser.add_argument('-inputcfg', '-i',  type=str, required=True, help='Path to default .cfg')
    parser.add_argument('-classes', '-c',  type=int, required=True, help='Detect how many classes')
    parser.add_argument('-training', '-tr',  type=bool, default=True, help='Is the cfg for training?')
    parser.add_argument('-num_images', '-n',  type=int, default=6000, help='Number of training images')
    parser.add_argument('-width', '-wi',  type=int, default = 416, help='network size- width')
    parser.add_argument('-height', '-he', type=int, default = 416, help='network size- height')
    parser.add_argument('-batch', '-b',  type=int, default = 64, help='')
    parser.add_argument('-subdivisions', '-sub',  type=int,  default = 32, help='')
    parser.add_argument("-no_random", help="change random to 0", action="store_true")
    parser.add_argument("-no_flip", help="if the model needs to distinguish between left and right objects", action="store_true")
    args = parser.parse_args()

    main(**vars(args))
    print(vars(args))
