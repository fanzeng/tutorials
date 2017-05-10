import cv2
import numpy as np

face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier('haarcascade_eye.xml')
mouth_cascade = cv2.CascadeClassifier('mouth_cascade.xml')

# test using static test images used in generating the cascade
mouth_test_img = cv2.imread('./opencv_workspace/mouthtest1.jpg')
mouths = mouth_cascade.detectMultiScale(mouth_test_img, 1.3, 5)
for (mx, my, mw, mh) in mouths:
    cv2.rectangle(mouth_test_img, (mx, my), (mx + mw, my + mh), (255, 255, 0), 2)
cv2.imwrite('./opencv_workspace/mouth_test_img.jpg', mouth_test_img)


# test using live video stream captured from video camera
cap = cv2.VideoCapture(0)
while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)
        roi_gray = gray[y:y + h, x: x + w]
        roi_color = img[y:y + h, x: x + w]
        eyes = eye_cascade.detectMultiScale(roi_gray)

        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

        mouths = mouth_cascade.detectMultiScale(roi_gray, 1.3, 5)
        for (mx, my, mw, mh) in mouths:
            font = cv2.FONT_HERSHEY_SIMPLEX
            # cv2.putText(img, 'mouth', (x - w, y - h), font, 0.5, (0, 255, 255), 2, cv2.LINE_AA)
            cv2.rectangle(roi_color, (mx, my), (mx + mw, my + mh), (255, 255 ,0), 2)
    cv2.imshow('img', img)
    k = cv2.waitKey(30) & 0xff
    if k == 27:
        break
cap.release()
cv2.destroyAllWindows()