#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

in1 = 12
in2 = 16
in3 = 20
in4 = 21

# Speed settings
step_sleep = 0.002  # Default speed
slow_start_steps = 100  # Number of steps to start slowly
slow_sleep = 0.05   # Slow speed for initial steps

# 28BYJ-48: 360 degrees = 4096 steps (half-step)
steps_per_rotation = 4096

# Step sequence
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

# Initialization
GPIO.output(in1, GPIO.LOW)
GPIO.output(in2, GPIO.LOW)
GPIO.output(in3, GPIO.LOW)
GPIO.output(in4, GPIO.LOW)

motor_pins = [in1, in2, in3, in4]
motor_step_counter = 0

def cleanup():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    GPIO.cleanup()

try:
    # Get user input
    duration_minutes = float(input("Enter rotation time (minutes): "))
    
    # Calculate steps based on input
    total_steps = int(steps_per_rotation * (duration_minutes / 60))
    
    print(f"Calculated steps: {total_steps}")
    print(f"Expected rotation angle: {total_steps / steps_per_rotation * 360:.2f} degrees")

    # Forward rotation
    print("Moving to target angle...")
    for i in range(total_steps):
        for pin in range(0, len(motor_pins)):
            GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])
        
        motor_step_counter = (motor_step_counter + 1) % 8  # Clockwise
        
        # Start slowly
        sleep_time = slow_sleep if i < slow_start_steps else step_sleep
        time.sleep(sleep_time)
        
        # Debug every 512 steps
        if (i + 1) % 512 == 0:
            print(f"Forward step: {i + 1}, Expected angle: {(i + 1) / steps_per_rotation * 360:.2f} degrees")

    time.sleep(1)  # Pause

    # Reverse rotation
    print("Returning to 0 degrees...")
    for i in range(total_steps):
        for pin in range(0, len(motor_pins)):
            GPIO.output(motor_pins[pin], step_sequence[motor_step_counter][pin])
        
        motor_step_counter = (motor_step_counter - 1) % 8  # Counter-clockwise
        
        sleep_time = slow_sleep if i < slow_start_steps else step_sleep
        time.sleep(sleep_time)
        
        if (i + 1) % 512 == 0:
            print(f"Reverse step: {i + 1}, Expected angle: {(total_steps - (i + 1)) / steps_per_rotation * 360:.2f} degrees")

except KeyboardInterrupt:
    cleanup()
    exit(1)
except ValueError:
    print("Please enter a valid number")
    cleanup()
    exit(1)

cleanup()
exit(0)
