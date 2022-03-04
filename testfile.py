#!/usr/bin/env python
# Created by Kevin M
import time
import grovepi
import usRead
grovepi.set_bus("RPI_1")
distArray = [0,0,0]
while True:
    try:
        distArray = usRead.ultraread(2,3,4)
        print(distArray)
    except Exception as e:
        print("Error:{}".format(e))
    time.sleep(.5)
