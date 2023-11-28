from PIL import Image
import numpy as np
import cv2

li = Image.open('li.png')
li = li.resize((224, 224))

# 将图片转化为RGB图片
li = li.convert('RGB')
# 取出图像的RGB值
r, g, b = li.split()
r = np.array(r)
li = np.array(li)
# 将图像的R通道置零
li[:, :, 0] = 0

li = cv2.cvtColor(li, cv2.COLOR_RGB2GRAY)
li = cv2.medianBlur(li, 5)
# li = cv2.GaussianBlur(li, (5, 5), 0)
ret, li = cv2.threshold(li, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
# skel = np.zeros_like(li)
# while True:
#     # Erode the image
#     eroded = cv2.erode(li, element)
#     # Dilate the eroded image
#     temp = cv2.dilate(eroded, element)
#     # Subtract the temp from the original image
#     temp = cv2.subtract(li, temp)
#     # Or with the skeleton
#     skel = cv2.bitwise_or(skel, temp)
#     li = eroded.copy()
#     cv2.waitKey()
#
#     # If the image is fully eroded, break
#     if cv2.countNonZero(li) == 0:
#         break
# 显示图像
li = Image.fromarray(li)
li.show()
# li.save('li_pre.png')
