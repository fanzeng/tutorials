import cv2
import numpy as np


img = cv2. imread('pillars.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
template = cv2.imread('pillarBody.jpg', cv2.IMREAD_GRAYSCALE)
h, w = template.shape
res = cv2.matchTemplate(gray, template, cv2.TM_CCOEFF_NORMED)
cv2.imshow('res', res)
threshold = 0.6
loc = np.where(res > threshold)
for pt in zip(*loc):
    cv2.rectangle(img, pt, (pt[0]+w, pt[1]+h), (0, 255, 255), 1)
    cv2.imshow('img', img)
    cv2.waitKey()
cv2.imshow('template', template)
cv2.waitKey()
cv2.destroyAllWindows()