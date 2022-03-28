import motorDrive as motor
import time

for angle in range(360):
	motor.drive("left", True)
	time.sleep(.011)
motor.drive("stop", False)
