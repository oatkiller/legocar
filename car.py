# See http://www.brianhensley.net/2012/08/wii-controller-raspberry-pi-python.html
# See https://www.youtube.com/watch?v=hfBXRgUKqtc
# See http://www.philohome.com/motors/motorcomp.htm
# See http://sourceforge.net/p/raspberry-gpio-python/wiki/PWM/
# See http://www.robotplatform.com/howto/L293/motor_driver_1.html
# See http://www.ti.com/lit/ds/symlink/l293d.pdf

#!/usr/bin/env python

import cwiid
import time
import RPi.GPIO as GPIO

class Motor(object):
    STOP = (0,0)
    SPEEDS = [
        (0,100),
        (0,88.2),
        (0,76.1),
        (0,63.5),
        (0,50.4),
        (0,38.2),
        (0,25.8),
        STOP,
        (25.8,0),
        (38.2,0),
        (50.4,0),
        (63.5,0),
        (76.1,0),
        (88.2,0),
        (100,0)
    ]
    FREQUENCY = 1170
    GPIOSetup = False
    def __init__(self,firstPinNumber,secondPinNumber):
        self.firstPinNumber = firstPinNumber
        self.secondPinNumber = secondPinNumber
        self.currentSpeedIndex = 8
        GPIO.setmode(GPIO.BOARD)

    def setupGPIO(self):
        if self.GPIOSetup == False:
            GPIO.setup([self.firstPinNumber,self.secondPinNumber],GPIO.OUT)

            self.firstPin = GPIO.PWM(self.firstPinNumber,self.FREQUENCY)
            self.secondPin = GPIO.PWM(self.secondPinNumber,self.FREQUENCY)

            self.firstPin.start(self.STOP[0])
            self.secondPin.start(self.STOP[1])

            self.GPIOSetup = True

    def setSpeed(self,speedTuple):
        self.setupGPIO()
        self.firstPin.ChangeDutyCycle(speedTuple[0])
        self.secondPin.ChangeDutyCycle(speedTuple[1])

    def faster(self):
        if self.currentSpeedIndex < len(self.SPEEDS) - 1:
            self.currentSpeedIndex = self.currentSpeedIndex + 1
            self.setSpeed(self.SPEEDS[self.currentSpeedIndex])

    def slower(self):
        if self.currentSpeedIndex > 0:
            self.currentSpeedIndex = self.currentSpeedIndex - 1
            self.setSpeed(self.SPEEDS[self.currentSpeedIndex])

class WiiRC(object):
    PLUS = 4096
    LEFT = 256
    RIGHT = 512
    UP = 1024
    DOWN = 256
    HOME = 128
    #POWER = 64 or 32 maybe?
    MINUS = 16
    A = 8
    B = 4
    # SERIOUSLY LOL
    ONE = 2
    TWO = 1

    def __init__(self,leftMotor,rightMotor):
        self.leftMotor = leftMotor
        self.rightMotor = rightMotor

    def connect(self):
        print 'Press button 1 + 2 on your Wii Remote...'
        time.sleep(1)
        self.wm=cwiid.Wiimote()
	print 'Wii Remote connected...'
	print '\nPress the ONE button to disconnect the Wii and end the application'
        self.wm.rpt_mode = cwiid.RPT_BTN
        self.processInput()

    def processInput(self):
        while True:
            if self.buttonPressed(self.RIGHT):
                self.leftMotor.faster()
            if self.buttonPressed(self.LEFT):
                self.leftMotor.slower()
            if self.buttonPressed(self.PLUS):
                self.rightMotor.faster()
            if self.buttonPressed(self.MINUS):
                self.rightMotor.slower()
            if self.buttonPressed(self.ONE):
                print "closing Bluetooth connection. Good Bye!"
                GPIO.cleanup()
                exit(self.wm)
            time.sleep(.1)

    def buttonPressed(self,BUTTON):
        return BUTTON & self.wm.state['buttons'] == BUTTON

def main():
    leftMotor = Motor(7,11)
    rightMotor = Motor(12,15)
    wiirc = WiiRC(leftMotor,rightMotor)
    wiirc.connect()

if __name__ == '__main__':
    try:
        main()
    finally:
        GPIO.cleanup()
