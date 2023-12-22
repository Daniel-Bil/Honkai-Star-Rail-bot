import os

import cv2


if __name__ == "__main__":
    images = [(cv2.imread(f"{os.getcwd()}\\gathered_data\\all_jarilo4\\{file}"), int(file.strip(".jpg"))) for file in os.listdir(f"{os.getcwd()}\\gathered_data\\all_jarilo4")]
    labels = os.listdir(f"{os.getcwd()}\\gathered_data\\jarilo4_labels")
    labels2 = [int(label.strip(".txt")) for label in labels]

    for image_tuple in images:
        if not image_tuple[1] in labels2:
            print(image_tuple[1])
            cv2.imwrite(f"{os.getcwd()}\\gathered_data\\not_labeled\\{image_tuple[1]}.png",image_tuple[0])
