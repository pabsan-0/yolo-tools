import cv2
import os
import sys
import glob

if __name__ == '__main__':

    LEN = len(glob.glob('DATASET/images/test/*'))

    for idx, img_path in enumerate(sorted(glob.glob('DATASET/images/test/*'))):
        ln_path = f'./links/{str(idx).rjust(9,"0")}.jpg'
        os.system('ln -s %s %s' % (img_path, ln_path))
