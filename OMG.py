#!/usr/bin/python3
import RPi.GPIO as GPIO
import time

# GPIO pins
in1 = 12
in2 = 16
in3 = 20
in4 = 21
motor_pins = [in1, in2, in3, in4]

# Standard working sequence (clockwise)
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

        if forward:
            motor_step_counter = (motor_step_counter + 1) % 8
        else:
            motor_step_counter = (motor_step_counter - 1 + 8) % 8

        time.sleep(step_sleep)

try:
    # 실험 1: 정방향 돌리기
    rotate(512, forward=True)   # 약 45도
    time.sleep(1)

    # 실험 2: 역방향 돌리기
    rotate(512, forward=False)  # 반대로 45도
    time.sleep(1)

    print("✅ Test complete!")

except KeyboardInterrupt:
    print("\n[Interrupted]")
    cleanup()
    exit(1)

cleanup()
exit(0)
