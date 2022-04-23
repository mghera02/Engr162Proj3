import motorDrive as motor
import time

for angle in range(90):
	motor.drive("left", True, "low")
	time.sleep(.019)
motor.drive("stop", False, "low")

time.sleep(3)

for angle in range(90):
	motor.drive("right", True, "low")
	time.sleep(.018)
motor.drive("stop", False, "low")

time.sleep(3)

for angle in range(180):
	motor.drive("left", True, "low")
	time.sleep(.02)
motor.drive("stop", False, "low")

motor.drive("backwards", False, "low")
time.sleep(1)
motor.drive("stop", False, "low")

time.sleep(3)

