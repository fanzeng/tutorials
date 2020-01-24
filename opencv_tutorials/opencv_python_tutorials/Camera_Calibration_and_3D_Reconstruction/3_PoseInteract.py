import numpy as np
import cv2
import glob
import os
import time

print 'to collect new chessboard image samples, uncomment the corresponding line in the script.'
print 'otherwise, sample images will be used.'
print

def gather_sample():
    cap = cv2.VideoCapture(0)
    for i in range(1, 10):
        ret, img = cap.read()
        time.sleep(1)
        cv2.imwrite(sample_path + str(i).zfill(2) + '.jpg', img)
    cap.release()

def calibrate():
    #termination criteria
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    #prepare object points, like (0, 0, 0), (1, 0, 0), (2, 0, 0), ..., (6, 5, 0)
    objp = np.zeros((chessboard_size[0]*chessboard_size[1], 3), np.float32)
    objp[:, :2] =np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images
    objpoints = [] # 3d point in real world space
    imgpoints = [] # 2d poitns in image plane

    images = glob.glob(sample_path + '*.jpg')

    for fname in images:
        img = cv2.imread(fname)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Find the chess board corners
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, chessboard_size, corners, ret)
        cv2.imshow('img', img)
        cv2.waitKey(100)
    cv2.destroyAllWindows()

    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)
    ##print 'ret =', ret
    print 'mtx =', mtx
    print 'dist =', dist
    ##print 'rvecs =', rvecs
    ##print 'tvecs =', tvecs
    np.savez('./B.npz', mtx = mtx, dist = dist, rvecs = rvecs, tvecs = tvecs)

def draw(img, corners, imgpts):
    corner = tuple(corners[0].ravel())
    img = cv2.line(img, corner, tuple(imgpts[0].ravel()), (255, 0, 0), 2)
    img = cv2.line(img, corner, tuple(imgpts[1].ravel()), (0, 255, 0), 2)
    img = cv2.line(img, corner, tuple(imgpts[2].ravel()), (0, 0, 255), 2)
    return img

def interact(grid_size):
    with np.load('./B.npz') as X:
        mtx, dist, _, _ = [X[i] for i in ('mtx', 'dist', 'rvecs', 'tvecs')]
    cap = cv2.VideoCapture(0)
    ret, img = cap.read()
    h, w = img.shape[:2]
    newcameramtx, roi = cv2.getOptimalNewCameraMatrix(mtx, dist, (w, h), 0, (w, h))
    print 'newcameramtx =', newcameramtx
    print 'roi =', roi

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

    #prepare object points, like (0, 0, 0), (1, 0, 0), (2, 0, 0), ..., (6, 5, 0)
    objp = np.zeros((chessboard_size[0]*chessboard_size[1], 3), np.float32)
    objp[:, :2] =np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

    axis = np.float32([[grid_size, 0, 0], [0, grid_size, 0], [0, 0, -grid_size]]).reshape(-1, 3)

    while True:

        ret, img = cap.read()

        # undistort
        # method 1
        dst = cv2.undistort(img, mtx, dist, None, newcameramtx)
        # method 2
        # mapx, mapy = cv2.initUndistortRectifyMap(mtx, dist, None, newcameramtx, (w, h), 5)
        # dst = cv2.remap(img, mapx, mapy, cv2.INTER_LINEAR)
        x, y, w, h = roi
        img = dst[y:y + h, x: x + w]
        # # Re-projection Error
        # mean_error = 0
        # for i in xrange(len(objpoints)):
        #     imgpoints2, _ = cv2.projectPoints(objpoints[i], rvecs[i], tvecs[i], mtx, dist)
        #     error = cv2.norm(imgpoints[i], imgpoints2, cv2.NORM_L2)/len(imgpoints2)
        #     mean_error += error
        # print "total error: ", mean_error/len(objpoints)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        if ret:
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            # Find the rotation and translation vectors
            ret, rvecs, tvecs = cv2.solvePnP(objp, corners2, mtx, dist)
            # project 3D poionts to image plane
            imgpts, jac = cv2.projectPoints(axis, rvecs, tvecs, mtx, dist)
            img = draw(img, corners2, imgpts)

        cv2.imshow('img', img)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            break

sample_path = './3_PoseInteract/sample/'
if not os.path.isdir(sample_path):
    os.makedirs(sample_path)

chessboard_size = (6, 9)

# print "Gathering samples (should take about 5 secs) ..."
# gather_sample()
# print 'Done.'

print 'Calibrating ...'
calibrate()
print "Done.\nStart interaction. Press 'q' to end."
grid_size = 1.2
interact(grid_size)

