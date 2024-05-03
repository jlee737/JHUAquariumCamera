import socket
import cv2
import numpy as np

socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ip = "192.168.53.192"
port = 5005
serverAddress = (ip, port)
socket.connect(serverAddress)

#capture = cv2.VideoCapture(2)
capture = cv2.VideoCapture(r"C:\Users\jclee\Downloads\Rivervideo360 - Made with Clipchamp.mp4")

if not capture.isOpened():
    print("Cannot open camera")
    exit()

shift = 0
zoom = 0
v_margins = 200
new_height = 960 - 2 * v_margins

while True:
    data = socket.recv(2048)
    values = [v == "True" for v in data.decode().split()]

    print(values)
    
    ret, frame = capture.read()
    if not ret:
        print("Cannot receive frame")
        break

    # Crop top and bottom of feed to filter warping
    cropped_frame = frame[v_margins:960-v_margins, 0:1920]    
    
    # Specify ROI dimensions (Can change this depending on monitor)
    ratio = 1.5
    roi_x = 1600
    roi_y = roi_x/ratio
    
    # Pad frame with extra ROI width
    half_frame = cropped_frame[:, 0:int(roi_x)]
    padded_frame = np.hstack((cropped_frame, half_frame))
    
    # Crop to ROI
    shift = shift%cropped_frame.shape[1]
    roi = padded_frame[zoom:new_height-zoom, ((0+shift)%(padded_frame.shape[1]))+int(2*zoom*ratio):((roi_x+shift)%(padded_frame.shape[1]))-int(2*zoom*ratio)]

    finalImage = cv2.resize(roi, (int(roi_x), int(roi_y)))
    #upscaledImage = sr.upsample(finalImage, )
    #upscaledImage = cv2.resize(upscaledImage, (int(roi_x), int(roi_y)))
   
    cv2.imshow('finalImage', finalImage)
    #cv2.imshow('upscaledImage', upscaledImage)    
    
    key = cv2.waitKey(20) & 0xFF

    # Stop feed wwhen q hit
    if key == ord('q') or key == 27:
        break
    elif key == ord('a') or values[0]:
        shift -= 10
    elif key == ord('d') or values[1]:
        shift += 10
    elif key == ord('w') or values[2]:
        zoom += 10
    elif key == ord('s') or values[3]:
        zoom -= 10
        
    if zoom <= 0:
        zoom = 0
    elif zoom >=200:
        zoom = 200

# End feed
capture.release()
cv2.destroyAllWindows()

#from cv2 import dnn_superres

# Connect to Theta V (port 3 on Jaechan's computer)

## Set up neural upscaling
# Create an SR object
#upsample_factor = 2
#sr = dnn_superres.DnnSuperResImpl_create()
#sr.readModel(r"C:\Users\Jaechan Lee\Desktop\JHU\__SP24\MultiD_AquariumProject\Upscaling\FSRCNN-small_x2.pb")
#sr.setModel("fsrcnn", upsample_factor)



# Set up video livestream frame
#while True:
    
    
    
#print(capture.get(cv2.CAP_PROP_FRAME_WIDTH))
#print(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))


