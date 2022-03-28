#---------USER DEFINED LIBRARY IMPORTS---------#
import motorDrive as motor
import tSensor as touch
import usRead as us
import IRSensor as ir

#-----------OTHER LIBRARY IMPORTS--------------#
import time

#-----------VARIABLE DECLARATION---------------#
desiredDistanceFromWallLeftRight = 20
desiredDistanceFromWallFront = 30
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

#------------------MAIN LOOP------------------#
while True:
        try:
                # On/off power using touch sensor as on/off button
                power = touch.checkIfOn(power)
                time.sleep(.2)
                if power:
                        # Detect IR beacons
                        IRVal1, IRVal2 = ir.IRRead()
                        print(IRVal1, IRVal2)
                        if IRVal1 > minIRSensorVal or IRVal2 > minIRSensorVal and time.time() - timeOfIRObstacle > 10:
                                IRObstacleDetected = True
                                timeOfIRObstacle = time.time()
                        else:
                                IRObstacleDetected = False

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

                        # Direction changes
                        if (wallsOnLeft and wallsOnRight) and not wallInFront:# Keep going forward
                                print("case 1")
                                currDirect = "forward"
                        elif wallsOnRight and wallInFront and not wallsOnLeft: # Correcting to adjust left
                                print("case 2")
                                currDirect = "left"
                        elif wallsOnLeft and wallInFront and not wallsOnRight:# Correcting to adjust right
                                print("case 3")
                                currDirect = "right"
                        elif wallsOnLeft and not (wallsOnRight and wallInFront):# Correcting to adjust right
                                print("case 4")
                                currDirect = "right"
                        elif wallInFront and not (wallsOnLeft and wallsOnRight): # Left has precedence
                                print("case 5")
                                currDirect = "left"
                        elif not(wallInFront and wallsOnLeft and wallsOnRight):
                                """print("case 6")
                                currDirect = "left"""
                        

                        motor.drive(currDirect, False)
                        prevDirect = updateDirect(currDirect, prevDirect)
                else:
                        motor.drive("stop", False)
        
        except KeyboardInterrupt:
                motor.drive("stop")
                break
        
