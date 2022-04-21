from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

import time     # import the time library for the sleep function
import brickpi3 # import the BrickPi3 drivers
import grovepi
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import csv

pic = np.zeros([50, 20])
with open('DC3_Data.csv') as csvfile:
    fileIn = csv.reader(csvfile)
    for row in fileIn:
        sensorVal = float(row[0])
        x = int(row[1])
        y = int(row[2])
        pic[x][y] = sensorVal
pic = np.fliplr(pic)
Xaxis = np.linspace(0,50)
Yaxis = np.linspace(0,20)
[X,Y] = np.meshgrid(Xaxis,Yaxis)
plt.imshow(pic, cmap='gray', interpolation='nearest')
plt.show()
