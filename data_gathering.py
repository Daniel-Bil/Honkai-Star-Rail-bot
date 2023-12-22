import time
import os

import cv2

from main import get_image

if __name__ == '__main__':
    time.sleep(1)


    h=0
    while h < 20:
        time.sleep(0.8)
        img = get_image(place="all")
        path = f"{os.getcwd()}\\gathered_data\\herta_new"
        dir = os.listdir(path)
        nr = len(dir)
        print(nr)
        cv2.imwrite(f"{path}\\{nr+457}.png", img)
        h+=1