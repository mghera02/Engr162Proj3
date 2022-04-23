#---------USER DEFINED LIBRARY IMPORTS---------#
import motorDrive as motor
import tSensor as touch
import usRead as us
import IRSensor as ir
import imuMag as imu

#-----------OTHER LIBRARY IMPORTS--------------#
import time
from MPU9250 import MPU9250

#-----------VARIABLE DECLARATION---------------#
desiredDistanceFromWallLeftRight = 17
desiredCriticalDistanceFromWallLeftRight = 5
desiredDistanceFromWallFront = 25
currDirect = "forward"
prevDirect = "stop"
power = False
minIRSensorVal = 20 # NEEDS TO BE CHANGED THIS IS JUST A RANDOM NUMBER
minMagSensorVal = 140
IRObstacleDetected = False
magObstacleDetected = False
timeOfIRObstacle = 0
delayTime = 1.5
fileMade = False
facingDirect = "N"
y = 0
x = 0


class fileObj:
    def __init__(obj,filename):
    #String adds ./ for file address, will add to common file
        obj.name = './'+filename
        obj.f = open(obj.name,'w')
        obj.f.write('Hazard Type\t|Parameter of Interest\t|Parameter Value\t|Location X Coordinate [cm]\t|Location Y Coordinate [cm]')
    def hazardwrite(obj,data):
    #data must be an array of length 4 with the following values:
        # 1. Type, either 1 for Temperature or 2 for Electrical
        # 2. Intensity
        # 3. X Coordinate
        # 4. Y Coordinate
        if data[0] == 1:
            typ = 'Temperature'
            poi = 'Kelvin [K]'
            pv = data[1]
            locx = data[2]
            locy = data[3]
        else:
            typ = 'Electrical'
            poi = 'Tesla (T)'
            pv = round(data[1] / 1000,4)
            locx = round(data[2],4)
            locy = round(data[3],4)
        string = typ+'\t|'+poi+'\t\t|'+str(pv)+'\t\t\t|'+str(locx)+'\t\t\t\t|'+str(locy)
        obj.f.write('\n'+string)
    def filemode(obj,mode):
    #mode must be of form accepted by open() (ie. 'r', 'w', 'a', etc.)
        obj.f.close()
        obj.f.open(obj.name,mode)
    def close(obj):
    #Be sure to close the file object at the end
        obj.f.close()


#-------------HELPER FUNCTIONS-----------------#
"""
Param:
currDirect and prevDirect: Direction as a string ("forward", "left", "right", "stop", "backwards")
returns prevDirect
"""
def updateDirect(currDirect, prevDirect):
        if currDirect != prevDirect:
                print(f"Direction: {currDirect}")
        return currDirect

def updateWall(wallDistLeft, wallDistRight, wallDistFront, desiredDistanceFromWallFront, desiredDistanceFromWallLeftRight):
        wallsOnLeft = True
        wallsOnRight = True
        wallsInFront = True

        if wallDistLeft <= desiredDistanceFromWallLeftRight:
                wallsOnLeft = True
        else:
                wallsOnLeft = False

        if wallDistRight <= desiredDistanceFromWallLeftRight:
                wallsOnRight = True
        else:
                wallsOnRight = False

        if wallDistFront <= desiredDistanceFromWallFront:
                wallInFront = True
        else:
                wallInFront = False
        
        return wallsOnLeft, wallInFront, wallsOnRight

def updateCriticalWall(wallDistLeft, wallDistRight, desiredCriticalDistanceFromWallLeftRight):
        wallsOnLeft = True
        wallsOnRight = True

        if wallDistLeft <= desiredCriticalDistanceFromWallLeftRight:
                wallsOnLeft = True
        else:
                wallsOnLeft = False

        if wallDistRight <= desiredCriticalDistanceFromWallLeftRight:
                wallsOnRight = True
        else:
                wallsOnRight = False
        
        return wallsOnLeft, wallsOnRight
