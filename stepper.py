#!/usr/bin/python3
#--------------------------------------
#    ___  ___  _ ____          
#   / _ \/ _ \(_) __/__  __ __ 
#  / , _/ ___/ /\ \/ _ \/ // / 
# /_/|_/_/  /_/___/ .__/\_, /  
#                /_/   /___/   
#
#    Stepper Motor Test
#
# A simple script to control
# a stepper motor.
#
# Author : Matt Hawkins
# Date   : 28/09/2015
#
# http://www.raspberrypi-spy.co.uk/
#
#--------------------------------------

# Import required libraries
import sys
import time
import RPi.GPIO as GPIO

# Use BCM GPIO references
# instead of physical pin numbers
GPIO.setmode(GPIO.BCM)

# Define GPIO signals to use
# Physical pins 11,15,16,18
# GPIO17,GPIO22,GPIO23,GPIO24
StepPins = [17,18,27,22]

GPIO.setwarnings(False)

# Set all pins as output
for pin in StepPins:
  #print("Setup pins")
  GPIO.setup(pin,GPIO.OUT)
  GPIO.output(pin, False)

# Define advanced sequence
# as shown in manufacturers datasheet
Seq = [[1,0,0,1],
       [1,0,0,0],
       [1,1,0,0],
       [0,1,0,0],
       [0,1,1,0],
       [0,0,1,0],
       [0,0,1,1],
       [0,0,0,1]]
       
StepCount = len(Seq)
Full = 4096

posters = [0, 1, 2]

current_poster = 1
print("Current Poster = %d"%current_poster)

def DegToSteps(deg):
    return 4096*abs(deg)/360, -1 if deg<0 else 1

def GetParams(argv):

    global current_poster
    # Read wait time from command line
    if len(argv)>2:
      WaitTime = int(argv[2])/float(1000)
    else:
      WaitTime = 1/float(1000)

    val = int(argv[1])
    if val in posters:
        new_poster = current_poster - val
       
        print("New poster angle = "+str(new_poster*28))
        current_poster = val
        steps, dir = DegToSteps(new_poster*28)
        return WaitTime, steps, dir
    else:
        NbSteps, StepDir = DegToSteps(val)
        print("Turn %d deg, %d steps"%(val, NbSteps))

        return WaitTime, NbSteps, StepDir

def TurnOff():
      for pin in range(0, 4):
        xpin = StepPins[pin]
        GPIO.output(xpin, False)


def TurnMotor(NbSteps, StepDir, WaitTime):
    StepCounter = 0
    Steps=0

    # Start main loop
    while (Steps<NbSteps):

      #print(Steps, end='\r\n')
      Steps += 1
      #print StepCounter,
      #print Seq[StepCounter]
    
      for pin in range(0, 4):
        xpin = StepPins[pin]
        if Seq[StepCounter][pin]!=0:
          #print " Enable GPIO %i" %(xpin)
          GPIO.output(xpin, True)
        else:
          #print " Disable GPIO %i" %(xpin)
          GPIO.output(xpin, False)
    
      StepCounter += StepDir
    
      # If we reach the end of the sequence
      # start again
      if (StepCounter>=StepCount):
        StepCounter = 0
      if (StepCounter<0):
        StepCounter = StepCount+StepDir
    
      # Wait before moving on
      time.sleep(WaitTime)

while True:
    name = input('Poster?\n')     

    WaitTime, NbSteps, StepDir = GetParams(['', name])
    TurnMotor(NbSteps, StepDir, WaitTime)
    TurnOff()

