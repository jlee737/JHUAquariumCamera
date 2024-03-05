import cv2
import numpy as np
from PyQt6.QtWidgets import QApplication, QWidget

# Initialize window using PyQt6

# Connect to Theta V (port 3 on Jaechan's computer)
capture = cv2.VideoCapture(3)
if not capture.isOpened():
    print("Cannot open camera")
    exit()

shift = 0
v_margins = 200
new_height = 960 - 2 * v_margins

# Video livestream
while True:
    ret, frame = capture.read()
    if not ret:
        print("Cannot receive frame")
        break
    
    # Crop top and bottom of feed
    cropped_frame = frame[v_margins:960-v_margins, 0:1920]    
    
    #Specify ROI dimensions
    roi_x = 400
    roi_y = roi_x / 2 #Could change this if display isn't 2:1
    
    # Pad frame with extra ROI width
    half_frame = frame[:, 0:int(roi_y)]
    padded_frame = np.hstack((frame, half_frame))
    
    # Crop to ROI
    # Modulo to come back over!!!
    roi = padded_frame[0:new_height,(0+shift)%roi_x:roi_x+shift]
    
    cv2.imshow('frame', roi)    
    key = cv2.waitKey(20) & 0xFF

    # Stop feed wwhen q hit
    if key == ord('q') or key == 27:
        break
    elif key == ord('a'):
        shift -= 1
    elif key == ord('d'):
        shift += 1

print(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
print(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# End feed
capture.release()
cv2.destroyAllWindows()