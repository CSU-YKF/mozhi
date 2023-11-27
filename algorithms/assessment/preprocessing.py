"""
Contains functions for preprocessing the input image before passing it to the model.
"""

# Author: Rvosuke
# Date: 2023/09/27

import cv2
import numpy as np
from skimage import morphology


def resize_image(image, width):
    """
    Resize the input image to the specified width while maintaining the aspect ratio.

    :param image: Input image (NumPy array).
    :param width: Desired width of the output image.
    :return: Resized image (NumPy array).
    """
    height = int(width * image.shape[0] / image.shape[1])
    resized_image = cv2.resize(image, (width, height), interpolation=cv2.INTER_AREA)
    return resized_image


def binarize_image(image, threshold=127):
    """
    Binarize the input image using a specified threshold.

    :param image: Input image (NumPy array).
    :param threshold: Threshold for binarization.
    :return: Binarized image (NumPy array).
    """
    _, binarized_image = cv2.threshold(image, threshold, 255, cv2.THRESH_BINARY_INV)
    return binarized_image


def num2true(img):
    """
    Convert numerical image to boolean image.

    :param img: Input image (NumPy array).
    :return: Boolean image (NumPy array).
    """
    img = np.array(img).astype(bool)
    for i in range(img.shape[0]):
        for j in range(img.shape[1]):
            if img[i][j] == 0:
                img[i][j] = bool(True)
            else:
                img[i][j] = bool(False)
    return img


def remove_ink_blobs(image, min_size=5):
    """
    Remove small ink blobs from the binarized image using morphological operations.

    :param image: Binarized image (NumPy array).
    :param min_size: Minimum size of ink blobs to be retained.
    :return: Image with small ink blobs removed (NumPy array).
    """
    boolean_img = num2true(image)
    cleaned_image = morphology.remove_small_objects(boolean_img, min_size=min_size)
    return cleaned_image.astype(np.uint8) * 255

# Additional preprocessing functions can be added based on the `utils` Python file
