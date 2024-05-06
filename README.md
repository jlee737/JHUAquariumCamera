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
If using with only Raspberry Pi:
1. Boot-up Raspberry Pi and display
2. Turn on camera, connect to Raspberry Pi, and set to "livestreaming" via the mode button (should already be set)
3. Download and run program "opencv_livecam"

If using with PC and Raspberry Pi (For slightly less latency)
1. Boot-up PC, Raspberry Pi, and Display
2. Temporarily connect Display to Raspberry Pi
3. Turn on camera, connect to PC, and set to "livestreaming" via the mode button (should already be set)
4. Download and run program "--" on Raspberry Pi
5. Disconnect monitor from Raspberry Pi and reconnect to PC
6. Download and run program "frompi.py" on Monitor
