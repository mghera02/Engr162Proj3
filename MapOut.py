from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division       #                           ''

#import time     # import the time library for the sleep function
#import brickpi3 # import the BrickPi3 drivers
#import grovepi
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

def mapOut(filename,xsize,ysize):
    fn = "./"+filename
    pic = np.zeros([xsize, ysize])
    file = open(fn,'r')
    lines = file.readlines()

    for row in lines:
        gridspace = int(row[0])
        x = int(row[1])
        y = int(row[2])
        pic[y][x] = gridspace
    Xaxis = np.linspace(0,5)
    Yaxis = np.linspace(0,5)
    [X,Y] = np.meshgrid(Xaxis,Yaxis)
    plt.imshow(pic, cmap='gray', interpolation='nearest', origin='lower')
    plt.show()
    print("end")
    
mapOut("DatIn.txt",5,5)