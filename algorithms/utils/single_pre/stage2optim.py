from skimage import io, morphology, measure, util
import numpy as np
from scipy import ndimage
from scipy.spatial.distance import cdist

# Define utility functions
def draw_line(p1, p2):
    """Generate the coordinates of a line from p1 to p2 using Bresenham's algorithm"""
    # Setup initial conditions
    x1, y1 = p1
    x2, y2 = p2
    dx = x2 - x1
    dy = y2 - y1

    # Determine how steep the line is
    is_steep = abs(dy) > abs(dx)

    # Rotate line
    if is_steep:
        x1, y1 = y1, x1
        x2, y2 = y2, x2

    # Swap start and end points if necessary and store swap state
    swapped = False
    if x1 > x2:
        x1, x2 = x2, x1
        y1, y2 = y2, y1
        swapped = True

    # Recalculate differentials
    dx = x2 - x1
    dy = y2 - y1

    # Calculate error
    error = int(dx / 2.0)
    ystep = 1 if y1 < y2 else -1

    # Iterate over bounding box generating points between start and end
    y = y1
    points = []
    for x in range(x1, x2 + 1):
        coord = (y, x) if is_steep else (x, y)
        points.append(coord)
        error -= abs(dy)
        if error < 0:
            y += ystep
            error += dx

    # Reverse the list if the coordinates were swapped
    if swapped:
        points.reverse()
    return points

def is_line_on_skeleton(p1, p2, skel):
    """Check if a line between two points lies entirely on the skeleton."""
    line = draw_line(p1, p2)
    return all(skel[x, y] for x, y in line)

# Load the images
original_image_path = 'segmentation.png'
skeleton_image_path = 'li_skeleton.png'

original_image = io.imread(original_image_path, as_gray=True)
skeleton_image = io.imread(skeleton_image_path, as_gray=True)

# Threshold the images
original_image = (original_image > 0.5).astype(np.uint8)
skeleton_image = (skeleton_image > 0.5).astype(np.uint8)

# Calculate the width of the font
N_S = np.sum(skeleton_image)
N_O = np.sum(original_image)
W_f = N_S / (2.0 * N_O)

# Label endpoints on the skeleton
def skeleton_endpoints(skel):
    # Apply endpoint kernel to skeleton
    endpoint_kernel = np.array([[1, 1, 1],
                                [1, 10, 1],
                                [1, 1, 1]])
    filtered = ndimage.convolve(skel, endpoint_kernel, mode='constant', cval=1)
    return np.transpose(np.nonzero(filtered == 11))

# Extract endpoints from the skeleton
endpoints = skeleton_endpoints(skeleton_image)

# Function to get the neighborhood of a point
def get_neighborhood(point, distance, shape):
    """Return a list of points forming a square (neighborhood) around a point."""
    x, y = point
    x_min = max(x - distance, 0)
    x_max = min(x + distance + 1, shape[0])
    y_min = max(y - distance, 0)
    y_max = min(y + distance + 1, shape[1])
    return [(i, j) for i in range(x_min, x_max) for j in range(y_min, y_max)]

# Function to determine if a point is a T-junction
def is_T_junction(point, skel, endpoints, distance):
    """Check if a point is a T-junction."""
    neighborhood = get_neighborhood(point, distance, skel.shape)
    count = 0
    for neighbor in neighborhood:
        if neighbor in endpoints and is_line_on_skeleton(point, neighbor, skel):
            count += 1
    return count >= 3

# Detect T-junctions in the skeleton
T_junctions = [point for point in endpoints if is_T_junction(point, skeleton_image, endpoints, int(W_f))]

# Display the results
print(f"Width of the font (W_f): {W_f}")
print(f"Number of endpoints: {len(endpoints)}")
print(f"Detected T-junctions: {len(T_junctions)}")
T_junctions[:5] 
