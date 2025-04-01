#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# GPIO pins
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# Step sequence (your actual working direction)
step_sequence = [[1,0,0,1],
                 [1,0,0,0],
                 [1,1,0,0],
                 [0,1,0,0],
                 [0,1,1,0],
                 [0,0,1,0],
                 [0,0,1,1],
                 [0,0,0,1]]

steps_per_rotation = 4096
step_sleep = 0.005

GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def cleanup():
    for pin in motor_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

def rotate(steps, forward=True):
    print(f"{'Forward' if forward else 'Reverse'} rotation, steps: {steps}")
    motor_step_counter = 0
    for _ in range(steps):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)

        # 🔄 FLIP DIRECTION
        if forward:
            motor_step_counter = (motor_step_counter - 1 + 8) % 8
        else:
            motor_step_counter = (motor_step_counter + 1) % 8

        time.sleep(step_sleep)

try:
    duration_minutes = float(input("Enter duration in minutes (1 min = 6 degrees): "))
    direction = input("Enter direction (f = forward, r = reverse): ").strip().lower()

    rotation_degrees = duration_minutes * 6
    total_steps = int((rotation_degrees / 360) * steps_per_rotation)

    if direction == 'f':
        rotate(total_steps, forward=True)
    elif direction == 'r':
        rotate(total_steps, forward=False)
    else:
        raise ValueError("Direction must be 'f' or 'r'.")

    print("Rotation complete!")

except KeyboardInterrupt:
    print("\n[Interrupted by user]")
    cleanup()
    exit(1)

except ValueError as ve:
    print(f"Input error: {ve}")
    cleanup()
    exit(1)

cleanup()
exit(0)
