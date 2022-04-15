from MPU9250 import MPU9250
import sys
import smbus
import time
from math import sqrt
import brickpi3

import motorDrive as motor

mpu9250 = MPU9250()

time.sleep(0.1)
motor.drive("stop")

while True:
    mag = mpu9250.readMagnet()
    print(mag)
    time.sleep(0.1)
    motor.drive("forward")
    if(mag['x'] > 45 or mag['y']> 45):
        time.sleep(.5)
        motor.drive("left")
        time.sleep(1)
        motor.drive("forward")
        time.sleep(1.5)
        motor.drive("stop")
        break

motor.drive("stop")
