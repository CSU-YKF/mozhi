# claude_comment.py

# Author: Rvosuke
# Date: 2023/09/28

import cv2
import numpy as np
from preprocessing import resize_image, binarize_image, remove_ink_blobs
from registration import high_precision_registration
from feature_extraction import calculate_iou, calculate_image_similarity, calculate_keypoint_matching
from scoring import calculate_score
from algorithms.comment.claude_comment import claude


def main(image, template):
    """
    Execute the complete algorithm to evaluate the calligraphic copy.

    :param image: Path to the input calligraphic copy image.
    :param template: Path to the template image.
    :return: Final score (float).
    """
    # # Load the images
    # image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    # template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)

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
    # keypoint_matching = calculate_keypoint_matching(keypoints1, keypoints2)

    # Scoring
    features = {
        'iou': iou,
        'similarity': similarity,
        # 'keypoint_matching': keypoint_matching,
    }
    score = calculate_score(features)
    comment = claude(features['iou'], features['similarity'])
    return score, comment


if __name__ == "__main__":
    image_path = "../src/data/4-2.png"
    template_path = "../src/data/4-2.png"
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
    template = cv2.imread(template_path, cv2.IMREAD_GRAYSCALE)
    score, comment = main(image, template)
    print(f"Final Score: {int(score)}")
    print(comment)
