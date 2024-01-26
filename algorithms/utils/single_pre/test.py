import numpy as np
import matplotlib.pyplot as plt
import skimage as ski
# 读取图像或创建一个空白图像
image = np.zeros((100, 100, 3), dtype=np.uint8)

# 定义圆的中心和半径
center = (7, 0)
radius = 7

# 使用skimage.draw绘制圆
rr, cc = ski.draw.circle_perimeter(center[0], center[1], radius)
image[rr, cc] = 255
image[0, 10] = 255
ski.io.imshow(image)
plt.show()