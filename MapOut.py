from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

#import time     # import the time library for the sleep function
#import brickpi3 # import the BrickPi3 drivers
#import grovepi
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import math

def mapOut(filename,xsize,ysize):
    fn = "./"+filename
    file = open(fn,'r')
    lines = file.readlines()
    pic = np.zeros([xsize, ysize])

    for row in lines:
        gridspace = int(row[0])
        x = int(math.floor(float(row[1])))
        y = int(math.floor(float(row[2])))
        pic[y][x] = gridspace
    Xaxis = np.linspace(0,xsize)
    Yaxis = np.linspace(0,ysize)
    [X,Y] = np.meshgrid(Xaxis,Yaxis)
    plt.imshow(pic, cmap='gray', interpolation='nearest', origin='lower')
    plt.show()
    
mapOut("DatIn.txt",6,6)

