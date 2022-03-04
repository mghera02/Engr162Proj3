from __future__ import print_function # use python 3 syntax but make it compatible with python 2
from __future__ import division

import brickpi3 # import the BrickPi3 drivers
import time

BP = brickpi3.BrickPi3() # Create an instance of the BrickPi3 class. BP will be the BrickPi3 object.

BP.set_sensor_type(BP.PORT_1, BP.SENSOR_TYPE.TOUCH)

def checkIfOn(currPower):
    try:
        touchValue = BP.get_sensor(BP.PORT_1)
        if (touchValue == 1):
            return not currPower
        else:
            return currPower
    except brickpi3.SensorError as error:
        return error

