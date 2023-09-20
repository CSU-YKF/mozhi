"""
Corrects orientation and shape distortions in an image. Typically, this can be achieved through a perspective transform.
The perspective transform requires four points as input, which are the corner points of the region you wish to correct.
We then need another four points to define the corner points of the output image.
Since the image is a word post, we can choose the intersection of the four corners as the input points.
"""

# Author: Rvosuke
# Date: 2023/09/20

import cv2
import numpy as np
from matplotlib import pyplot as plt


# 利用边角检测进行透视变换的装饰器
def withAngleDetection(fn):
    def wrapper(input_image):
        points = angleDetection(input_image)
        if points is not None:
            return fn(input_image, points)
        else:
            print("Skipping perspective transform due to insufficient points.")
            return input_image

    return wrapper


def angleDetection(input_image):
    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)  # 将图像转换为灰度图
    blurred_image = cv2.GaussianBlur(gray_image, (5, 5), 0)  # 对图像应用高斯模糊

    # 对图像进行阈值处理得到二值图像
    _, thresh_image = cv2.threshold(blurred_image, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    contours, _ = cv2.findContours(thresh_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)  # 查找轮廓
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:1]  # 按面积从大到小排序，保留最大的等值线

    # 将轮廓近似为多边形
    epsilon = 0.05 * cv2.arcLength(contours[0], True)
    approx = cv2.approxPolyDP(contours[0], epsilon, True)

    # 检查我们是否有 4 个透视转换点
    if len(approx) == 4:
        print("Successfully detected 4 points for perspective transformation.")
        return approx
    else:
        print(f"Could not detect 4 points for perspective transformation. Detected points: {len(approx)}")
        return None


@withAngleDetection
def perspectiveTransform(input_image, points):
    # 定义透视变换的点（按特定顺序排列）
    rect = np.zeros((4, 2), dtype="float32")
    s = points.sum(axis=2)
    rect[0] = points[np.argmin(s)]  # 左上角点的和最小
    rect[2] = points[np.argmax(s)]  # 右下角点的总和最大
    diff = np.diff(points, axis=2)
    rect[1] = points[np.argmin(diff)]  # 右上角的差异最小
    rect[3] = points[np.argmax(diff)]  # 左下角的差异最大

    # 新转换图像的尺寸
    (tl, tr, br, bl) = rect
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    maxHeight = max(int(heightA), int(heightB))

    # 尺寸增加 5% 以确保我们不会丢失任何信息
    maxWidth = int(maxWidth * 1.05)
    maxHeight = int(maxHeight * 1.05)

    # 调整透视变换的目标点
    dst = np.array([
        [0 + maxWidth * 0.025, 0 + maxHeight * 0.025],
        [maxWidth - 1 - maxWidth * 0.025, 0 + maxHeight * 0.025],
        [maxWidth - 1 - maxWidth * 0.025, maxHeight - 1 - maxHeight * 0.025],
        [0 + maxWidth * 0.025, maxHeight - 1 - maxHeight * 0.025]], dtype="float32")

    # 计算透视变换矩阵并应用
    M = cv2.getPerspectiveTransform(rect, dst)
    warped = cv2.warpPerspective(input_image, M, (maxWidth, maxHeight))
    return warped


if __name__ == '__main__':
    image = cv2.imread('../src/data/7.jpg')
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    warped_image = perspectiveTransform(image, )

    plt.figure(figsize=(10, 10))
    plt.title('Perspective Transformed Image')
    plt.imshow(warped_image)
    plt.axis('off')
    plt.show()
