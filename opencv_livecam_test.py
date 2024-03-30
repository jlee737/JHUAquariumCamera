import cv2
import numpy as np

# Connect to Theta V (port 3 on Jaechan's computer)
capture = cv2.VideoCapture(3)
if not capture.isOpened():
    print("Cannot open camera")
    exit()

shift = 0
zoom = 0
v_margins = 200
new_height = 960 - 2 * v_margins

# Set up video livestream frame
while True:
    ret, frame = capture.read()
    if not ret:
        print("Cannot receive frame")
        break
    
    # Crop top and bottom of feed to filter warping
    cropped_frame = frame[v_margins:960-v_margins, 0:1920]    
    
    # Specify ROI dimensions (Can change this depending on monitor)
    ratio = 1.5
    roi_x = 800
    roi_y = roi_x/ratio
    
    # Pad frame with extra ROI width
    half_frame = cropped_frame[:, 0:int(roi_x)]
    padded_frame = np.hstack((cropped_frame, half_frame))
    
    # Crop to ROI
    shift = shift%cropped_frame.shape[1]
    print(shift)
    roi = padded_frame[zoom:new_height-zoom, ((0+shift)%(padded_frame.shape[1]))+int(zoom*ratio):((roi_x+shift)%(padded_frame.shape[1]))-int(zoom*ratio)]

    finalImage = cv2.resize(roi, (int(roi_x), int(roi_y)))

    cv2.imshow('finalImage', finalImage)    
    key = cv2.waitKey(20) & 0xFF

    # Stop feed wwhen q hit
    if key == ord('q') or key == 27:
        break
    elif key == ord('a'):
        shift -= 3
    elif key == ord('d'):
        shift += 3
    elif key == ord('w'):
        zoom += 10
    elif key == ord('s'):
        zoom -= 10
        
    if zoom <= 0:
        zoom = 0
    elif zoom >=100:
        zoom = 100

    
    
#print(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
#print(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

# End feed
capture.release()
cv2.destroyAllWindows()

