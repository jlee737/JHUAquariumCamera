__Instructions__

*Hardware*:
- Ricoh Theta V Camera (Should be interchangable with Ricoh Theta X if preferred)
- Raspberry Pi 4b
- 6" MicroUSB cable
- 30' USB 2.0 Extension cable
- HDMI to microHDMI cable
- USB-C charging cable
- SaiDian 4-axis joystick (or other joystick if preferred)
- Adafruit Arcade Bonnet


*Set-up*:
1. For Windows, download Ricoh livestreaming drivers here: https://topics.theta360.com/en/faq/c_00_v/304_1/
2. For Linux (Raspberry Pi), use gstthetauvc package here: https://github.com/nickel110/gstthetauvc
    - Note, if new Raspberry Pi, some work likely has to be done assigning environmental variables after building for both libuvc and gstthetauvc.so

*Usage*:

Livestream
If using with only Raspberry Pi:
1. Boot-up Raspberry Pi and display
2. Turn on camera, connect to Raspberry Pi, and set to "livestreaming" via the mode button (should already be set)
3. Download program "Joystick.py"
4. Download and run program "opencv_livecam" (*Note that you may have to change the camera port on line 

If using with PC and Raspberry Pi (For slightly less latency)
1. Boot-up PC, Raspberry Pi, and Display
2. Temporarily connect Display to Raspberry Pi
3. Turn on camera, connect to PC, and set to "livestreaming" via the mode button (should already be set)
4. Download program "Joystick.py"
5. Download and run program "--" on Raspberry Pi
6. Disconnect monitor from Raspberry Pi and reconnect to PC
7. Download and run program "frompi.py" on Monitor

Recorded footage
1. Record 360 footage with Ricoh Theta V or any other 360 camera
2. Convert to Equirectangular footage (There should exist a software that comes with the camera to do this)
3. Convert to MP4 file and save on Raspberry pi or PC
4. Change the code by commenting out the existing VideoRecorder and replacing it with a new VideoRecorder containing the path to the MP4 video
   
*Current State*:
- The software all works and is optimized for the LG TV monitor size
- Vertical margins have roughly been adjusted to minimize view of cap
- Joystick is mapped so left and right is panning while twisting is zooming
- Runs at 2K resolution with almost no latency on PC and about 1 second of latency on Raspberry Pi (video latency; joystick latency is non-existent)
- For PC, can be used with ethernet adaptor (more latency) or USB extension cord (no latency)
- For Raspberry Pi, can be used with USB extension cord (currently ethernet adaptor does not work)

*Future Steps*:
1. Remapping controls:
   - In user testing, some people felt that up and down were more intuitive for zooming
   - To implement this, someone would have to resolder the connections on the joystick to remap the zoom to up and down
   - Personally, I thought this was more intuitive as well, so this was the way I previously had it before changing it to twisting at the Aquarium's request. Thus, I've verified that up and down can be done, and this should not require any alterations to the code if the correct wires are swapped
  
2. Adding up and down in zoomed state:
   - In user testing, some people wanted up and down on the joystick to be able to move the camera field of view up and down when it was zoomed
   - This poses a slightly bigger issue in that the current header board (adafruit arcade bonnet) only takes in two joystick inputs (currently x and twist [which has been mapped to y]). Note, it can take in six more button inputs if wanted
   - Thus, to retain X (panning), Y (Up and down), and twist (zooming), a different board with more inputs would have to be chosen. The important part in choosing a new board is that it must be able to convert analog inputs to digital as the joystick outputs analog inputs which the raspberry pi cannot take as input. A potential work around for this (not at all validated) might be to have the joystick input go into an arduino and then have the arduino send joystick data to the raspberry pi via serial communication. The code for this would probably look very similar to what is found at the top of "frompi.py" which I've written to allow serial communication between the raspberry pi and PC.
   - This would also require slight modifications to Joystick.py depending on how the new board communicates with the Raspberry pi
  
3. Fully waterproofing:
   - Currently, we believe that the best way to send signal and power between the camera and Raspberry pi is via a USB2.0 extension cable. We have verified that this works for cables up to 32 feet long (both normal extension cables as well as those with active repeaters). Our hand-off state has a 32 foot long ethernet cable that has been cut by us to insert through the cable penetrator. While the signal and power transduction works, this is not currently waterproof or safe to submerge in water. Further steps would be to redo the wire connections and add some sort of waterproof sheath (ie. Polyurethane tubing) around the USB cable itself.
   - Another option we explored was to use USB to ethernet adaptors to send the signal 30+ feet. While this works with some latency with the PC, this introduced too much latency for the LIBUVC library to work with Raspberry Pi. Doing some research, there are more expensive adaptors that exist for exactly this application (webcams, etc.). These products are in the $500-1000 range, however. But if an ethernet cable is desired, it did seem like they should work (Icron Ranger 2311).

4. New interface:
   - Currently, there is not an interface to switch between live video and stored footage. This is currently accomplished by commenting out lines in the main "__________" file that selects which input is fed into the VideoCapture object.
   - Depending on the Aquarium's needs, it may be nice to have a menu that pops up when the program is initiated. This menu would likely include the option to toggle between live and recorded footage. Additionally, this menu could allow the Aquarium to select exactly which piece of recorded footage they would like to play, or even give them the option to place recorded footage in a queue to play.
  
5. Upgraded resolution:
   - To me, the biggest upgrade that could be made to this exhibit would be increasing the resolution of the camera. The camera supports 4K resolution, but I found that the Raspberry Pi processer is too slow to display the 4K resolution which is why the software is currently configured for 2K video. At 4K, the frame rate of the footage becomes very slow, decreasing to somewhere between 2-10 frames per second. The resolution itself is very easy to change; simply changing 2K to 4K in line ____ of ____ changes the resolution.
   - While not a trivial fix, the likely solution to this would be to upgrade to a more powerful processor. Options might include the Raspberry pi 5 (32GB), Factor 201 Raspberry pi, NVIDIA Jetson, or Intel NUC. For many of these, an alternate way of integrating the joystick would be necessary, likely incorporating some kind of USB IO board. 
