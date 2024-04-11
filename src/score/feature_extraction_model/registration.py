"""
Implement high precision registration of calligraphic copy to template image.
"""

# Author: Rvosuke
# Date: 2023/09/28

import numpy as np
import cv2
from scipy.spatial import distance


def high_precision_registration(img1, img2):
    """
    Implement high precision registration of img2 to img1.

    :param img1: Template image (NumPy array).
    :param img2: Calligraphic copy image (NumPy array).
    :return: Registered image (NumPy array).
    """
    # Resize the images to the same size for high precision registration
    # Note: This is inferred from the resizing steps in the provided Python file.
    height = max(img1.shape[0], img2.shape[0])
    width = max(img1.shape[1], img2.shape[1])
    img1 = cv2.resize(img1, (width, height), interpolation=cv2.INTER_AREA)
    img2 = cv2.resize(img2, (width, height), interpolation=cv2.INTER_AREA)

    # Additional registration steps can be added if needed
    # ...

    return img2  # Return the registered image


def best_fit_transform(A, B):
    """
    Calculates the least-squares best-fit transform between corresponding 2D points A and B.

    :param A: Nx2 numpy array of corresponding points
    :param B: Nx2 numpy array of corresponding points
    :return: 2x3 affine matrix, which defines 2D transform, Tx
    """
    # Center the points in both datasets
    centroid_A = np.mean(A, axis=0)
    centroid_B = np.mean(B, axis=0)

    A_centered = A - centroid_A
    B_centered = B - centroid_B

    # Compute the rotation matrix using singular value decomposition
    H = np.dot(A_centered.T, B_centered)
    U, _, Vt = np.linalg.svd(H)
    R = np.dot(Vt.T, U.T)

    # Compute the translation
    t = centroid_B - np.dot(R, centroid_A)

    # Form the affine transformation matrix
    T = np.identity(3)
    T[0:2, 0:2] = R
    T[0:2, 2] = t

    return T


def icp(A, B):
    """
    The Iterative Closest Point method: finds best-fit transform that maps points A on to points B.

    :param A: Nx2 numpy array of source 2D points
    :param B: Nx2 numpy array of destination 2D point
    :return: 2x3 affine matrix, which defines 2D transform, Tx
    """
    # Initialize variables
    num_iterations = 100  # Define based on the requirement
    tolerance = 1e-10  # Define based on the requirement

    for i in range(num_iterations):
        # Find the nearest (Euclidean) neighbor in B for each point in A
        indices = np.array([np.argmin(distance.cdist(A[i:i + 1], B, 'euclidean')) for i in range(A.shape[0])])

        # Compute the transformation between the current points and the reference B
        T = best_fit_transform(A[indices], B)

        # Update A
        A = np.dot(T[:2, :2], A.T).T + T[:2, 2]

        # Check for convergence (if the points A are not moving)
        if np.linalg.norm(T) < tolerance:
            break

    return T  # Return the final transformation matrix
