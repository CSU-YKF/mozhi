"""
Local Mean Brightness Matching (LMBM) is usually performed by subtracting the local mean brightness.
This adjusts the brightness of different areas of the image to make it more consistent.
In the following, I will try to use this method to design a function to correct the local brightness of an image.
"""

# Author: Rvosuke
# Date: 2023/09/20

import cv2
import numpy as np
from matplotlib import pyplot as plt


# 执行局部平均亮度匹配的函数
def localMeanBrightnessMatching(image, kernel_size=(50, 50)):
    # 将图像转换为 float32，以提高精度
    image_float = image.astype('float32')

    # 使用核计算图像的局部平均值
    local_mean = cv2.boxFilter(image_float, ddepth=-1, ksize=kernel_size)

    # 从原始图像中减去局部平均值
    brightness_matched = image_float - local_mean + 255  # 添加 255 使像素值居中

    # 在 [0, 255] 范围内剪切数值
    brightness_matched = np.clip(brightness_matched, 0, 255).astype('uint8')
    brightness_matched[brightness_matched < local_mean] = 0
    return brightness_matched


if __name__ == '__main__':
    original_image = cv2.imread('../../dataset/test_data/7.jpg')
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)
    # 对图像进行局部平均亮度匹配
    brightness_matched_image = localMeanBrightnessMatching(original_image)

    # 显示原始图像和亮度匹配图像
    plt.figure(figsize=(10, 10))

    plt.title('Brightness Matched')
    plt.imshow(brightness_matched_image)
    plt.axis('off')

    plt.show()
