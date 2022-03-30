import math
#Function returns array of four values, xyz magnet value and magnet magnitude
#Input is the MPU9250 object
def magRead(obj):
    mag = obj.readMagnet()
    magn = math.sqrt(pow(mag['x'],2)+pow(mag['y'],2)+pow(mag['z'],2))
    ret = [mag,magn]
    return ret