#------------------MAIN LOOP------------------#
while True:
        try:
                # On/off power using touch sensor as on/off button
                power = touch.checkIfOn(power)
                time.sleep(.2)
                if power:
                        if not fileMade:
                                tableMap = fileObj("tableMap.txt")
                                fileMade = True
                        # Detect IR beacons
                        """IRVal1, IRVal2 = ir.IRRead()
                        print(IRVal1, IRVal2)
                        if IRVal1 > minIRSensorVal or IRVal2 > minIRSensorVal and time.time() - timeOfIRObstacle > 10:
                                IRObstacleDetected = True
                                timeOfIRObstacle = time.time()
                        else:
                                IRObstacleDetected = False
                        """
                        mpu9250 = MPU9250()
                        magVals = imu.magRead(mpu9250)
                        magVal = abs(magVals[1])
                        print(f"magnet {magVal1}")
                        if magVal > minMagSensorVal and time.time() - timeOfIRObstacle > 10:
                                magObstacleDetected = True
                                timeOfIRObstacle = time.time()
                        else:
                                magObstacleDetected = False

                        if magObstacleDetected:
                                tableMap.hazardwrite([2, magVal, x, y])
                                motor.drive("stop", False, power)
                                continue

                        # Detect walls in front and on side
                        usDistanceArray = us.ultraread(5,2,6)
                        wallDistLeft = usDistanceArray[0]
                        wallDistFront = usDistanceArray[1]
                        wallDistRight = usDistanceArray[2]
                        #wallDistLeft, wallDistFront, wallDistRight = us.ultraread(4,5,6)
                        wallsOnLeft, wallInFront, wallsOnRight = updateWall(wallDistLeft, wallDistRight, wallDistFront, desiredDistanceFromWallFront, desiredDistanceFromWallLeftRight)
                        print(f"Wall left {wallDistLeft} {wallsOnLeft}")
                        print(f"Wall right {wallDistRight} {wallsOnRight}")
                        print(f"Wall front {wallDistFront} {wallInFront}")
                        criticalWallOnLeft, criticalWallOnRight = updateCriticalWall(wallDistLeft, wallDistRight, desiredCriticalDistanceFromWallLeftRight)

                        if criticalWallOnLeft:
                                print("case 101")
                                currDirect = "right"
                                power = "low"
                        elif criticalWallOnRight:
                                print("case 102")
                                currDirect = "left"
                                power = "low"
                        else:
                                power = "high"
                                # Direction changes
                                if (wallsOnLeft and wallsOnRight) and not wallInFront:# Keep going forward
                                        print("case 1")
                                        currDirect = "forward"
                                elif wallsOnRight and wallInFront and not wallsOnLeft: # Correcting to adjust left
                                        print("case 2")
                                        if (prevDirect == "forward"):
                                                time.sleep(delayTime)
                                elif wallsOnLeft and wallInFront and not wallsOnRight:# Correcting to adjust right
                                        print("case 3")
                                        if (prevDirect == "forward"):
                                                time.sleep(delayTime)
                                        currDirect = "right"
                                elif wallsOnLeft and not (wallsOnRight and wallInFront):# Correcting to adjust right
                                        print("case 4")
                                        if (prevDirect == "forward"):
                                                time.sleep(delayTime)
                                        currDirect = "right"
                                elif wallsOnRight and not (wallsOnLeft and wallInFront):# Correcting to adjust right
                                        print("case 5")
                                        if (prevDirect == "forward"):
                                                time.sleep(delayTime)
                                        currDirect = "left"
                                elif wallInFront and not (wallsOnLeft and wallsOnRight): # Left has precedence
                                        print("case 6")
                                        if (prevDirect == "forward"):
                                                time.sleep(delayTime)
                                elif wallInFront and wallsOnLeft and wallsOnRight:
                                        print("case 7")
                                        motor.drive("left", False, "low")
                                        time.sleep(.85)
                                        currDirect = "backwards"
                                elif not(wallInFront and wallsOnLeft and wallsOnRight):
                                        """print("case 6")
                                        currDirect = "left"""

                        if power == "low":
                                motor.drive(currDirect, False, power)
                        else:                        
                                if (currDirect == "forward"):
                                        if facingDirect == "N":
                                                y += 1
                                        elif facingDIrect == "S":
                                                y -= 1
                                        elif facingDirect == "E":
                                                x += 1
                                        elif facingDIrect == "W":
                                                x -= 1
                                        motor.drive(currDirect, False, power)
                                elif (currDirect == "backwards"):
                                        for angle in range(180):
                                                motor.drive("right", True, "low")
                                                time.sleep(.017)
                                        if currDirect == "N":
                                            currDirect = "S"
                                        elif currDirect == "S":
                                            currDirect = "N"
                                        elif currDirect == "E":
                                            currDirect = "W"
                                        elif currDirect == "W":
                                            currDirect = "E"
                                        motor.drive("forward", False, "low")
                                        time.sleep(delayTime)
                                else:
                                        for angle in range(90):
                                                motor.drive(currDirect, True, "low")
                                                time.sleep(.015)
                                        if currDirect == "right":
                                            if currDirect == "N":
                                                currDirect = "E"
                                            elif currDirect == "E":
                                                currDirect = "S"
                                            elif currDirect == "S":
                                                currDirect = "W"
                                            elif currDirect == "W":
                                                currDirect = "N"
                                        else:
                                            if currDirect == "N":
                                                currDirect = "W"
                                            elif currDirect == "W":
                                                currDirect = "S"
                                            elif currDirect == "S":
                                                currDirect = "E"
                                            elif currDirect == "E":
                                                currDirect = "N"
                                        motor.drive("forward", False, "low")
                                        time.sleep(delayTime)
                        prevDirect = updateDirect(currDirect, prevDirect)
                else:
                        power = False
                        motor.drive("stop", False, power)
                        try:
                                tableMap.close()
                        except:
                                continue
                        print("FINISHED")
                        break
        
        except KeyboardInterrupt:
                motor.drive("stop")
                break
        
