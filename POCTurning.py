import motorDrive as motor
import time

for angle in range(360):
	motor.drive("left", True, power)
	time.sleep(.013)
motor.drive("stop", False, power)
