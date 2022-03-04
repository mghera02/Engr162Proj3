#!/usr/bin/env python
# Created by Kevin M
import grovepi

#Parameter: Ports of input, in order from left, middle right
#Output: Distance from object being viewed in order of left, middle, right
grovepi.set_bus("RPI_1")

def ultraread(portL,portM,portR):
    try:
        reading = [grovepi.ultrasonicRead(portL),grovepi.ultrasonicRead(portM),grovepi.ultrasonicRead(portR)]
        print(reading)
        #return reading
    except Exception as e:
        print ("Error is {}".format(e))
