import numpy as np
import cv2
import matplotlib.pyplot as plt

input_image = cv2.imread('moon.png')
input_image = input_image[:,:,::-1]
print('input_image', input_image.shape, input_image.dtype, input_image.min(), input_image.max())

plt.figure()
plt.imshow(input_image)
plt.show()
