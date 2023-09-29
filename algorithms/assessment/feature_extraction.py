"""
Contains functions for feature extraction and similarity calculation.
"""

# Author: Rvosuke
# Date: 2023/09/27

import cv2
import numpy as np
from skimage.metrics import structural_similarity as ssim


def calculate_iou(image1, image2):
    """
    Calculate the Intersection over Union (IoU) between two binary images.

    :param image1: First binary image (NumPy array).
    :param image2: Second binary image (NumPy array).
    :return: IoU value (float).
    """
    # Compute the intersection
    intersection = np.logical_and(image1, image2)

    # Compute the union
    union = np.logical_or(image1, image2)

    # Compute IoU
    iou = np.sum(intersection) / np.sum(union)
    return iou


def calculate_image_similarity(image1, image2):
    """
    Calculate the similarity between two images using Structural Similarity Index (SSIM).

    :param image1: First image (NumPy array).
    :param image2: Second image (NumPy array).
    :return: Similarity value (float).
    """
    similarity, _ = ssim(image1, image2, full=True)
    return similarity


def calculate_keypoint_matching(keypoints1, keypoints2):
    """
    Calculate the keypoint matching score between two sets of keypoints.

    :param keypoints1: Keypoints from the first image.
    :param keypoints2: Keypoints from the second image.
    :return: Keypoint matching score (float).
    """
    # Implement the keypoint matching score calculation based on the provided Python file
    keysum = 0
    for i in range(len(keypoints1)):
        keysum += np.sqrt((keypoints2[i, 0] - keypoints1[i, 0]) ** 2 + (keypoints2[i, 1] - keypoints1[i, 1]) ** 2)
    keyavg = keysum / len(keypoints1)
    return keyavg
