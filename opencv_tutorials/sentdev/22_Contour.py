import cv2
import numpy as np

img = cv2.imread('watch.jpg')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, threshold = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
cv2.imshow('threshold', threshold)
im2, contours, hierarchy = cv2.findContours(threshold,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
print contours
cv2.drawContours(img, contours, -1, (0,255,0), 3)
cv2.imshow('contour', img)
cv2.waitKey()

cv2.destroyAllWindows()