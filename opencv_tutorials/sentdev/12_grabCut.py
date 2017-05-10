import cv2
import numpy as np
import matplotlib.pyplot as plt

img = cv2.imread('opencv-python-foreground-extraction-tutorial.jpg')
mask = np.zeros(img.shape[:2], np.uint8)

bgdModel = np.zeros((1, 65), np.float64)
fgdModel = np.zeros((1, 65), np.float64)

rect = (161, 79, 150, 150)
cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
# 0, 2: bg; 1, 3: fg
mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
img = img * mask2[:, :, np.newaxis]

#
# cv2.rectangle(img, (161, 79), (161 + 150, 161 + 150), (255, 255, 255), 2)
# cv2.imshow('img', img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

plt.imshow(img)
plt.colorbar()
plt.show()

