#---------USER DEFINED LIBRARY IMPORTS---------#
import motorDrive as motor
import tSensor as touch

#-----------OTHER LIBRARY IMPORTS--------------#
import time

#-----------VARIABLE DECLARATION---------------#
desiredDistanceFromWall = 20
wallsOnLeftRight = True
wallInFront = False
currDirect = "forward"
prevDirect = "stop"
power = False

"""
Param:
currDirect and prevDirect: Direction as a string ("forward", "left", "right", "stop", "backwards")
returns prevDirect
"""
def updateDirect(currDirect, prevDirect):
        if currDirect != prevDirect:
                print(f"Direction: {currDirect}")
        return currDirect

while True:
        try:
                # On/off power using touch sensor as on/off button
                power = touch.checkIfOn(power)
                if power:
                        #Detect walls in front and on sides
                        wallDistLeft, wallDistRight, wallDistFront = 1, 1, 1# insert func
                        
                        if (wallDistLeft < desiredDistanceFromWall and wallDistRight < desiredDistanceFromWall):
                                wallsOnLeftRight = True
                        else:
                                wallsOnLeftRight = False

                        if wallDistFront > desiredDistanceFromWall:
                                wallInFront = False
                        else:
                                wallInFront = True

                        wallsOnLeftRight = True
                        wallInFront= False
                        if wallsOnLeftRight and not wallInFront:
                                currDirect = "forward"
                                motor.drive(currDirect)
                                prevDirect = updateDirect(currDirect, prevDirect)
                else:
                        motor.drive("stop")
        
        except KeyboardInterrupt:
                motor.drive("stop")
                break
        
