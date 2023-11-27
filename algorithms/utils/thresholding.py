"""
This is a Python script that does thresholding.
"""

# Author: Rvosuke
# Date: 2023/09/19

import cv2
import os
from matplotlib import pyplot as plt


def thresholding(input_image):
    _, thresholded = cv2.threshold(input_image.astype('uint8'), 10, 255, cv2.THRESH_BINARY)

    # 对结果进行形态学处理
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
    thresholded = cv2.morphologyEx(thresholded, cv2.MORPH_OPEN, kernel)
    tws = input_image.shape[1] // 30
    sws = tws * 3
    thresholded = cv2.fastNlMeansDenoising(thresholded, None, tws, tws, sws)

    return thresholded


# 构建相对路径
relative_path = os.path.join('..', 'src', 'test_data', '2.png')
absolute_path = os.path.abspath(relative_path)

# 检查文件是否存在
if os.path.exists(absolute_path):
    print(f"File exists at {absolute_path}")
else:
    print(f"File does not exist. Checked at {absolute_path}")

# 读取图像
image_origin = cv2.imread(relative_path)

# # 显示图像（仅作测试）
# cv2.imshow('image_origin', image_origin)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
