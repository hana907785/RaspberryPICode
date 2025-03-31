#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

in1 = 12
in2 = 16
in3 = 20
in4 = 21

# Speed setting
step_sleep = 0.01  # Consistent speed

# 28BYJ-48: Test with 4096 steps per rotation
steps_per_rotation = 4096  # 360 degrees

# Step sequence (half-step for 28BYJ-48)
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

motor_pins = [in1, in2, in3, in4]  # Check this order
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
        current_sequence = step_sequence[motor_step_counter]
        GPIO.output(in1, current_sequence[0])
        GPIO.output(in2, current_sequence[1])
        GPIO.output(in3, current_sequence[2])
        GPIO.output(in4, current_sequence[3])
        
        motor_step_counter = (motor_step_counter + 1) % 8  # Clockwise
        time.sleep(step_sleep)
        
        if (i + 1) % 512 == 0:
            print(f"Forward step: {i + 1}, Expected angle: {(i + 1) / steps_per_rotation * 360:.2f} degrees")

    time.sleep(1)  # Pause

    # Reverse rotation
    print("Returning to 0 degrees...")
    for i in range(total_steps):
        current_sequence = step_sequence[motor_step_counter]
        GPIO.output(in1, current_sequence[0])
        GPIO.output(in2, current_sequence[1])
        GPIO.output(in3, current_sequence[2])
        GPIO.output(in4, current_sequence[3])
        
        motor_step_counter = (motor_step_counter - 1) % 8  # Counter-clockwise
        time.sleep(step_sleep)
        
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
