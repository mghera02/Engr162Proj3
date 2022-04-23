import motorDrive as motor
import time


for x in range(10):
    motor.drive("forward", False, "very high")
    time.sleep(.2)
    motor.drive("backwards", False, "very high")
    time.sleep(.2)
    
motor.drive("stop", False, "high")
