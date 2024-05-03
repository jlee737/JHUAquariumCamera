import socket
import cv2
import numpy as np

## Change variable definitions here:
# Panning
pan_speed = 10

# Zooming
zoom_speed = 10
max_zoom = 200

# Specify Display Dimensions
ratio = 1.5
roi_x = 1600
roi_y = roi_x/ratio

# Choose how many pixels to crop vertically
v_margins = 200
new_height = 960 - 2 * v_margins

# Initialize variables    
shift = 0
zoom = 0

## Connecting to Raspberry Pi for Joystick Input
socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "192.168.53.192"
port = 5005
serverAddress = (ip, port)
socket.connect(serverAddress)


## Chose Video Feed
## Uncomment line depending on which function should be used

# Live video from camera
# Note, device port may have to be changed
capture = cv2.VideoCapture(2)

# Pre-recorded footage in equirectangular mp4 file
#capture = cv2.VideoCapture(r"C:\Users\jclee\Downloads\Rivervideo360 - Made with Clipchamp.mp4")

## Video Capture Loop
if not capture.isOpened():
    print("Cannot open camera")
    exit()

while True:
    data = socket.recv(2048)
    values = [v == "True" for v in data.decode().split()]

    print(values)
    
    ret, frame = capture.read()
    if not ret:
        print("Cannot receive frame")
        break

    # Crop top and bottom of feed to remove obscured regions
    cropped_frame = frame[v_margins:960-v_margins, 0:1920]    
    
    # Pad frame with extra ROI width to enable 360 rotation
    half_frame = cropped_frame[:, 0:int(roi_x)]
    padded_frame = np.hstack((cropped_frame, half_frame))
    
    # Crop to region of interest (ROI)
    shift = shift%cropped_frame.shape[1]
    roi = padded_frame[zoom:new_height-zoom, ((0+shift)%(padded_frame.shape[1]))+int(2*zoom*ratio):((roi_x+shift)%(padded_frame.shape[1]))-int(2*zoom*ratio)]

    # Resize to specified monitor dimensions
    finalImage = cv2.resize(roi, (int(roi_x), int(roi_y)))

    # Display final image
    cv2.imshow('finalImage', finalImage)
 
    key = cv2.waitKey(20) & 0xFF

    # Keyboard and joystick bindings
    # Note, escape or q to break window! X button does not work for default OpenCV
    if key == ord('q') or key == 27:
        break
    elif key == ord('a') or values[0]:
        shift -= pan_speed
    elif key == ord('d') or values[1]:
        shift += pan_speed
    elif key == ord('w') or values[2]:
        zoom += zoom_speed
    elif key == ord('s') or values[3]:
        zoom -= zoom_speed
        
    if zoom <= 0:
        zoom = 0
    elif zoom >=max_zoom:
        zoom = max_zoom

# End feed
capture.release()
cv2.destroyAllWindows()
