#---------USER DEFINED LIBRARY IMPORTS---------#
import motorDrive as motor
import tSensor as touch
import IRSensor as ir
import imuMag as imu

#-----------OTHER LIBRARY IMPORTS--------------#
import time
from MPU9250 import MPU9250

#-----------VARIABLE DECLARATION---------------#
currDirect = "forward"
prevDirect = "stop"
power = False
minIMUSensorVal = 20
minIRSensorVal = 20 # NEEDS TO BE CHANGED THIS IS JUST A RANDOM NUMBER
IRObstacleDetected = False
timeOfIRObstacle = 0
points = [(1,1),(2,2),(1,2)]
currCoord = (0,0)

#-------------HELPER FUNCTIONS-----------------#

#------------------MAIN LOOP------------------#
for point in points:
        xCoord = point[0]
        yCoord = point[1]

        """IRVal1, IRVal2 = ir.IRRead()
        print(IRVal1, IRVal2)
        if IRVal1 > minIRSensorVal or IRVal2 > minIRSensorVal and time.time() - timeOfIRObstacle > 10:
                IRObstacleDetected = True
                timeOfIRObstacle = time.time()
        else:
                IRObstacleDetected = False

        mpu9250 = MPU9250()
        magVal1, magVal2 = imu.magRead(mpu9250)
        if magVal1 > minIMUSensorVal or magVal2 > minIMUSensorVal and time.time() - timeOfIRObstacle > 10:
                MagObstacleDetected = True
                timeOfIRObstacle = time.time()
        else:
                MagObstacleDetected = False
        """
        
        if xCoord > currCoord[0]:
                motor.drive("forward", True, "low")
        else:
                motor.drive("backwards", True, "low")
        time.sleep(abs(xCoord-currCoord[0])*3.1)
        motor.drive("stop", False, "low")
        for angle in range(90):
                motor.drive("left", True, "low")
                time.sleep(.019)
        motor.drive("stop", False, "low")
        if yCoord > currCoord[1]:
                motor.drive("forward", True, "low")
        else:
                motor.drive("backwards", True, "low")
        time.sleep(abs(yCoord-currCoord[1])*3.1)
        motor.drive("stop", False, "low")
        currCoord = (xCoord, yCoord)
        for angle in range(90):
                motor.drive("right", True, "low")
                time.sleep(.019)
        motor.drive("stop", False, "low")


