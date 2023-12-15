import cv2
import skimage as ski
import numpy as np

from imutils.contours import sort_contours


def character_color_segmentation(image_input):
	"""
	Segment the ink in the picture and complete the binarization at the same time.

	:param image_input: a RGB image
	:return: a binary image
	"""
	# Define the range of character in HSV space
	# Note: The range of hue in HSV is 0 to 1.
	image_hsv = ski.color.rgb2hsv(image_input)
	center_hsv = [0, 0, 0.1]
	# the hand written character is black, so we only need to consider the saturation and value
	distances = np.linalg.norm(center_hsv[1:3] - image_hsv[:,:,1:3], axis=2)
	thresh = ski.filters.threshold_otsu(distances)
	mask = distances < thresh
	image_hsv[mask] = [0, 0, 0]
	image_hsv[~mask] = [0, 0, 1]

	image_rgb = ski.color.hsv2rgb(image_hsv)
	image_rgb = ski.util.img_as_ubyte(image_rgb)
	image_rgb = ~image_rgb

	image_gray = np.mean(image_rgb, axis=2)
	right_inclined = np.array([[0, 1, 1],[0, 1, 0],[1, 1, 0]], dtype='uint8')
	# selem = ski.morphology.disk(3)
	image_output = ski.morphology.closing(image_gray, right_inclined)

	return image_output


def skeleton_endpoints(skel):
    # Function source: https://stackoverflow.com/questions/26537313/
    # how-can-i-find-endpoints-of-binary-skeleton-image-in-opencv
    # make out input nice, possibly necessary
    skel = skel.copy()
    skel[skel != 0] = 1
    skel = np.uint8(skel)

    # apply the convolution
    kernel = np.uint8([[1,  1, 1],
                       [1, 10, 1],
                       [1,  1, 1]])
    src_depth = -1
    filtered = cv2.filter2D(skel, src_depth,kernel)

    # now look through to find the value of 11
    # this returns a mask of the endpoints, but if you just want the coordinates, 
    # you could simply return np.where(filtered==11)
    out = np.zeros_like(skel)
    out[np.where(filtered == 11)] = 1
    rows, cols = np.where(filtered == 11)
    coords = list(zip(cols, rows))
    return coords


# def endpoints(th, contours):



def main():
	filename = 'handwrite'
	character = ski.io.imread(filename+'.png')
	character = ski.transform.resize(character, (224, 224))
	
	# if the image is RGBA, we need to convert it to RGB first
	if character.shape[-1] == 4:
		character = ski.color.rgba2rgb(character)
	character = character_color_segmentation(character)
	skeleton = ski.morphology.skeletonize(character)
	skeleton = ski.util.img_as_ubyte(skeleton)

	contours, _ = cv2.findContours(skeleton.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	contours, _ = sort_contours(contours, )
	# List for endpoints and (x, y) coordinates of the skeletons
	endpoints, skeletons = [], []

	for contour in contours:
	    if cv2.arcLength(contour, True) > 100:
	        # Initialize mask
	        mask = np.zeros(character.shape, np.uint8)  # 这里可能需要原始图像的shape
	        # Bounding rect of the contour
	        x, y, w, h = cv2.boundingRect(contour)
	        mask[y:y+h, x:x+w] = 255
	        # Get only the skeleton in the mask area
	        mask = cv2.bitwise_and(mask, skeleton)
	        # Take the coordinates of the skeleton points
	        rows, cols = np.where(mask == 255)
	        # Add the coordinates to the list
	        skeletons.append(list(zip(cols, rows)))

	        # Find the endpoints for the shape and update a list
	        eps = skeleton_endpoints(mask)
	        endpoints.append(eps)

	        # Draw the endpoints
	        [cv2.circle(skeleton, ep, 7, 255, 1) for ep in eps]
	        # cv2.imshow('mask', mask)
	        # cv2.waitKey(500)


	# ski.io.imshow(skeleton)
	# ski.io.show()
	# cv2.imshow('mask', skeleton)
	# cv2.waitKey(0)
	# cv2.destroyAllWindows()
	ski.io.imsave(f'{filename}_skeleton.png', skeleton)

if __name__ == '__main__':
	main()
# RIGHT_INCLINED = np.array([[0, 1, 1],[0, 1, 0],[1, 1, 0]], dtype='uint8')
# character = threshold(character)
# character = closing(character, RIGHT_INCLINED)
# img = ski.filters.gaussian(character, sigma=3)
# # img = ski.transform.resize(character, (224, 224))
# _, thresh = threshold(img)
