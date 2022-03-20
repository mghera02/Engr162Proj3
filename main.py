#---------USER DEFINED LIBRARY IMPORTS---------#
import motorDrive as motor
import tSensor as touch
import usRead as us
import IRSensor as ir

#-----------OTHER LIBRARY IMPORTS--------------#
import time

#-----------VARIABLE DECLARATION---------------#
desiredDistanceFromWall = 20
currDirect = "forward"
prevDirect = "stop"
power = False
minIRSensorVal = 20 # NEEDS TO BE CHANGED THIS IS JUST A RANDOM NUMBER
IRObstacleDetected = False
timeOfIRObstacle = 0

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

def updateWall(wallDistLeft, wallDistRight, wallDistFront, desiredDistanceFromWall):
        if wallDistLeft < desiredDistanceFromWall:
                wallsOnLeft = True
        else:
                wallsOnRight = False

        if wallDistRight < desiredDistanceFromWall:
                wallsOnRight = True
        else:
                wallsOnRight = False

        if wallDistFront > desiredDistanceFromWall:
                wallInFront = False
        else:
                wallInFront = True
        
        return wallsOnLeft, wallInFront, wallsOnRight

#------------------MAIN LOOP------------------#
while True:
        try:
                # On/off power using touch sensor as on/off button
                power = touch.checkIfOn(power)
                if power:
                        # Detect IR beacons
                        IRVal1, IRVal2 = ir.IRRead()
                        if IRVal1 > minIRSensorVal or IRVal2 > minIRSensorVal and time.time() - timeOfIRObstacle > 10:
                                IRObstacleDetected = True
                                timeOfIRObstacle = time.time()
                        else:
                                IRObstacleDetected = False

                        # Detect walls in front and on sides
                        wallDistLeft, wallDistFront, wallDistRight = us.ultraread(4,5,6)
                        wallsOnLeft, wallInFront, wallsOnRight = updateWall(wallDistLeft, wallDistRight, wallDistFront, desiredDistanceFromWall)

                        # Direction changes
                        if (wallsOnLeft and wallsOnRight) and not wallInFront:# Keep going forward
                                currDirect = "forward"
                        elif wallsOnRight and wallInFront and not wallsOnLeft: # Correcting to adjust left
                                currDirect = "left"
                        elif wallsOnLeft and wallInFront and not wallsOnRight:# Correcting to adjust right
                                currDirect = "right"
                        elif wallInFront and not (wallsOnLeft and wallsOnRight): # Left has precedence
                                currDirect = "left"
                        else:
                                print("ERROR with maze navigation algorithm!!!")

                        motor.drive(currDirect)
                        prevDirect = updateDirect(currDirect, prevDirect)
                else:
                        motor.drive("stop")
        
        except KeyboardInterrupt:
                motor.drive("stop")
                break
        
