import os
from copy import deepcopy

import cv2
import numpy as np

from utilities import show_images

def match_descriptors(descriptor1, descriptor2):
    # Create a BFMatcher object
    bf = cv2.BFMatcher()

    # Perform the matching
    matches = bf.match(descriptor1, descriptor2)

    # Sort the matches by distance
    matches = sorted(matches, key=lambda x: x.distance)

    return matches

def create_sift_descriptors(image):


    # Convert the image to grayscale
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Initialize the SIFT detector
    sift = cv2.SIFT_create()

    # Detect keypoints and compute descriptors
    keypoints, descriptors = sift.detectAndCompute(gray_image, None)

    return keypoints, descriptors


if __name__ == "__main__":
    img1 = cv2.imread(f"{os.getcwd()}\\test_images\\enemies\\noticed1.png")
    # gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    # ret, thresh1 = cv2.threshold(gray1, 150, 255, cv2.THRESH_BINARY)

    img2 = cv2.imread(f"{os.getcwd()}\\test_images\\locked_enemy.png")
    #
    show_images([img1, img2])

    gray1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    gray2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)

    methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR',
               'cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    w, h = gray1.shape[::-1]
    for meth in methods:
        img = gray2.copy()
        method = eval(meth)
        # Apply template Matching
        res = cv2.matchTemplate(img, gray1, method)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
        # If the method is TM_SQDIFF or TM_SQDIFF_NORMED, take minimum
        if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
            top_left = min_loc
        else:
            top_left = max_loc
        bottom_right = (top_left[0] + w, top_left[1] + h)
        cv2.rectangle(img, top_left, bottom_right, 255, 2)
        show_images(img)














    kp1, des1 = create_sift_descriptors(img1)
    kp2, des2 = create_sift_descriptors(img2)
    print(kp1)

    img1_copy = deepcopy(img1)
    img2_copy = deepcopy(img2)

    img1_copy = cv2.drawKeypoints(img1_copy, kp1, None)
    img2_copy = cv2.drawKeypoints(img2_copy, kp2, None)

    show_images([img1_copy,img2_copy])


    matches = match_descriptors(des1,des2)

    matched_image = cv2.drawMatches(
        img1_copy, kp1,
        img2_copy, kp2,
        matches[:30], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    show_images(matched_image)

    src_pts = np.float32([kp1[m.queryIdx].pt for m in matches]).reshape(-1, 1, 2)
    dst_pts = np.float32([kp2[m.trainIdx].pt for m in matches]).reshape(-1, 1, 2)
    M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC, 5.0)
    print(mask)
    matches2 = []
    for mat, mas in zip(matches, mask):
        if mas[0]==1:
            matches2.append(mat)
        # matches = matches[mask>0]
    matched_image2 = cv2.drawMatches(
        img1_copy, kp1,
        img2_copy, kp2,
        matches2[:30], None, flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    show_images(matched_image2)
    # def draw_keypoints(image_path, keypoints):
    #     # Load the image
    #     image = cv2.imread(image_path)
    #
    #     # Draw keypoints on the image
    #     image_with_keypoints = cv2.drawKeypoints(image, keypoints, None)
    #
    #     # Display the image with keypoints
    #     cv2.imshow("Image with Keypoints", image_with_keypoints)
    #     cv2.waitKey(0)
    #     cv2.destroyAllWindows()