import cv2
import os
import sys
import glob

if __name__ == '__main__':

    color = (50, 255, 50)
    thickness = 20
    font = cv2.FONT_HERSHEY_SIMPLEX
    fontScale = 0.5
    LEN = len(glob.glob('DATASET/images/test/*'))

    for idx, img_path in enumerate(sorted(glob.glob('DATASET/images/test/*'))):
        pic = cv2.imread(img_path)

        lab_path = img_path.replace('/images/', '/labels/').replace('.jpg', '.txt')
        with open(lab_path) as file:
            for i in file.readlines():
                cat, x, y, w, h = [float(k) for k in i.split()]
                x1, y1 = int((x - w/2) * pic.shape[1]),  int((y - h/2) * pic.shape[0])
                x2, y2 = int(x1 + w * pic.shape[1]), int(y1 + h * pic.shape[0])
                pic = cv2.rectangle(pic, (x1, y1), (x2, y2), color, thickness)
        print('{} / {}'.format(idx, LEN), end='\r')
        cv2.imwrite(f'./out/{str(idx).rjust(9,"0")}.jpg', pic)

        # pic = cv2.pyrDown(cv2.pyrDown(cv2.pyrDown(pic)))
        # cv2.imshow('a', pic)
        # cv2.waitKey(10)
    # cv2.destroyAllWindows()