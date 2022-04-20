import grovepi
from IR_Functions import *
import time

IR_setup(grovepi)

"""
Returns a tuple of ints of the two values from the two IR sensor
Paramaters: none
"""
def IRRead():
    try:
        [sensor1_value, sensor2_value]=IR_Read(grovepi)
        
        #print ("One = " + str(sensor1_value) + "\tTwo = " + str(sensor2_value))
        return sensor1_value, sensor2_value

    except IOError:
        #print ("Error")
        return "error"
