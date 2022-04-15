from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import grovepi
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import csv

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

light_sensor = 2
grovepi.pinMode(light_sensor,"INPUT")

outputArray = []

pic = np.zeros([50, 20])
for y in range(20):
    BP.set_motor_power(BP.PORT_A, 20)
    BP.set_motor_power(BP.PORT_B, 20)
    for x in range(50):
        sensor_value = grovepi.analogRead(light_sensor)
        #print(sensor_value)

        output = sensor_value/700
        outputArray.append((output, x, y))
        print(output)
                            
        time.sleep(.015)

        pic[x][y] = output
    BP.set_motor_power(BP.PORT_A, 0)
    BP.set_motor_power(BP.PORT_B, 0)
    time.sleep(3)


input("Create file: press space");

with open("DC_Data.csv", "w") as o:
    for data in outputArray:
        writer = csv.writer(o)
        writer.writerow(data)
