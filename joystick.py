#!/usr/bin/python

import os
import time
import RPi.GPIO as gpio
from smbus import SMBus

'''
key = [ # EDIT KEYCODES IN THIS TABLE TO YOUR PREFERENCES:
	# See /usr/include/linux/input.h for keycode names
	# Keyboard        Bonnet        EmulationStation
	e.KEY_LEFTCTRL, # 1A            'A' button
	e.KEY_LEFTALT,  # 1B            'B' button
	e.KEY_A,        # 1C            'X' button
	e.KEY_S,        # 1D            'Y' button
	e.KEY_5,        # 1E            'Select' buttons	
	e.KEY_1,        # 1F            'Start' button
	0,              # Bit 6 NOT CONNECTED on Bonnet
	0,              # Bit 7 NOT CONNECTED on Bonnet
	e.KEY_DOWN,     # 4-way down    D-pad down
	e.KEY_UP,       # 4-way up      D-pad up
	e.KEY_RIGHT,    # 4-way right   D-pad right
	e.KEY_LEFT,     # 4-way left    D-pad left
	e.KEY_L,        # Analog right
	e.KEY_H,        # Analog left
	e.KEY_J,        # Analog down
	e.KEY_K         # Analog up
]
'''

class Joystick:
    def __init__(self):
        self.addr   = 0x26 # I2C Address of MCP23017
        self.irqPin = 17   # IRQ pin for MCP23017

        #os.system("sudo modprobe uinput")

        self.bus     = SMBus(1)
        IODIRA  = 0x00
        IOCONA  = 0x0A
        self.INTCAPA = 0x10

        # Initial MCP23017 config:
        self.bus.write_byte_data(self.addr, 0x05  , 0x00) # If bank 1, switch to 0
        self.bus.write_byte_data(self.addr, IOCONA, 0x44) # Bank 0, INTB=A, seq, OD IRQ

        # Read/modify/write remaining MCP23017 config:
        cfg = self.bus.read_i2c_block_data(self.addr, IODIRA, 14)
        cfg[ 0] = 0xFF # Input bits
        cfg[ 1] = 0xFF
        cfg[ 2] = 0x00 # Polarity
        cfg[ 3] = 0x00
        cfg[ 4] = 0xFF # Interrupt pins
        cfg[ 5] = 0xFF
        cfg[12] = 0xFF # Pull-ups
        cfg[13] = 0xFF
        self.bus.write_i2c_block_data(self.addr, IODIRA, cfg)

        # Clear interrupt by reading INTCAP and GPIO registers
        x = self.bus.read_i2c_block_data(self.addr, self.INTCAPA, 4)

        self.buttons = { "up": 13, "down": 12, "left": 15, "right": 14 }
        self.values = { button : False for button in self.buttons.keys() }

    # Callback for MCP23017 interrupt request
    def mcp_irq(self, pin):
        x = self.bus.read_i2c_block_data(self.addr, self.INTCAPA, 4)
        data = x[2] | (x[3] << 8)
        for button in self.buttons:
            bit_idx = self.buttons[button]
            value = bool((data >> bit_idx) % 2)
            self.values[button] = not value

    def up(self):
        return self.values["up"]

    def down(self):
        return self.values["down"]

    def left(self):
        return self.values["left"]

    def right(self):
        return self.values["right"]

    def start(self):
        # GPIO init
        gpio.setwarnings(False)
        gpio.setmode(gpio.BCM)

        # Enable pullup and callback on MCP23017 IRQ pin
        gpio.setup(self.irqPin, gpio.IN, pull_up_down=gpio.PUD_UP)
        gpio.add_event_detect(self.irqPin, gpio.FALLING, callback=self.mcp_irq)

    def test(self):
        while True:
            print(self.values)
            time.sleep(0.25)

if __name__ == "__main__":
    joy = Joystick()
    joy.start()
    joy.test()

