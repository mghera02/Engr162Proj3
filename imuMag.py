import math
import time
from MPU9250 import MPU9250

mpu9250 = MPU9250()
#Function returns array of four values, xyz magnet value and magnet magnitude
#Input is the MPU9250 object
def magRead(obj):
    mag = obj.readMagnet()
    magn = math.sqrt(pow(mag['x'],2)+pow(mag['y'],2)+pow(mag['z'],2))
    ret = [mag,magn]
    return ret
