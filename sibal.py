#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# GPIO pins
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# Step sequences
step_sequence_forward = [[0,0,0,1],
                         [0,0,1,1],
                         [0,0,1,0],
                         [0,1,1,0],
                         [0,1,0,0],
                         [1,1,0,0],
                         [1,0,0,0],
                         [1,0,0,1]]

step_sequence_reverse = list(reversed(step_sequence_forward))

steps_per_rotation = 4096
step_sleep = 0.005

# GPIO setup
GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin
