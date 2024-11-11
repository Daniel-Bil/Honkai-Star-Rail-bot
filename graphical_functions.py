import PIL.ImageGrab
import cv2
import numpy as np


def get_screen(gray: bool = True) -> np.ndarray:
    pil_image = PIL.ImageGrab.grab()
    np_image = np.array(pil_image)
    np_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2BGR)
    if gray:
        np_image = cv2.cvtColor(np_image, cv2.COLOR_RGB2GRAY)
    return np_image


def find_multiple_templates(template, screen, threshold=0.8, max_distance=10):
    """
    Find multiple instances of a template in the given screen using template matching
    and remove duplicates that are within a certain distance.

    :param screen: The main image (numpy array).
    :param template: The template to search for (numpy array).
    :param threshold: Matching threshold (default 0.8).
    :param max_distance: Maximum pixel distance to consider matches as duplicates (default 10).
    :return: List of bounding boxes where the template was found.
    """
    # Perform template matching
    result = cv2.matchTemplate(screen, template, cv2.TM_CCOEFF_NORMED)

    # Find locations where the match is greater than the threshold
    locations = np.where(result >= threshold)

    # Get the width and height of the template
    h, w = template.shape[:2]

    # Store center points for matches
    matches = []
    for pt in zip(*locations[::-1]):  # Switch x and y coordinates
        center = (pt[0] + w // 2, pt[1] + h // 2)
        matches.append(center)

    # Cluster points that are within max_distance of each other
    unique_matches = []
    for match in matches:
        if not any(np.linalg.norm(np.array(match) - np.array(existing_match)) < max_distance for existing_match in unique_matches):
            unique_matches.append(match)

    return unique_matches