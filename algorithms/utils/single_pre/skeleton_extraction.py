import cv2
import sys
import skimage as ski
import numpy as np

from imutils.contours import sort_contours
from sklearn.cluster import DBSCAN


sys.setrecursionlimit(1000000)

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
	image_output = np.uint8(image_output)
	# image_output = ski.util.img_as_ubyte(image_output)
	ski.io.imsave('segmentation.png', image_output)

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
	src_depth = -1  # this means cv2.CV_16S
	filtered = cv2.filter2D(skel, src_depth, kernel)

	# now look through to find the value of 11
	# this returns a mask of the endpoints, but if you just want the coordinates, 
	# you could simply return np.where(filtered==11)
	out = np.zeros_like(skel)
	out[np.where(filtered == 11)] = 1
	rows, cols = np.where(filtered == 11)
	coords = list(zip(cols, rows))
	out = np.zeros_like(skel)
	out[np.where(filtered == 10)] = 1
	rows, cols = np.where(filtered == 10)
	coords.extend(list(zip(cols, rows)))

	cross = np.zeros_like(skel)
	cross[np.where(filtered >= 13)] = 1
	rows, cols = np.where(filtered >= 13)
	cross_coords = list(zip(cols, rows))
	# coords.extend(cross_coords)
	return coords, cross_coords


def point_cluster(points, points_clusters_label):
	points = np.array(points, dtype=np.float32)

	# 初始化一个字典来存储每个类别的交叉点坐标和计数
	clusters = {}

	# 遍历每个点及其类别标签
	for point, label in zip(points, points_clusters_label):
		# 跳过噪声点（DBSCAN中标签为-1的点）
		if label == -1:
			continue
		
		# 如果类别标签在字典中不存在，则初始化
		if label not in clusters:
			clusters[label] = {"sum": np.zeros_like(point), "count": 0}
		
		# 累加同类别点的坐标并计数
		clusters[label]["sum"] += point
		clusters[label]["count"] += 1

	# 计算每个类别的平均坐标
	new_points = []
	for label in clusters:
		average_point = clusters[label]["sum"] / clusters[label]["count"]
		new_points.append(average_point)

	# new_cross 现在包含了每个聚类的平均坐标点
	new_points = np.array(new_points, dtype=np.int32)
	return new_points


def keypoints_search(contours, skeleton, src):
	dbscan = DBSCAN(eps=14, min_samples=1)
	contours, _ = sort_contours(contours, )
	# List for endpoints and (x, y) coordinates of the skeletons
	endpoints, crosspoints, skeletons = [], [], []
	points_ls = []

	for contour in contours:
		if cv2.arcLength(contour, True) > 10:
			# Initialize mask
			mask = np.zeros(skeleton.shape, np.uint8)  # 这里可能需要原始图像的shape
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
			eps, cross = skeleton_endpoints(mask)
			points = eps + cross
			points_ls.extend(points)

	points_clusters_label = dbscan.fit_predict(points_ls)
	points = point_cluster(points_ls, points_clusters_label)

	return points


def find_white_neighbors(img, x, y, visited):
	directions = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
	neighbors = []
	for dx, dy in directions:
		nx, ny = x + dx, y + dy
		directions = [(dx, dy), ()]
		if 0 <= nx < img.shape[0] and 0 <= ny < img.shape[1] and (nx, ny) not in visited:
			if img[nx, ny] != 0:  # 检查是否为白色像素
				neighbors.append((nx, ny))
	return neighbors


def dfs(img, point, points, visited):
	x, y = point
	if tuple(point) in visited or img[x, y] == 0:
		return None
	visited.add(tuple(point))  # 将当前点标记为访问过
	neighbors = find_white_neighbors(img, x, y, visited)
	for neighbor in neighbors:
		if tuple(neighbor) != tuple(point) and neighbor in points:
			return neighbor
		result = dfs(img, neighbor, points, visited)
		if result:
			return result


def connect_check(img, points):
	connected_points = []
	for point in points:
		visited = set()  # 记录访问过的像素点
		result = dfs(img, point, points, visited)
		if result:
			connected_points.append((point, result))
	return connected_points


def main():
	filename = '23'
	character = ski.io.imread(filename+'.png')
	character = ski.transform.resize(character, (224, 224))
	
	# if the image is RGBA, we need to convert it to RGB first
	if character.shape[-1] == 4:
		character = ski.color.rgba2rgb(character)
	character = ski.util.img_as_ubyte(character)
	character_bi = character_color_segmentation(character)
	character_edge = ski.feature.canny(character_bi, sigma=3)

	skeleton = ski.morphology.skeletonize(character_bi)
	skeleton = ski.util.img_as_ubyte(skeleton)
	# ski.io.imsave(f'{filename}_skeleton.png', skeleton)

	contours, _ = cv2.findContours(skeleton.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
	points = keypoints_search(contours, skeleton, character_bi)

		
	# connected_points = connect_check(character, points)
	# print("Connected points:", connected_points, len(connected_points))

	# 定义有效区域的掩码（二值化图像中白色区域）
	mask = character_bi == 0
	[cv2.circle(character, p, 8, 255, -1) for p in points]
	[cv2.circle(skeleton, p, 8, 225, 1) for p in points]
	character[mask] = 255
	character = character.astype(np.uint8)
	# 保存或显示图像
	ski.io.imsave(f'{filename}_points.png', character)
	ski.io.imsave(f'{filename}_sk.png', skeleton)
if __name__ == '__main__':
	main()
