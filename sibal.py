#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# GPIO pin setup
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# Step sequence (forward direction)
step_sequence = [[0,0,0,1],
                 [0,0,1,1],
                 [0,0,1,0],
                 [0,1,1,0],
                 [0,1,0,0],
                 [1,1,0,0],
                 [1,0,0,0],
                 [1,0,0,1]]

steps_per_rotation = 4096  # steps for 360 degrees
step_sleep = 0.005         # delay between steps

# GPIO initialization
GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def cleanup():
    for pin in motor_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

try:
    duration_minutes = float(input("Enter duration in minutes (1 minute = 6 degrees): "))
    direction = input("Enter direction (f: forward / r: reverse): ").strip().lower()

    rotation_degrees = duration_minutes * 6
    total_steps = int((rotation_degrees / 360) * steps_per_rotation)

    print(f"Target angle: {rotation_degrees:.1f}°, Steps: {total_steps}")

    if direction not in ['f', 'r']:
        raise ValueError("Direction must be 'f' (forward) or 'r' (reverse)")

    print("Rotating motor...")
    motor_step_counter = 0
    for i in range(total_steps):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)

        if direction == 'f':
            motor_step_counter = (motor_step_counter + 1) % 8
        else:
            motor_step_counter = (motor_step_counter - 1 + 8) % 8

        time.sleep(step_sleep)

    print("Rotation complete!")

except KeyboardInterrupt:
    print("\n[Interrupted]")
    cleanup()
    exit(1)

except ValueError as ve:
    print(f"Input error: {ve}")
    cleanup()
    exit(1)

cleanup()
exit(0)
