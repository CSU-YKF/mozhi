"""
Contains the functions for calculating the final score based on the extracted features.
"""

# Author: Rvosuke
# Date: 2023/09/28


def calculate_score(features):
    """
    Calculate the final score based on the extracted features.

    :param features: A dictionary containing the extracted features.
    :return: Final score (float).
    """
    # Define the weights for each feature based on the paper or other information
    weights = {
        'iou1': 1.94064354,
        'iou2': 6.51982931,
        'similar1': -0.96069589,
        'similar2': 4.23679642,
        'keyavg': 1.0,  # The weight for keyavg needs to be defined
    }

    # Calculate the weighted sum of the features to get the final score
    score = sum(weights[feature] * value for feature, value in features.items())

    # Subtract a constant value
    score -= 2.637720298361252

    return score
