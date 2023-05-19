import cv2
import numpy as np

def show_images(images):

    if isinstance(images,list):
        for i, img in enumerate(images):
            cv2.imshow(f"{i}",img)
    else:
        cv2.imshow(f"image", images)

    cv2.waitKey(0)

def read_image(path):
    image = cv2.imread(path)
    return image