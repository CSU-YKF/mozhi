# Author: Rvosuke
# Date: 2023-11-17
# Reference: SRAFE: Siamese Regression Aesthetic Fusion Evaluation for Chinese Calligraphic Copy
# (https://doi.org/10.1049/cit2.12095)


import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from scipy.spatial import ConvexHull
from skimage.feature import canny
from skimage.transform import hough_line, hough_line_peaks, rotate


def f1_f2_score(handwrite_bin, template_bin):
    # Calculate the areas (number of black pixels)
    A_C = np.sum(handwrite_bin)
    A_T = np.sum(template_bin)

    # Calculate the overlapping area
    A_CT_overlap = np.sum(handwrite_bin & template_bin)

    f1 = A_CT_overlap / (A_C + A_T - A_CT_overlap)


    f2 = 10 * f1 * (2 - f1)
    return f1, f2, A_C, A_T, A_CT_overlap


def f3_score(handwrite_bin, template_bin):
    # Calculate the convex hull areas for C and T
    S_C_convex_hull_area = calculate_convex_hull_area(handwrite_bin)
    S_T_convex_hull_area = calculate_convex_hull_area(template_bin)

    # Calculate the overlapping area of the convex hulls
    # For the overlapping area, we need to calculate the convex hull of the overlap
    # First, we take the logical AND of the binarized images to get the overlap
    overlap_bin = handwrite_bin & template_bin

    # Then, calculate the convex hull area of the overlapping region
    S_CT_convex_hull_overlap_area = calculate_convex_hull_area(overlap_bin)

    # Calculate f3 score
    f3 = S_CT_convex_hull_overlap_area / (S_C_convex_hull_area + S_T_convex_hull_area - S_CT_convex_hull_overlap_area)

    return f3, S_C_convex_hull_area, S_T_convex_hull_area, S_CT_convex_hull_overlap_area


def f4_f11_score(handwrite_bin, template_bin):
    # Angles for the 'mizi' grid
    angles = [0, -45, 45, 90]

    # Calculate histograms for all angles and their f4 and f5 scores
    f_scores = {}
    for idx, angle in enumerate(angles):
        HT = calculate_projection_histogram(template_bin, angle)
        HC = calculate_projection_histogram(handwrite_bin, angle)
        f4 = calculate_histogram_overlapping_ratio(HT, HC)
        f5 = calculate_histogram_correlation(HT, HC)
        f_scores[f"f{4 + idx * 2}"] = f4
        f_scores[f"f{5 + idx * 2}"] = f5

    return f_scores


# Define a function to calculate the convex hull of the binarized image
def calculate_convex_hull_area(binary_image):
    # Extract the coordinates of the black pixels
    points = np.column_stack(np.where(binary_image > 0))
    # Calculate the convex hull
    if len(points) >= 3:  # Convex hull is only defined for 3 or more points
        hull = ConvexHull(points)
        # Return the area of the convex hull
        return hull.volume
    else:
        # If there are less than 3 points, the convex hull area is 0
        return 0


# Define a function to calculate histogram projection
def calculate_projection_histogram(binary_image, angle):
    # Rotate image for the given angle
    rotated_image = rotate(binary_image, angle, resize=True) > 0
    # Sum over columns to get the histogram
    histogram = np.sum(rotated_image, axis=0)
    return histogram


# Define a function to calculate the overlapping ratio of histograms
def calculate_histogram_overlapping_ratio(hist1, hist2):
    # Using minima of histograms for intersection and sum for union
    intersection = np.sum(np.minimum(hist1, hist2))
    union = np.sum(hist1) + np.sum(hist2) - intersection
    return intersection / union


# Define a function to calculate correlation between histograms
def calculate_histogram_correlation(hist1, hist2):
    # Mean of the histograms
    mean1 = np.mean(hist1)
    mean2 = np.mean(hist2)
    # Correlation calculation
    numerator = np.sum((hist1 - mean1) * (hist2 - mean2))
    denominator = np.sqrt(np.sum((hist1 - mean1) ** 2) * np.sum((hist2 - mean2) ** 2))
    # To prevent division by zero
    if denominator == 0:
        return 0
    return numerator / denominator


def main():
    # Load the images
    handwrite_path = 'handwrite.png'
    template_path = 'li_pre.png'
    handwrite_img = Image.open(handwrite_path).convert("L")
    template_img = Image.open(template_path).convert("L")

    # Binarize the images
    # Assuming that the background is white and the character is black
    threshold = 128
    handwrite_bin = (np.array(handwrite_img) < threshold).astype(int)
    template_bin = (np.array(template_img) < threshold).astype(int)
    f1, f2, A_C, A_T, A_CT_overlap = f1_f2_score(handwrite_bin, template_bin)
    f3, S_C_convex_hull_area, S_T_convex_hull_area, S_CT_convex_hull_overlap_area = f3_score(handwrite_bin, template_bin)
    f4_f11 = f4_f11_score(handwrite_bin, template_bin)
    f = {'f1': f1, 'f2': f2, 'f3': f3, 'f4': f4_f11['f4'], 'f5': f4_f11['f5'], 'f6': f4_f11['f6'], 'f7': f4_f11['f7'],
         'f8': f4_f11['f8'], 'f9': f4_f11['f9'], 'f10': f4_f11['f10'], 'f11': f4_f11['f11']}
    print(f)


if __name__ == '__main__':
    main()
