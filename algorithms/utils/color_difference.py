"""
Calculate colour channel differences:
It is possible to calculate the difference between the red channel and the blue and green channels.
Theoretically, this difference should be greater for borderlines (mainly red).
"""

# Author: Rvosuke
# Date: 2023/09/20

import cv2
import matplotlib.pyplot as plt
import numpy as np


def colorDifference(input_image):
    # 从图像中提取通道
    red_channel = input_image[:, :, 0]
    green_channel = input_image[:, :, 1]
    blue_channel = input_image[:, :, 2]

    # 计算红色通道与绿色和蓝色通道平均值之间的差值
    color_difference = red_channel.astype(int) * 2 - (green_channel.astype(int) + blue_channel.astype(int))
    color_difference = np.clip(color_difference, 0, 255).astype('uint8')

    return color_difference


if __name__ == '__main__':
    from lmb_matching import localMeanBrightnessMatching
    from perspective_shift import perspectiveTransform
    # Load the new uploaded image
    image_path = '../dataset/test_data/4-2.png'
    original_image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    original_image = cv2.cvtColor(original_image, cv2.COLOR_BGR2RGB)

    original_image = localMeanBrightnessMatching(original_image)
    original_image = perspectiveTransform(original_image)

    color_difference = colorDifference(original_image)

    # 应用阈值来突出红色通道明显强于其他通道的区域

    plt.figure(figsize=(15, 15))
    plt.title('color_difference')
    plt.imshow(color_difference, cmap='gray')
    plt.axis('off')
    plt.show()
