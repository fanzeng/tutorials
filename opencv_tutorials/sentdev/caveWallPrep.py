import cv2
import numpy as np

def prep(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.adaptiveThreshold(gray, 150, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    GaussianBlur = cv2.GaussianBlur(gray, (55, 55), 0)
    kernel = np.ones((11, 11), np.uint8)
    dilate = cv2.dilate(gray, kernel, iterations = 1)
    dilateBlur = cv2.GaussianBlur(dilate, (15, 15), 0)
    dilateThreshold = cv2.adaptiveThreshold(dilateBlur, 200, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 115, 1)
    sobel_x = cv2.Sobel(dilateThreshold, cv2.CV_8UC1, 1, 0, ksize = 5)
    cv2.imshow('gray', gray)
    cv2.imshow('GaussianBlur', GaussianBlur)
    cv2.imshow('dilate', dilate)
    cv2.imshow('dilateBlur', dilateBlur)
    cv2.imshow('dilateThreshold', dilateThreshold)
    cv2.imshow('sobel_x', sobel_x)
    cv2.waitKey(0)
    return sobel_x

frame = cv2.imread('cave.jpg')
prep(frame)