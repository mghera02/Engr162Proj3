from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division

import brickpi3 # import the BrickPi3 drivers

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

"""
HELPER FUNCTIONS FOR DRIVE()
"""
def backwards():
    return -20, -20

def forward():
    return 30, 20

def right(POC, power):
    #Left, right
    if POC:
        return 90, -90
    else:
        if (power == "high"):
            return 40, -40
        else:
            return 30, -30

def left(POC, power):
    if POC:
        return -90, 90
    else:
        if (power == "high"):
            return -40, 40
        else:
            return -30, 30

def stop():
    return 0, 0

"""
Used for telling both left and right motors to move left, right, forward,
and backwards. Pass in the direction as a string.

Possible Parameters:
"forward"
"backwards"
"left"
"right"

"""
def drive(direction, POC, power):
    try:
        speed1 = 0 # Speed of motor 1
        speed2 = 0 # Speed of motor 2
        
        if direction == "forward":
            speed1, speed2 = forward()
        elif direction == "right":
            speed1, speed2 = right(POC, power)
        elif direction == "left":
            speed1, speed2 = left(POC, power)
        elif direction == "backwards":
            speed1, speed2 = backwards()
        else:
            speed1, speed2 = stop()
            
        BP.set_motor_power(BP.PORT_A, speed1)
        BP.set_motor_power(BP.PORT_B, speed2)
        
    except KeyboardInterrupt:
        # Unconfigure the sensors, disable the motors, and restore the LED to the control of the BrickPi3 firmware.
        BP.reset_all()
