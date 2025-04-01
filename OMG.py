#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# GPIO 핀 정의
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# 작동하는 시퀀스 (절대 바꾸지 마!)
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

# GPIO 설정
GPIO.setmode(GPIO.BCM)
for pin in motor_pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.LOW)

def cleanup():
    for pin in motor_pins:
        GPIO.output(pin, GPIO.LOW)
    GPIO.cleanup()

def rotate(steps, direction):
    print(f"Rotating {'forward' if direction == 'f' else 'reverse'}, steps: {steps}")
    motor_step_counter = 0
    for _ in range(steps):
        seq = step_sequence[motor_step_counter]
        for pin, val in zip(motor_pins, seq):
            GPIO.output(pin, val)

        # ❗ 여기 핵심: 정방향은 -1, 역방향은 +1
        if direction == 'f':
            motor_step_counter = (motor_step_counter - 1 + 8) % 8
        else:
            motor_step_counter = (motor_step_counter + 1) % 8

        time.sleep(step_sleep)

try:
    duration_minutes = float(input("Enter duration in minutes (1 min = 6 degrees): "))
    direction = input("Enter direction (f = forward, r = reverse): ").strip().lower()

    rotation_degrees = duration_minutes * 6
    total_steps = int((rotation_degrees / 360) * steps_per_rotation)

    if direction not in ['f', 'r']:
        raise ValueError("Direction must be 'f' or 'r'.")

    rotate(total_steps, direction)

    print("✅ Rotation complete!")

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
