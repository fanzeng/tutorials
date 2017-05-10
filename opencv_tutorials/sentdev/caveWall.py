import cv2
import numpy as np
import caveWallPrep

cap = cv2.VideoCapture('Truck Driving in a Cave.mp4')

count = 0

while count < 10:
    ret, frame = cap.read()
    count += 1
    res = caveWallPrep.prep(frame)

    # edges = cv2.Canny(res, 0, 20, 200)
    # edges = cv2.GaussianBlur(edges, (15, 15), 0)
    lines = cv2.HoughLinesP(res, 5, 2*np.pi/180, 10, minLineLength = 20, maxLineGap = 15)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]
            theta = np.arctan2(y2 - y1, x2 - x1) * 180 / np.pi
            if np.abs(theta) >80:
                cv2.line(frame, (x1, y1), (x2, y2), (255, 0, 0), 1)
    else:
        print 'No line detected.'

    # cv2.imshow('edges', edges)
    cv2.imshow('frame', frame)
    cv2.waitKey(0)

cap.release()
cv2.destroyAllWindows()
