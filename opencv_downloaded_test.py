import cv2
import cv2.fisheye
import numpy as np

capture = cv2.VideoCapture('video360_test.mp4')

while capture.isOpened():
    ret, frame = capture.read()
    
    if not ret:
        print("Can't receive frame")
        break

    frame = cv2.resize(frame, [1960, 1080])
    
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'):
        break
    
capture.release()
cv2.destroyAllWindows()