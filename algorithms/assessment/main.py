# main.py

# Author: Rvosuke
# Date: 2023/09/28

import cv2
import numpy as np
from preprocessing import resize_image, binarize_image, remove_ink_blobs
from registration import high_precision_registration
from feature_extraction import calculate_iou, calculate_image_similarity, calculate_keypoint_matching
from scoring import calculate_score


def main(image_path, template_path):
    """
    Execute the complete algorithm to evaluate the calligraphic copy.

    :param image_path: Path to the input calligraphic copy image.
    :param template_path: Path to the template image.
    :return: Final score (float).
    """
    # Load the images
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

    # Preprocessing
    image = resize_image(image, width=400)
    template = resize_image(template, width=400)
    image = binarize_image(image)
    template = binarize_image(template)
    image = remove_ink_blobs(image)
    template = remove_ink_blobs(template)

    # Registration
    registered_image = high_precision_registration(template, image)

    # Feature Extraction
    iou = calculate_iou(registered_image, template)
    similarity = calculate_image_similarity(registered_image, template)
    # Note: calculate_keypoint_matching requires keypoints, which need to be extracted or provided.
    # keypoints1 = ...
    # keypoints2 = ...
    keypoint_matching = calculate_keypoint_matching(keypoints1, keypoints2)

    # Scoring
    features = {
        'iou': iou,
        'similarity': similarity,
        'keypoint_matching': keypoint_matching,
    }
    score = calculate_score(features)

    return score


if __name__ == "__main__":
    image_path = "path_to_the_input_image"
    template_path = "path_to_the_template_image"
    score = main(image_path, template_path)
    print("Final Score:", score)
