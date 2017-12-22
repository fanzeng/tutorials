from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import SGDClassifier
from sklearn.metrics import classification_report
from sklearn.cross_validation import train_test_split
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import os

def extract_color_histogram(image, bins=(8,8,8)):
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	hist = cv2.calcHist([hsv], [0, 1, 2], None, bins, [0, 180, 0, 256, 0, 256])

	cv2.normalize(hist,hist)
	return hist.flatten()


parser = argparse.ArgumentParser()
parser.add_argument('-d', '--dataset', required=True, help='path to input dataset')
args = parser.parse_args()