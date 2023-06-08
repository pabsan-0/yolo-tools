##
## This script is meant will plot your labels so far in time series
## Meant to help with single-class sparse video labelling where items in consecutive frames are nearby
## Hardcoded stuff in here, adjust to your needs.
## 
## Labels follow the name convention of, f1c1_XXXXX.txt, XXXXX being increasing integer
##

import os
import matplotlib.pyplot as plt
import sys
import numpy as np


fxcy = sys.argv[1]
assert fxcy, "specify a f1c1-like dir, path is taken from `all_pseudolabels_so_far/` dir "


# Directory path containing the YOLO label files
directory = '../all_pseudolabels_so_far/' + fxcy

x_values = []
y_values = []
area_values = []

for ii in range(15000):
    
    fileidx = '{0:05d}'.format(ii)
    filename = f"{fxcy}_{fileidx}.txt"
    filepath = os.path.join(directory, filename)
        
    # Initialize x, y, and area values
    try:
        # Read the label file and extract x, y, and area values
        with open(filepath, 'r') as file:
            lines = file.readlines()
            if len(lines) > 0:
                line = lines[0].split()
                if len(line) >= 5:
                    x = float(line[1])
                    y = float(line[2])
                    width = float(line[3])
                    height = float(line[4])
                    area = width * height * 100 ## AREA GAIN

        # Append the values to the corresponding lists
        x_values.append(x)
        y_values.append(y)
        area_values.append(area)

    except FileNotFoundError:
        x_values.append(np.nan)
        y_values.append(np.nan)
        area_values.append(np.nan)

# Plotting the time series
plt.figure(figsize=(12, 4))
plt.plot(y_values, label='y')
plt.plot(x_values, label='x')
plt.plot(area_values, label='area')
plt.xlabel('Label Number')
plt.ylabel('Value')
plt.legend()

# Save the plot as an SVG file to disk
output_path = f'{fxcy}_time_series.png'
plt.savefig(output_path)
