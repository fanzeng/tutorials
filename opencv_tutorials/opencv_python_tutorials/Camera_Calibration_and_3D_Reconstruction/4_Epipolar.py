import cv2
import numpy as np
from matplotlib import pyplot as plt

print 'This script might not work for some versions of opencv.'
print 'It\'s been verified to work for opencv 3.3.1.11.'
print 'Note: Does not work with lower versions like 3.1.0 or higher versions 4.1.2'
print 'The main issue is that SIFT features used in the script are not free.'
print 'And this is not a problem of the script itself or opencv.'
print 'If you see errors below, please consider running it with a compatible opencv verion.'
print 'Easist way is to create a virtualenv, then'
print 'pip install opencv-contrib-python==3.3.1.11'
print 'pip install opencv-python==3.3.1.11'
print 'pip install matplotlib'
print 'tested with python==2.7.17, and pip==20.0.1'
print

img1 = cv2.imread('../../samples/left.jpg', 0) # queryimage # left image
img2 = cv2.imread('../../samples/right.jpg', 0) # queryimage  # right image

print 'img1.shape =', img1.shape
print 'img2.shape =', img2.shape

sift = cv2.xfeatures2d.SIFT_create()

# find the keypoints and descriptors with SIFT
kp1, des1 = sift.detectAndCompute(img1, None)
kp2, des2 = sift.detectAndCompute(img2, None)

# FLANN parameters
FLANN_INDEX_KDTREE = 1
index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
search_params = dict(checks = 50)

flann = cv2.FlannBasedMatcher(index_params, search_params)

matches = flann.knnMatch(des1, des2, k = 2)

good = []
pts1 = []
pts2 = []
goodmatches = []

# ratio test as per Lowe's paper
for i, (m, n) in enumerate(matches):
    if m.distance < 0.8 * n.distance:
        good.append(m)
        pts2.append(kp2[m.trainIdx].pt)
        pts1.append(kp1[m.queryIdx].pt)
        goodmatches.append(matches[i])

imgmatch = cv2.drawMatchesKnn(img1, kp1, img2, kp2, goodmatches[:], None)
plt.imshow(imgmatch)

pts1 = np.int32(pts1)
pts2 = np.int32(pts2)
F, mask = cv2.findFundamentalMat(pts1, pts2, cv2.FM_LMEDS)
print F

# We select only inlier points
pts1 = pts1[mask.ravel()==1]
pts2 = pts2[mask.ravel()==1]


def drawlines(img1, img2, lines, pts1, pts2):
    '''img1 - image on which we draw the epilines for the points in img2
       lines - corresponding epilines'''
    _, c = img1.shape
    img1 = cv2.cvtColor(img1, cv2.COLOR_GRAY2BGR)
    img2 = cv2.cvtColor(img2, cv2.COLOR_GRAY2BGR)
    for line, pt1, pt2 in zip(lines, pts1, pts2):
        color = tuple(np.random.randint(0, 255, 3).tolist())
        x0, y0 = map(int, [0, -line[2] / line[1]])
        x1, y1 = map(int, [c, -(line[2] + line[0] * c) / line[1]])
        img1 = cv2.line(img1, (x0, y0), (x1, y1), color, 1)
        img1 = cv2.circle(img1, tuple(pt1), 5, color, -1)
        img2 = cv2.circle(img2, tuple(pt2), 5, color, -1)
    return img1, img2

# Find the epilines corresponding to points in right image (second image) and
# drawing its lines on the left image
lines1 = cv2.computeCorrespondEpilines(pts2.reshape(-1, 1, 2), 2, F)
lines1 = lines1.reshape(-1, 3)
img5, img6  = drawlines(img1, img2, lines1, pts1, pts2)

# Find the epilines corresponding to points in left image (first image) and
# drawing its lines on the right image
lines2 = cv2.computeCorrespondEpilines(pts1.reshape(-1, 1, 2), 1, F)
lines2 = lines2.reshape(-1, 3)
img3, img4  = drawlines(img2, img1, lines2, pts2, pts1)

plt.subplot(1, 2, 1), plt.imshow(img5)
plt.subplot(1, 2, 2), plt.imshow(img3)
plt.show()