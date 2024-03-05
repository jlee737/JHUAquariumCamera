#from SimpleCV import Camera, VideoStream, Color, Display, Image, VirtualCamera
import cv2
import numpy as np
import time

# build the mapping
def buildMap(Ws,Hs,Wd,Hd,R1,R2,Cx,Cy):
    map_x = np.zeros((Hd,Wd), dtype=np.float32)
    map_y = np.zeros((Hd,Wd), dtype=np.float32)
    for y in range(0,int(Hd-1)):
        for x in range(0,int(Wd-1)):
            r = (float(y)/float(Hd))*(R2-R1)+R1
            theta = (float(x)/float(Wd))*2.0*np.pi
            xS = Cx+r*np.sin(theta)
            yS = Cy+r*np.cos(theta)
            map_x.itemset((y,x),int(xS))
            map_y.itemset((y,x),int(yS))
        
    return map_x, map_y
# do the unwarping 
def unwarp(img,map_x,map_y):
    output = cv2.remap(img,map_x,map_y,cv2.INTER_LINEAR)
    result = cv2.Image(output,cv2image=True)
    return result

capture = cv2.VideoCapture(3)

'''
disp = cv2.Display((800,600))
vals = [(), (), ()]
last = (0,0)
# Load the video from the rpi
vc = cv2.VirtualCamera("video360_test.mp4","video")
# Sometimes there is crud at the begining, buffer it out
for i in range(0,10):
    img = vc.getImage()
    img.save(disp)
# Show the user a frame let them left click the center
# of the "donut" and the right inner and outer edge
# in that order. Press esc to exit the display
while not disp.isDone():
    test = disp.leftButtonDownPosition()
    if( test != last and test is not None):
        last = test
        vals.append(test)
'''

# 0 = xc yc
# 1 = r1
# 2 = r2
# center of the "donut"    
Cx = 960
Cy = 480
# Inner donut radius
R1x = 985
R1y = 505
R1 = R1x-Cx
# outer donut radius
R2x = 1010
R2y = 530
R2 = R2x-Cx
# our input and output image sizes
Wd = int(2.0*((R2+R1)/2)*np.pi)
Hd = (R2-R1)
Ws = 1920
Hs = 960

# build the pixel map, this could be sped up
print("BUILDING MAP!")
map_x,map_y = buildMap(Ws,Hs,Wd,Hd,R1,R2,Cx,Cy)
print("MAP DONE!")
# do an unwarping and show it to us
result = unwarp(capture,map_x,map_y)
#result.save(disp)

# SimpleCV/OpenCV video out was giving problems
# decided to output frames and convert using
# avconv / ffmpeg. 

# I used these params for converting the raw frames to video
# avconv -f image2 -r 30 -v:b 1024K -i samples/lapinsnipermin/%03d.jpeg output.mpeg
i = 0
while img is not None:
    result = unwarp(img,map_x,map_y)
    # Once we get an image overlay it on the source
    derp = img.blit(result,(0,img.height-result.height))
    derp = derp.applyLayers()
    derp.save(capture)
    fname = "FRAME{num:05d}.png".format(num=i)
    derp.save(fname)
    #vs.writeFrame(derp)
    # get the next frame
    img = vc.getImage()
    i = i + 1